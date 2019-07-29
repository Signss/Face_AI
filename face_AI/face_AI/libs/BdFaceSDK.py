from aip import AipFace


APP_ID = '16861001'
API_KEY = 'lWzQaGcuwt5ahuNq126oXm9f'
SECRET_KEY = 'KghqIoAI2bra3HMfE24rvYAG6mpHcZZM'

class FaceCheck(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(FaceCheck, cls).__new__(cls, *args, *kwargs)
            client = AipFace(APP_ID, API_KEY, SECRET_KEY)
            cls._instance = client
        return cls._instance
