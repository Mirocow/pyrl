# FILE: plugins/datetime/plugin.py
"""
DateTime Plugin for Pyrl
Provides date and time manipulation functions
"""

from pyrl_plugin_system import PluginBase
from datetime import datetime, date, timedelta
import time


class DateTimePlugin(PluginBase):
    """Date and time functions"""
    
    NAME = "datetime"
    VERSION = "1.0.0"
    DESCRIPTION = "Date and time manipulation functions"
    AUTHOR = "Pyrl Ecosystem Team"
    
    def on_load(self):
        """Register datetime functions"""
        self.register_function("now", self._now)
        self.register_function("today", self._today)
        self.register_function("format_date", self._format_date)
        self.register_function("parse_date", self._parse_date)
        self.register_function("date_add", self._date_add)
        self.register_function("date_diff", self._date_diff)
        self.register_function("timestamp", self._timestamp)
        self.register_function("strftime", self._strftime)
        self.register_function("year", self._year)
        self.register_function("month", self._month)
        self.register_function("day", self._day)
        self.register_function("hour", self._hour)
        self.register_function("minute", self._minute)
        self.register_function("second", self._second)
        self.register_function("weekday", self._weekday)
        self.log("DateTime functions loaded")
    
    def _now(self):
        """Get current datetime in ISO format"""
        return datetime.now().isoformat()
    
    def _today(self):
        """Get current date in ISO format"""
        return date.today().isoformat()
    
    def _format_date(self, date_str, fmt="%Y-%m-%d"):
        """Format date string"""
        try:
            dt = datetime.fromisoformat(date_str)
            return dt.strftime(fmt)
        except ValueError:
            # Try parsing with common formats
            for fmt_try in ["%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"]:
                try:
                    dt = datetime.strptime(date_str, fmt_try)
                    return dt.strftime(fmt)
                except ValueError:
                    continue
            return date_str
    
    def _parse_date(self, date_str, fmt="%Y-%m-%d"):
        """Parse date string to ISO format"""
        dt = datetime.strptime(date_str, fmt)
        return dt.isoformat()
    
    def _date_add(self, date_str, days=0, hours=0, minutes=0, seconds=0):
        """Add time interval to date"""
        try:
            dt = datetime.fromisoformat(date_str)
            delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            return (dt + delta).isoformat()
        except ValueError:
            return date_str
    
    def _date_diff(self, date1_str, date2_str):
        """Calculate difference between two dates in seconds"""
        dt1 = datetime.fromisoformat(date1_str)
        dt2 = datetime.fromisoformat(date2_str)
        return (dt2 - dt1).total_seconds()
    
    def _timestamp(self):
        """Get current Unix timestamp"""
        return int(time.time())
    
    def _strftime(self, fmt):
        """Format current time with format string"""
        return datetime.now().strftime(fmt)
    
    def _year(self, date_str=None):
        """Get year from date"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.year
    
    def _month(self, date_str=None):
        """Get month from date"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.month
    
    def _day(self, date_str=None):
        """Get day from date"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.day
    
    def _hour(self, date_str=None):
        """Get hour from datetime"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.hour
    
    def _minute(self, date_str=None):
        """Get minute from datetime"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.minute
    
    def _second(self, date_str=None):
        """Get second from datetime"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.second
    
    def _weekday(self, date_str=None):
        """Get weekday (0=Monday, 6=Sunday)"""
        if date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.now()
        return dt.weekday()


# Export plugin class
plugin_class = DateTimePlugin
