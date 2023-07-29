import ssl
import os
import subprocess
from gevent.pywsgi import WSGIServer
from libs.__main__ import app

if os.path.exists("private_key.pem") and os.path.exists("certificate.pem"):
    print("Certificate found")
else:
    print("Please upload a certificate and key file in the main folder. Names: private_key.pem, certificate.pem")

http_server = WSGIServer(('0.0.0.0', 5000), app, keyfile='private_key.pem', certfile='certificate.pem', ssl_version=ssl.PROTOCOL_TLS)
http_server.serve_forever()