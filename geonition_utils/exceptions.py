
class Http400(Exception):
    
    def __init__(self, msg):
        self.msg = msg
        