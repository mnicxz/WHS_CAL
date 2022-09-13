from datetime import datetime

def timezone_change(time):
    local_time = datetime.now()
    utc_time = datetime.utcnow()
    tmp = local_time-utc_time

    start_time=tmp+time
    return start_time
    # return tmp