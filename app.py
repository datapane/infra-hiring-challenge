from flask import Flask

# Where the clients' projects are created
UPLOAD_FOLDER = '/home/user/datapane-infra-challenge/'

app = Flask(__name__)
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Size of the allowed scripts being uploaded
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16mb
