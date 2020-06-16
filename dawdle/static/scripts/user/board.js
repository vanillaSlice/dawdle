(function() {

  var board;
  var columnId;

  /*
   * Create Column
   */

  $(document).on('submit', '.js-create-column-form', function(e) {
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
      '   <div class="board-column column is-fullheight is-12 js-board-column" data-column-id="' + column._id.$oid + '">  '  +
      '     <div class="has-background-info box is-fullwidth is-fullheight px-4 py-4">  '  +
      '       <div class="columns is-vcentered is-mobile">  '  +
      '         <div class="column is-9">  '  +
      '           <h2 class="title is-6 has-alt-text has-text-white js-shave-sm">' + column.name + '</h2>  '  +
      '         </div>  '  +
      '         <div class="column is-3">  '  +
      '           <div class="dropdown is-hoverable is-right">  '  +
      '             <div class="dropdown-trigger">  '  +
      '               <button class="button is-info is-inverted" aria-haspopup="true" aria-controls="dropdown-menu" aria-label="dropdown menu">  '  +
      '                 <span class="icon is-small">  '  +
      '                   <i class="fas fa-angle-down" aria-hidden="true"></i>  '  +
      '                 </span>  '  +
      '               </button>  '  +
      '             </div>  '  +
      '             <div class="dropdown-menu" id="dropdown-menu" role="menu">  '  +
      '               <div class="dropdown-content">  '  +
      '                 <a href="#" class="dropdown-item js-modal-trigger" data-target="#js-update-column-modal">  '  +
      '                   Update Column  '  +
      '                 </a>  '  +
      '                 <hr class="dropdown-divider">  '  +
      '                 <a href="#" class="dropdown-item js-modal-trigger js-delete-column-modal-trigger" data-target="#js-delete-column-modal">  '  +
      '                   Delete Column  '  +
      '                 </a>  '  +
      '               </div>  '  +
      '             </div>  '  +
      '           </div>  '  +
      '         </div>  '  +
      '       </div>  '  +
      '     </div>  '  +
      '  </div>  '
    );
  }


  $(document).on('click', '.js-create-column-form .js-modal-trigger', function() {
    var formElement = $('.js-create-column-form');
    dawdle.resetFormElement(formElement);
  });

  /*
   * Delete Column
   */

  $(document).on('submit', '.js-delete-column-form', function(e) {
    e.preventDefault();

    var formElement = $(this);

    var deleteColumnPath = '/column/' + columnId + '/delete';

    $.post(deleteColumnPath, formElement.serialize())
      .done(function(res) {
        var modalElement = $('#js-delete-column-modal');
        dawdle.toggleModal(modalElement);
        dawdle.resetFormElement(formElement);
        removeColumn(res.id);
      })
      .fail(function(err) {
        var submitElement = formElement.find('.js-submit');
        var errors = err.responseJSON || { error: 'Could not delete column. Please try again.' }
        dawdle.renderFormErrors(formElement, errors);
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  function removeColumn(columnId) {
    $('[data-column-id=' + columnId+ ']').remove();
  }

  $(document).on('click', '.js-delete-column-form .js-modal-trigger', function() {
    var formElement = $('.js-delete-column-form');
    dawdle.resetFormElement(formElement);
  });

  $(document).on('click', '.js-delete-column-modal-trigger', function() {
    columnId = $(this).parents('.js-board-column').data('column-id');
  });

  /*
   * Update Board
   */

  $(document).on('submit', '.js-update-board-form', function(e) {
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

  $(document).on('click', '.js-board-settings-quickview .js-quickview-close', function() {
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
