import json
import requests


class Debug:

    def __init__(self):
        """
        Usage:
        from Debug.Discord import Debug

        debug=Debug()

        try:
            ...
        except Exception as ex:

            debug.error(ex)

        :rtype: None
        """
        self.__message = {}
        self.__webhook = "https://discordapp.com/api/webhooks/757947298880946186/NwKbJO4_0s2QzYSJHgVoZ-vECc2f_3aQ404OZmzo_wGfLpzVBf0TwiDAN0RGFyVsiUH0"
        self.__error_message = "No Error message passed"
        self.__sandbox = False
        self.__username = "Big Brain"
        self.__embed = {}

    def __str__(self):
        return self.__error_message

    @staticmethod
    def __init_message(self):
        self.__message['username'] = self.__username
        self.__message['embeds'] = []
        self.__message['embeds'].append(self.__embed)

    @staticmethod
    def __send_message(self):
        if not self.__sandbox:
            requests.post(self.__webhook, data=json.dumps(self.__message), headers={"Content-Type": "application/json"})
        else:
            print(json.dumps(self.__message))

    @staticmethod
    def __parse_message(message):
        if len(message) > 2000:
            message = message[-1900:]
            return message
        else:
            return message

    def info(self, error_message="", sandbox=False):
        self.__sandbox = sandbox
        if len(error_message) > 1:
            self.__error_message = self.__parse_message(error_message)
        self.__embed['title'] = "Info"
        self.__embed['description'] = self.__error_message
        self.__embed['color'] = 14089984

        self.__init_message(self)
        self.__send_message(self)

    def warn(self, error_message="", sandbox=False):
        self.__sandbox = sandbox
        if len(error_message) > 1:
            self.__error_message = self.__parse_message(error_message)
        self.__embed['title'] = "Warning!"
        self.__embed['description'] = self.__error_message
        self.__embed['color'] = 16753408

        self.__init_message(self)
        self.__send_message(self)

    def error(self, error_message="", sandbox=False):
        self.__sandbox = sandbox
        if len(error_message) > 1:
            self.__error_message = self.__parse_message(error_message)
        self.__embed['title'] = "Error"
        self.__embed['description'] = self.__error_message
        self.__embed['color'] = 16711680

        self.__init_message(self)
        self.__send_message(self)
