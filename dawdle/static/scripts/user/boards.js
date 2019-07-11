(function() {

  $('.js-create-board-form').submit(function(e) {
    e.preventDefault();

    var formElement = $(this);
    var submitElement = formElement.find('.js-submit');

    $.post('/board/', formElement.serialize())
      .done(function(res) {
        window.location = res.url;
      })
      .fail(function(err) {
        var errors = err.responseJSON || { error: 'Could not create board. Please try again.' }
        dawdle.renderFormErrors(formElement, errors);
      })
      .always(function() {
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  $('.js-create-board-form .js-modal-trigger').click(function() {
    var formElement = $('.js-create-board-form');
    dawdle.resetFormElement(formElement);
  });
})();
