// Function to show password
const passwordInput = document.getElementById('password');
const showPasswordCheckbox = document.getElementById('showPassword');

showPasswordCheckbox.addEventListener('change', function () {
    if (showPasswordCheckbox.checked) {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
});

// Remove flash messages after a few seconds
$(document).ready(function() {
    $(".login-flashes").delay(6000).fadeOut("slow");
});