document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submitButton').addEventListener('click', function (event) {
        event.preventDefault();
        
        // Validation
        var facebook = document.getElementById('facebook').value.trim();
        var twitter = document.getElementById('twitter').value.trim();
        var linkedin = document.getElementById('linkedin').value.trim();
        var instagram = document.getElementById('instagram').value.trim();
        
        var isValid = true;
        
        // Check if inputs are empty
        if (facebook === '') {
            document.getElementById('facebookError').innerText = 'Facebook is required';
            isValid = false;
        } else {
            document.getElementById('facebookError').innerText = '';
        }
        
        if (twitter === '') {
            document.getElementById('twitterError').innerText = 'Twitter is required';
            isValid = false;
        } else {
            document.getElementById('twitterError').innerText = '';
        }
        
        if (linkedin === '') {
            document.getElementById('linkedinError').innerText = 'LinkedIn is required';
            isValid = false;
        } else {
            document.getElementById('linkedinError').innerText = '';
        }
        
        if (instagram === '') {
            document.getElementById('instagramError').innerText = 'Instagram is required';
            isValid = false;
        } else {
            document.getElementById('instagramError').innerText = '';
        }
        
        // If form is valid, submit it
        if (isValid) {
            document.getElementById('profileFormSocial').submit();
        }
    });
});
