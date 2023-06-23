window.onload = function () {
    if (is_encrypted) {
        document.getElementById("encryption_icon").style.backgroundColor = "#32CD32"
        document.getElementById("encryption_label").innerHTML = "The file is already encrypted"
        document.getElementById("encrypt_button").hidden = true
        document.getElementById("decrypt_button").hidden = false
    }
    document.getElementById("encrypt_button").onclick = function () {
        document.getElementById("password_box_backend_encrypt").value = document.getElementById("password_box_user").value
        document.getElementById("filename_box_backend_encrypt").value = file_for_enc
        document.getElementById("encrytion_form_submitter").submit()
    }
    document.getElementById("decrypt_button").onclick = function () {
        document.getElementById("password_box_backend_decrypt").value = document.getElementById("password_box_user").value
        document.getElementById("filename_box_backend_decrypt").value = file_for_enc
        document.getElementById("decryption_form_submitter").submit()
    }
    function hide_info() {
        document.getElementById("info").hidden = true;
    }
    if (sessionStorage.getItem("last_screen_info") == "encryption_done") {
        document.getElementById("info").hidden = false;
        document.getElementById("info_message").innerHTML = "Security task done <a href='/' class=margin-left-small>Go back</a>";
        sessionStorage.removeItem("last_screen_info")
        setTimeout(hide_info, 2000)
    }
    else if (sessionStorage.getItem("last_screen_info") == "encryption_fail") {
        document.getElementById("info").hidden = false;
        document.getElementById("info_message").innerHTML = "Wrong password <a href='/' class=margin-left-small>Go back</a>";
        sessionStorage.removeItem("last_screen_info")
        setTimeout(hide_info, 2000)
    }
}