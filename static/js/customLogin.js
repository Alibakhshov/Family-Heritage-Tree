document.addEventListener("DOMContentLoaded", function() {
    var loginForm = document.getElementById('loginForm');
    var loginButton = document.getElementById('loginButton');
    var usernameInput = document.getElementById('id_username');
    var passwordInput = document.getElementById('id_password');
    var usernameError = document.getElementById('username_error');
    var passwordError = document.getElementById('password_error');

    loginButton.addEventListener('click', function(event) {
        // Prevent default form submission
        event.preventDefault();

        // Validate form fields
        var isValid = true;

        // Check if username is empty
        if (usernameInput.value.trim() === '') {
            usernameError.textContent = "Please enter your username.";
            usernameError.style.color = "red";
            isValid = false;
        } else {
            usernameError.textContent = ""; 
        }

        // Check if password is empty
        if (passwordInput.value.trim() === '') {
            passwordError.textContent = "Please enter your password.";
            passwordError.style.color = "red";
            isValid = false;
        } else {
            passwordError.textContent = ""; 
        }

        // If form is valid, submit the form
        if (isValid) {
            loginForm.submit();
        }
    });

    // Clear error messages when user types in the input fields
    usernameInput.addEventListener('input', function() {
        if (usernameInput.value.trim() !== '') {
            usernameError.textContent = ""; 
        }
    });

    passwordInput.addEventListener('input', function() {
        if (passwordInput.value.trim() !== '') {
            passwordError.textContent = ""; 
        }
    });
});