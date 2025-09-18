document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    if (chatbox) {
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    const uploadForm = document.querySelector('form[action="/upload"]');
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            const phoneInput = document.getElementById('phone_number');
            if (phoneInput.value && !/^\+\d{10,15}$/.test(phoneInput.value)) {
                e.preventDefault();
                alert('Please enter a valid phone number starting with + and followed by 10-15 digits.');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    console.log("Script loaded");
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => alert.style.display = 'none', 5000);
    });
});
