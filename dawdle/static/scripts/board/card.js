(function() {

  var columnId;

  /*
   * Create card
   */

  $(document).on('submit', '.js-create-card-form', function(e) {
    e.preventDefault();

    var formElement = $(this);

    var createCardPath = '/card/?column_id=' + columnId;

    $.post(createCardPath, formElement.serialize())
      .done(function(res) {
        var modalElement = $('#js-create-card-modal');
        dawdle.toggleModal(modalElement);
        dawdle.resetFormElement(formElement);
        addNewCard(res.card);
      })
      .fail(function(err) {
        var submitElement = formElement.find('.js-submit');
        var errors = err.responseJSON || { error: 'Could not create card. Please try again.' }
        dawdle.renderFormErrors(formElement, errors);
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  function addNewCard(card) {
    var columnElement = $('[data-column-id=' + card.column_id.$oid + ']');
    return columnElement.find('.js-create-new-card-container').before(
      '   <div class="column is-12">  '  +
      '     <div class="box has-alt-text has-text-weight-bold">' + card.name + '</div>  '  +
      '  </div>  '
    );
  }

  $(document).on('click', '.js-create-card-form .js-modal-trigger', function() {
    var formElement = $('.js-create-card-form');
    dawdle.resetFormElement(formElement);
  });

  $(document).on('click', '.js-create-card-modal-trigger', function() {
    columnId = $(this).parents('.js-board-column').attr('data-column-id');
  });
})();
