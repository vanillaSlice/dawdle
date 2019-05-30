document.addEventListener('DOMContentLoaded', function() {

  // hides notifications when 'delete' button clicked
  document.querySelectorAll('.notification .delete').forEach(function(el) {
    notification = el.parentNode;
    el.addEventListener('click', function() {
      notification.parentNode.removeChild(notification);
    });
  });

  // toggles 'is-danger' class on input when invalid
  document.querySelectorAll('input').forEach(function(el) {
    el.addEventListener('invalid', function() {
      el.classList.add('is-danger');
    });

    el.addEventListener('input', function() {
      if (el.validity.valid) {
        el.classList.remove('is-danger');
      }
    });
  });
});
