function hide_menu() {
    setTimeout(function () {
        document.getElementById("menu").hidden = true;
    }, 200)
}

function open_menu() {
    document.getElementById("menu").style.top = "60px"
    document.getElementById("menu").style.opacity = "100%"
    document.getElementById("menu").hidden = !document.getElementById("menu").hidden
}

function open_info() {
    document.getElementById("info").hidden = !document.getElementById("info").hidden
}

function show_file_menu(file, event) {
    document.getElementById("file_menu").hidden = false
    document.getElementById("file_menu_delete_button").onclick = function () {
        if (confirm("Do you want to delete \"" + file + "\"?")) {
            location.href = "/delete-file/" + file
        }
    }
    document.getElementById("file_menu_encryption_button").onclick = function () {
        location.href = "/mng-encryption-file/" + file
    }
    document.getElementById("file_menu_download_button").onclick = function () {
        window.open("/load-file/" + file)
    }
    document.getElementById("file_menu_rename_button").onclick = function () {
        new_name = prompt("Rename", file)
        if (new_name != null) {
            location.href = "/rename-file/" + file + "/" + new_name
        }
        else {
            alert("You need to enter a valid file name.")
        }
    }
    var x = event.clientX;
    var y = event.clientY;
    document.getElementById("file_menu").style.left = (x - document.getElementById("file_menu").offsetWidth / 2 + 90) + 'px';
    document.getElementById("file_menu").style.top = (y - document.getElementById("file_menu").offsetHeight / 2 + 90) + 'px';
    document.body.onclick = function () {
        document.getElementById("file_menu").hidden = true
    }
    return false;
}

help_page= 0
sites = ["upload_file", "file_options"]

function next_topic() {
    help_page = help_page+1
    location.href = "#"+sites[help_page]
    if (help_page > sites.length - 1) {
        help_page = sites.length - 1
        location.href = "#"+sites[help_page]
    }
}

function last_topic() {
    help_page = help_page-1
    location.href = "#"+sites[help_page]
    if (help_page < 0) {
        help_page = 0
        location.href = "#"+sites[help_page]
    }
}

window.onload = function () {
    if (sessionStorage.getItem("last_screen_info") == "password_load_file") {
        document.getElementById("password_request").hidden = false;
        sessionStorage.removeItem("last_screen_info")
    }
    else if (sessionStorage.getItem("last_screen_info") == "wrong_password") {
        document.getElementById("password_request").hidden = false;
        sessionStorage.removeItem("last_screen_info")
    }
    if (sessionStorage.getItem("filename") != undefined) {
        document.getElementById("filename").value = sessionStorage.getItem("filename")
    }
}