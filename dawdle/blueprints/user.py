"""
Exports User blueprint.
"""

from datetime import datetime

from bson.objectid import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user

from dawdle.forms.user import UpdatePasswordForm
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

    return render_template('user/settings-account-details.html')

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

    return render_template('user/settings-delete-account.html')

@user.route('/settings/delete-account', methods=['POST'])
@login_required
def settings_delete_account_POST():
    """
    Settings Delete Account POST route.
    """

    current_user.delete()

    flash('Your account has been deleted.', 'info')

    return redirect(url_for('home.index_GET'))
