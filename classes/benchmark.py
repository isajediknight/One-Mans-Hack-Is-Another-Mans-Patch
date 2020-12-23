import datetime

class Benchmark:
    def __init__(self):
        # Start the clock
        self.begin_time = datetime.datetime.now()

        # Weeks
        self.weeks = 0
        self.weeks_text = ''

        # Days
        self.days = 0
        self.days_text = ''

        # Hours
        self.hours = 0
        self.hours_text = ''

        # Minutes
        self.minutes = 0
        self.minutes_text = ''

        # Seconds
        self.seconds = 0
        self.seconds_text = ''

        # Microseconds
        self.microseconds = 0
        self.microseconds_text = 'Microseconds'

        # Total Seconds
        self.total_seconds = 0

        # Did we ever stop the counter?
        self.counter_reset = 0

        # Tracks if we are running or not
        self.boolean_running = True

    def reset_start(self):
        """
        Resets all the counters
        """
        # Start the clock
        self.begin_time = datetime.datetime.now()

        # Weeks
        self.weeks = 0
        self.weeks_text = ''

        # Days
        self.days = 0
        self.days_text = ''

        # Hours
        self.hours = 0
        self.hours_text = ''

        # Minutes
        self.minutes = 0
        self.minutes_text = ''

        # Seconds
        self.seconds = 0
        self.seconds_text = ''

        # Microseconds
        self.microseconds = 0
        self.microseconds_text = 'Microseconds'

        # Total Seconds
        self.total_seconds = 0

        # Track we reset
        self.counter_reset += 1

        self.boolean_running = True

    # Are these needed?
    #def start(self):
    #    self.begin_time = datetime.datetime.now()
    #
    #def begin(self):
    #    self.begin_time = datetime.datetime.now()

    def stop(self):
        """
        Stop the benchmark and calculate all the runtime
        """

        # Stop the clock
        self.end_time = datetime.datetime.now()
        self.boolean_running = False
        self.total_seconds = (self.end_time - self.begin_time).seconds
        self.microseconds = (self.end_time - self.begin_time).microseconds

        ans = ''

        # I didn't want changes to total_seconds affecting seconds
        # There has to be a better way to do this
        counter = 0
        while(counter < self.total_seconds):
            counter += 1

        # Makes it it's own number
        convert_seconds = counter

        # Weeks
        weeks = int(convert_seconds // 604800)
        if (weeks == 0):
            pass
        elif (weeks == 1):
            ans += str(weeks) + ' Week '
            self.weeks_text = 'Week'
        else:
            ans += str(weeks) + ' Weeks '
            self.weeks_text = 'Weeks'
        self.set_weeks(weeks)

        convert_seconds = convert_seconds - (weeks * 604800)

        # Days
        days = int(convert_seconds // 86400)
        if (days == 0):
            pass
        elif (days == 1):
            ans += str(days) + ' Day '
            self.days_text = 'Day'
        else:
            ans += str(days) + ' Days '
            self.days_text = 'Days'
        self.set_days(days)

        convert_seconds = convert_seconds - (days * 86400)

        # Hours
        hours = int(convert_seconds // 3600)
        if (hours == 0):
            pass
        elif (hours == 1):
            ans += str(hours) + ' Hour '
            self.hours_text = 'Hour'
        else:
            ans += str(hours) + ' Hours '
            self.hours_text = 'Hours'
        self.set_hours(hours)

        convert_seconds = convert_seconds - (hours * 3600)

        # Minutes
        minutes = int(convert_seconds // 60)
        if (minutes == 0):
            pass
        elif (minutes == 1):
            ans += str(minutes) + ' Minute '
            self.minutes_text = 'Minute'
        else:
            ans += str(minutes) + ' Minutes '
            self.minutes_text = 'Minutes'
        self.set_minutes(minutes)

        convert_seconds = int(convert_seconds - (minutes * 60))

        # Seconds
        if (convert_seconds == 0):
            pass
        elif (convert_seconds == 1):
            ans += str(convert_seconds) + ' Second'
            self.seconds_text = 'Second'
        else:
            ans += str(convert_seconds) + ' Seconds'
            self.seconds_text = 'Seconds'
        self.set_seconds(convert_seconds)

    def end(self):
        """
                Stop the benchmark and calculate all the runtime
                """

        # Stop the clock
        self.end_time = datetime.datetime.now()
        self.boolean_running = False
        self.total_seconds = (self.end_time - self.begin_time).seconds
        self.microseconds = (self.end_time - self.begin_time).microseconds

        ans = ''

        # I didn't want changes to total_seconds affecting seconds
        # There has to be a better way to do this
        counter = 0
        while (counter < self.total_seconds):
            counter += 1

        # Makes it it's own number
        convert_seconds = counter

        # Weeks
        weeks = int(convert_seconds // 604800)
        if (weeks == 0):
            pass
        elif (weeks == 1):
            ans += str(weeks) + ' Week '
            self.weeks_text = 'Week'
        else:
            ans += str(weeks) + ' Weeks '
            self.weeks_text = 'Weeks'
        self.set_weeks(weeks)

        convert_seconds = convert_seconds - (weeks * 604800)

        # Days
        days = int(convert_seconds // 86400)
        if (days == 0):
            pass
        elif (days == 1):
            ans += str(days) + ' Day '
            self.days_text = 'Day'
        else:
            ans += str(days) + ' Days '
            self.days_text = 'Days'
        self.set_days(days)

        convert_seconds = convert_seconds - (days * 86400)

        # Hours
        hours = int(convert_seconds // 3600)
        if (hours == 0):
            pass
        elif (hours == 1):
            ans += str(hours) + ' Hour '
            self.hours_text = 'Hour'
        else:
            ans += str(hours) + ' Hours '
            self.hours_text = 'Hours'
        self.set_hours(hours)

        convert_seconds = convert_seconds - (hours * 3600)

        # Minutes
        minutes = int(convert_seconds // 60)
        if (minutes == 0):
            pass
        elif (minutes == 1):
            ans += str(minutes) + ' Minute '
            self.minutes_text = 'Minute'
        else:
            ans += str(minutes) + ' Minutes '
            self.minutes_text = 'Minutes'
        self.set_minutes(minutes)

        convert_seconds = int(convert_seconds - (minutes * 60))

        # Seconds
        if (convert_seconds == 0):
            pass
        elif (convert_seconds == 1):
            ans += str(convert_seconds) + ' Second'
            self.seconds_text = 'Second'
        else:
            ans += str(convert_seconds) + ' Seconds'
            self.seconds_text = 'Seconds'
        self.set_seconds(convert_seconds)

    def set_microseconds(self,microseconds):
        self.microseconds = microseconds

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
        return self.days

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def get_seconds(self):
        return self.seconds

    def get_microseconds(self):
        return self.microseconds

    def get_weeks_text(self):
        return self.weeks_text

    def get_days_text(self):
        return self.days_text

    def get_hours_text(self):
        return self.hours_text

    def get_minutes_text(self):
        return self.minutes_text

    def get_seconds_text(self):
        return self.seconds_text

    def get_microseconds_text(self):
        return self.microseconds_text

    def current_benchmark_without_stopping(self):
        """
        Print Current timings
        """
        # See where we currently are
        end_time = datetime.datetime.now()
        total_seconds = (end_time - self.begin_time).seconds
        microseconds = (end_time - self.begin_time).microseconds

        ans = ''

        # I didn't want changes to total_seconds affecting seconds
        # There has to be a better way to do this
        counter = 0
        while (counter < total_seconds):
            counter += 1

        # Makes it it's own number
        convert_seconds = counter

        # Weeks
        weeks = int(convert_seconds // 604800)
        if (weeks == 0):
            pass
        elif (weeks == 1):
            ans += str(weeks) + ' Week '
            weeks_text = 'Week'
        else:
            ans += str(weeks) + ' Weeks '
            weeks_text = 'Weeks'

        convert_seconds = convert_seconds - (weeks * 604800)

        # Days
        days = int(convert_seconds // 86400)
        if (days == 0):
            pass
        elif (days == 1):
            ans += str(days) + ' Day '
            days_text = 'Day'
        else:
            ans += str(days) + ' Days '
            days_text = 'Days'
        set_days(days)

        convert_seconds = convert_seconds - (days * 86400)

        # Hours
        hours = int(convert_seconds // 3600)
        if (hours == 0):
            pass
        elif (hours == 1):
            ans += str(hours) + ' Hour '
            hours_text = 'Hour'
        else:
            ans += str(hours) + ' Hours '
            hours_text = 'Hours'

        convert_seconds = convert_seconds - (hours * 3600)

        # Minutes
        minutes = int(convert_seconds // 60)
        if (minutes == 0):
            pass
        elif (minutes == 1):
            ans += str(minutes) + ' Minute '
            minutes_text = 'Minute'
        else:
            ans += str(minutes) + ' Minutes '
            minutes_text = 'Minutes'

        convert_seconds = int(convert_seconds - (minutes * 60))

        # Seconds
        if (convert_seconds == 0):
            pass
        elif (convert_seconds == 1):
            ans += str(convert_seconds) + ' Second'
            seconds_text = 'Second'
        else:
            ans += str(convert_seconds) + ' Seconds'
            seconds_text = 'Seconds'

        return ans

    def human_readable_string(self):
        """
        Returns a string of the elapsed time
        """
        if(self.boolean_running):
            return self.current_benchmark_without_stopping()
        else:
            ans = self.weeks

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
        counter = 0
        while(counter < self.total_seconds):
            counter += 1

        total_seconds = counter

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

        # Seconds
        if (total_seconds == 0):
            pass
        elif (total_seconds == 1):
            ans += str(total_seconds) + ' Second'
        else:
            ans += str(total_seconds) + ' Seconds'
        self.set_seconds(total_seconds)

        if (return_type == 'string'):
            if (ans == ''):
                return '0 Seconds'
            else:
                return ans.strip()
        else:
            return self.get_seconds()