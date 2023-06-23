window.onload = function () {
    function hide_info() {
        document.getElementById("info").hidden = true;
    }
    function popup(info) {
        document.getElementById("info").hidden = false;
        document.getElementById("info_message").innerHTML = info;
    }
    document.getElementById("login_formular").onsubmit = function () {
        document.getElementById("loading_wheel").hidden = false;
        document.getElementById("submit_button").disabled = "true";
    }
    if (sessionStorage.getItem("last_screen_info") == "login_auth_fail_password") {
        popup("Wrong password")
        sessionStorage.removeItem("last_screen_info");
        setTimeout(hide_info, 3400);
    }
    else if (sessionStorage.getItem("last_screen_info") == "logged_of") {
        popup("You're logged out")
        sessionStorage.removeItem("last_screen_info");
        setTimeout(hide_info, 3400);
    }
    else if (sessionStorage.getItem("last_screen_info") == "register_success") {
        popup("Registration worked.<br>You can now login")
        sessionStorage.removeItem("last_screen_info");
        setTimeout(hide_info, 3400);
    }
}