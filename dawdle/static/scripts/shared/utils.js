document.addEventListener('DOMContentLoaded', function() {

  // hides notifications when button "delete" button clicked
  (document.querySelectorAll('.notification .delete') || []).forEach(function(el) {
    notification = el.parentNode;
    el.addEventListener('click', function() {
      notification.parentNode.removeChild(notification);
    });
  });
});
