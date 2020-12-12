import json


class Response(object):

    SUCCESS = {"success": True, 'code': 0, 'msg': 'Success', 'dt': {}}

    FAILED = {"success": False, 'code': -1, 'msg': 'Failed', 'dt': {}}

    ERROR = {"success": False, 'code': 100, 'msg': 'Unknown Error', 'dt': {}}

    DENIED_BY_RULE = {"success": False, 'code': 7,
                      'msg': 'Denied by Rule', 'dt': {}}


    def __init__(self):
        self.success = False
        self.code = 0
        self.msg = ''
        self.dt = {}

    def create(self, params, msg=None, data={}):
        self.success = params['success']
        self.code = params['code']
        self.msg = params['msg'] if not msg else msg
        self.dt = data

    def to_dict(self):
        return {"success": self.success, 'code': self.code, 'msg': self.msg, 'dt': self.dt}

    def to_json_string(self):
        return json.dumps({"success": self.success, 'code': self.code, 'msg': self.msg, 'dt': self.dt})
