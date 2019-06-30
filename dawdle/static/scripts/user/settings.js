$(document).ready(function() {

  var userSettingsLinksElement = $('.js-user-settings-links');
  var activeElement = userSettingsLinksElement.find('.js-active');

  function scrollToActiveLink() {
    userSettingsLinksElement.animate({ scrollLeft: activeElement.position().left - 20 }, 0);
  }

  if (userSettingsLinksElement.length) {
    scrollToActiveLink();
    $(window).on('resize', _.debounce(scrollToActiveLink, 250, { leading: true }));
  }
});
