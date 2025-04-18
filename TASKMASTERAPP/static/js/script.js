// Password toggle functionality
document.querySelectorAll('.fa-eye').forEach(icon => {
    icon.addEventListener('click', function() {
        const passwordField = this.closest('.input-focus-effect').querySelector('input[type="password"]');
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            this.classList.remove('fa-eye');
            this.classList.add('fa-eye-slash');
        } else {
            passwordField.type = 'password';
            this.classList.remove('fa-eye-slash');
            this.classList.add('fa-eye');
        }
    });
});