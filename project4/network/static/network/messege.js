document.addEventListener('DOMContentLoaded', function () {
  console.log('Page loaded');
  // Add event listener here
  var alert = document.querySelector('#sm-alert');
  alert.onanimationend = () => {
    alert.remove();
    console.log(alert);
  };
});
