$(document).ready(function() {

  // displays navbar menu when clicked
  $('.js-navbar-burger').click(function() {
    var navbarBurgerElement = $(this);
    navbarBurgerElement.toggleClass('is-active');
    navbarBurgerElement.attr('aria-expanded', navbarBurgerElement.attr('aria-expanded') === 'false');
    $(navbarBurgerElement.data('target')).toggleClass('is-active');
  });
});
