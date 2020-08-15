# -*- coding: utf-8 -*-
import jwt
import datetime
import base64
from utils.hash_verification import Hash

class Auth(object):

    def __init__(self, secret_key):
        self.secret_key = base64.b64decode(secret_key)

    def generateCookie(self, org_object, pwd):
        if Hash.verify_two_hash(org_object.get('password'), pwd):
            now = datetime.datetime.now()
            payload = org_object
            payload['expiration_time'] = str(now.year) + str(now.month) + str(now.day) + str(now.hour)  # Valid for one hour
            del payload['birth_date']
            del payload['created_at']
            del payload['modified_at']
            del payload['deleted_at']
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        return False

    def verifyCookie(self, token_exist, org_object):
        org_token = jwt.decode(token_exist, self.secret_key, algorithms=['HS256'])
        print(org_token)
        now = datetime.datetime.now()
        org_object['expiration_time'] = str(now.year) + str(now.month) + str(now.day) + str(now.hour)
        if org_token:
            attrbs = list(org_token.keys())
            for atb in attrbs:
                if org_token.get(atb) != org_object.get(atb):
                    print('>>>>', org_token.get(atb))
                    print('---', org_object.get(atb))
                    return False
            return True
        return False
