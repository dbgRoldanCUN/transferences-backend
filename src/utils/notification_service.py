import os
from flask_mail import Mail, Message
from flask import Flask, render_template
from config.settings import getConfig
conf = getConfig().get('mail_config')

class EmailSender:
    def __init__(self, app: Flask):
        app.config['MAIL_SERVER']   = conf.get('server')
        app.config['MAIL_PORT']     = conf.get('port')
        app.config['MAIL_USERNAME'] = conf.get('username')
        app.config['MAIL_PASSWORD'] = conf.get('password')
        app.config['MAIL_USE_TLS']  = False
        app.config['MAIL_USE_SSL']  = True
        app.config['MAIL_ASCII_ATTACHMENTS'] = True
        self.mail = Mail(app)

    def sendMessage(self, subject: str, message_data:dict , to: list, atts:list=None):
        msg = Message(subject, sender = conf.get('username'),
          recipients = to)
        if atts:
            for file in atts:
                print(' Server: Nuevos Archivos')
                # with open_resource(file) as fp:
                #     msg.attach(file, fp.read()) #msg.attach(file, "image/png", fp.read())
        msg.html = self.buildMessage(message_data)
        self.mail.send(msg)
        return 'Server: Message sended'

    def buildMessage(self, props: dict):
        email = os.path.join(conf.get('template'))
        return render_template(email, props = props)
