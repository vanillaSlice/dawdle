(function() {

  $('.js-delete-board-form').submit(function(e) {
    e.preventDefault();

    var formElement = $(this);

    var deleteBoardPath = formElement.find('#delete_board_path').val();

    $.post(deleteBoardPath, formElement.serialize())
      .done(function(res) {
        var modalElement = $('#js-delete-board-modal');
        dawdle.toggleModal(modalElement);
        dawdle.resetFormElement(formElement);
        window.location = res.url;
      })
      .fail(function(err) {
        var submitElement = formElement.find('.js-submit');
        var errors = err.responseJSON || { error: 'Could not delete board. Please try again.' }
        dawdle.renderFormErrors(formElement, errors);
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  $('.js-delete-board-form .js-modal-trigger').click(function() {
    var formElement = $('.js-delete-board-form');
    dawdle.resetFormElement(formElement);
  });
})();
