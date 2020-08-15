def formatObjToDict(params, data):
    object = dict(zip(params, data))
    # for locked_data in ['actualizado']:
    #     del object[locked_data]
    return object

def getObjById(id, control):
    keys = control.paramsData()
    data = control.findById(id)
    if keys and data:
        return formatObjToDict(keys, data)
    return False

def buildMsgEmail(init_msg:dict, tup_name:tuple, data_msg=None):
    msg = {}
    msg['name'] = init_msg['name']%tup_name
    msg['message'] = init_msg['message']
    if data_msg:
        if not isinstance(data_msg, str):
            data = ''
            for key in data_msg:
                data += '{}: {}\n'.format(key.capitalize(), data_msg.get(key))
            msg['message'] = msg['message'].format(data)
        else:
            msg['message'] = data_msg
    return msg

def removeEmptyData(data: dict):
    keys = list(data.keys())
    for item in keys:
        if not data.get(item) or data.get(item) == '':
            del data[item]
    return data
