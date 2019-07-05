(function() {

  /*
   * Navbar
   */

  function handleNavbarBurgerClick() {
    var navbarBurgerElement = $(this);
    var navbarMenuElement = $(navbarBurgerElement.data('target'));
    var isActive = navbarBurgerElement.hasClass('is-active');
    navbarBurgerElement.toggleClass('is-active', !isActive);
    navbarBurgerElement.attr('aria-expanded', !isActive);
    navbarMenuElement.toggleClass('is-active', !isActive);
  }

  $('.js-navbar-burger').click(handleNavbarBurgerClick);

  /*
   * Notifications
   */

  function handleNotificationCloseClick() {
    $(this).parent().remove();
  }

  $('.js-notification-close').click(handleNotificationCloseClick);

  /*
   * Forms
   */

  function handleFormSubmit() {
    $(this).find('.js-submit').attr('disabled', true);
  }

  $('.js-form').submit(handleFormSubmit);

  function handleFieldInput() {
    toggleFieldElementErrorClass($(this), false);
  }

  function handleFieldInvalid() {
    toggleFieldElementErrorClass($(this), true);
  }

  function toggleFieldElementErrorClass(fieldElement, state) {
    if (!state && !fieldElement[0].validity.valid) {
      return;
    }

    fieldElement.toggleClass('is-danger', state);

    var helpElement = $(fieldElement.data('help'));
    helpElement.toggleClass('is-danger', state);

    var passwordMaskElement = $(fieldElement.data('password-mask'));
    passwordMaskElement.toggleClass('is-danger', state);
  }

  $('.js-form-field').on('input', handleFieldInput);
  $('.js-form-field').on('invalid', handleFieldInvalid);

  function handlePasswordMaskClick() {
    var buttonElement = $(this);
    var fieldElement = $(buttonElement.data('field'));
    var iconElement = buttonElement.find('.js-password-mask-icon');
    if (fieldElement.attr('type') === 'password') {
      fieldElement.attr('type', 'text');
      iconElement.removeClass('fa-eye');
      iconElement.addClass('fa-eye-slash');
    } else {
      fieldElement.attr('type', 'password');
      iconElement.removeClass('fa-eye-slash');
      iconElement.addClass('fa-eye');
    }
  }

  $('.js-password-mask').on('click', handlePasswordMaskClick);

  /*
   * Truncation
   */

  function truncateText() {
    $('.js-shave').shave(150, { spaces: false });
  }

  truncateText();

  $(window).on('resize', _.debounce(truncateText, 250, { leading: true }));

  /*
   * Export functions
   */

  window.dawdle = {
    handleNavbarBurgerClick: handleNavbarBurgerClick,
    handleNotificationCloseClick: handleNotificationCloseClick,
    handleFormSubmit: handleFormSubmit,
    handleFieldInput: handleFieldInput,
    handleFieldInvalid: handleFieldInvalid,
    handlePasswordMaskClick: handlePasswordMaskClick,
    truncateText: truncateText,
  };
})();
