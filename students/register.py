class Register():
    __instance__ = None

    def __init__(self):
        if Register.__instance__ is None:
            Register.__instance__ = self
            Register.__instance__.data = {}

    @staticmethod
    def instance():
        if not Register.__instance__:
            Register()
        return Register.__instance__

    @staticmethod
    def get(key):
        return Register.__instance__.data.get(key, None)

    @staticmethod
    def set(key, value):
        Register.__instance__.data[key] = value
