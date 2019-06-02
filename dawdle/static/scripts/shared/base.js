$(document).ready(function() {

  // hides notifications when 'delete' button clicked
  $('.notification .delete').click(function() {
    $(this).parent().remove();
  });

  // adds error class to field element when invalid
  $('input').on('invalid', function() {
    toggleFieldElementErrorClass($(this), true);
  });

  // removes error class from field element when valid
  $('input').on('input', function() {
    toggleFieldElementErrorClass($(this), false);
  });

  function toggleFieldElementErrorClass(fieldElement, state) {
    if (state || fieldElement[0].validity.valid) {
      fieldElement.toggleClass('is-danger', state);
      $('#' + fieldElement.attr('id') + '-help').toggleClass('is-danger', state);
    }
  }
});
