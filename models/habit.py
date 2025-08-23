from datetime import datetime, timedelta, date


class Habit:
   """
   The Habit class main purpose is to create objects - habits that function as real objects
   in Python. This class captures the essence of the habit, its periodicity, the time it
   was created, each log in, each date it was checked off, calculates the streaks and most
   importantly, it converts these attributes into a dictionary by the end of it.
   """


   def __init__(self, habit_name: str, periodicity: str):
       """
       Initializes the habit object.
       Args:
           habit_name (str): name of the habit.
           periodicity (str): periodicity of the habit (daily/weekly).
       """


       self.habit_name = habit_name
       self.periodicity = periodicity
       self.created_at = datetime.now().isoformat()
       self.log_ins = []
       self.current_streak = 0
       self.days_list = []


   def checked_off(self):
       """
       Checks off a habit and appends the log_ins list each time this habit is checked off.
       """


       current_time = datetime.now()
       if current_time.date() not in [d.date() for d in self.log_ins]:
           self.log_ins.append(current_time)


   def sort_days_only(self):
       """
       Organizes the log_ins list and exerts only singular days, creating a new list.
       Returns:
           list: A days list containing the log_ins dates (each date is mentioned only once).
       """


       # Normalize all entries to date objects
       normalized_days = []
       for d in self.days_list:
           if isinstance(d, datetime):
               normalized_days.append(d.date())
           elif isinstance(d, date):
               normalized_days.append(d)
           else:
               raise TypeError(f"Unexpected type in days_list: {type(d)}")


       self.days_list = sorted(normalized_days, reverse=True)


       # Ensure all log_ins are accounted for
       existing_days = set(self.days_list)
       for login in self.log_ins:
           login_day = login.date()
           if login_day not in existing_days:
               self.days_list.append(login_day)
               existing_days.add(login_day)


       # Sort again after adding any missing days
       self.days_list = sorted(self.days_list, reverse=True)


       return self.days_list


   def streaks(self):
       """
       Calculates the streaks based on periodicity. A habit is broken automatically if it
       is not checked off by the user in two or more consecutive days (and for weekly habits,
       two or more consecutive days).
       Returns:
           int: The current streak length.
       """


       self.sort_days_only()  # Ensure days_list is clean and sorted
       if not self.days_list:
           self.current_streak = 0
           return 0


       today = datetime.now().date()
       streak = 0


       # The daily streaks are separated from the weekly streaks calculations.
       if self.periodicity == 'daily':
           days = sorted(self.days_list, reverse=True)
           last_day = days[0]


           # If last check-in was not today → streak reset
           if (today - last_day).days > 0:
               self.current_streak = 0
               return 0


           streak = 1
           for i in range(1, len(days)):
               if (days[i - 1] - days[i]).days == 1:
                   streak += 1
               else:
                   break


       # Weekly streaks calculation.
       elif self.periodicity == 'weekly':
           week_list = []
           for d in self.days_list:
               year_week = d.isocalendar()[:2]  # (year, week number)
               if year_week not in week_list:
                   week_list.append(year_week)


           week_list.sort(reverse=True)
           current_year, current_week, _ = today.isocalendar()
           last_year, last_week = week_list[0]


           # If no activity this week → streak reset
           if (last_year, last_week) != (current_year, current_week):
               self.current_streak = 0
               return 0


           streak = 1
           for i in range(1, len(week_list)):
               prev_year, prev_week = week_list[i - 1]
               curr_year, curr_week = week_list[i]


               # Same year consecutive weeks
               if prev_year == curr_year and prev_week - curr_week == 1:
                   streak += 1
               # Year rollover consecutive weeks
               elif prev_year - curr_year == 1:
                   weeks_in_prev_year = datetime(prev_year, 12, 28).isocalendar()[1]
                   if prev_week == weeks_in_prev_year and curr_week == 1:
                       streak += 1
                   else:
                       break
               else:
                   break


       self.current_streak = streak
       return streak


   def to_dict(self):
       """
       Formalizes the habit data into a readable dictionary.
       Returns:
           dict: A dictionary with habit's details.
       """


       return {
           "name": self.habit_name,
           "periodicity": self.periodicity,
           "time of creation": self.created_at,
           "streak": self.current_streak,  # kept for JSON saving
           "days_list": [d.isoformat() for d in self.days_list],
           "log_ins": [dt.isoformat() for dt in self.log_ins]
       }

