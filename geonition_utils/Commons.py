from exceptions import Exception
import sys
import time
import datetime

class CustomError(Exception):
    def __init__(self, customMessage, statusCode, message):
        self.customMessage = customMessage
        self.statusCode = statusCode
        self.message = message
    def __str__(self):
        return repr(self.customMessage)

class SoftGISFormatUtils:
    @staticmethod
    def parse_time(time_string):
        """
        Helper function to parse a POST or GET time
        from the following format:
        yyyy-mm-dd-HH-MM-SS
        
        yyyy - year
        mm - month
        dd - day
        HH - hour
        MM - minute
        SS - second
        
        The less accurate time value have to be given before any less
        accurate time value.
        
        returns a datetime.datetime instance
        or None if format was wrong
        """

        
        if sys.version_info >= (2, 6): #remove this when django drops support for 2.4
            time_accuracy = time_string.count('-')
            if time_accuracy == 0:
                return datetime.datetime.strptime(time_string, "%Y")
            elif time_accuracy == 1:
                return datetime.datetime.strptime(time_string, "%Y-%m")
            elif time_accuracy == 2:
                return datetime.datetime.strptime(time_string, "%Y-%m-%d")
            elif time_accuracy == 3:
                return datetime.datetime.strptime(time_string, "%Y-%m-%d-%H")
            elif time_accuracy == 4:
                return datetime.datetime.strptime(time_string, "%Y-%m-%d-%H-%M")
            elif time_accuracy == 5:
                return datetime.datetime.strptime(time_string, "%Y-%m-%d-%H-%M-%S")
        else:
            time_accuracy = time_string.count('-')
            time_split = time_string.split('-')
            if time_accuracy == 0:
                return datetime.datetime(int(time_split[0]))
            elif time_accuracy == 1:
                return datetime.datetime(int(time_split[0]),
                                         int(time_split[1]))
            elif time_accuracy == 2:
                return datetime.datetime(int(time_split[0]),
                                         int(time_split[1]),
                                         int(time_split[2]))
            elif time_accuracy == 3:
                return datetime.datetime(int(time_split[0]),
                                         int(time_split[1]),
                                         int(time_split[2]),
                                         int(time_split[3]))
            elif time_accuracy == 4:
                return datetime.datetime(int(time_split[0]),
                                         int(time_split[1]),
                                         int(time_split[2]),
                                         int(time_split[3]),
                                         int(time_split[4]))
            elif time_accuracy == 5:
                return datetime.datetime(int(time_split[0]),
                                         int(time_split[1]),
                                         int(time_split[2]),
                                         int(time_split[3]),
                                         int(time_split[4]),
                                         int(time_split[5]))