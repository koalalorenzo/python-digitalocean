# -*- coding: utf-8 -*-

'''
Misc tools and utils

convert_datestamp - donated from harbor-wave by author(GI_Jack)
'''

class Utils:

    def convert_datestamp(in_date):
        '''takes a string from droplet.createdate, and returns a python datetime object'''
        
        from datetime import datetime, tzinfo, timedelta
        from zoneinfo import ZoneInfo
        
        # this is the format that createdate returns
        # see: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        do_timeformat = "%Y-%m-%dT%XZ"
        do_timezone   = ZoneInfo("Zulu")
        local_tz      = datetime.now().astimezone().tzinfo
    
        # get a timedate object out of Digital Ocean's formating, including re-add timezone
        date_obj  = datetime.strptime(in_date,do_timeformat)
        date_obj  = date_obj.replace(tzinfo=do_timezone)
        # convert to local date
        date_obj  = date_obj.astimezone(local_tz)
        # strip timezone because otherwise maths don't work. ?!?!?
        date_obj  = date_obj.replace(tzinfo=None)
        return date_obj
