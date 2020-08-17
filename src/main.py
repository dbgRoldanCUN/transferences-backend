# -*- coding: utf-8 -*-
import os
import random
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from src.user.user_routes import cons_user_blueprint
from src.transference.transf_routes import cons_transf_blueprint
from src.admin.admin_routes import cons_admin_blueprint
from src.subject.subject_routes import cons_subj_blueprint
#from homologation.homologation_routes import cons_hmlog_blueprint
from src.config.settings import getConfig
from werkzeug.security import generate_password_hash
from utils.notification_service import EmailSender

port = getConfig().get('port_http')
host = getConfig().get('host')

key_token = 'key token'

# Server Application
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


key_seed = 'developedbydbgroldan' + str(random.randint(1, 100000))
srtkey = generate_password_hash(key_seed)
app.secret_key = srtkey

email_sender = EmailSender(app)

# Defined Routes
@app.route('/', methods = ['GET'])
def index():
    return {'code': 200, 'message': 'Server: Server started successfully'}

app.register_blueprint(cons_admin_blueprint(srtkey, email_sender), url_prefix='/admin')
app.register_blueprint(cons_user_blueprint(srtkey, email_sender), url_prefix='/users')
app.register_blueprint(cons_transf_blueprint(srtkey, email_sender), url_prefix='/transferences')
app.register_blueprint(cons_subj_blueprint(srtkey), url_prefix='/subjects')
#app.register_blueprint(cons_hmlog_blueprint(srtkey), url_prefix='/homologations')



# Application initialization
if __name__ == '__main__':
    print('Server is listening in port: ' + str(port))
    app.run(port=port, debug=True, host = host)
