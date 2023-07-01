# ![](asset/ReadmeHeader.png)
# Self host your own cloud

## How does it work

<div align=center>
<img src="asset/login_illustration.png" height="200" style="border-radius: 10px;" alt="Lumos Login"> <br> <br>
</div>

Lumos is a self hostable python & flask application you can run on Windows or Linux Servers.

It has an easy webshell & filemanager for the admin and for your team mates or family members.

Lumos also offers a samll chat solution embeded in the filemanager.

Its lightweigh web interface and small kept design makes it simple to manage files and keep a fast workflow.

It also gives you the opportunity to protect your files using robutst symetric encryption out of the box.

You can connect to it on port 5000 or 4999 for setup.

### Screenshots

<div align=center>
<img src="asset/login_screen.png" height="200" style="border-radius: 10px;" alt="Lumos Login"> <br> <br>
<img src="asset/admin_screen.png" height="200" style="border-radius: 10px;" alt="Lumos Admin"> <br> <br>
<img src="asset/homescreen_screenshot.png" height="200" style="border-radius: 10px;" alt="Lumos Admin"> <br> <br>
</div>

### Prequisites

Lumos uses python to work. On Linux it is installed by default. If you want to use it under Windows, you'll need to download Python from the [official website](https://www.python.org/).

### The setup

After you downloaded the code from the respository, run the following command or install the following packages using pip on your computer.

`pip3 install pyAesCrypt flask Pillow` *This installes pyAesCrypt for encryption, Flask as the webserver with werkzeug and Pillow for image manipulaion*

When everything is done run the python file `__main__.py` by running `python3 ./__main__.py` in the Lumos folder.

After few seconds, you'll be able to access the address `0.0.0.0:4999` (Linux) or `127.0.0.1:4999` in your webbrowser.

Now you can follow the instructions on the website.

### After the setup

You now can give the ACCID code you set in the process to your family members or team mates.

They can create an own account at your cloud. Therfore you need to give them the IP address of your
server, too. It might look like: `192.168.1.83:5000`.

After that, your members can log in and upload files and you are done.

### Legal information

Lumos is released under the Apache 2.0 license. Please be honest and don't violate its conditions, 
but feel free to fork it or edit it for your purposes.

More information at [legal.md](legal.md)