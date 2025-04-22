document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('#login-form');

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const username = document.querySelector('#username').value;
        const password = document.querySelector('#password').value;
        const role = document.querySelector('input[name="role"]:checked').value;

        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, password, role})
        })

        .then(response => response.json())

        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            if (data.role === 'student') {
                window.location.href = '/home';
            } 
            
            else if (data.role === 'teacher') {
                alert('Teacher Home Page is in development, stay tuned!');
                // window.location.href = '/teacher_home';
            } 
            
            else if (data.role === 'admin') {
                alert('Admin Home Page is in development, stay tuned!');
                // window.location.href = '/admin_home';
            } 
            
            else if (data.role === 'secretary') {
                alert('Secretary Home Page is in development, stay tuned!');
                // window.location.href = '/secretary_home';
            }
        })

        .catch(error => {
            alert('Error: Could not connect to server');
        });
    });
});