from db.storage_saver import load_habits
from datetime import datetime, date, timedelta

"""
This file contains the code to analyze the habits. Gives all of the habits, then returns them by periodicity, then
if called returns the longest streak for a habit, considering past history and answer the question which habit has 
most streaks. It takes arguments from the "main.py" manu(), specifically the "Analytics menu" section and it uses
the function load.habits() in db.storage_saver.py to load the habits, so that later they can be analyzed. 
"""

def all_habits():
    """
    Loads the habits from the "habits.json" file using the load.habits() function in "storage_saver.py".
    Returns:
        list: A list of the habits' names.
    """

    habits = load_habits()
    if not habits:
        print("No habits found.")
        return []
    print("\nCurrently tracked habits:")
    for h in habits:
        print(f"- {h['name']}")
    return [h["name"] for h in habits]

def habits_by_periodicity(periodicity):
    """
    Once again, with the help of load.habits(), loads the habits and based on their periodicity returns a list of names
    only with the habits that correspond to the said periodicity.
    Args:
        periodicity (str) : One of "daily", "weekly" or "monthly".
    Returns:
        list: A list of the habits' names filtered by the given periodicity.
    """
    habits = load_habits()
    return [h["name"] for h in habits if h["periodicity"] == periodicity]

def _calculate_longest_streak(habit):
    """
    Returns the longest streak for a habit.
    Args:
        habit(dict): A dictionary of the habit.
    Returns:
        int: The longest streak.
    """
    if not habit.get("days_list"):
        return 0

    # Convert all days to date objects.
    days = [datetime.fromisoformat(d).date() if isinstance(d, str) else d for d in habit["days_list"]]
    days = sorted(days)
    # Converting saved days into date objects (strings → datetime.date).

    max_streak = 0
    current_streak = 1
    periodicity = habit.get("periodicity", "daily")
    # Track the maximum streak found so far.

    for i in range(1, len(days)):
        diff = (days[i] - days[i-1]).days
        if (periodicity == "daily" and diff == 1) or (periodicity == "weekly" and diff <= 7):
            current_streak += 1
        else:
            current_streak = 1
        if current_streak > max_streak:
            max_streak = current_streak
    return max_streak

def longest_streak_all():
    """
    Compares and analyzes the streaks for all existing habits. Gives the longest current streak from the habits.
    Returns:
        tuple: A pair (habit_name, max_streak).
    """

    habits = load_habits()
    if not habits:
        print("No habits found. Cannot calculate streaks.")
        return None, 0

    max_streak = 0
    habit_name = None
    for habit in habits:
        streak = _calculate_longest_streak(habit)
        if streak > max_streak:
            max_streak = streak
            habit_name = habit["name"]
    if habit_name is None:
        print("No streaks found for any habit.")
        return None, 0
    return habit_name, max_streak

def longest_streak_habit(habit_name):
    """
    Returns the longest streak for a habit. The function analyzes previous records and returns the longest streak overall
    for the whole past history of the habit.
    Args:
        habit_name (str): The name of the habit.
    Returns:
        streak (int): The longest streak.
    """

    habits = load_habits()
    habit = next((h for h in habits if h["name"] == habit_name), None)
    if not habit:
        print(f"Habit '{habit_name}' not found.")
        return 0
    streak = _calculate_longest_streak(habit)
    if streak == 0:
        print(f"No streaks found for habit '{habit_name}'.")
    return streak