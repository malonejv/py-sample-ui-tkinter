from distutils.util import strtobool
from infrastructure.configHelper import ConfigHelper, ConfigKeys
from infrastructure.singleton import singleton

@singleton
class AppConfig:

    @staticmethod
    def IsThemeEnabled():
        return bool(strtobool(ConfigHelper().GetValue(ConfigKeys.ENABLE_THEME)))

    
    @staticmethod
    def GetLoginConfig():
        user = ConfigHelper().GetValue(ConfigKeys.LOGIN_USER)
        password = ConfigHelper().GetValue(ConfigKeys.LOGIN_PASSWORD)
        if user is not None and password is not None:
            loginConfig = (user,password)
        else:
            loginConfig = None
        return loginConfig