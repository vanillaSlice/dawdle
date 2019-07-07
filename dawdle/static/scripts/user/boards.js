(function() {

  function handleCreateBoardFormSubmit(e) {
    e.preventDefault();

    var name = $('#name').val();
    var owner = $('#owner').val();
    var visibility = $('#visibility').val();

    $.post('/board/', {
      name: name,
      owner: owner,
      visibility: visibility,
    }, function(res) {
      window.location = res.url;
    });
  }

  $('.js-create-board-form').submit(handleCreateBoardFormSubmit);
})();
