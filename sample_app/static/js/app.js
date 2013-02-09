var signinLink = document.getElementById('signin');
var signoutLink = document.getElementById('signout');

signinLink.onclick = function() {
  navigator.id.request();
};
 
signoutLink.onclick = function() {
  navigator.id.logout();
};
