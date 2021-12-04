from datetime import datetime
import time
import pendulum

if __name__ == "__main__":
    dt = pendulum.datetime(2021, 11, 22)

    print(dt)
    print(isinstance(dt, datetime))
    print(dt.timezone.name)
    print(dt.to_date_string())
    print(dt.to_time_string())
    print(dt.to_datetime_string())
    print(dt.to_formatted_date_string())
    print(dt.to_day_datetime_string())
    print(dt.to_cookie_string())
    print(dt.is_future())
    print(dt.is_past())
    print(dt.is_leap_year())

    dt2 = pendulum.now()
    p = dt2.diff(dt)
    print(p.in_days)
    print(p.in_months)
    print(dt2.diff_for_humans(dt))
