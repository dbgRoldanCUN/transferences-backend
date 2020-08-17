# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, make_response
from werkzeug.utils import secure_filename
from admin.admin_service import AdminService
from config.settings import getConfig

def cons_admin_blueprint(secret, email_sender):
    admin_bp = Blueprint('admin_bp', __name__)
    admin_control = AdminService(email_sender)

    @admin_bp.route('/register', methods = ['POST'])
    def register():
        if request.method == 'POST':
            requestJson = request.get_json(force = True)
            code, message = admin_control.addAdmin(requestJson)
            return make_response({ 'message': message }, code)

    @admin_bp.route('/<id>', methods = ['GET'])
    def getProfileAdmin(id):
        code, message = admin_control.getAdminById(id)
        return make_response({ 'message': message }, code)

    @admin_bp.route('/login', methods = ['POST'])
    def login():
        if request.method == 'POST':
            requestJson = request.get_json(force = True)
            code, msg = admin_control.loginAdmin(requestJson)
            return make_response({ 'message': msg }, code)

    @admin_bp.route('/<id>/update', methods = ['PUT'])
    def updateAdmin(id):
        if request.method == 'PUT':
            requestJson = request.form.to_dict(flat=False)
            dict_keys = list(requestJson.keys())
            resultUpt = {dict_keys[i]: requestJson.get(dict_keys[i])[0] for i in range(len(dict_keys))}
            if 'imagen' in request.files:
                file_image = request.files['imagen']
                filename = secure_filename(file_image.filename)
                filename = '{}admin_img.{}'.format(id, filename.split('.')[-1])
                file_image.save(
                    os.path.join(getConfig().get('upload_user_files'),
                     filename))
                resultUpt['imagen'] = getConfig().get('upload_user_files') + filename
            code, msg = admin_control.updateData(id, resultUpt)
            return { 'code': code, 'message': msg }

    @admin_bp.route('/<id>/assignement', methods = ['POST'])
    def assignementAdmin(id):
        if request.method == 'POST':
            requestJson = request.get_json(force = True)
            code, msg = admin_control.assignAdmin(requestJson)
            return { 'code': code, 'message': msg }

    return admin_bp
