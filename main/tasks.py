"""class module for custom object: Tasks, obj that holds Tasks"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.0'

# import modules
from datetime import datetime
import os
import pickle
import task

# global constants
DATA_ROOT_PATH = ''

def main():
    task_list = Tasks()

    print(task.Task.start_id)

    

    task1 = task.Task('get basic exercise (30 min)',r'8/20/2021')
    task2 = task.Task('read book',r'10/2/2021')
    task3 = task.Task('visit sister',r'09/10/2021')
    task4 = task.Task('write some code')

    new_tasks = [task1,task2,task3,task4]

    for new_task in new_tasks:
        task_list.add(new_task)

    #task_list.pickle_tasks()
    # task_list.done(2)
    task_list.list()
    #task_list.report()
    # task_list.delete(2)
    # task_list.report()
    # task_list.query('exercise')
    # task_list.report()
 

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

        # set ID counter to next available unique number for creating new
        # tasks and making sure they are given a unique ID.
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

    # Complete the rest of the methods, change the method definitions as needed
    def list(self):
        """print out the Task objects that are incomplete"""
        incomplete_tasks = [task_item for task_item in self.tasks if not task_item.completed]
        print(self.__str__(incomplete_tasks))

    def delete(self,id):
        """delete a Task from the tasks list (and from memory)"""
        for idx,task_item in enumerate(self.tasks):
            if task_item.id == id:
                # remove from memory
                del self.tasks[idx]

    def report(self):
        """displays all Task objects nicely. Includes extra information (e.g. completion date)
        
        representation idea borrowed from:
        https://www.kite.com/python/answers/how-to-print-a-list-of-lists-in-columns-in-python
        """

        # code below a little complicated. see __str__() for discussion
         
        table_of_tasks_to_print = [["ID", "Age", "Due Date", "Priority", "Task","Created","Completed"]]
        table_of_tasks_to_print +=[["-"*2, "-"*3, "-"*8, "-"*8, "-"*4,"-"*27, "-"*25]]

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
        """prints out a table of tasks containing search_term in task name"""
        related_tasks = [related_task for related_task in self.tasks if search_term in related_task.name]
        print(self.__str__(related_tasks))

    def add(self,new_task):
        """adds new task to the list of tasks. After, sorts
        the tasks list by creation date.
        """
        self.tasks.append(new_task)
        self.tasks.sort(key=lambda x: x.created)

    def __str__(self,opt_task_list = None) -> str:
        """this representation prints out id, description, creation date of all Task
        objects stored in this Tasks object. It prints them out nicely with padding.

        By default, all tasks are displayed. Optionally, a list of tasks can be
        provided for printing a subset of tasks.
        
        representation idea borrowed from:
        https://www.kite.com/python/answers/how-to-print-a-list-of-lists-in-columns-in-python
        """

        # code below a little complicated. Basically, we calculate the length of all str objs
        # to be printed in a column of a table, and we have the max str length be the character
        # width set for that column. This is to ensure we can pad each string with enough
        # characters so it prints out nicely (we are printing a list of lists).
         
        table_of_tasks_to_print = [["ID", "Age", "Due Date", "Priority", "Task"]]
        table_of_tasks_to_print +=[["-"*2, "-"*3, "-"*8, "-"*8, "-"*4,]]

        # grab things we want to print from each task object    
        if opt_task_list:
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


    