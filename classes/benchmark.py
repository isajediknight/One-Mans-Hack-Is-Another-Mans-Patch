import datetime

class Benchmark:
    def __init__(self):
        self.begin_time = datetime.datetime.now()
        self.weeks = 0
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.total_seconds = 0
        self.counter_reset = 0

    def reset_start(self):
        self.begin_time = datetime.datetime.now()
        self.counter_reset += 1

    def start(self):
        self.begin_time = datetime.datetime.now()

    def begin(self):
        self.begin_time = datetime.datetime.now()

    def stop(self):
        self.end_time = datetime.datetime.now()
        self.total_seconds = self.seconds_to_human_readable((self.begin_time - self.end_time).seconds)

    def end(self):
        self.end_time = datetime.datetime.now()
        self.total_seconds = self.seconds_to_human_readable((self.begin_time - self.end_time).seconds)

    def set_weeks(self,weeks):
        self.weeks = weeks

    def set_days(self,days):
        self.weeks = days

    def set_hours(self,hours):
        self.hours = hours

    def set_minutes(self,minutes):
        self.minutes = minutes

    def set_seconds(self,seconds):
        self.seconds = seconds

    def get_weeks(self):
        return self.weeks

    def get_days(self):
        return self.weeks

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def get_seconds(self):
        return self.seconds

    def current_benchmark(self):
        """
        Print Current timings
        """
        return seconds_to_human_readable(self.total_seconds)

    def seconds_to_human_readable(self, seconds, return_type='string'):
        """
        Method to get the difference between times more human readable

        begin_time and end_time need to be datetime.datetime objects

        return_type can be:
             String
             Int (Seconds)
        """
        # If I ever make this a standalone method it'll need these imports
        # import datetime,sys,platform
        # from collections import namedtuple

        if (type(seconds) != type(0)):
            if (return_type == 'string'):
                return "Please call the method 'seconds_to_human_readable' with an integer"
            else:
                return self.get_seconds()
        else:
            # We're good to do calculations
            ans = ''

        # I didn't want changes to total_seconds affecting seconds
        total_seconds = seconds + 1
        total_seconds = total_seconds - 1
        print("start: " + str(self.total_seconds))

        # Weeks
        weeks = int(total_seconds // 604800)
        if (weeks == 0):
            pass
        elif (weeks == 1):
            ans += str(weeks) + ' Week '
        else:
            ans += str(weeks) + ' Weeks '
        self.set_weeks(weeks)

        total_seconds = total_seconds - (weeks * 604800)
        print("1: " + str(total_seconds))

        # Days
        days = int(total_seconds // 86400)
        if (days == 0):
            pass
        elif (days == 1):
            ans += str(days) + ' Day '
        else:
            ans += str(days) + ' Days '
        self.set_days(days)

        total_seconds = total_seconds - (days * 86400)
        print("2: " + str(total_seconds))

        # Hours
        hours = int(total_seconds // 3600)
        if (hours == 0):
            pass
        elif (hours == 1):
            ans += str(hours) + ' Hour '
        else:
            ans += str(hours) + ' Hours '
        self.set_hours(hours)

        total_seconds = total_seconds - (hours * 3600)
        print("3: " + str(total_seconds))

        # Minutes
        minutes = int(total_seconds // 60)
        if (minutes == 0):
            pass
        elif (minutes == 1):
            ans += str(minutes) + ' Minute '
        else:
            ans += str(minutes) + ' Minutes '
        self.set_minutes(minutes)

        total_seconds = int(total_seconds - (minutes * 60))
        print("4: " + str(total_seconds))

        # Seconds
        if (total_seconds == 0):
            pass
        elif (total_seconds == 1):
            ans += str(total_seconds) + ' Second'
        else:
            ans += str(total_seconds) + ' Seconds'
        self.set_seconds(total_seconds)
        print("5: " + str(total_seconds))

        if (return_type == 'string'):
            if (ans == ''):
                return '0 Seconds'
            else:
                return ans.strip()
        else:
            return self.get_seconds()