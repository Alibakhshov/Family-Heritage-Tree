// Function to validate a single input field
function validateInput(inputId, errorId, errorMessage) {
    var value = document.getElementById(inputId).value.trim();
    if (value === "") {
        document.getElementById(errorId).innerText = errorMessage;
        return false; // Return false if validation fails
    } else {
        document.getElementById(errorId).innerText = "";
        return true; // Return true if validation passes
    }
}

// Attach change event listeners to input fields
document.getElementById("username").addEventListener("change", function() {
    validateInput("username", "usernameError", "Please fill in the username.");
});

document.getElementById("email").addEventListener("change", function() {
    validateInput("email", "emailError", "Please fill in the email.");
});

document.getElementById("name").addEventListener("change", function() {
    validateInput("name", "nameError", "Please fill in the name.");
});

document.getElementById("position").addEventListener("change", function() {
    validateInput("position", "positionError", "Please fill in the position.");
});

// Form submit event handler
document.getElementById("profileForm").addEventListener("submit", function(event) {
    var isValid = true;

    // Validate each input field before form submission
    isValid = validateInput("username", "usernameError", "Please fill in the username.") && isValid;
    isValid = validateInput("email", "emailError", "Please fill in the email.") && isValid;
    isValid = validateInput("name", "nameError", "Please fill in the name.") && isValid;
    isValid = validateInput("position", "positionError", "Please fill in the position.") && isValid;

    if (!isValid) {
        event.preventDefault(); // Prevent form submission if validation fails
    } else {
        document.getElementById("successMessage").style.display = "block";
        setTimeout(function() {
            document.getElementById("successMessage").style.display = "none";
        }, 5000);
    }
});
