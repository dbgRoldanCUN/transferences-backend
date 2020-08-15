# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, make_response
from werkzeug.utils import secure_filename
from user.user_service import UserService
from config.settings import getConfig

def cons_user_blueprint(secret, email_sender):
    user_bp = Blueprint('user_bp', __name__)
    user_control = UserService(email_sender)

    @user_bp.route('/signin', methods = ['POST'])
    def signin():
        if request.method == 'POST':
            requestJson = request.get_json(force = True)
            code, message = user_control.addUser(requestJson)
            return make_response({ 'message': message }, code)

    @user_bp.route('/login', methods = ['POST'])
    def login():
        if request.method == 'POST':
            requestJson = request.get_json(force = True)
            user = user_control.loginUser(requestJson)
            if isinstance(user, tuple):
                code, msg = user
                return {'code': code, 'message': msg}
            return user

    @user_bp.route('/<id>', methods = ['GET'])
    def getProfile(id):
        code, message = user_control.getUserById(id)
        return make_response({ 'message': message }, code)

    @user_bp.route('/<id>/update', methods = ['PUT'])
    def updateUser(id):
        if request.method == 'PUT':
            requestJson = request.form.to_dict(flat=False)
            dict_keys = list(requestJson.keys())
            resultUpt = {dict_keys[i]: requestJson.get(dict_keys[i])[0] for i in range(len(dict_keys))}
            if 'imagen' in request.files:
                file_image = request.files['imagen']
                filename = secure_filename(file_image.filename)
                filename = '{}user_img.{}'.format(id, filename.split('.')[-1])
                file_image.save(
                    os.path.join(getConfig().get('upload_user_files'),
                     filename))
                resultUpt['imagen'] = getConfig().get('upload_user_files') + filename
            code, msg = user_control.updateData(id, resultUpt)
            return { 'code': code, 'message': msg }

    return user_bp
