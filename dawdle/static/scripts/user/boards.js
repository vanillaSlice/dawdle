(function() {

  $('.js-create-board-form').submit(function(e) {
    e.preventDefault();

    var formElement = $(this);
    var submitElement = formElement.find('.js-submit');

    var name = $('#name').val();
    var owner = $('#owner').val();
    var visibility = $('#visibility').val();

    $.post('/board/', {
      name: name,
      owner: owner,
      visibility: visibility,
    }, function(res) {
      window.location = res.url;
    })
      .fail(function(err) {
        var errors = err.responseJSON || { default: 'Could not create board. Please try again.' }
        dawdle.renderFormErrors(formElement, errors);
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  });

  $('.js-create-board-form .js-modal-trigger').click(function() {
    var formElement = $('.js-create-board-form');
    dawdle.resetFormElement(formElement);
  });
})();
