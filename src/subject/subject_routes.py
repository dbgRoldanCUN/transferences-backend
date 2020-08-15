import uuid
from flask import Blueprint, request, make_response, jsonify
from subject.subject_service import SubjectService

def cons_subj_blueprint(secret):
    subj_bp = Blueprint('subj_bp', __name__)
    subject_control = SubjectService()

    @subj_bp.route('/<transf_id>/add', methods = ['POST'])
    def addSubject(transf_id):
        if request.method == 'POST':
            requestJson = request.get_json(force = True)
            requestJson['id'] = str(uuid.uuid1())
            requestJson['transferencia_id'] = transf_id
            print('======>>>', requestJson)
            code, msg =subject_control.addSubject(requestJson)
            return make_response({ 'message': msg }, code)

    @subj_bp.route('/transferences/<transf_id>', methods = ['GET'])
    def getAllSubjects(transf_id):
        code, msg = subject_control.getAllSubjects(transf_id)
        return make_response(jsonify({ 'message': msg }), code)

    @subj_bp.route('/<subj_id>', methods = ['GET'])
    def getSubject(subj_id):
        code, msg = subject_control.getSubject(subj_id)
        return make_response(jsonify({ 'message': msg }), code)

    return subj_bp
