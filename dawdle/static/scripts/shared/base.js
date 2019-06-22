$(document).ready(function() {

  // hides notifications when clicked
  $('.js-notification-close').click(function() {
    $(this).parent().remove();
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
    }
  }

  // truncate text
  $('.js-shave').shave(150, { spaces: false });
  $(window).on('resize', _.debounce(function() {
    $('.js-shave').shave(150, { spaces: false });
  }, 250, { leading: true }));
});
