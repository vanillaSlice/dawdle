"""
Exports User blueprint.
"""

from datetime import datetime

from bson.objectid import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from flask_mail import Message

from dawdle.blueprints.auth import send_verification_email
from dawdle.extensions.mail import mail
from dawdle.forms.user import DeleteUserForm, UpdateAccountDetailsForm, UpdateEmailForm, UpdatePasswordForm
from dawdle.models.user import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/boards')
@login_required
def boards_GET():
    """
    Boards GET route.
    """

    return render_template('user/boards.html')

@user.route('/settings')
@login_required
def settings_GET():
    """
    Settings GET route.
    """

    return redirect(url_for('user.settings_account_details_GET'))

@user.route('/settings/account-details')
@login_required
def settings_account_details_GET():
    """
    Settings Account Details GET route.
    """

    form = UpdateAccountDetailsForm(request.form, obj=current_user)
    return render_template('user/settings-account-details.html', form=form)

@user.route('/settings/account-details', methods=['POST'])
@login_required
def settings_account_details_POST():
    """
    Settings Account Details POST route.
    """

    # parse the form
    form = UpdateAccountDetailsForm(request.form, obj=current_user)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('user/settings-account-details.html', form=form), 400

    # don't update if not needed
    if not form.update_needed():
        flash('No update needed.', 'info')
        return redirect(url_for('user.settings_account_details_POST'))

    # update the user's account details
    form.populate_obj(current_user)
    current_user.last_updated = datetime.utcnow()
    current_user.save()

    # notify the user
    flash('Your account details have been updated.', 'success')

    # redirect back to account details page again
    return redirect(url_for('user.settings_account_details_POST'))

@user.route('/settings/update-email')
@login_required
def settings_update_email_GET():
    """
    Settings Update Email GET route.
    """

    form = UpdateEmailForm(request.form, email=current_user.email)
    return render_template('user/settings-update-email.html', form=form)

@user.route('/settings/update-email', methods=['POST'])
@login_required
def settings_update_email_POST():
    """
    Settings Update Email POST route.
    """

    # parse the form
    form = UpdateEmailForm(request.form, email=current_user.email)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('user/settings-update-email.html', form=form), 400

    # don't update if not needed
    if not form.update_needed():
        flash('No update needed.', 'info')
        return redirect(url_for('user.settings_update_email_POST'))

    # update the user's email (making sure to update the auth id and last updated)
    current_user.active = False
    current_user.auth_id = ObjectId()
    current_user.email = form.email.data
    current_user.last_updated = datetime.utcnow()
    current_user.save()

    redirect_target = url_for('user.settings_update_email_POST')

    # send verification email
    send_verification_email(current_user, redirect_target=redirect_target)

    # redirect to verify resend page
    return redirect(url_for('auth.verify_resend_GET', email=form.email.data, next=redirect_target))

@user.route('/settings/update-password')
@login_required
def settings_update_password_GET():
    """
    Settings Update Password GET route.
    """

    return render_template('user/settings-update-password.html', form=UpdatePasswordForm(request.form))

@user.route('/settings/update-password', methods=['POST'])
@login_required
def settings_update_password_POST():
    """
    Settings Update Password POST route.
    """

    # parse the form
    form = UpdatePasswordForm(request.form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('user/settings-update-password.html', form=form), 400

    # don't update if not needed
    if not form.update_needed():
        flash('No update needed.', 'info')
        return redirect(url_for('user.settings_update_password_POST'))

    # update the user's password (making sure to update the auth id and last updated)
    current_user.password = User.encrypt_password(form.new_password.data)
    current_user.auth_id = ObjectId()
    current_user.last_updated = datetime.utcnow()
    current_user.save()

    # notify the user
    flash('Your password has been updated.', 'success')

    # login the user with the updated password
    login_user(current_user)

    # redirect back to update password page again
    return redirect(url_for('user.settings_update_password_POST'))

@user.route('/settings/delete-account')
@login_required
def settings_delete_account_GET():
    """
    Settings Delete Account GET route.
    """

    return render_template('user/settings-delete-account.html', form=DeleteUserForm(request.form))

@user.route('/settings/delete-account', methods=['POST'])
@login_required
def settings_delete_account_POST():
    """
    Settings Delete Account POST route.
    """

    # parse the form
    form = DeleteUserForm(request.form)

    # render form again if submitted form is invalid
    if not form.validate_on_submit():
        return render_template('user/settings-delete-account.html', form=form), 400

    message = Message('Dawdle Account Deleted', recipients=[current_user.email])
    message.html = render_template('user/settings-delete-account-email.html', user=current_user)
    try:
        mail.send(message)
    except:
        pass

    current_user.delete()

    flash('Your account has been deleted.', 'info')

    return redirect(url_for('home.index_GET'))
