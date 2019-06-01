document.addEventListener('DOMContentLoaded', function() {

  // hides notifications when 'delete' button clicked
  document.querySelectorAll('.notification .delete').forEach(function(deleteElement) {
    notificationElement = deleteElement.parentNode;
    deleteElement.addEventListener('click', function() {
      notificationElement.parentNode.removeChild(notificationElement);
    });
  });

  // toggles error class on inputs when invalid
  var errorClass = 'is-danger';
  document.querySelectorAll('input').forEach(function(inputElement) {
    var helpElement = document.getElementById(inputElement.id + '-help');

    inputElement.addEventListener('invalid', function() {
      inputElement.classList.add(errorClass);
      if (helpElement) {
        helpElement.classList.add(errorClass);
      }
    });

    inputElement.addEventListener('input', function() {
      if (inputElement.validity.valid) {
        inputElement.classList.remove(errorClass);
        if (helpElement) {
          helpElement.classList.remove(errorClass);
        }
      }
    });
  });
});
