"""class module for custom object task"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.0'

# import modules
import re                             # parsing dates
import time
from datetime import date, datetime   # handle dates
from itertools import count           # handle ID counting

def main():
    t = Task("feed me","01/25/1995")
    print(t.name)
    print(t.id)
    print(t.due_date)

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

    # instantiate a counter to assign ID's to task objects
    # when created
    id_counter = count()

    def __init__(self,name,due_date,priority = 1):

        # check for bad inputs
        if priority not in [1,2,3]:
            raise ValueError('bad value given for priority (must be in [1,2,3]): '+str(priority))
        
        # parse date using regex.
        regex_date = r'[0]{0,1}([1-9]{1,2}[0-9]{0,1}/[0-9]{2}/[0-9]{4})'
        date_match = re.search(regex_date,due_date)
        if not date_match:
            raise ValueError('had trouble parsing due-date: '+str(due_date))

        # instantiate instance vars
        self.created = datetime.now()
        self.completed = None
        self.name = name
        self.id = next(self.id_counter)
        self.priority = priority
        self.due_date = ''.join(date_match.group(1))

if __name__ == '__main__':
    main()


    