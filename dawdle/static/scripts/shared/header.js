$(document).ready(function() {

  // displays menu when 'navbar-burger' clicked
  $('.navbar-burger').click(function() {
    var navbarBurgerElement = $(this);
    navbarBurgerElement.toggleClass('is-active');
    $(navbarBurgerElement.data('target')).toggleClass('is-active');
  });
});
