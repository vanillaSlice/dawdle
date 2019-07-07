(function() {

  function handleCreateBoardFormSubmit(e) {
    e.preventDefault();

    var submitElement = $(this).find('.js-submit');

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
      .fail(function() {
        submitElement.prop('disabled', false);
        submitElement.removeClass('is-loading');
      });
  }

  $('.js-create-board-form').submit(handleCreateBoardFormSubmit);
})();
