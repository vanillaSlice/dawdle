(function() {

  /*
   * Navbar
   */

  function toggleNavbar(navbarElement) {
    var navbarBurgerElement = navbarElement.find('.js-navbar-burger');
    var navbarMenuElement = navbarElement.find('.js-navbar-menu');
    var isActive = navbarBurgerElement.hasClass('is-active');
    navbarBurgerElement.toggleClass('is-active', !isActive);
    navbarBurgerElement.attr('aria-expanded', !isActive);
    navbarMenuElement.toggleClass('is-active', !isActive);
  }

  $('.js-navbar-burger').click(function() {
    toggleNavbar($(this).parents('.js-navbar'));
  });

  /*
   * Notifications
   */

  $('.js-notification-close').click(function() {
    $(this).parent().remove();
  });

  /*
   * Forms
   */

  $('.js-form').submit(function() {
    var submitElement = $(this).find('.js-submit');
    submitElement.prop('disabled', true);
    submitElement.addClass('is-loading');
  });

  function toggleFieldElementErrorClass(fieldElement, state) {
    if (!state && !fieldElement[0].validity.valid) {
      return;
    }

    var formFieldContainerElement = fieldElement.parents('.js-form-field-container');
    var helpElement = formFieldContainerElement.find('.js-help');
    var passwordMaskElement = formFieldContainerElement.find('.js-password-mask');
    fieldElement.toggleClass('is-danger', state);
    helpElement.toggleClass('is-danger', state);
    passwordMaskElement.toggleClass('is-danger', state);
  }

  $('.js-form-field').on('input', function() {
    toggleFieldElementErrorClass($(this), false);
  });

  $('.js-form-field').on('invalid', function() {
    toggleFieldElementErrorClass($(this), true);
  });

  function togglePasswordMask(buttonElement) {
    var formFieldContainerElement = buttonElement.parents('.js-form-field-container');
    var fieldElement = formFieldContainerElement.find('.js-form-field');
    var iconElement = formFieldContainerElement.find('.js-password-mask-icon');
    if (fieldElement.prop('type') === 'password') {
      fieldElement.prop('type', 'text');
      iconElement.removeClass('fa-eye');
      iconElement.addClass('fa-eye-slash');
    } else {
      fieldElement.prop('type', 'password');
      iconElement.removeClass('fa-eye-slash');
      iconElement.addClass('fa-eye');
    }
  }

  $('.js-password-mask').click(function() {
    togglePasswordMask($(this));
  });

  /*
   * Truncation
   */

  function truncateText() {
    $('.js-shave').shave(150, { spaces: false });
  }

  truncateText();

  $(window).on('resize', _.debounce(truncateText, 250, { leading: true }));

  /*
   * Modals
   */

  function toggleModal(modalElement) {
    modalElement.toggleClass('is-active');
    $('html, body, main').toggleClass('is-clipped');
  }

  $('.js-modal-trigger').click(function() {
    var triggerElement = $(this);
    var target = triggerElement.data('target');
    var modalElement = target ? $(target) : triggerElement.parents('.js-modal');
    triggerElement.blur();
    toggleModal(modalElement);
  });

  /*
   * Export functions
   */

  window.dawdle = {
    toggleFieldElementErrorClass: toggleFieldElementErrorClass,
    toggleModal: toggleModal,
    toggleNavbar: toggleNavbar,
    togglePasswordMask: togglePasswordMask,
    truncateText: truncateText,
  };
})();
