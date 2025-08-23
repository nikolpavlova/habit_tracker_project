from models.habit import Habit
from db.habit_names import habits
from db.storage_saver import append_habit_to_json, user_check_off, user_streaks, delete_habit
import analytics.analytics as analytics




def add_habit_to_habit_names_file(name, periodicity):
    """
    Adds a habit to db/habit_names.py.

    Parameters:
        name (str): The name of the habit.
        periodicity (str): Daily or weekly.
    """
    with open('db/habit_names.py', 'r') as f:
        lines = f.readlines()
    new_line = f"    Habit('{name}', '{periodicity}'),\n"

    for i, line in enumerate(lines):
        if line.strip() == ']':
            lines.insert(i, new_line)
            break

    with open('db/habit_names.py', 'w') as f:
        f.writelines(lines)


def add_habit():
    """"
    Asks the user for the habit name and periodicity.
    """
    name = input("Habit name: ")
    periodicity = input("Periodicity (daily/weekly): ")

    add_habit_to_habit_names_file(name, periodicity)
    new_habit = Habit(name, periodicity)
    append_habit_to_json(new_habit)
    # The habit is created in memory, made into a dictionary and then imported into the JSON file.

    print(f"Habit '{name}' ({periodicity}) added successfully!")


def menu():
    """
    This function represents the main CLI of the program. Displays the options that
    the user can choose from, as well as the analytics menu. Navigates the answer based
    on the choice of the user.
    """
    while True:
        print("\n" + "=" * 40)
        print("📋  Habit Tracker Menu")
        print("=" * 40)
        print("1. Add a new habit")
        print("2. Check off a habit")
        print("3. Calculate streaks")
        print("4. Delete a habit")
        print("5. Analyze your habits")
        print("6. Exit")
        print("=" * 40)
        answer = input("Your choice: ")

        if answer == '1':
            add_habit()
        elif answer == '2':
            habit_name = input("Habit name: ")
            user_check_off(habit_name)
        elif answer == '3':
            habit_name = input("Habit name: ")
            streak = user_streaks(habit_name)
            print(f"Current streak for '{habit_name}': {streak}")
        elif answer == '4':
            habit_name = input("Habit name to delete: ")
            delete_habit(habit_name)
        elif answer == '5':
            while True:
                print("\n📊 Analytics Menu")
                print("1. List all habits")
                print("2. Habits by periodicity")
                print("3. Longest streak overall")
                print("4. Longest streak for a habit")
                print("5. Exit Analytics Menu")
                choice = input("Choose an option: ")

                if choice == '1':
                    analytics.all_habits()
                elif choice == '2':
                    p = input("Enter periodicity (daily/weekly): ")
                    habits = analytics.habits_by_periodicity(p)
                    # Filters between daily and weekly
                    if habits:
                        print(f"\nHabits with '{p}' periodicity:")
                        for h in habits:
                            print(f"- {h}")
                    else:
                        print("No habits found with that periodicity.")
                elif choice == '3':
                    habit_name, streak = analytics.longest_streak_all()
                    if habit_name:
                        print(f"\nHabit with the longest streak: {habit_name} ({streak})")
                    else:
                        print("No habits tracked yet.")
                elif choice == '4':
                    h = input("Habit name: ")
                    streak = analytics.longest_streak_habit(h)
                    print(f"Longest streak for '{h}': {streak}")
                elif choice == '5':
                    print("\nExiting Analytics Menu...")
                    break
                else:
                    print("\n⚠️  Invalid option, try again.")
        elif answer == '6':
            print("\nGoodbye! 👋")
            break
        else:
            print("\n⚠️  Invalid option, try again.")

        print("\n" + "-" * 40)


if __name__ == '__main__':
   menu()


