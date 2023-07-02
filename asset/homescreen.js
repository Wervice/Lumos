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

function l_confirm(message, function_if_confirmed) {
    document.getElementById("confirm_popup").hidden = false;
    document.getElementById("confirm_popup_message").innerHTML = message;
    document.getElementById("confirm_popup_confirm").onclick = function_if_confirmed;
}

function show_file_menu(file, event) {
    document.getElementById("file_menu").hidden = false
    document.getElementById("file_menu_delete_button").onclick = function () {
        filename = event.srcElement.innerHTML.split("> ")[1]
        l_confirm("<b>Do you want to delete \"" + filename + "\"?</b>", function () {
            fetch(location.protocol + "//" + location.hostname + ":" + location.port + "/delete-file/" + filename)
            event.srcElement.remove()
            document.getElementById("confirm_popup").hidden = true;
        })
    }
    document.getElementById("file_menu_encryption_button").onclick = function () {
        filename = event.srcElement.innerHTML.split("> ")[1]
        document.getElementById("encryption_popup").hidden = false;
        document.getElementById("filename_encpop").value = filename
        setTimeout(function () {
            window.onclick = function (event) {
                var divElement = document.getElementById("encryption_popup")
                var targetElement = event.target;

                if (!divElement.contains(targetElement) && divElement != targetElement) {
                    console.log(targetElement)
                    document.getElementById("encryption_popup").hidden = true;
                    setTimeout(function () {
                        window.onclick = function () { }
                    }, 100)
                }
            }

        }, 100)
    }
    document.getElementById("file_menu_download_button").onclick = function () {
        filename = event.srcElement.innerHTML.split("> ")[1]
        window.open("/load-file/" + filename)
    }
    document.getElementById("file_menu_rename_button").onclick = function () {
        l_confirm("<b>Rename</b><br><br><input id=new_name_input placeholder=\"New name\" value=\""+event.srcElement.innerHTML.split("> ")[1]+"\">", function () {
            new_name = document.getElementById("new_name_input").value
            if (new_name != "") {
                event.srcElement.innerHTML = event.srcElement.innerHTML.split(">")[0] + "> " + event.srcElement.innerHTML.split(">")[1].replaceAll(event.srcElement.innerHTML.split(">")[1], new_name)
                fetch(location.protocol + "//" + location.hostname + ":" + location.port + "/rename-file/" + file + "/" + new_name)
                document.getElementById("confirm_popup").hidden = true;
            }
        })
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

help_page = 0
sites = ["upload_file", "file_options"]

function next_topic() {
    help_page = help_page + 1
    location.href = "#" + sites[help_page]
    if (help_page > sites.length - 1) {
        help_page = sites.length - 1
        location.href = "#" + sites[help_page]
    }
}

function last_topic() {
    help_page = help_page - 1
    location.href = "#" + sites[help_page]
    if (help_page < 0) {
        help_page = 0
        location.href = "#" + sites[help_page]
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
    else if (sessionStorage.getItem("last_screen_info") == "encryption_done") {
        sessionStorage.removeItem("last_screen_info")
    }
    else if (sessionStorage.getItem('last_screen_info') == "upload_success") {
        document.getElementById("info_msg").hidden = false;
        document.getElementById("info_message").innerHTML = "Upload successfully";
        sessionStorage.removeItem("last_screen_info")
        setTimeout(hide_info, 2000)
    }
    else if (sessionStorage.getItem('last_screen_info') == "upload_fail_blacklist") {
        document.getElementById("info_msg").hidden = false;
        document.getElementById("info_message").innerHTML = "The file type is blocked";
        sessionStorage.removeItem("last_screen_info")
        setTimeout(hide_info, 2000)
    }
    else if (sessionStorage.getItem('last_screen_info') == "upload_fail_already") {
        document.getElementById("info_msg").hidden = false;
        document.getElementById("info_message").innerHTML = "This file already exists";
        sessionStorage.removeItem("last_screen_info")
        setTimeout(hide_info, 6500)
    }else if (sessionStorage.getItem('last_screen_info') == "upload_fail_virus") {
        document.getElementById("info_msg").hidden = false;
        document.getElementById("info_message").innerHTML = "The file is a virus<br>"+sessionStorage.getItem("virus_name+");
        sessionStorage.removeItem("last_screen_info")
        sessionStorage.removeItem("virus_name")
        setTimeout(hide_info, 6500)
    }
    if (sessionStorage.getItem("filename") != undefined) {
        document.getElementById("filename").value = sessionStorage.getItem("filename")
        sessionStorage.removeItem("filename")
    }
    function hide_info() {
        document.getElementById("info_msg").hidden = true;
    }
    
}
function show_file_info(filename, filesize, filetype, filemday, filecday, mimeicon) {
    filename = event.srcElement.innerHTML.split("> ")[1]
    document.getElementById("file_info_menu").hidden = false;
    document.getElementById("file_info_menu_icon").src = "asset/" + mimeicon
    document.getElementById("file_info_menu_filename").innerHTML = filename.replaceAll("_", " ");
    document.getElementById("file_info_menu_filesize").innerHTML = filesize + "MB";
    document.getElementById("file_info_menu_filetype").innerHTML = filetype;
    document.getElementById("file_info_menu_fmd").innerHTML = "Last modification: " + filemday;
    document.getElementById("file_info_menu_fcd").innerHTML = "Creation: " + filecday
    if (filename.includes(".jpg") || filename.includes(".png") || filename.includes(".jpeg") || filename.includes(".tiff") || filename.includes(".webp") || filename.includes(".heic") || filename.includes(".ico")) {
        document.getElementById("file_info_menu_icon").src = "/thumbnail-load-file/" + filename.replaceAll(" ", "_")
        document.getElementById("file_info_menu_icon").style.borderRadius = "5px"
    }
    else {
        document.getElementById("file_info_menu_icon").style.borderRadius = "0px"
    }
}

function show_file(file) {
    filename = event.srcElement.innerHTML.split("> ")[1]
    var elbgb = event.srcElement.style.backgroundColor
    event.srcElement.style.backgroundColor = "dodgerblue"
    var evl = event
    fetch(location.protocol + "//" + location.hostname + ":" + location.port + "/load-file/" + filename).then(
        function (response) {
            if (response.status == "901") {
                sessionStorage.setItem('last_screen_info', 'password_load_file'); sessionStorage.setItem('filename', filename
                ); location.reload()
            }
            else {
                evl.srcElement.style.backgroundColor = elbgb
                evl.srcElement.blur()
                location.assign("/load-file/" + filename)
            }
        }
    )
}
function search_for_file(filename) {
    if (filename != "") {
        fetch(location.protocol + "//" + location.hostname + ":" + location.port + "/search/q/" + filename)
            .then(function (response) {
                return response.text();
            })
            .then(function (data) {
                document.getElementById("file_box").innerHTML = data;
            })
            .catch(function () {
                location.reload();
            });
    } else {
        location.reload();
    }
}

function upload_new_file() {
    document.getElementById("file_upload_button").click()
    window.onchange = function () {
        document.getElementById("filename_upload_hidden_input").value = document.getElementById("file_upload_button").value.split("\\")[document.getElementById("file_upload_button").value.split("\\").length - 1]
        document.getElementById("file_upload_form").submit()
    }
} 