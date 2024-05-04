document.addEventListener("DOMContentLoaded", function() {
    var firstNameInput = document.getElementById('id_first_name');
    var lastNameInput = document.getElementById('id_last_name');
    var usernameInput = document.getElementById('id_username');
    var emailInput = document.getElementById('id_email');
    var password1Input = document.getElementById('id_password1');
    var password2Input = document.getElementById('id_password2');
    var registrationForm = document.getElementById('registrationForm');
    var registerButton = document.getElementById('registerButton');

    registerButton.addEventListener('click', function(event) {
        // Prevent default form submission
        event.preventDefault();

        // Validate form fields
        var isValid = true;
        var formInputs = registrationForm.querySelectorAll('.theme-input-style');
        formInputs.forEach(function(input) {
            if (input.value.trim() === '') {
                var errorDiv = document.getElementById(input.name + '_error');
                errorDiv.textContent = "This field is required.";
                errorDiv.style.color = "red";
                isValid = false;
            }
        });

        // If form is valid, submit the form
        if (isValid) {
            registrationForm.submit();
        }
    });


    firstNameInput.addEventListener('input', function() {
        var errorDiv = document.getElementById('first_name_error');
        if (!/^[a-zA-Z]+$/.test(firstNameInput.value)) {
            errorDiv.textContent = "Please enter only letters.";
        } else {
            errorDiv.textContent = "";
        }
    });

    lastNameInput.addEventListener('input', function() {
        var errorDiv = document.getElementById('last_name_error');
        if (!/^[a-zA-Z]+$/.test(lastNameInput.value)) {
            errorDiv.textContent = "Please enter only letters.";
        } else {
            errorDiv.textContent = "";
        }
    });

    usernameInput.addEventListener('input', function() {
        var errorDiv = document.getElementById('username_error');
        if (!/^[a-zA-Z0-9_]+$/.test(usernameInput.value)) {
            errorDiv.textContent = "Please use only letters, numbers, and underscores.";
        } else {
            errorDiv.textContent = "";
        }
    });

    emailInput.addEventListener('input', function() {
        var errorDiv = document.getElementById('email_error');
        if (!/^\S+@\S+\.\S+$/.test(emailInput.value)) {
            errorDiv.textContent = "Please enter a valid email address.";
            errorDiv.style.color = "red";
        } else {
            errorDiv.textContent = "";
        }
    });

    password1Input.addEventListener('input', function() {
        var errorDiv = document.getElementById('password1_error');
        if (password1Input.value.length < 8) {
            errorDiv.textContent = "Password must be at least 8 characters long.";
        } else {
            errorDiv.textContent = "";
        }
    });

    password2Input.addEventListener('input', function() {
        var errorDiv = document.getElementById('password2_error');
        if (password2Input.value !== password1Input.value) {
            errorDiv.textContent = "Passwords do not match.";
        } else {
            errorDiv.textContent = "";
        }
    });
});