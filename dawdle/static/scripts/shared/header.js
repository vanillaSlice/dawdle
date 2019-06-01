document.addEventListener('DOMContentLoaded', function() {

  // displays menu when 'navbar-burger' clicked
  document.querySelectorAll('.navbar-burger').forEach(function(navbarBurgerElement) {
    navbarBurgerElement.addEventListener('click', function() {
      navbarBurgerElement.classList.toggle('is-active');
      document.getElementById(navbarBurgerElement.dataset.target).classList.toggle('is-active');
    });
  });
});
