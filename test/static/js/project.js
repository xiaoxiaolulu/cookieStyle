function getCookie(name) {
    if (document.cookie && document.cookie.length) {
        var cookies = document.cookie
            .split(';')
            .filter(function (cookie) {
                return cookie.indexOf(name + "=") !== -1;
            })[0];
        try {
            return decodeURIComponent(cookies.trim().substring(name.length + 1));
        } catch (e) {
            if (e instanceof TypeError) {
                console.info("No cookie with key \"" + name + "\". Wrong name?");
                return null;
            }
            throw e;
        }
    }
    return null;
}

function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
