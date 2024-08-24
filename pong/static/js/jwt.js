function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const jwtToken = getCookie('jwt_token');
    console.log('JWT Token:', jwtToken);
    // You can now use jwtToken for API requests or other purposes
});

function checkJwt() {
    const token = getCookie('jwt_token');
    const authNav = document.getElementById('auth-nav-links');
    const guestNav = document.getElementById('guest-nav-links');

    if (token) {
        fetch('/player/verify-jwt/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                authNav.style.display = 'block';
                guestNav.style.display = 'none';
            } else {
                deleteCookie('jwt_token');  // Remove invalid token
                guestNav.style.display = 'block';
                authNav.style.display = 'none';
            }
        })
        .catch(() => {
            guestNav.style.display = 'block';
            authNav.style.display = 'none';
        });
    } else {
        guestNav.style.display = 'block';
        authNav.style.display = 'none';
    }
}

window.onload = checkJwt;
