var signinLink = document.getElementById('signin');
var signoutLink = document.getElementById('signout');

function veryfyAssertion(assertion){
	document.location.href = window.location + assertion;
}

signinLink.onclick = function() {
  navigator.id.request();
};
 
signoutLink.onclick = function() {
  navigator.id.logout();
};

navigator.id.watch({
	onlogin: function(assertion){
		veryfyAssertion(assertion);
	},
	onlogout: function(){
		
	}
});

