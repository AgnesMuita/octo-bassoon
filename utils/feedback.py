class Feedback:
    INPUT_ERROR = 1
    DB_ERROR = 2
    GENERAL_ERROR = 3
    SUCCESS = 0

    def __init__(self):
        self.status = 0
        self.data = None
        self.message = None

    def setfb(self, status, data, message):
        self.status = status
        self.data = data
        self.message = message

    def getfb(self):
        return {"status": self.status, "data": self.data, "message": self.message}

    def get(self, **kwargs):
        status = kwargs.get("status", None)
        data = kwargs.get("data", None)
        message = kwargs.get("message", "")
        if status != None:
            self.status = status
            self.data = data
            self.message = message
        return {"status": self.status, "data": self.data, "message": self.message}
