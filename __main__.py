"""
Lumos Server Main File
**
by Constantin Volke (wervice@proton.me)
Please notice, that I'm using third party libraries. 
Legal notes under https://www.github.com/Wervice/Lumos/legal.md
**
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
import pyAesCrypt
import threading
import re
import psutil
import math
import datetime as dt
import random
mime = MimeTypes()

open("asset/themeoverride.css", "w").write(open("asset/themes/"+open("theme.cfg", "r").read()+".css").read())

if not os.path.exists("users"):
    os.mkdir("users/")

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
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    try:
        if os.path.exists("users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp"):
            os.remove("users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp")
    except:
        pass
    files = os.listdir("users/"+username+"/")
    html_code = ""
    for file in files:
        if file != "userpassword.cfg" and file != "enced_files" and file != "Thumbs.db" and file != "ckey.cfg" and not file.startswith("chat_log_file_") and file != "chat_inbox" and file != "shared_files":
            # mime_image.svg
            # mime_doc.svg
            # mime_presentation.svg
            # mime_spreadsheet.svg
            # mime_pdf.svg
            # mime_video.svg
            mime_icon_dict = {
                # Images
                "png": "mime_image.svg",
                "jpg": "mime_image.svg",  
                "heic": "mime_image.svg",  
                "gif": "mime_image.svg",  
                "heif": "mime_image.svg",  
                "bmp": "mime_image.svg",  
                "ico": "mime_image.svg",
                # Text Document
                "doc": "mime_doc.svg",
                "docx": "mime_doc.svg",
                "odt": "mime_doc.svg",
                "md": "mime_doc.svg",
                "txt": "mime_doc.svg",
                # Presentation
                "ppt": "mime_presentation.svg",
                "pptx": "mime_presentation.svg",
                "odp": "mime_presentation.svg",
                "pptm": "mime_presentation.svg",
                # Spreadsheet
                "xls": "mime_spreadsheet.svg",
                "xlsx": "mime_spreadsheet.svg",
                "ods": "mime_spreadsheet.svg",
                "csv": "mime_spreadsheet.svg",
                # PDF
                "pdf": "mime_pdf.svg",
                # Videos
                "mp4": "mime_video.svg",
                "mov": "mime_video.svg",
                "avi": "mime_video.svg",
                "webm": "mime_video.svg",
                # Archive
                "zip": "mime_archive.svg",
                "tar": "mime_archive.svg",
                "xz": "mime_archive.svg",
                "exe": "mime_archive.svg",
                "iso": "mime_archive.svg",
                }
            try:
                mimet = file.split(".")[1]
            except IndexError:
                mimet = "mime_none.svg"
            print(mimet)
            if mimet in mime_icon_dict:
                mime_icon = mime_icon_dict[mimet]
            else:
                mime_icon = "mime_none.svg"
            fileattrs = os.stat("users/"+username+"/"+file)
            filesize = str(math.floor(fileattrs.st_size / 1024))
            filetypel = {
                # Images
                "png": "Image file",
                "jpg": "Image file",  
                "heic": "Image file",  
                "gif": "Image file",  
                "heif": "Image file",  
                "bmp": "Image file",
                "ico": "Icon file",  
                # Text Document
                "doc": "Word Document",
                "docx": "Word Document",
                "odt": "LibreOffice Writer Document",
                "md": "Markdown",
                "txt": "Plain Text",
                # Presentation
                "ppt": "PowerPoint Presentation",
                "pptx": "PowerPoint Presentation",
                "odp": "LibreOffice Impress Document",
                "pptm": "PowerPoint Macro File",
                # Spreadsheet
                "xls": "Excel Spreadsheet",
                "xlsx": "Excel Spreadsheet",
                "ods": "LibreOffice Spreadsheet",
                "csv": "CSV Table Text Document",
                # PDF
                "pdf": "PDF Document",
                # Videos
                "mp4": "Video",
                "mov": "Video",
                "avi": "Video",
                "webm": "Video",
                # Archive
                "zip": "Archive",
                "tar": "Archive",
                "xz": "Archive",
                "exe": "Archive / Windows Executable",
                "iso": "Archive / Disk Image",
                # Plain
                "html": "HTML Code Document",
                "js": "JavaScript Code Document",
                "css": "CSS Code Document",
                "py": "Python Code Document",
                "pyw": "Python Code Document",
                "c": "C Code Document",
                "csharp": "C# Code Document",
                "cpp": "C++ Code Document",
                "sh": "Shell Code Document",
                "bat": "Batch Code Document",
            }
            if not mimet in filetypel:
                filetype = "mime_none.svg"
            else:
                filetype = filetypel[mimet]
            filecday = str(dt.datetime.fromtimestamp(os.path.getctime("users/"+username+"/"+file)).strftime("%Y/%m/%d %H:%M"))
            filemday = str(dt.datetime.fromtimestamp(os.path.getmtime("users/"+username+"/"+file)).strftime("%Y/%m/%d %H:%M"))
            
            html_code += "<div class=file_button ondblclick=\"show_file('"+file+"')\" onclick=\"show_file_info('"+file+"', "+"'"+filesize+"', '"+filetype+"', '"+filemday+"', '"+filecday+"', '"+mime_icon+"')\" oncontextmenu=\"show_file_menu(\'"+file+"\', event); return false;\"><img src=asset/"+mime_icon+" height=20> "+file.replace("_", " ")+"</div>"
    if html_code == "":
        html_code = "<div align=center><img src=/asset/empty.png height=200 id=empty_icon></div>"
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
blacklist_filenames = ["is_admin", "userconfig.cfg", "enced_files", "Thumbs.db", "decryption_tempfile.tmp", "", "chat_inbox", "userpassword.cfg", "ckey.cfg", "shared_files"]

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
        login_user_input_file = open('loggedin_users')
        json_array = json.load(login_user_input_file)
        if request.remote_addr in json_array and "ckey" in request.cookies:
            if request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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
                    cpu_value = psutil.cpu_percent(2)
                    theme = open("theme.cfg", "r").read().split(".")[0]
                    return render_template("admin/admin_dashboard.html", version=version,
                                        platform=platform.system(), virscanner=virscanner, last_vir_update=open("last_virus_update.txt", "r").read(), blockbinary=enbin, ram=ram_value, cpu=cpu_value, servername = login_subtitle, acttheme=theme).replace("[[ userlist ]]", userdirlisthtml)
                else:
                    return render_template("homescreen.html", version=version).replace("[[ files ]]", file_html)
            else:
                open("users/"+json_array[request.remote_addr]+"/ckey.cfg", "w").write("")
                if request.remote_addr in json_array:
                    del json_array[request.remote_addr]
                loggedin_users_writer = open("loggedin_users", "w")
                loggedin_users_writer.write(json.dumps(json_array))
                loggedin_users_writer.close()
                return render_template("login.html", login_subtitle=login_subtitle)
        else:
            return render_template("login.html", login_subtitle=login_subtitle)  
    else:
        return "Method not allowed"

# * Login & Register

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        login_user_input_file = open('loggedin_users')
        json_array = json.load(login_user_input_file)
        if not request.remote_addr in json_array:
            return render_template("login.html", login_subtitle=login_subtitle)
        else:
            return "<script>location.href = '/'</script>"
    elif request.method == "POST":
        time.sleep(3)
        print("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/userpassword.cfg")
        if os.path.exists("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/userpassword.cfg"):
            if hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest() ==\
                    open("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/userpassword.cfg", "r").read():
                login_user_input_file = open('loggedin_users')
                json_array = json.load(login_user_input_file)
                json_array[request.remote_addr] = encode_as_base64(
                    secure_filename(request.form["username"]))
                json_array_json = json.dumps(json_array)
                loggedin_users_writer = open("loggedin_users", "w")
                loggedin_users_writer.write(json_array_json)
                loggedin_users_writer.close()
                i = 0
                cookiekeystr = ""
                while i != 512:
                    cookiekeystr += chr(random.randint(1, 128))
                    i = i+1
                cookiekey = hashlib.sha512(cookiekeystr.encode("utf-8")).hexdigest()
                if os.path.exists("users/"+encode_as_base64(secure_filename(request.form["username"]))+"/is_admin"):
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
                    cpu_value = psutil.cpu_percent(2)
                    theme = open("theme.cfg", "r").read().split(".")[0]
                    open("users/"+json_array[request.remote_addr]+"/"+"ckey.cfg", "w").write(cookiekey)
                    return render_template("admin/admin_dashboard.html", version=version,
                                       platform=platform.system(), virscanner=virscanner, last_vir_update=open("last_virus_update.txt", "r").read(), blockbinary=enbin, ram=ram_value, cpu=cpu_value, servername = login_subtitle, acttheme=theme).replace("[[ userlist ]]", userdirlisthtml).replace("[[ ckey ]]", cookiekey)
                else:
                    open("users/"+json_array[request.remote_addr]+"/"+"ckey.cfg", "w").write(cookiekey)
                    return "<script>document.cookie = 'ckey="+cookiekey+"' ;location.href = '/'</script>"
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
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array:
        open("users/"+json_array[request.remote_addr]+"/ckey.cfg", "w").write("")
        del json_array[request.remote_addr]
        loggedin_users_writer = open("loggedin_users", "w")
        loggedin_users_writer.write(json.dumps(json_array))
        loggedin_users_writer.close()
        return "<script>sessionStorage.setItem('last_screen_info', 'logged_of'); document.cookie = 'ckey=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'; location.replace('/')</script>"
    else:
        return "<script>location.href = '/'</script>"


# * File upload

@app.route("/upload/web", methods=["GET", "POST"])
# ! Is it secure?
def upload():
    if request.method == "GET":
        login_user_input_file = open('loggedin_users')
        json_array = json.load(login_user_input_file)
        if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
            return render_template("upload.html")
        else:
            return "You're not logged in", 403
    elif request.method == "POST":
        login_user_input_file = open('loggedin_users')
        json_array = json.load(login_user_input_file)
        username = json_array[request.remote_addr]
        if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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
                            file_html = file_html_gen(json_array[request.remote_addr])
                            return render_template("homescreen.html", version=version).replace("[[ files ]]", file_html)
                        else:
                            return "", 905
                    else:
                        file_writer = open(
                            "users/"+username+"/" + secure_filename(request.form["filename"]), "wb")
                        file_writer.write(file_contents)
                        file_writer.close()
                        file_html = file_html_gen(json_array[request.remote_addr])
                        return render_template("homescreen.html", version=version).replace("[[ files ]]", file_html)
                else:
                    # Execu or illegal filename detected
                    return "", 903
            else:
                # The file already exists
                return "", 904
        else:
            return "You're not logged in"


@app.route("/load-file/<string:filename>")
def load_file(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    enced_files = open('users/'+json_array[request.remote_addr]+"/enced_files")
    enced_file_array = json.load(enced_files)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        username = json_array[request.remote_addr]
        if not validate_access_permissions(filename=filename):
            if not filename in enced_file_array:
                music_extensions = ["mp3", "wav", "m4a"]
                if not filename.split(".")[1] in music_extensions:
                    return send_file(
                        io.BytesIO(open("users/"+username+"/" +
                                secure_filename(filename), 'rb').read()),
                        mimetype=str(mime.guess_type(
                            "users/"+username+"/"+secure_filename(filename))),
                            as_attachment=True,
                            download_name=filename
                    )
                else:
                    b64_data = "data:audio/"+filename.split(".")[1]+";base64,"+str(base64.b64encode(open("users/"+json_array[request.remote_addr]+"/"+filename, "rb").read())).replace("b'", "").replace("'","")
                    return render_template("music_player.html", filename = filename, song_in_b64 = b64_data)
            else:
                return "", 901
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"

@app.route("/load-file-password", methods=["POST"])
def load_file_password():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        if not validate_access_permissions(filename=request.form["filename"]):
            try:
                pyAesCrypt.decryptFile("users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]), outfile="users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp", passw=hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest(), bufferSize=131072)
            except ValueError:
                return "<script>sessionStorage.setItem('last_screen_info', 'wrong_password'); history.back();</script>"
            temp_file_reader_dec = open("users/"+json_array[request.remote_addr]+"/decryption_tempfile.tmp", "rb")
            return send_file(temp_file_reader_dec, mimetype=str(mime.guess_type(
                            "users/"+json_array[request.remote_addr]+"/"+secure_filename(request.form["filename"]))), as_attachment=True, download_name=secure_filename(request.form["filename"]))
    else:
        return "You're not allowed to access this file"

@app.route("/thumbnail-load-file/<string:filename>")
def thumbnail_load_file(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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
                return_data = send_file("asset/no_access.png", "image/png")
            return return_data
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"


@app.route("/delete-file/<string:filename>")
def delete_file(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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
            filename = str(secure_filename(filename))
            username = json_array[request.remote_addr]
            user_shared_list = open('users/'+username+"/shared_files")
            user_shared_list_parsed = json.load(user_shared_list)
            try:
                del user_shared_list_parsed[filename]
            except:
                pass
            open('users/'+username+"/shared_files", "w").write(json.dumps(user_shared_list_parsed))
            return "<style>* { background-color: #02050f}</style><script>history.back()</script>"
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"


@app.route("/rename-file/<string:filename>/<string:new_file_name>")
def rename_file(filename, new_file_name):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        username = json_array[request.remote_addr]
        if not validate_access_permissions(filename=filename) and not validate_access_permissions(filename=new_file_name):
            os.rename("users/"+username+"/"+secure_filename(filename),
                      "users/"+username+"/"+secure_filename(new_file_name))
            return "<style>* { background-color: #02050f}</style><script>history.back()</script>"
        else:
            return "You aren't allowed to access this file", 403
    else:
        return "You're not logged in"

@app.route("/mng-encryption-file-formular-handler", methods=["POST"])
def mng_encryption_file_formular_handler():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    filename = request.form["filename"]
    if not validate_access_permissions(filename=filename):
        if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
            if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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

@app.route("/search/q/<string:query>")
def search(query):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        username = json_array[request.remote_addr]
        results = []
        for e in os.listdir("users/"+username+"/"):
            if query in e:
                results += [e]
        html_code = ""
        for r in results:
            if not validate_access_permissions(r):
                try:
                    mimet = r.split(".")[1]
                except IndexError:
                    mimet = "mime_none.svg"
                filetypel = {
                    # Images
                    "png": "Image file",
                    "jpg": "Image file",  
                    "heic": "Image file",  
                    "gif": "Image file",  
                    "heif": "Image file",  
                    "bmp": "Image file",
                    "ico": "Icon file",  
                    # Text Document
                    "doc": "Word Document",
                    "docx": "Word Document",
                    "odt": "LibreOffice Writer Document",
                    "md": "Markdown",
                    "txt": "Plain Text",
                    # Presentation
                    "ppt": "PowerPoint Presentation",
                    "pptx": "PowerPoint Presentation",
                    "odp": "LibreOffice Impress Document",
                    "pptm": "PowerPoint Macro File",
                    # Spreadsheet
                    "xls": "Excel Spreadsheet",
                    "xlsx": "Excel Spreadsheet",
                    "ods": "LibreOffice Spreadsheet",
                    "csv": "CSV Table Text Document",
                    # PDF
                    "pdf": "PDF Document",
                    # Videos
                    "mp4": "Video",
                    "mov": "Video",
                    "avi": "Video",
                    "webm": "Video",
                    # Archive
                    "zip": "Archive",
                    "tar": "Archive",
                    "xz": "Archive",
                    "exe": "Archive / Windows Executable",
                    "iso": "Archive / Disk Image",
                    # Plain
                    "html": "HTML Code Document",
                    "js": "JavaScript Code Document",
                    "css": "CSS Code Document",
                    "py": "Python Code Document",
                    "pyw": "Python Code Document",
                    "c": "C Code Document",
                    "csharp": "C# Code Document",
                    "cpp": "C++ Code Document",
                    "sh": "Shell Code Document",
                    "bat": "Batch Code Document",
                }
                if not mimet in filetypel:
                    filetype = "mime_none.svg"
                else:
                    filetype = filetypel[mimet]
                filesize = str(os.stat("users/"+username+"/"+r).st_size)
                filetype = str(os.stat("users/"+username+"/"+r).st_size)
                filecday = str(dt.datetime.fromtimestamp(os.path.getctime("users/"+username+"/"+r)).strftime("%Y/%m/%d %H:%M"))
                filemday = str(dt.datetime.fromtimestamp(os.path.getmtime("users/"+username+"/"+r)).strftime("%Y/%m/%d %H:%M"))
                mime_icon_dict = {
                    # Images
                    "png": "mime_image.svg",
                    "jpg": "mime_image.svg",  
                    "heic": "mime_image.svg",  
                    "gif": "mime_image.svg",  
                    "heif": "mime_image.svg",  
                    "bmp": "mime_image.svg",  
                    "ico": "mime_image.svg",
                    # Text Document
                    "doc": "mime_doc.svg",
                    "docx": "mime_doc.svg",
                    "odt": "mime_doc.svg",
                    "md": "mime_doc.svg",
                    "txt": "mime_doc.svg",
                    # Presentation
                    "ppt": "mime_presentation.svg",
                    "pptx": "mime_presentation.svg",
                    "odp": "mime_presentation.svg",
                    "pptm": "mime_presentation.svg",
                    # Spreadsheet
                    "xls": "mime_spreadsheet.svg",
                    "xlsx": "mime_spreadsheet.svg",
                    "ods": "mime_spreadsheet.svg",
                    "csv": "mime_spreadsheet.svg",
                    # PDF
                    "pdf": "mime_pdf.svg",
                    # Videos
                    "mp4": "mime_video.svg",
                    "mov": "mime_video.svg",
                    "avi": "mime_video.svg",
                    "webm": "mime_video.svg",
                    # Archive
                    "zip": "mime_archive.svg",
                    "tar": "mime_archive.svg",
                    "xz": "mime_archive.svg",
                    "exe": "mime_archive.svg",
                    "iso": "mime_archive.svg",
                    }
                try:
                    mimet = r.split(".")[1]
                except IndexError:
                    mimet = "mime_none.svg"
                print(mimet)
                if mimet in mime_icon_dict:
                    mime_icon = mime_icon_dict[mimet]
                else:
                    mime_icon = "mime_none.svg"
                html_code += "<div class=file_button ondblclick=\"show_file('"+r+"')\" onclick=\"show_file_info('"+r+"', "+"'"+filesize+"', '"+filetype+"', '"+filemday+"', '"+filecday+"', '"+mime_icon+"')\" oncontextmenu=\"show_file_menu(\'"+r+"\', event); return false;\"><img src=asset/"+mime_icon+" height=20> "+r.replace("_", " ")+"</div>"
        if html_code == "":
            html_code = "<div style=padding:10px;>No results</div>"    
        return html_code
    else:
        return "You are not logged in"

# * Lumos Chat


def remove_emojis(data):
    emoji_smile_k_l = ["😀", "😁", "😃", "🙂", "☺", ":smile:"]
    for emoji_smile_k in emoji_smile_k_l:
        data = data.replace(emoji_smile_k, ":smile:")
    emoj = re.compile("["
        u"\U00002700-\U000027BF" 
        u"\U0001F600-\U0001F64F" 
        u"\U00002600-\U000026FF" 
        u"\U0001F300-\U0001F5FF" 
        u"\U0001F900-\U0001F9FF" 
        u"\U0001FA70-\U0001FAFF" 
        u"\U0001F680-\U0001F6FF" 
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

@app.route("/chat/web")
def chat_web():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.method == "POST":
        if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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
            if request.files["file-upload"] != "":
                fileformchat = request.files["file-upload"]
                filecontents = fileformchat.read()
                if not os.path.exists("users/"+encode_as_base64(secure_filename(reciver_name))+"/chat_inbox"):
                    os.mkdir("users/"+encode_as_base64(secure_filename(reciver_name))+"/chat_inbox")
                if open("virus_scanner.cfg", "r").read() == "1":
                    if not hashlib.md5(filecontents).hexdigest() in open("hashes_main.txt", "r").read().split("\n") and not validate_access_permissions(filename=request.form["filename"]):
                        open("users/"+encode_as_base64(reciver_name)+"/chat_inbox/by_"+secure_filename(sender_name)+"_"+secure_filename(request.form["file-name"]))
                else:
                    if not validate_access_permissions(filename=request.form["filename"]):
                        open("users/"+encode_as_base64(reciver_name)+"/chat_inbox/by_"+secure_filename(sender_name)+"_"+secure_filename(request.form["filename"]), "wb").write(filecontents)
            return "<script>location.href = '/chat/web/l'; </script>'"
        else:
            return "You are not allowed to access this chat"
    else:
        return "<script>location.href = '/chat/web/l'; </script>'"


@app.route("/chat/web/l", methods=["GET", "POST"])
def chat_web_load():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.method == "POST":
        reciver_name = secure_filename(request.form["username"])
        sender_name = decode_from_base64(json_array[request.remote_addr])
        sender_log_file = "users/"+encode_as_base64(sender_name)+"/chat_log_file_"+reciver_name+".txt"
        if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
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

@app.route("/chat/web/fb")
def filebox():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    filelist_html = ""
    if os.path.exists("users/"+json_array[request.remote_addr]+"/chat_inbox"):
        if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
            for file in os.listdir("users/"+json_array[request.remote_addr]+"/chat_inbox"):
                filelist_html += "<div class=filelist onclick=window.open('/chat/web/fb/l/"+file+"')> <span class=sender>"+file.split("_")[1]+"</span> "+file.split("_")[2]+"</div><br>"
    else:
        filelist_html = "Your filebox is empty"
    return render_template("filebox.html").replace("[[ filelist ]]", filelist_html)

@app.route("/chat/web/fb/l/<string:filename>")
def filebox_load(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        return send_file(
            "users/"+json_array[request.remote_addr]+"/chat_inbox/"+secure_filename(filename),
            mimetype=str(mime.guess_type("users/"+json_array[request.remote_addr]+"/chat_inbox/"+secure_filename(filename)))
        )
    else:
        return "You're not allowed to access this location"

# * Lumos Admin

@app.route("/admin/update")
def admin_update():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        return render_template("admin/update.html")
    else:
        return "You are not allowed to access this site", 403
  
@app.route("/admin/system")
def admin_system():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        return render_template("admin/system.html")
    else:
        return "You are not allowed to access this site", 403
    
@app.route("/admin/vrscnr")
def admin_vrscnr():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
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
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        main_file = request.files["main_upload"]
        daily_file = request.files["daily_upload"]
        main_file.save("main.cvd")
        daily_file.save("daily.cvd")
        if open("virus_scanner.cfg").read() == "1" and os.path.exists("main.cvd") and os.path.exists("daily.cvd"):
            print("Updating virus definitions from local files\nPlease wait...")
            t1 = threading.Thread(gethashes.get_hashes_names("main"))
            t2 = threading.Thread(gethashes.get_hashes_names("daily"))
            t1.start()
            t2.start()
            print("Virus Update Done")
        return render_template("admin/upload_done.html")
    else:
        return "You are not allowed to access this site", 403
    
@app.route("/admin_virus_protection_settings", methods=["POST"])
def apply_settings_av():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
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
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
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
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        if platform.system() == "Windows":
            os.system("rmdir /q /s \"users/"+encode_as_base64(secure_filename(username))+"\"")
            print("rmdir /q /s users/"+encode_as_base64(secure_filename(username)))
        elif platform.system() == "Linux":
            os.system("rm -r -f -d users/"+encode_as_base64(secure_filename(username)))
        return "<script>history.back()</script>"
    else:
        return "You are not allowed to access this site", 403

@app.route("/admin/ciconupload", methods=["POST"])
def ciupload():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        request.files["icon_upload"].save("asset/company_icon.png")
        return "<script>history.back()</script>"

@app.route("/admin/themechange/<string:theme>")
def theme_change(theme):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if os.path.exists("users/"+json_array[request.remote_addr]+"/is_admin"):
        if os.path.exists("asset/themes/"+theme+".css"):
            open("theme.cfg", "w").write(theme)
            open("asset/themeoverride.css", "w").write(open("asset/themes/"+open("theme.cfg", "r").read()+".css").read())
            return ""
        else:
            return "doesnotexist"
            

@app.route("/favicon.ico")
def favicon():
    return send_file("asset/logo.png")

@app.route("/info")
def info():
    return render_template("info.html", version=version, login_subtitle=login_subtitle)

@app.route("/info/p")
def info_privacy():
    return render_template("privacy.html")

@app.route("/rawedit/<string:filename>")
def rawedit(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        try:
            username = json_array[request.remote_addr]
            load_filename = "users/"+username+"/"+secure_filename(filename)
            file_content = open(load_filename, "r").read()
            return render_template("rawedit.html", filename = filename).replace("[[ file_content ]]", file_content)
        except UnicodeDecodeError:
            return "<script>window.top.document.getElementById('editor_popup').hidden = true; window.top.l_confirm('This file type is not supported.', function () {window.top.document.getElementById('confirm_popup').hidden = true;})</script>"
    else:
        return "", 403

@app.route("/rawedits", methods=["POST"])
def rawedit_s():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        filename = secure_filename(request.form["filename"])
        username = json_array[request.remote_addr]
        open("users/"+json_array[request.remote_addr]+"/"+secure_filename(filename), "w").write(request.form["file_content"])
        load_filename = "users/"+username+"/"+secure_filename(filename)
        file_content = open(load_filename, "r").read()
        return render_template("rawedit.html", filename = filename).replace("[[ file_content ]]", file_content)
    else:
        return ""

@app.route("/security_advisor")
def security_advisor():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        return render_template("security_advisor.html")
    else:
        return "You are not allowed to access this page", 403

@app.route("/security_advisor/start", methods=["POST"])
def security_advisor_start():
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array and request.cookies["ckey"] == open("users/"+json_array[request.remote_addr]+"/ckey.cfg").read():
        password = request.form["password"]
        p_score = 0
        if len(password) < 5:
            p_score = 1
        elif len(password) < 10:
            p_score = 40
        elif len(password) < 15:
            p_score = 70
        elif len(password) < 20:
            p_score = 100
        elif len(password) < 30:
            p_score = 120
        else:
            p_score = 180
        scs = 0
        special_chars = ["!", "\"", "§", "$", "%", "&", "/", "(", ")", "=", "?", "+", "*", "#", "'", "-", ".", ":", ",", ";", "[", "]", "{", "}", "\\", "^", "°", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for c in password:
            if c in special_chars:
                scs = scs+1
        p_score = p_score - (10 - scs)
        p_score = p_score / 2
        if p_score > 100:
            p_score = 100
        if p_score < 20:
            p_score = 20
        p_score = p_score * 4
        p_score = str(p_score)+"px"
        user_encrypted_files = json.load(open("users/"+json_array[request.remote_addr]+"/enced_files"))
        m_f_list_html = ""
        for file in os.listdir("users/"+json_array[request.remote_addr]):
            if not file in user_encrypted_files:
                try:
                    if file.split(".")[1] in ["doc", "docx", "rtf", "pdf", "odt", "xls", "xlsx", "csv", "ods", "ppt", "pptx", "odp"]:
                     m_f_list_html += "<div class='missing_file'>"+file+"</div>"
                except IndexError:
                    pass
        return render_template("security_advisor_overview.html", p_score = p_score).replace("[[ m_f_list_html ]]", m_f_list_html)
    else:
        return "You are not allowed to access this page", 403
    
@app.route("/share/link/<string:username>/<string:filename>/<string:code>")
def share_link(username, filename, code):
    username = decode_from_base64(str(username))
    user_shared_list = open('users/'+encode_as_base64(secure_filename(username))+"/shared_files")
    user_shared_list_parsed = json.load(user_shared_list)
    if secure_filename(filename) in user_shared_list_parsed and user_shared_list_parsed[secure_filename(filename)] == code and not validate_access_permissions(filename):
        return send_file(
            "users/"+encode_as_base64(secure_filename(username))+"/"+secure_filename(filename),
            mimetype=secure_filename(filename),
            as_attachment=True,
            download_name=filename
        )
    else:
        return render_template("share_wrong_code.html")

@app.route("/share/info/<string:filename>")
def share_info(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array:
        username = json_array[request.remote_addr]
        user_shared_list = open('users/'+username+"/shared_files")
        user_shared_list_parsed = json.load(user_shared_list)
        filename = decode_from_base64(str(filename))
        if filename in user_shared_list_parsed:
            return "shared"
        else:
            return "not_shared"
    else:
        return "This part of the API is locked down for you"
    
@app.route("/share/reglink/<string:filename>")
def share_reglink(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array:
        filename = secure_filename(decode_from_base64(str(filename)))
        username = json_array[request.remote_addr]
        user_shared_list = open('users/'+username+"/shared_files")
        user_shared_list_parsed = json.load(user_shared_list)
        share_code = str(hashlib.sha256(str(random.randint(1,1000000)).encode("utf-8")).hexdigest())
        user_shared_list_parsed[filename] = share_code
        open('users/'+username+"/shared_files", "w").write(json.dumps(user_shared_list_parsed))
        return "/share/link/"+username+"/"+filename+"/"+share_code
    else:
        return "This part of the API is locked down for you"

@app.route("/share/unreg/<string:filename>")
def share_unreg(filename):
    login_user_input_file = open('loggedin_users')
    json_array = json.load(login_user_input_file)
    if request.remote_addr in json_array:
        filename = secure_filename(decode_from_base64(str(filename)))
        username = json_array[request.remote_addr]
        user_shared_list = open('users/'+username+"/shared_files")
        user_shared_list_parsed = json.load(user_shared_list)
        del user_shared_list_parsed[filename]
        open('users/'+username+"/shared_files", "w").write(json.dumps(user_shared_list_parsed))
        return "done"
    else:
        return "This part of the API is locked down for you"
    

app.run(host="0.0.0.0", port=5000, debug=False, ssl_context="adhoc")
