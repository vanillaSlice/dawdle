(function() {

  var board;

  /*
   * Create Column
   */

  $('.js-create-column-form').submit(function(e) {
    e.preventDefault();

    var formElement = $(this);

    var createColumnPath = formElement.find('#create_column_path').val();

    $.post(createColumnPath, formElement.serialize())
      .done(function(res) {
        var modalElement = $('#js-create-column-modal');
        dawdle.toggleModal(modalElement);
        dawdle.resetFormElement(formElement);
        addNewColumn(res.column);
      })
      .fail(function(err) {
        var submitElement = formElement.find('.js-submit');
        var errors = err.responseJSON || { error: 'Could not create column. Please try again.' }
        dawdle.renderFormErrors(formElement, errors);
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  function addNewColumn(column) {
    $('.js-create-new-column-container').before(
      '<div class="board-column column is-fullheight is-12">' +
      '<div class="box is-fullwidth is-fullheight">' +
      '<h2 class="title has-alt-text is-6">' + column.name + '</h2>' +
      '</div>' +
      '</div>'
    );
  }

  $('.js-create-column-form .js-modal-trigger').click(function() {
    var formElement = $('.js-create-column-form');
    dawdle.resetFormElement(formElement);
  });

  /*
   * Update Board
   */

  $('.js-update-board-form').submit(function(e) {
    e.preventDefault();

    var formElement = $(this);

    var updateBoardPath = formElement.find('#update_board_path').val();

    $.post(updateBoardPath, formElement.serialize())
      .done(function(res) {
        dawdle.renderNotification(res.flash.message, res.flash.category);
        var boardNameElements = $('.js-board-name');
        boardNameElements.text(res.board.name);
        dawdle.truncateText();
        board = res.board;
        resetUpdateBoardForm(formElement);
      })
      .fail(function(err) {
        var submitElement = formElement.find('.js-submit');
        var errors = err.responseJSON || { error: 'Could not update board. Please try again.' }
        dawdle.resetNotification();
        dawdle.renderFormErrors(formElement, errors);
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  function resetUpdateBoardForm(formElement) {
    var options = {};
    if (board) {
      options.state = {
        name: board.name,
        owner: board.owner_id.$oid,
        visibility: board.visibility,
      }
    }

    dawdle.resetFormElement(formElement, options);
  }

  $('.js-board-settings-quickview .js-quickview-close').click(function() {
    var formElement = $('.js-update-board-form');
    resetUpdateBoardForm(formElement);
  });

  /*
   * Delete Board
   */

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
