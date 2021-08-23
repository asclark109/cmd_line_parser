"""class module for custom object: Tasks, obj that holds Tasks"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.0'

# import modules
from datetime import datetime
import os
import pickle
import task
import operator

# global constants
DATA_ROOT_PATH = ''

def main():
    # create an instance of Tasks and test basic functionality.
    task_list = Tasks()

    task1 = task.Task('get basic exercise (30 min)',r'8/20/2021')
    task2 = task.Task('read book',r'10/2/2021')
    task3 = task.Task('visit sister',r'09/10/2021')
    task4 = task.Task('write some code')
    new_tasks = [task1,task2,task3,task4]

    for new_task in new_tasks:
        task_list.add(new_task)

    # task_list.pickle_tasks()
    # task_list.done(2)
    # task_list.list()
    # task_list.report()
    # task_list.delete(2)
    # task_list.report()
    # task_list.report()
    task_list.query('exercise')
 

class Tasks:
    """A list of `Task` objects."""

    def __init__(self):
        """Read pickled tasks file into a list"""
        self.tasks = [] 

        # load in data of tasks if such data exists
        path_to_data = os.path.join(DATA_ROOT_PATH,'.todo.pickle')
        if os.path.exists(path_to_data):
            with open(path_to_data, 'rb') as f:
                self.tasks = pickle.load(f)

        # set ID counter to be the next available unique number, determined
        # from examining the ID's already used in the self.tasks list read
        # in from pickle file. Updating ID counter in task.Task class will
        # ensure we use the next available unique ID for naming any new
        # tasks we create. If no pickled data exists, set counter to 1.
        id_list = []
        for task_item in self.tasks:
            id_list.append(task_item.id)
        if id_list:
            task.Task.set_id_iterator(max(id_list)+1) 
        else:
            task.Task.set_id_iterator(1)
            
    def pickle_tasks(self):
        """Pickle task list to a file"""
        with open('.todo.pickle', 'wb') as f:
            pickle.dump(self.tasks,f)

    def list(self):
        """print out the Task objects that are incomplete"""
        incomplete_tasks = self.get_incomplete_tasks()
        # sort with three keys of most importance to least importance: 
        # (1): most importantly, sort by defined due date to not defined (puts '-' at the bottom),
        # (2): next importantly, sort by task priority
        # (3): least importantly, sort by due date.
        incomplete_tasks.sort(key= lambda x: (x.due_date is None,x.priority,x.due_date if x.due_date is not None else "99/99/9999"))
        print(self.__str__(incomplete_tasks))

    def delete(self,id):
        """delete a Task from the tasks list (and from memory)"""
        for idx,task_item in enumerate(self.tasks):
            if task_item.id == id:
                # remove from memory
                del self.tasks[idx]

    def report(self):
        """displays all Task objects nicely. Includes extra information (e.g. completion date)
        
        repurposed a str formatting approach described here:
        https://www.kite.com/python/answers/how-to-print-a-list-of-lists-in-columns-in-python
        """

        # code below a little complicated. see __str__() for discussion
        table_of_tasks_to_print = [["ID", "Age", "Due Date", "Priority", "Task","Created","Completed"]]
        table_of_tasks_to_print +=[["-"*2, "-"*3, "-"*8, "-"*8, "-"*4,"-"*27, "-"*25]]

        # sort tasks
        self.tasks.sort(key=lambda x: x.priority)
        self.tasks.sort(key=lambda x: x.due_date if x.due_date is not None else "-")

        # grab things we want to print from each task object 
        table_of_tasks_to_print += [this_task.report_attributes() for this_task in self.tasks]
        table_of_tasks_to_print = [list(map(str,x)) for x in table_of_tasks_to_print]

        # calculate the character width of every str to be printed out,
        # and calculate the minimum amount of space needed to fit all strs
        # in a column
        length_of_elements = [list(map(len,item)) for item in table_of_tasks_to_print]
        column_widths = list(map(list, zip(*length_of_elements)))
        max_column_widths = [max(width) for width in column_widths]

        # print out the list of lists, padding each string with the right amount of blank space
        entire_representation = ''
        for row in table_of_tasks_to_print:
            for idx,elem in enumerate(row):
                entire_representation += elem.ljust(max_column_widths[idx] + 2)
            entire_representation += "\n"

        print(entire_representation)

    def done(self,id):
        """marks a task complete by changing due date of task to '-'."""
        for task_item in self.tasks:
            if task_item.id == id:
                task_item.due_date = '-'
                task_item.completed = datetime.now()

    def query(self,search_term):
        """prints out a table of tasks containing search_term in task name.
        search_term could be a single str object or a list of str objects.
        """
        incomplete_tasks = self.get_incomplete_tasks()
        related_tasks=[]
        if type(search_term) == list:
            for task in incomplete_tasks:
                if any(term in task.name for term in search_term):
                    related_tasks.append(task)
        else:
            related_tasks += [related_task for related_task in incomplete_tasks if search_term in related_task.name]
        print(self.__str__(related_tasks))

    def add(self,new_task):
        """adds new task to the list of tasks. After, sorts
        the tasks list by creation date.
        """
        self.tasks.append(new_task)
        self.tasks.sort(key=lambda x: x.created)

    def get_incomplete_tasks(self):
        """returns a list of the incomplete tasks."""
        return [task_item for task_item in self.tasks if not task_item.completed]

    def __str__(self,opt_task_list = None) -> str:
        """this representation prints out id, description, creation date of all Task
        objects stored in this Tasks object. It prints them out nicely with padding.

        By default, all tasks are displayed. Optionally, user can pass in a smaller list of
        tasks (opt_task_list) for printing a subset of the tasks (this is used in Tasks.query()).
        
        representation idea borrowed from:
        https://www.kite.com/python/answers/how-to-print-a-list-of-lists-in-columns-in-python
        """

        # code below a little complicated. Basically, we calculate the length of all str objs
        # to be printed in a column of a table, and we have the max str length be the character
        # width set for the padding of that column. This is to ensure we can pad each string 
        # with enough characters so it prints out nicely (we are printing a list of lists).
        table_of_tasks_to_print = [["ID", "Age", "Due Date", "Priority", "Task"]]
        table_of_tasks_to_print +=[["-"*2, "-"*3, "-"*8, "-"*8, "-"*4,]]

        # grab things we want to print from each task object    
        if opt_task_list or opt_task_list == []:
            table_of_tasks_to_print += [this_task.printable_attributes() for this_task in opt_task_list]
        else:
            table_of_tasks_to_print += [this_task.printable_attributes() for this_task in self.tasks]
        table_of_tasks_to_print = [list(map(str,x)) for x in table_of_tasks_to_print]

        # calculate the character width of every str to be printed out,
        # and calculate the minimum amount of space needed to fit all strs
        # in a column
        length_of_elements = [list(map(len,item)) for item in table_of_tasks_to_print]
        column_widths = list(map(list, zip(*length_of_elements)))
        max_column_widths = [max(width) for width in column_widths]

        # print out the list of lists, padding each string with the right amount of blank space
        entire_representation = ''
        for row in table_of_tasks_to_print:
            for idx,elem in enumerate(row):
                entire_representation += elem.ljust(max_column_widths[idx] + 2)
            entire_representation += "\n"

        return entire_representation


if __name__ == '__main__':
    main()


    