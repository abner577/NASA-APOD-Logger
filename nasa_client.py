import requests
import os
from dotenv import load_dotenv
import datetime
import json

load_dotenv()

NASA_API_KEY = os.getenv('NASA_API_KEY')
BASE_URL = os.getenv('BASE_URL')
NASA_APOD_START_DATE = datetime.date(1995, 6, 16)

def get_todays_apod():
    print("Getting today's apod...")

    full_url = f"{BASE_URL}?api_key={NASA_API_KEY}"
    response = requests.get(full_url)
    print(response)


    if response.status_code == 200:
        print("Today's apod was successfully retrieved! 🚀")
        apod_data = response.json()
        apod_data = format_apod_data(apod_data)

        if check_if_data_exists():
            print("Writing data to csv... 🗄️")
            log_data_to_csv()

            print("Writing to json... 🗃️")
            log_data_to_json()

            return apod_data

        else:
            print("Data directory doesnt exist ❌. Creating Data Directory... ")
            create_data_directory()

            print("Writing data to csv... 🗄️")
            log_data_to_csv()

            print("Writing to json... 🗃️")
            log_data_to_json()

            return apod_data

    elif response.status_code == 404 or response.status_code == 403:
        print("This is a user error. Check your API key and try again.")
        return None
    elif response.status_code == 500 or response.status_code == 503 or response.status_code == 504:
        print("This is a server error. Try again later.")
        return None

    return None


def get_apod_for_specific_day():
    flag = True
    while flag:
        try:
            print("\n================== GET APOD MENU 🛰️==================")
            user_choice = int(input("Enter (1-2) for one of the options below:\n"
                                    "1. Enter a Date\n"
                                    "2. Exit GET APOD Menu\n"))

            match user_choice:
                case 1:
                    year = int(input("Enter a year (YYYY): "))
                    month = int(input("Enter a month (MM): "))
                    day = int(input("Enter a day (DD): "))

                    date_object = datetime.date(year, month, day)
                    date_today = datetime.date.today()

                    if date_object < NASA_APOD_START_DATE:
                        print("⚠️ Please enter a date after June 16, 1995")
                        print(flag)
                    elif date_object > date_today:
                        print(f"⚠️ Please enter a date before {date_today}")
                    else:
                        full_url = f"{BASE_URL}?api_key={NASA_API_KEY}&date={date_object}"
                        print(full_url)
                        print(date_object)
                        print(f"Retrieving {date_object}'s APOD...")
                        response = requests.get(full_url)
                        print(response)

                        if response.status_code == 200:
                            print("Today's apod was successfully retrieved! 🚀")
                            apod_data = response.json()
                            apod_data = format_apod_data(apod_data)

                            if check_if_data_exists():
                                print("Data directory already exists ✅")

                                print("Writing data to csv... 🗄️")
                                log_data_to_csv()

                                print("Writing to json... 🗃️")
                                log_data_to_json()

                                flag = False
                                return apod_data

                            else:
                                print("Data directory doesnt exist ❌. Creating Data Directory... ")
                                create_data_directory()

                                print("Writing data to csv... 🗄️")
                                log_data_to_csv()

                                print("Writing to json... 🗃️")
                                log_data_to_json()

                                flag = False
                                return apod_data


                        elif response.status_code == 404 or response.status_code == 403:
                            print("🚫 This is a user error. Check your API key and try again.")

                        elif response.status_code == 500 or response.status_code == 503 or response.status_code == 504:
                            print("⚠️ This is a server error. Try again later.")

                case 2:
                    print("Exiting...")
                    flag = False

        except Exception as e:
                print(e)
    return None


def format_apod_data(apod_data):
    cur_time = datetime.datetime.now()
    cur_time = cur_time.strftime("Day: %m-%d-%Y | Time: %H:%M:%S")

    explanation = apod_data["explanation"].split(".") # makes a list of all the diff sentences, then we just want to return the first 2 sentences
    explanation = explanation[0].strip(" ") + "." + explanation[1] + "." # First we strip off all white space from before the first sentence, then we manually add periods right after each sentence.
    print(explanation)

    dict_to_return = {'date': apod_data['date'], 'title': apod_data['title'], 'url': apod_data['url'],
                      'explanation': explanation, 'logged_at': cur_time}

    return dict_to_return


def log_data_to_json():
    pass

def log_data_to_csv():
    pass

def check_if_data_exists():
    return False

def create_data_directory():
    pass