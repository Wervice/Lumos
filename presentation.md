---
marp: true
theme: gaia
---
<style>
:root {
    --color-background: #02050f;
    --color-foreground: white;
}
</style>

<!-- class: lead -->

# Lumos
## Self-hostable cloud solution
---
## What is Lumos?

- Self-Hosted Cloud
- Open Source
- For teams and companies
- Easy administaration
- Enhanced security features
    - Virus scanning

---
## What does Self Hosted mean
- All data under the own control
- Full control over the server
- No hidden costs

---

## What about collaboration
- Lumos Chat
- File Sharing

---
## Make administration easy
- Administration from a web interface
- Full control
- Auto-adapt
- Members can register them self
---
## Protect your server
- Scan files for virus before uploading
    - Signature Sign
    - ClamAV Virus Definition
- Block executables from uploading
- Change the running port
- Prevent third-parties from registration

---
<!-- class: lead -->
# Installing Lumos
---
<!-- class: default -->
## #1 Download Lumos
1. Go to [github.com/Wervice/Lumos](github.com/Wervice/Lumos)
2. Click `Code`
3. Click `Download as ZIP`
---
## #2 Run Lumos
1. Install dependencies (Using `pip3`) 
    - Flask (`flask`)
    - pyAesCrypt (`pyAesCrypt`)
2. Run `__main__.py` using `python3 __main__.py`
3. Go to your servers IP Address or the servers localhost at port **4999**
---
## #3.1 Create admin account
1. Choose a username for your admin account
2. Enter a strong and long password
3. Click `Submit`
----
## #3.2 Set up settings
1. Choose wheather you want to use Virus Scanning or not
2. Choose wheather you want to allow executable file uploads
3. Set the Access ID used by your members to create an account at your server. The Access ID should be long and hard to guess.
---
## 3.3 Finish the setup
1. Click the `Finish` button. **Don't skip this step!**
2. Wait 15 seconds
3. Open the console in which Lumos is running
4. Press `CTRL+C` until everything stopped
5. Re-start Lumos
6. Go to your servers IP adress or your servers localhost at port **5000**
7. Go to Login & Enter your username and password
---
<!-- class: lead -->

# Create a new account
---
## How to create a new account
1. Go to the servers login screen
2. Click `Go to register`
3. Enter a new username
4. Enter a long and strong password
5. Click `Done`
6. Go to login
7. Login with your new credentials
---
# Upload new file
---
1. Login
2. Click `Upload`
3. Pick a file from your computer
4. Click upload
5. Go back to the home screen