"""
Lumos Server Main File
--------------------------------
by Constantin Volke (wervice@proton.me)
Please notice, that I'm using third party libraries. 
Legal notes under https://www.github.com/Wervice/Lumos/legal.md
--------------------------------
The files accid.cfg, admin_set.cfg, login_subtitle.cfg, no_binary.cfg, virus_scanner.cfg should be set to 0 at first launch.
"""

import platform
from libs import gethashes
import time
import io
from PIL import Image
from flask import Flask, request, render_template, send_file
import base64
from werkzeug.utils import secure_filename
import hashlib
import os
import json
from mimetypes import MimeTypes
import pyAesCrypt  # ? Under Apache License 2.0 by Marco Bellaccini
import threading
mime = MimeTypes()
import re
import psutil

def encode_as_base64(str):
    if str != "":
        message_bytes = str.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')
        return base64_message
    else:
        return ""


def decode_from_base64(str):
    if str != "":
        message_bytes = str.encode('utf-8')
        base64_bytes = base64.b64decode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')
        return base64_message
    else:
        return ""


if (open("admin_set.cfg").read() == "0"):
    print("Welcome to Lumos")
    setup_app = Flask(
        "Admin Setup", template_folder="setup/templates", static_folder="setup/asset")

    @setup_app.route("/")
    def setup_welcome():
        return render_template("welcome_s1.html")

    @setup_app.route("/admin_register", methods=["POST"])
    def admin_register():
        os.mkdir(
            "users/"+encode_as_base64(secure_filename(request.form['admin_username'])))
        is_admin_writer = open(
            "users/"+encode_as_base64(secure_filename(request.form['admin_username']))+"/is_admin", "w")
        is_admin_writer.write("1yisadmin$")
        is_admin_writer.close()
        enced_file_writer = open(
            "users/"+encode_as_base64(secure_filename(request.form["admin_username"]))+"/enced_files", "w")
        enced_file_writer.write("{}")
        enced_file_writer.close()
        user_info_writer = open("users/"+encode_as_base64(
            secure_filename(request.form["admin_username"]))+"/"+"userpassword.cfg", "w")
        user_info_writer.write(hashlib.sha256(
            request.form["admin_password"].encode("utf-8")).hexdigest())
        user_info_writer.close()
        return render_template("welcome_s2.html")

    @setup_app.route("/admin_settings", methods=["POST"])
    def admin_settings():
        open("accid.cfg", "w").write(request.form["accid"])
        open("login_subtitle.cfg", "w").write(request.form["server-name"])
        if "enable-antivirus" in request.form:
            if request.form["enable-antivirus"] == "on":
                open("virus_scanner.cfg", "w").write("1")
        else:
            open("virus_scanner.cfg", "w").write("0")

        if "block-binary" in request.form:
            if request.form["block-binary"] == "on":
                open("no_binary.cfg", "w").write("1")
        else:
            open("no_binary.cfg", "w").write("0")
        return render_template("done.html")

    @setup_app.route("/done")
    def done():
        print("Setup done. Please close the app by pressing CTRL+C util the app closed.")
        open("admin_set.cfg", "w").write("1")
        exit()
    setup_app.run(host="0.0.0.0", port=4999, debug=True, ssl_context="adhoc")
else:
    pass

if open("virus_scanner.cfg").read() == "1" and os.path.exists("main.cvd") and os.path.exists("daily.cvd"):
    print("Updating virus definitions from local files\nPlease wait...")
    t1 = threading.Thread(gethashes.get_hashes_names("main"))
    t2 = threading.Thread(gethashes.get_hashes_names("daily"))
    t1.start()
    t2.start()
    print("Virus Update Done")


def compress_image(image_bytes, username, filename):
    try:
        mime_type = mime.guess_type(
            "users/"+username+"/"+secure_filename(filename))
        format = str(mime_type)[1].replace(
            "image/", "").upper().replace("JPEG", "JPG")
        with Image.open(io.BytesIO(image_bytes)) as img:
            output_buffer = io.BytesIO()
            img.thumbnail((300, 300))
            img.save(output_buffer, format="PNG", optimize=False, quality=10)
            output_buffer.seek(0)
        return output_buffer
    except:
        print("Image Compression Error: Maybe encrypted Image")
        return None


def file_html_gen(username):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp"):
        os.remove("users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp")
    files = os.listdir("users/"+username+"/")
    html_code = ""
    for file in files:
        if file != "userpassword.cfg" and file != "enced_files" and file != "Thumbs.db" and not file.startswith("chat_log_file_"):
            file_mime = mime.guess_type("users/"+username+"/"+file)[0]
            if file_mime == "image/png" or file_mime == "image/jpeg" or file_mime == "image/jpg" or file_mime == "image/heic":
                html_code += "<div class=file_button onclick=\"location.href = '/load-file/" + \
                    file+"'\" style=\"background-image: linear-gradient(var(--filter-gradient), var(--filter-gradient)),\
                    url(\'/thumbnail-load-file/"+file+"\') !important\" oncontextmenu=\
                    \"show_file_menu(\'"+file+"\', event); return false;\">"+file.split(".")[0]\
                    .replace("_", " ").replace("-", " ")+"</div>"
            else:
                html_code += "<div class=file_button onclick=\"location.href = '/load-file/" + \
                    file+"'\" oncontextmenu=\"show_file_menu(\'"+file+"\', event); return false;\">\
                    "+file.split(".")[0].replace("_", " ").replace("-", " ")+"</div>"
    if html_code == "":
        html_code = "<img src=/asset/empty.png height=200 id=empty_icon>"
    return html_code


app = Flask(__name__, template_folder="templates", static_folder="asset")


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


@app.errorhandler(405)
def forbiden(error):
    return render_template("errors/405.html"), 405


subtitle_reader = open("login_subtitle.cfg")
login_subtitle = subtitle_reader.read()
subtitle_reader.close()
version_reader = open("version.cfg", "r")
version = version_reader.read()
version_reader.close()


if open("no_binary.cfg").read() == "1":
    blacklist_extensions = [
        "application/x-msdownload", "application/octet-stream"]
    print("Block binaries")
else:
    blacklist_extensions = []
blacklist_filenames = ["is_admin", "userconfig.cfg", "enced_files", "Thumbs.db", "decryption_tempfile.tmp", ""]

def validate_access_permissions(filename):
    if secure_filename(filename) in blacklist_filenames or filename.startswith('chat_log_file_'):
        retval = True
    else:
        retval = False
    return retval

# * Lumos filemanager

@app.route("/", methods=["GET"])
def startscreen():
    if request.method == "GET":
        input_file = open('loggedin_users')
        json_array = json.load(input_file)
        if not request.remote_addr in json_array:
            return render_template("login.html", login_subtitle=login_subtitle)
        else:
            file_html = file_html_gen(json_array[request.remote_addr])
            if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
                if open("virus_scanner.cfg", "r").read() == "1":
                    virscanner = "Enabled"
                else:
                    virscanner = "Disabled"
                if open("no_binary.cfg", "r").read() == "1":
                    enbin = "yes"
                else:
                    enbin = "no"
                userdirlisthtml = ""
                userdirlist = os.listdir("users/")
                for username_encoded in userdirlist:
                    if username_encoded != json_array[request.remote_addr]:
                        userdirlisthtml += "<div class='userdiv'>"+decode_from_base64(username_encoded)+"<button onclick=\"rmuser('"+decode_from_base64(username_encoded)+"')\">Remove</button></div>"
                ram_value = psutil.virtual_memory()[2]
                cpu_value = psutil.cpu_percent(4)
                
                return render_template("admin/admin_dashboard.html", version=version,
                                       platform=platform.system(), virscanner=virscanner, last_vir_update=open("last_virus_update.txt", "r").read(), blockbinary=enbin, ram=ram_value, cpu=cpu_value, servername = login_subtitle).replace("[[ userlist ]]", userdirlisthtml)
            else:
                return render_template("homescreen.html", version=version).replace("[[ files ]]", file_html)

# * Login & Register

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        input_file = open('loggedin_users')
        json_array = json.load(input_file)
        if not request.remote_addr in json_array:
            return render_template("login.html", login_subtitle=login_subtitle)
        else:
            return "<script>location.href = '/'</script>"
    elif request.method == "POST":
        time.sleep(3)
        if os.path.exists("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/userpassword.cfg"):
            if hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest() ==\
                    open("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/userpassword.cfg", "r").read():
                input_file = open('loggedin_users')
                json_array = json.load(input_file)
                json_array[request.remote_addr] = encode_as_base64(
                    secure_filename(request.form["username"]))
                json_array_json = json.dumps(json_array)
                loggedin_users_writer = open("loggedin_users", "w")
                loggedin_users_writer.write(json_array_json)
                loggedin_users_writer.close()
                if os.path.exists("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/is_admin"):
                    return render_template("admin/admin_dashboard.html")
                else:
                    return "<script>location.href = '/'</script>"
            else:
                return "<script>sessionStorage.setItem('last_screen_info', 'login_auth_fail_password'); location.href = '/login'</script>"
        else:
            return "<script>sessionStorage.setItem('last_screen_info', 'login_auth_fail_password'); location.href = '/login'</script>"


@app.route("/register", methods=["GET", "POST"])
# TODO Messages
def register():
    if request.method == "GET":
        return render_template("welcome.html", login_subtitle=login_subtitle)
    elif request.method == "POST":
        time.sleep(3)
        if request.form["accid"] == open("accid.cfg", "r").read():
            if not os.path.exists("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/"+"userpassword.cfg"):
                os.mkdir(
                    "users/"+encode_as_base64(secure_filename(request.form["username"]))+"/")
                enced_file_writer = open("users/"+encode_as_base64(
                    secure_filename(request.form["username"]))+"/enced_files", "w")
                enced_file_writer.write("{}")
                enced_file_writer.close()
                user_info_writer = open("users/"+encode_as_base64(
                    secure_filename(request.form["username"]))+"/"+"userpassword.cfg", "w")
                user_info_writer.write(hashlib.sha256(
                    request.form["password"].encode("utf-8")).hexdigest())
                user_info_writer.close()
                time.sleep(3)
                return "<script>sessionStorage.setItem('last_screen_info', 'register_success'); location.href = '/login'</script>"
            else:
                return "<script>sessionStorage.setItem('last_screen_info', 'register_fail_dbl'); location.href = '/register'</script>"
        else:
                return "<script>sessionStorage.setItem('last_screen_info', 'register_fail_unknown'); location.href = '/register'</script>"


@app.route("/logoff")
def logoff():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        del json_array[request.remote_addr]
        loggedin_users_writer = open("loggedin_users", "w")
        loggedin_users_writer.write(json.dumps(json_array))
        loggedin_users_writer.close()
        return "<script>sessionStorage.setItem('last_screen_info', 'logged_of'); location.replace('/')</script>"
    else:
        return "You're not logged in anymore"


# * File upload

@app.route("/upload/web", methods=["GET", "POST"])
# ! Is it secure?
def upload():
    if request.method == "GET":
        input_file = open('loggedin_users')
        json_array = json.load(input_file)
        if request.remote_addr in json_array:
            return render_template("upload.html")
        else:
            return "You're not logged in", 403
    elif request.method == "POST":
        input_file = open('loggedin_users')
        json_array = json.load(input_file)
        username = json_array[request.remote_addr]
        if request.remote_addr in json_array:
            if not os.path.exists("users/"+username+"/"+secure_filename(request.form["filename"])):
                file = request.files["file_upload"]
                username = json_array[request.remote_addr]
                print(file.content_type)
                if not file.content_type in blacklist_extensions and not validate_access_permissions(filename=request.form["filename"]):
                    file_contents = file.read()
                    if open("virus_scanner.cfg") == "1":
                        if not hashlib.md5(file_contents).hexdigest() in open("hashes_main.txt", "r").read().split("\n"):
                            file_writer = open(
                                "users/"+username+"/" + secure_filename(request.form["filename"]), "wb")
                            file_writer.write(file_contents)
                            file_writer.close()
                            return "<script>sessionStorage.setItem('last_screen_info', 'upload_success'); location.href = '/upload/web'</script>"
                        else:
                            return "<script>sessionStorage.setItem('last_screen_info', \
                            'upload_fail_virus'); sessionStorage.setItem('virus_name', '"+\
                            open("names_main.txt", "r").read().split("\n")[open("hashes_main.txt", "r").read().split("\n").\
                            index(hashlib.md5(file_contents).hexdigest())]+"') location.href = '/upload/web'</script>"
                    else:
                        file_writer = open(
                            "users/"+username+"/" + secure_filename(request.form["filename"]), "wb")
                        file_writer.write(file_contents)
                        file_writer.close()
                        return "<script>sessionStorage.setItem('last_screen_info', 'upload_success'); location.href = '/upload/web'</script>"
                else:
                    return "<script>sessionStorage.setItem('last_screen_info', 'upload_fail_blacklist'); location.href = '/upload/web'</script>"
                
            else:
                return "<script>sessionStorage.setItem('last_screen_info', 'upload_fail_already'); location.href = '/upload/web'</script>"
        else:
            return "You're not logged in"


@app.route("/load-file/<string:filename>")
def load_file(filename):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    enced_files = open('users/'+json_array[request.remote_addr]+"/enced_files")
    enced_file_array = json.load(enced_files)
    if request.remote_addr in json_array:
        username = json_array[request.remote_addr]
        if not validate_access_permissions(filename=filename):
            if not filename in enced_file_array:
                return send_file(
                    io.BytesIO(open("users/"+username+"/" +
                            secure_filename(filename), 'rb').read()),
                    mimetype=str(mime.guess_type(
                        "users/"+username+"/"+secure_filename(filename)))
                )
            else:
                return "<script>sessionStorage.setItem('last_screen_info', 'password_load_file');sessionStorage.setItem('filename', '"+secure_filename(filename)+"'); history.back()</script>"
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"

@app.route("/load-file-password", methods=["POST"])
def load_file_password():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        if not validate_access_permissions(filename=request.form["filename"]):
            pyAesCrypt.decryptFile("users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]), outfile="users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp", passw=hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest(), bufferSize=131072)
            temp_file_reader_dec = open("users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp", "rb")
            return send_file(temp_file_reader_dec, mimetype=str(mime.guess_type(
                            "users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]))))
    else:
        return "You're not allowed to access this file"

@app.route("/thumbnail-load-file/<string:filename>")
def thumbnail_load_file(filename):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        username = json_array[request.remote_addr]
        if not validate_access_permissions(filename=filename):
            file_reader = open("users/"+username+"/" +
                               secure_filename(filename), "rb").read()
            cbytes = compress_image(
                file_reader, username=username, filename=filename)
            try:
                    return_data = send_file(
                    cbytes,
                    mimetype=str(mime.guess_type(
                        "users/"+username+"/"+secure_filename(filename))))
            except:
                return_data = "Can't render img"
            return return_data
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"


@app.route("/delete-file/<string:filename>")
def delete_file(filename):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        username = json_array[request.remote_addr]
        if not validate_access_permissions(filename=filename):
            os.remove("users/"+username+"/"+secure_filename(filename))
            input_file_enced = open('users/'+username+"/enced_files")
            json_array_enced = json.load(input_file_enced)
            if filename in json_array_enced:
                del json_array_enced[filename]
                loggedin_users_writer = open(
                    'users/'+username+"/enced_files", "w")
                loggedin_users_writer.write(json.dumps(json_array_enced))
                loggedin_users_writer.close()
            return "<style>* { background-color: #02050f}</style><script>history.back()</script>"
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"


@app.route("/rename-file/<string:filename>/<string:new_file_name>")
def rename_file(filename, new_file_name):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        username = json_array[request.remote_addr]
        if not validate_access_permissions(filename=filename) and not validate_access_permissions(filename=new_file_name):
            os.rename("users/"+username+"/"+secure_filename(filename),
                      "users/"+username+"/"+secure_filename(new_file_name))
            return "<style>* { background-color: #02050f}</style><script>history.back()</script>"
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"


@app.route("/mng-encryption-file/<string:filename>", methods=["GET"])
def manage_encryption_file(filename):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        input_file_enc = open(
            'users/'+json_array[request.remote_addr]+"/enced_files")
        json_array_enc = json.load(input_file_enc)
        if filename in json_array_enc:
            if json_array_enc[filename] == "1":
                is_encrypted = "true"
            else:
                is_encrypted = "false"
        else:
            is_encrypted = "false"
        return render_template("encryption.html", file_for_enc=filename, is_encrypted=is_encrypted)


@app.route("/mng-encryption-file-formular-handler", methods=["POST"])
def mng_encryption_file_formular_handler():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    filename = request.form["filename"]
    if not validate_access_permissions(filename=filename):
        if request.remote_addr in json_array:
            if request.remote_addr in json_array:
                input_file_enc = open(
                    'users/'+json_array[request.remote_addr]+"/enced_files")
                json_array_enc = json.load(input_file_enc)
                if request.form["filename"] in json_array_enc:
                    if json_array_enc[request.form["filename"]] == "1":
                        is_encrypted = True
                    else:
                        is_encrypted = False
                else:
                    is_encrypted = False
            if not is_encrypted:
                input_file_enced = open(
                    "users/"+json_array[request.remote_addr]+'/enced_files')
                json_array_enced = json.load(input_file_enced)
                json_array_enced[request.form["filename"]] = "1"
                json_array_json_enced = json.dumps(json_array_enced)
                enced_file_writer = open(
                    "users/"+json_array[request.remote_addr]+'/enced_files', "w")
                enced_file_writer.write(json_array_json_enced)
                enced_file_writer.close()
                password = hashlib.sha256(
                    request.form["password"].encode("utf-8")).hexdigest()
                pyAesCrypt.encryptFile("users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]), "users/" +
                                    json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"])+".aes.tmp", passw=password, bufferSize=131072)
                os.remove("users/"+json_array[request.remote_addr] +
                        "/"+secure_filename(request.form["filename"]))
                os.rename("users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]) +
                        ".aes.tmp", "users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]))
                return "<script>sessionStorage.setItem('last_screen_info', 'encryption_done'); history.back()</script>"  # * There is a <script>...</script>
            else:
                password = hashlib.sha256(
                    request.form["password"].encode("utf-8")).hexdigest()
                try:
                    pyAesCrypt.decryptFile("users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]), "users/" +
                                        json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"])+".aes.tmp", passw=password, bufferSize=131072)
                except ValueError:
                    return "<script>sessionStorage.setItem('last_screen_info', 'encryption_fail'); history.back()</script>" # * There is a script
                os.remove("users/"+json_array[request.remote_addr] +
                        "/"+secure_filename(request.form["filename"]))
                os.rename("users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]) +
                        ".aes.tmp", "users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]))
                input_file_enced = open(
                    "users/"+json_array[request.remote_addr]+'/enced_files')
                json_array_enced = json.load(input_file_enced)
                del json_array_enced[request.form["filename"]]
                enced_file_writer = open(
                    'users/'+json_array[request.remote_addr]+"/enced_files", "w")
                enced_file_writer.write(json.dumps(json_array_enced))
                enced_file_writer.close()
                return "<script>sessionStorage.setItem('last_screen_info', 'encryption_done'); history.back()</script>" # * There is a script
        else:
            return "You are not allowed to edit this file", 403

# * Lumos Chat


def remove_emojis(data):
    emoj = re.compile("["
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

@app.route("/chat/web")
def chat_web():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.remote_addr in json_array:
        users_dir_array = os.listdir("users/")
        userlist_parsed_to_html = ""
        for found_user in users_dir_array:
            if found_user != json_array[request.remote_addr]:
                userlist_parsed_to_html += "<button onclick=chat(\'"+decode_from_base64(found_user)+"\') class=user>"+decode_from_base64(found_user).replace("_", " ")+"</button>"
        return render_template("chat_main.html", username = "").replace("[[ userlist ]]", userlist_parsed_to_html).replace("[[ messages ]]", "")
    else:
        return "You are not allowed to access this chat"

@app.route("/chat/web/s", methods=["POST", "GET"])
def chat_web_send():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.method == "POST":
        if request.remote_addr in json_array:
            reciver_name = secure_filename(request.form["username"])
            sender_name = decode_from_base64(json_array[request.remote_addr])
            reciver_log_file = "users/"+encode_as_base64(reciver_name)+"/chat_log_file_"+sender_name+".txt"
            sender_log_file = "users/"+encode_as_base64(sender_name)+"/chat_log_file_"+reciver_name+".txt"
            message = remove_emojis(request.form["message"].replace("&", "&amp;")).replace("<", "&lt;").replace(">", "&gt;")
            if os.path.exists(sender_log_file):
                open(sender_log_file, "a").write("\ny:"+message)
            else:
                open(sender_log_file, "w").write("y:"+message)
            if os.path.exists(reciver_log_file):
                open(reciver_log_file, "a").write("\no:"+message)
            else:
                open(reciver_log_file, "w").write("o:"+message)
            users_dir_array = os.listdir("users/")
            userlist_parsed_to_html = ""
            for found_user in users_dir_array:
                if found_user != json_array[request.remote_addr]:
                    userlist_parsed_to_html += "<button onclick=chat(\'"+decode_from_base64(found_user)+"\') class=user>"+decode_from_base64(found_user).replace("_", " ")+"</button>"
            msg_html = ""
            if os.path.exists(sender_log_file):
                message_array = open(sender_log_file).read().split("\n")
                for message in message_array:
                    if message.startswith("y:"):
                        msg_html += "<div class=msg_you>"+message.removeprefix("y:")+"</div><br>"
                    if message.startswith("o:"):
                        msg_html += "<div class=msg_oth>"+message.removeprefix("o:")+"</div><br>"
            return "<script>location.href = '/chat/web/l'; </script>'"
        else:
            return "You are not allowed to access this chat"
    else:
        return "<script>location.href = '/chat/web/l'; </script>'"


@app.route("/chat/web/l", methods=["GET", "POST"])
def chat_web_load():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if request.method == "POST":
        reciver_name = secure_filename(request.form["username"])
        sender_name = decode_from_base64(json_array[request.remote_addr])
        sender_log_file = "users/"+encode_as_base64(sender_name)+"/chat_log_file_"+reciver_name+".txt"
        if request.remote_addr in json_array:
            users_dir_array = os.listdir("users/")
            userlist_parsed_to_html = ""
            for found_user in users_dir_array:
                if found_user != json_array[request.remote_addr]:
                  userlist_parsed_to_html += "<button onclick=chat(\'"+decode_from_base64(found_user)+"\') class=user>"+decode_from_base64(found_user).replace("_", " ")+"</button>"
            msg_html = ""
            if os.path.exists(sender_log_file):
                message_array = open(sender_log_file).read().split("\n")
                for message in message_array:
                    if message.startswith("y:"):
                        msg_html += "<div class=msg_you>"+message.removeprefix("y:")+"</div><br>"
                    if message.startswith("o:"):
                        msg_html += "<div class=msg_oth>"+message.removeprefix("o:")+"</div><br>"
            else:
                msg_html = ""
            return render_template("chat_main.html", username = reciver_name).replace("[[ userlist ]]", userlist_parsed_to_html).replace("[[ messages ]]", msg_html)
        else:
            return "You are not allowed to access this chat"
    else:
        users_dir_array = os.listdir("users/")
        userlist_parsed_to_html = ""
        for found_user in users_dir_array:
            if found_user != json_array[request.remote_addr]:
                userlist_parsed_to_html += "<button onclick=chat(\'"+decode_from_base64(found_user)+"\') class=user>"+decode_from_base64(found_user).replace("_", " ")+"</button>"
        return render_template("chat_main.html", username = "").replace("[[ userlist ]]", userlist_parsed_to_html).replace("[[ messages ]]", "")

# * Lumos Admin

@app.route("/admin/update")
def admin_update():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        return render_template("admin/update.html")
    else:
        return "You are not allowed to access this site", 403
  
@app.route("/admin/system")
def admin_system():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        return render_template("admin/system.html")
    else:
        return "You are not allowed to access this site", 403
    
@app.route("/admin/vrscnr")
def admin_vrscnr():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        if open("virus_scanner.cfg", "r").read() == "0":
            enabled = "false"
        else:
            enabled = "true"
        return render_template("admin/virusscanner.html", virus_scanner_enabled=enabled)
    else:
        return "You are not allowed to access this site", 403
    
@app.route("/admin_virus_definitions", methods=["POST"])
def upload_virus_definitions():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        main_file = request.files["main_upload"]
        daily_file = request.files["daily_upload"]
        main_file.save("main.cvd")
        daily_file.save("daily.cvd")
        return render_template("admin/upload_done.html")
    else:
        return "You are not allowed to access this site", 403
    
@app.route("/admin_virus_protection_settings", methods=["POST"])
def apply_settings_av():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        if len(request.form) == 1:
            open("virus_scanner.cfg", "w").write("1")
            if os.path.exists("main.cvd") and os.path.exists("daily.cvd"):
                return "<script>sessionStorage.setItem('last_screen_info', 'vrcsnr_update_settings_success'); location.href = '/admin/vrscnr'</script>"
            else:
                return "<script>sessionStorage.setItem('last_screen_info', 'vrscnr_update_settings_fail_defsmissing'); location.href = '/admin/vrscnr'</script>"
        else:
            open("virus_scanner.cfg", "w").write("0")
            return "<script>sessionStorage.setItem('last_screen_info', 'vrscnr_update_settings_success'); location.href = '/admin/vrscnr'</script>"
    else:
        return "You are not allowed to access this site", 403

@app.route("/admin/binary-block", methods=["POST"])
def binaryblock():
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        if "binary-block" in request.form:
            if request.form["binary-block"] == "on":
                open("no_binary.cfg", "w").write("1")
        else:
            open("no_binary.cfg", "w").write("0")
        return "<script>history.back()</script>"
    else:
        return "You are not allowed to access this site", 403

@app.route("/admin/rmuser/<string:username>")
def remover_user(username):
    input_file = open('loggedin_users')
    json_array = json.load(input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        if platform.system() == "Windows":
            os.system("rmdir /q /s \"users/"+encode_as_base64(secure_filename(username))+"\"")
            print("rmdir /q /s users/"+encode_as_base64(secure_filename(username)))
        elif platform.system() == "Linux":
            os.system("rm -r -f -d users/"+encode_as_base64(secure_filename(username)))
        return "<script>history.back()</script>"
    else:
        return "You are not allowed to access this site", 403

@app.route("/favicon.ico")
def favicon():
    return send_file("asset/logo.png")

@app.route("/info")
def info():
    return render_template("info.html", version=version, login_subtitle=login_subtitle)


app.run(host="0.0.0.0", port=5000, debug=True, ssl_context="adhoc")