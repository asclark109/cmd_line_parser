"""class module for custom object: Task, obj that holds
info about something that needs to be done
"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.1'

# import modules
import re                             # parsing dates
import time
from datetime import date, datetime   # handle dates
from dateutil.parser import parse     # validate dates
from itertools import count           # handle ID counting

def main():
    # create a few Task objects to test basic functionality.
    t = Task("feed me","01/25/2021")
    print(t.name)
    print(t.id)
    print(t.due_date)

    t1 = Task("feed me","12/30/2021")
    print(t1.name)
    print(t1.id)
    print(t1.due_date)

class Task:
    """Representation of a task
    
    Attributes:
        - created - date
        - completed - date
        - name - string
        - unique id - number
        - priority - int value of 1, 2, or 3; 1 is default
        - due date - date, this is optional
    """

    # set up a counter to assign ID's to task objects when created
    id_counter = count(start=1)

    def __init__(self,name,due_date,priority = 1):

        # check for bad inputs
        if priority not in [1,2,3]:
            raise ValueError('bad value given for priority (must be in [1,2,3]): '+str(priority))
        
        # parse date and confirm correctness
        self.validate_date(due_date)

        # knowing the date can be parsed,
        # create datetime object with date and save it as a str representation.
        # This is to make use of datetime module's ability to cleanly format date.
        due_date_datetime = datetime.strptime(due_date,"%m/%d/%Y")
        self.due_date = datetime.strftime(due_date_datetime, "%m/%d/%Y")

        # instantiate instance vars
        self.created = datetime.now()
        self.completed = None
        self.name = name
        self.id = next(self.id_counter)
        self.priority = priority

    # helper fcn to validate date: borrowing ideas from 
    # https://stackoverflow.com/questions/16870663/
    # how-do-i-validate-a-date-string-format-in-python/16870699
    def validate_date(self,date_str):
        """uses datetime module to confirm str representation of a date
        can be interpretted as a date. Returns True if str obj is 
        interprettable as a date; returns False otherwise.
        """
        try:
            if date_str != datetime.strptime(date_str, "%m/%d/%Y").strftime('%m/%d/%Y'):
                raise ValueError("Had trouble parsing date")
            return True
        except ValueError:
            return False

    def __str__(self):
        """representation idea borrowed from:
        https://www.kite.com/python/answers/how-to-print-a-list-of-lists-in-columns-in-python
        """
        table_of_objs_to_print = [[this_task.id,this_task.name,this_task.created] for this_task in self.tasks]

        length_list = [len(element) for row in table_of_objs_to_print for element in row]
        column_width = max(length_list)

        entire_representation = ''
        for row in table_of_objs_to_print:
            entire_representation += "".join(element.ljust(column_width + 2) for element in row)

        return entire_representation


if __name__ == '__main__':
    main()


    