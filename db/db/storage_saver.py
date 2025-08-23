import json
from models.habit import Habit
from db.habit_names import habits as all_defined_habits
# Renaming the habits list as predefined to prevent confusion in names.
from datetime import datetime, date

"""
This file contains the functions' management of the main tasks of the program: deleting a habit, appending a habit into the
list of previously existing habits, saving the habit, checking off a habit and calculating the streaks. It does that by
expecting arguments provided from the "main.py" menu() function and creating a Habit object as well as using the methods 
from the "habit.py" file to calculate the streaks and correctly check off the habit.
"""


file_name = 'db/habits.json'
habit_names_file = 'db/habit_names.py'
# Importing the two mains storage files where the habits data is stored.

def load_habits():

    """
    Uploading the habits' data from the JSON file as a list of dictionaries and saves them. If the habit exists in
    "habit_names.py" but not in "habits.json", it adds it into both of the files.
    Return:
        list: list of dictionaries habits with their attributes.
    """


    try:
        with open(file_name, 'r') as f:
            stored_habits = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stored_habits = []
    # If the file does nto exist it gives an empty list.
    stored_habits_dict = {h["name"]: h for h in stored_habits}
    # This line of code looks complicated but what it does is it convert as list of stored habits into dict for quick
    # lookup by name.
    merged_habits = []
    new_habits_added = False

    for defined_habit in all_defined_habits:
        habit_name = defined_habit.habit_name
        periodicity = defined_habit.periodicity

        if habit_name in stored_habits_dict:
            habit_data = stored_habits_dict[habit_name]
            merged_habits.append(habit_data)
        else:
            new_habit_data = {
                "name": habit_name,
                "periodicity": periodicity,
                "time of creation": datetime.now().isoformat(),
                "streak": 0,
                "days_list": [],
                "log_ins": []
            }
            merged_habits.append(new_habit_data)
            new_habits_added = True

    if new_habits_added:
        save_habits(merged_habits)

    return merged_habits


def save_habits(habits):
    """
    Saves the renewed list into the JSON file.
    Args:
        habits (list): List of dictionaries representing habits.
    """
    with open(file_name, 'w') as f:
        json.dump(habits, f, indent=2)


def append_habit_to_json(new_habit: Habit):
    """
    Saves a new habit into the already existing list of habits. It uploads the information from the JSON file and
    checks. If it does not the function creates a habit object, appends it to the list and saves the whole information
    back to the JSON file.
    """

    try:
        with open(file_name, 'r') as f:
            habits = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        habits = []

    existing_names = {h['name'] for h in habits}

    if new_habit.habit_name in existing_names:
        return

    habit_dict = new_habit.to_dict()
    habit_dict["streak"] = 0
    habit_dict["days_list"] = []
    habit_dict["log_ins"] = []
    habit_dict["time of creation"] = datetime.now().isoformat()

    habits.append(habit_dict)
    save_habits(habits)


def user_check_off(habit_name: str):
    """
    Checks off the habit which the user called. Finds the habit in the JSON file and it reconstructs the habit object,
    then it calls the checked_off() method from "habit.py". Appends the log_ins list as well ad the days list (if needed).
    Prints a statement saying the habit has been checked off successfully.

    Args:
        habit_name, from the main.py menu()
    """

    try:
        with open(file_name, 'r') as f:
            habits = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No habits file found.")
        return

    found_index = None
    habit_obj = None

    for i, h in enumerate(habits):
        if h.get("name") == habit_name:
            found_index = i
            # Creates once again the Habit objects from the JSON information.
            habit_obj = Habit(h["name"], h["periodicity"])
            habit_obj.created_at = h.get("time of creation", habit_obj.created_at)
            habit_obj.log_ins = [datetime.fromisoformat(ts) for ts in h.get("log_ins", [])]
            habit_obj.days_list = [date.fromisoformat(d) for d in h.get("days_list", [])]
            break

    if habit_obj is None:
        print(f"Habit '{habit_name}' not found.")
        return

    habit_obj.checked_off()
    # Recalculating the streak each time is safer than importing the streak value from JSON
    # because the JSON file information is the last saved information therefore it could be
    # outdated.
    habit_obj.sort_days_only()
    habit_obj.streaks()

    updated = habit_obj.to_dict()
    updated["time of creation"] = habits[found_index].get("time of creation", updated["time of creation"])
    habits[found_index] = updated

    with open(file_name, 'w') as f:
        json.dump(habits, f, indent=2)

    print(f"Habit '{habit_name}' has been checked off!")


def user_streaks(habit_or_name):
    """
    Updates the current streak of the habit. Recreated the Habit object and calls the streaks() method to savely updated
    the streak corresponding today's date and knowing the previous information - the days and log ins lists.
    Arg:
        habit_or_name:
    Returns:
        int: The updates streak as an integer.
    """

    habits = load_habits()  # Calls the previous function in order to load the merged habits' data and saves it into a
    # list called habit.


    if isinstance(habit_or_name, str):
        habit_data = next((h for h in habits if h["name"] == habit_or_name), None)
        if not habit_data:
            return 0
    else:
        habit_data = habit_or_name

    # Recreate Habit object
    habit_obj = Habit(habit_data["name"], habit_data.get("periodicity", "daily"))
    habit_obj.created_at = habit_data.get("time of creation", habit_obj.created_at)
    habit_obj.log_ins = [datetime.fromisoformat(ts) for ts in habit_data.get("log_ins", [])]
    habit_obj.days_list = [datetime.fromisoformat(d) for d in habit_data.get("days_list", [])]

    # Always recalculate streak. Errors may arieses if we simply expect to get the streaks value from the JSON file. That it
    # why the streaks should always be updated.
    habit_obj.streaks()
    return habit_obj.current_streak


def delete_habit(habit_name):
    """
    Deletes the habit that the user called from both files "habit_names.py" and "habits.json".
    Arg: habit_name: From "main.py" menu().
    """
    import json
    from models.habit import Habit
    from db import habit_names


    updated_habits = []
    for h in habit_names.habits:
        # Rebuilding the "habit_names.py" file without the habit we want to delete.
        name = h if isinstance(h, str) else h.habit_name
        periodicity = "daily" if isinstance(h, str) else h.periodicity
        if name != habit_name:
            updated_habits.append(Habit(name, periodicity))

    with open("db/habit_names.py", "w") as f:
        f.write("from models.habit import Habit\n\n")
        f.write("habits = [\n")
        for h in updated_habits:
            f.write(f"    Habit('{h.habit_name}', '{h.periodicity}'),\n")
        f.write("]\n")


    try:
        with open("db/habits.json", "r") as f:
            habits = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        habits = []

    habits = [h for h in habits if h["name"] != habit_name]

    with open("db/habits.json", "w") as f:
        json.dump(habits, f, indent=2)

    print(f"Habit '{habit_name}' deleted from habit_names.py and habits.json successfully.")
