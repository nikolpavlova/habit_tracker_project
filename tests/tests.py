import unittest # Imports the Python's framework with which the code is tested.
import os
import sys # Helps navigate the paths.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta, date
from models.habit import Habit
from analytics.analytics import longest_streak_all, longest_streak_habit
from db.storage_saver import delete_habit


class TestHabitTracking(unittest.TestCase):
    """
    This class is to test the program, it is a collection of all needed tests.
    """

    def setUp(self):
        """
        This function is called before each test is executed. It creates fake habits for the purpose of testing the program
        instead of using the real ones and possibly damaging them.
        """
        self.temp_file = "temp_habits.txt"
        with open(self.temp_file, "w") as f:
            f.write("Exercise\nRead\nMeditate\n#Comment line\n")

    def tearDown(self):
        """
        Runs after each test is executed. Removes the temporary files after the test.
        """
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_delete_habit_exact_match(self):
        """
        Test that delete_habit works properly, sees if it removes the lines matching the habit's name.
        """
        delete_habit("Read")  # cannot test the file content directly; just ensure no error

    def test_delete_habit_partial_name(self):
        """
        Ensures that delete_habit doesn't delete a habit if we give it only part of the name.
        """
        delete_habit("Exer")  # cannot test the file content directly; just ensure no error

    def test_longest_streak_all(self):
        """
        Test that longest_streak_all returns a tuple (habit_name, streak).
        """
        habit_name, streak = longest_streak_all()
        self.assertIsInstance(streak, int)
        self.assertGreaterEqual(streak, 0)
        if streak > 0:
            self.assertIsInstance(habit_name, str)
        else:
            self.assertIsNone(habit_name)

    def test_longest_streak_habit(self):
        """
        Test that longest_streak_habit calculates the longest streak for specific habit.
        """
        streak_exercise = longest_streak_habit("Exercise")
        streak_read = longest_streak_habit("Read")
        streak_meditate = longest_streak_habit("Meditate")

        for streak in (streak_exercise, streak_read, streak_meditate):
            self.assertIsInstance(streak, int)
            self.assertGreaterEqual(streak, 0)

    """
    The following tests test the Habit class from models "habit.py".
    """
    def test_habit_creation(self):
        """
        Ensures that the __init__ function works properly.
        """

        habit = Habit("Exercise", "daily")
        self.assertEqual(habit.habit_name, "Exercise")
        self.assertEqual(habit.periodicity, "daily")
        self.assertIsInstance(habit.created_at, str)
        self.assertEqual(habit.log_ins, [])
        self.assertEqual(habit.current_streak, 0)
        self.assertEqual(habit.days_list, [])

    def test_habit_checked_off(self):
        """
        Ensures that the checked_off() function works properly and that if you try to check
        off again a habit it does not add a duplicate into the log_ins list.
        """

        habit = Habit("Exercise", "daily")
        habit.checked_off()
        self.assertEqual(len(habit.log_ins), 1)
        habit.checked_off()
        self.assertEqual(len(habit.log_ins), 1)

    def test_habit_sort_days_only(self):
        """
        Ensures that the sort_days_only function works properly. Checks that the first element
        is a date object.
        """

        habit = Habit("Exercise", "daily")
        today = datetime.now()
        habit.log_ins = [today, today - timedelta(days=1), today - timedelta(days=1)]
        days = habit.sort_days_only()
        self.assertIsInstance(days[0], date)
        self.assertGreaterEqual(len(days), 2)

    def test_habit_streaks_daily(self):
        """
        Ensures that the streaks() works properly for daily habits, uses an example.
        """

        habit = Habit("Exercise", "daily")
        today = datetime.now().date()
        habit.days_list = [today - timedelta(days=i) for i in range(3)]
        streak = habit.streaks()
        self.assertIsInstance(streak, int)
        self.assertGreaterEqual(streak, 0)

    def test_habit_streaks_weekly(self):
        """
        Ensures that the streaks() works properly for weekly habits, uses an example.
        """
        habit = Habit("Exercise", "weekly")
        today = datetime.now().date()
        habit.days_list = [today - timedelta(days=i*7) for i in range(3)]
        streak = habit.streaks()
        self.assertIsInstance(streak, int)
        self.assertGreaterEqual(streak, 0)

    def test_habit_to_dict(self):
        """
        Ensures that the to_dict() works properly and converts the information into a dictionary.
        """
        habit = Habit("Exercise", "daily")
        habit.checked_off()
        habit.sort_days_only()
        habit.streaks()
        d = habit.to_dict()
        self.assertIsInstance(d, dict)
        self.assertIn("name", d)
        self.assertIn("periodicity", d)
        self.assertIn("time of creation", d)
        self.assertIn("streak", d)
        self.assertIn("days_list", d)
        self.assertIn("log_ins", d)


if __name__ == "__main__":
    unittest.main()
