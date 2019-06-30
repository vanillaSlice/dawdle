$(document).ready(function() {

  // hides notifications when clicked
  $('.js-notification-close').click(function() {
    $(this).parent().remove();
  });

  // disables submit button when form submitted to prevent double clicks
  $('.js-form').submit(function() {
    $(this).find('.js-submit').attr('disabled', true);
  });

  // adds error class to form field when invalid
  $('.js-form-field').on('invalid', function() {
    toggleFieldElementErrorClass($(this), true);
  });

  // removes error class from form field when valid
  $('.js-form-field').on('input', function() {
    toggleFieldElementErrorClass($(this), false);
  });

  function toggleFieldElementErrorClass(fieldElement, state) {
    if (state || fieldElement[0].validity.valid) {
      fieldElement.toggleClass('is-danger', state);
      $(fieldElement.data('help')).toggleClass('is-danger', state);
      fieldElement.parent().parent().find('.js-password-mask').toggleClass('is-danger', state);
    }
  }

  // unmasks password when clicked
  $('.js-password-mask').click(function() {
    var buttonElement = $(this);
    var fieldElement = buttonElement.parent().prev().find('.js-password');
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
  });

  function truncateText() {
    $('.js-shave').shave(150, { spaces: false });
  }
  truncateText();
  $(window).on('resize', _.debounce(truncateText, 250, { leading: true }));
});
