import datetime


NASA_APOD_START_DATE = datetime.date(1995, 6, 16)
DATE_TODAY = datetime.date.today()

def check_valid_nasa_date(date_object):
    if date_object < NASA_APOD_START_DATE:
        return f"⚠️ Please enter a date after: {NASA_APOD_START_DATE}"
    elif date_object > DATE_TODAY:
        return f"⚠️ Please enter a date before {DATE_TODAY}"

    return None