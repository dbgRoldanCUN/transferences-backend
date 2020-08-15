# -*- coding: utf-8 -*-
import os
import uuid
from flask import Blueprint, request, jsonify, make_response
from werkzeug.utils import secure_filename
from transference.transf_service import TransferenceService
from config.settings import getConfig

def cons_transf_blueprint(secret, email_sender):
    transf_bp = Blueprint('transf_bp', __name__)
    transf_control = TransferenceService(email_sender)

    @transf_bp.route('/admin/<id_admin>', methods = ['GET'])
    def showAdminTransf(id_admin):
        code, message = transf_control.showAdminTransf(id_admin)
        return make_response({ 'message': message }, code)

    @transf_bp.route('/users/<id>', methods = ['GET'])
    def showUserTransf(id):
        code, message = transf_control.showUserTransf(id)
        return make_response({ 'message': message }, code)

    @transf_bp.route('/<id>', methods = ['GET'])
    def showTransf(id):
        code, message = transf_control.showTransf(id)
        return make_response({ 'message': message }, code)

    @transf_bp.route('/users/<id>', methods = ['POST']) # User id
    def newTransference(id):
        if request.method == 'POST':
            if 'transf_carta' not in request.files:
                return {'code': 406, 'message': 'Transference Letter Required'}
            else:
                requestJson = request.form.to_dict(flat=False)
                dict_keys = list(requestJson.keys())
                result = {dict_keys[i]: requestJson.get(dict_keys[i])[0] for i in range(len(dict_keys))}
                result['id'] = transf_id = str(uuid.uuid1())
                file_letter = request.files['transf_carta']
                filename = secure_filename(file_letter.filename)
                filename = '{}carta{}.{}'.format(id, transf_id, filename.split('.')[-1])
                file_letter.save(
                    os.path.join(getConfig().get('upload_user_files'),
                     filename))
                result['transf_carta'] = getConfig().get('upload_user_files') + filename
                result['usuario_id'] = id
                code, msg = transf_control.addTransference(result, id)
                return make_response({ 'message': msg }, code)

    @transf_bp.route('/<id>/update', methods = ['PUT'])
    def updateFilesTransference(id):
        data = {}
        code, msg = 304, 'Server: No changes'
        fileItems = ['notas', 'nmaf05', 'nmaf06', 'nmaf15']
        for item in fileItems:
            file = request.files.get(item)
            if file:
                filename = secure_filename(file_letter.filename)
                filename = '{}{}.{}'.format(id, item, filename.split('.')[-1])
                file.save(
                    os.path.join(getConfig().get('upload_user_files'),
                     filename))
                data[item] = getConfig().get('upload_user_files') + filename
                code, msg = transf_control.updateTransference(data, id)
        return make_response({ 'message': msg }, code)

    @transf_bp.route('/<id>/delete', methods = ['PUT'])
    def deleteTransference(id):
        code, msg = transf_control.deleteTrasnference(id)
        return make_response({ 'message': msg }, code)

    @transf_bp.route('/managers/<transf_id>', methods = ['GET'])
    def showManagers(transf_id):
        code, msg = transf_control.getManagers(transf_id)
        return make_response({ 'message': msg }, code)

    @transf_bp.route('/assign/<transf_id>', methods = ['PUT'])
    def assignManager(transf_id):
        requestJson = request.get_json(force = True)
        code, msg = transf_control.assignManager(transf_id, requestJson)
        return make_response({ 'message': msg }, code)

    return transf_bp
