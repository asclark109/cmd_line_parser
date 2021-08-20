"""class module for custom object: Task, obj that holds
info about something that needs to be done
"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.1'

# import modules
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
    print(t1.age())
    print(t1)

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
    # create instance variable to store information about what the
    # next unique available ID is
    start_id = 1
    id_iterator = count(start=start_id)

    @classmethod
    def set_id_iterator(self,num):
        self.start_id = num
        self.id_iterator = count(start=num)

    def __init__(self,name,due_date=None,priority = 1):

        # check for bad inputs
        if priority not in [1,2,3]:
            raise ValueError('bad value given for priority \
            (must be in [1,2,3]): '+str(priority))

        # if type(id) != int:
        #     raise TypeError('non-int type given for ID.')
        
        # parse date and confirm correctness
        if due_date is not None:
            self.validate_date(due_date)
            # knowing the date can be parsed,
            # create datetime object with date and save it as a str
            # representation. This is to make use of datetime module's
            # ability to cleanly format date.
            due_date_datetime = datetime.strptime(due_date,"%m/%d/%Y")
            self.due_date = datetime.strftime(due_date_datetime, "%m/%d/%Y")
        else:
            self.due_date = due_date

        # instantiate instance vars
        self.created = datetime.now()
        self.completed = None
        self.name = name
        self.id = next(self.id_iterator)
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

    # def __str__(self):
    #     return "<{0:8d}, {0:20s}, {40s}>".format(self.id,self.name,self.created)

    def age(self):
        delta = datetime.now() - self.created
        return delta.days
        
    def printable_attributes(self):
        id_str = self.id
        age_str = str(self.age())+'d'
        due_date_str = self.due_date if self.due_date is not None else "-"
        return [id_str,age_str,due_date_str,self.priority,self.name]

    def report_attributes(self):
        creation_date_str = self.created.strftime("%c")
        
        if self.completed is not None:
            completion_date_str = self.completed.strftime("%c")
        else:
            completion_date_str = "-"

        return self.printable_attributes() + [creation_date_str, completion_date_str]


if __name__ == '__main__':
    main()


    