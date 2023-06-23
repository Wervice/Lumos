function chat(username) {
    document.getElementById("loader_form_username").value = username
    document.getElementById("loader_form").submit()
}

window.onload = function () {
    elem = document.getElementById("container")
    elem.scrollTop = elem.scrollHeight;
    if (document.getElementById('username').value != '') { document.getElementById('input').hidden = false }
}