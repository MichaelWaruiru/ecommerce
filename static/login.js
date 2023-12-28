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