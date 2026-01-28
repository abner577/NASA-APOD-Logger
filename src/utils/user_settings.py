import json
from pathlib import Path
from src.config import user_settings_path, user_settings_name

initial_automatically_redirect_dict = {
    "automatically_redirect": "yes"
}

initial_launch_count_dict = {
    "launch_count": "0"
}


def check_if_user_settings_exist():
    return Path(user_settings_path).is_file()


def create_user_settings():
    if check_if_user_settings_exist():
        print(f"Settings file already exists: '{user_settings_name}'. Skipping.")
        return

    Path(user_settings_path).touch()

    try:
        with open(file=user_settings_path, mode="w", encoding="utf-8") as file:
            file.write(json.dumps(initial_automatically_redirect_dict, ensure_ascii=False) + "\n")
            file.write(json.dumps(initial_launch_count_dict, ensure_ascii=False) + "\n")

    except PermissionError:
        print(f"Permission denied: Unable to write '{user_settings_name}' at '{user_settings_path}' ❌")
    except Exception as e:
        print(e)

    print(f"Created settings file: '{user_settings_name}' ✅")


# when we update, we need to write back the second setting as well
# so we would call the get_launch_count method
def update_user_settings():
    if not check_if_user_settings_exist():
        print(f"Settings file not found: '{user_settings_name}'. Please create it first.")
        return

    try:
        updated_setting = input('\nAuto-open APOD links in your browser? Type "yes" or "no": ').strip().lower()

        if updated_setting != "yes" and updated_setting != "no":
            print('Invalid input. Please enter "yes" or "no".\n')
            return

    except Exception as e:
        print(e)
        return

    current_automatically_redirect_dict = {"automatically_redirect": updated_setting}
    current_launch_count_dict = get_launch_count()

    try:
        with open(file=user_settings_path, mode="w", encoding="utf-8") as file:
            file.write(json.dumps(current_automatically_redirect_dict, ensure_ascii=False) + "\n")
            file.write(json.dumps(current_launch_count_dict, ensure_ascii=False) + "\n")


    except PermissionError:
        print(f"Permission denied: Unable to read/write '{user_settings_name}' at '{user_settings_path}' ❌")
    except Exception as e:
        print(e)

    print(f"Updated settings: '{user_settings_name}' ✅")


def get_user_settings():
    if not check_if_user_settings_exist():
        print(f"Settings file not found: '{user_settings_name}'. Please create it first.")
        return None

    count = 0

    try:
        with open(file=user_settings_path, mode="r", encoding="utf-8") as file:
            for line in file:
                count += 1
                content = json.loads(line)

                if count == 1:
                    return content

    except PermissionError:
        print(f"Permission denied: Unable to write '{user_settings_name}' at '{user_settings_path}' ❌")
    except Exception as e:
        print(e)

    return None


# when we update this we need to write back automatically_redirect as well which is why we call the get_user_settings method
def increment_launch_count(current_launch_count):
    current_launch_count += 1

    current_automatically_redirect_dict = get_user_settings() # returns user settings

    current_launch_count_dict = {
        "launch_count": f"{current_launch_count}"
    }

    try:
        with open(file=user_settings_path, mode="w", encoding="utf-8") as file:
            file.write(json.dumps(current_automatically_redirect_dict, ensure_ascii=False) + "\n")
            file.write(json.dumps(current_launch_count_dict, ensure_ascii=False) + "\n")

    except PermissionError:
        print(f"Permission denied: Unable to write '{user_settings_name}' at '{user_settings_path}' ❌")
    except Exception as e:
        print(e)


def get_launch_count():
    count = 0

    try:
        with open(file=user_settings_path, mode="r", encoding="utf-8") as file:
            for line in file:
                count += 1
                content = json.loads(line)
                if count == 2:
                    return content

    except PermissionError:
        print(f"Permission denied: Unable to read '{user_settings_name}' at '{user_settings_path}' ❌")
    except Exception as e:
        print(e)