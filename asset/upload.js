function file_select() {
    document.getElementById("file_upload_button").click()
}


function changed_upload() {
    document.getElementById("file_name_label").innerHTML = document.getElementById("file_upload_button").value.split("\\")[document.getElementById("file_upload_button").value.split("\\").length - 1]
    document.getElementById("submit_button").hidden = false
    document.getElementById("filename").value = document.getElementById("file_upload_button").value.split("\\")[document.getElementById("file_upload_button").value.split("\\").length - 1]
}

window.onload = function () {
    document.getElementById("formular").onsubmit = function () {
        document.getElementById("submit_button").innerHTML = "Uploading..."
        document.getElementById("submit_button").style.backgroundColor = "#00A86B"
    }
}

function check_for_extension() {
    if (!document.getElementById("filename").value.includes(".")) {
        document.getElementById("extension_info").innerHTML = "<br>Missing extension"
    }
    else {
        document.getElementById("extension_info").innerHTML = ""
    }
    if (document.getElementById("filename").value.includes("@") || document.getElementById("filename").value.includes("/") || document.getElementById("filename").value.includes("\\") || document.getElementById("filename").value.includes("..")) {
        document.getElementById("character_info").innerHTML = "<br>The characters @, /, \\ and .. aren't allowed."
    }
    else {
        document.getElementById("character_info").innerHTML = ""
    }
}