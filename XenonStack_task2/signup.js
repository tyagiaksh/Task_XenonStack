document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signupForm');

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const newUsername = document.getElementById('newUsername').value;
        const newPassword = document.getElementById('newPassword').value;

        // Send signup data to the server
        fetch('signup.js', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `newUsername=${encodeURIComponent(newUsername)}&newPassword=${encodeURIComponent(newPassword)}`,
        })
        .then(response => {
            if (response.ok) {
                alert('Signup successful!');
            } else if (response.status === 409) {
                alert('Username already exists. Please choose a different username.');
            } else {
                alert('Signup failed. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// Additional signup-related functions can be added here
