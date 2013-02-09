var signinLink = document.getElementById('signin');

if (signinLink) {
  signinLink.onclick = function() { navigator.id.request(); };
};
 
