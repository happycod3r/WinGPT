"""_summary_

    Returns:
        _type_: _description_
"""

import datetime

class NormalTime:
    def __init__(self) -> None:
        # Get the current time
        self.current_time = datetime.datetime.now().time()
        # Format the time to extract hours, minutes, seconds, and milliseconds
        self.normal_time = self.current_time.strftime("%I:%M:%S.%f %p")
        # Extract hours, minutes, seconds, and milliseconds
        self.normal_time_components = datetime.datetime.strptime(self.normal_time, "%I:%M:%S.%f %p").time()
        self.hour = self.normal_time_components.hour
        self.minutes = self.normal_time_components.minute
        self.seconds = self.normal_time_components.second
        self.microseconds = self.normal_time_components.microsecond 
        self.am_pm = self.normal_time_components.strftime("%p")
    
    def time(self, out: bool) -> str:
        if out == True:
            print(f"{self.hour}:{self.minutes}:{self.seconds}")
            return 0
        return f"{self.hour}:{self.minutes}:{self.seconds}"
    
    def preciseTime(self, out: bool) -> str:
        if out == True:
            print(f"{self.hour}:{self.minutes}:{self.seconds}:{self.microseconds}")
            return 0
        return f"{self.hour}:{self.minutes}:{self.seconds}:{self.microseconds}" 
    
    def getAmPm(self, out: bool) -> str:
        if out == True:
            print(self.am_pm)
            return 0
        return self.am_pm
    
    def getHour(self, out: bool) -> int:
        if out == True:
            print(self.hour)
            return 0
        return self.hour
    
    def getMinutes(self, out: bool) -> int:
        if out == True:
            print(self.minutes)
            return 0
        return self.minutes
    
    def getSeconds(self, out: bool) -> int:
        if out == True:
            print(self.seconds)
            return 0
        return self.seconds
    
    def getMicroSecs(self, out: bool) -> int:
        if out == True:
            print(self.microseconds)
            return 0
        return self.microseconds
    