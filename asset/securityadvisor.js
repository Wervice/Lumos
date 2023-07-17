window.onload = function () {
    if (localStorage.getItem("intro_security_advisor") != "true") {
        document.getElementById("intro").hidden = false;
    }
    localStorage.setItem("intro_security_advisor", "true")
}