function chat(username) {
    document.getElementById("loader_form_username").value = username
    document.getElementById("loader_form").submit()
}

window.onload = function () {
    elem = document.getElementById("container")
    elem.scrollTop = elem.scrollHeight;
    if (document.getElementById('username').value != '') { document.getElementById('input').hidden = false }
    document.getElementById("file-upload").onchange = function () {
        document.getElementById("message").value = "New file: "+document.getElementById("file-upload").value.split("\\")[document.getElementById("file-upload").value.split("\\").length - 1]
        document.getElementById("filename").value = document.getElementById("file-upload").value.split("\\")[document.getElementById("file-upload").value.split("\\").length - 1]
    }
}

function file_upload() {
    document.getElementById("file-upload").click()
}

