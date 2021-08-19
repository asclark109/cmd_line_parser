"""class module for custom object: Tasks, obj that holds Tasks"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.0'

# import modules
import os
import pickle
import task

# global constants
DATA_PATH = ''

def main():
    task1 = task.Task('get basic exercise (30 min)',r'8/20/2021')
    task2 = task.Task('read book',r'10/2/2021')
    task3 = task.Task('visit sister',r'09/10/2021')
    task4 = task.Task('write some code',r'11/01/2021')

    new_tasks = [task1,task2,task3,task4]

    task_list = Tasks()

    for new_task in new_tasks:
        task_list.add(new_task)

    print(task_list)
 

    

class Tasks:
    """A list of `Task` objects."""

    def __init__(self):
       """Read pickled tasks file into a list"""
       # List of Task objects
       self.tasks = [] 
       # # your code here

    def pickle_tasks(self):
        """Pickle your task list to a file"""
        # your code here

    # Complete the rest of the methods, change the method definitions as needed
    def list(self):
        pass

    def report(self):
        """displays all tasks nicely"""
        for saved_task in self.tasks:
            print(saved_task)

    def done(self):
        pass

    def query(self):
        pass

    def add(self,new_task):
        """adds new task to the list of tasks. After, sorts
        the tasks list by creation date.
        """
        self.tasks.append(new_task)
        self.tasks.sort(key=lambda x: x.created)

    def __str__(self) -> str:
        """this representation prints out id, description, creation date of all Task
        objects stored in this Tasks object. It prints them out nicely with padding.
        
        representation idea borrowed from:
        https://www.kite.com/python/answers/how-to-print-a-list-of-lists-in-columns-in-python
        """

        # code below a little complicated. Basically, we calculate the length of all str objs
        # to be printed in a column of a table, and we have the max str length be the character
        # width set for that column. This is to ensure we can pad each string with enough
        # characters so it prints out nicely (we are printing a list of lists).
  
        # grab things we want to print from each task object
        table_of_objs_to_print = [[this_task.id,this_task.name,this_task.created] for this_task in self.tasks]
        table_of_objs_to_print = [[str(x[0]),str(x[1]),str(x[2])] for x in table_of_objs_to_print]

        # calculate the character width of every str to be printed out,
        # and calculate the minimum amount of space needed to fit all strs
        # in a column
        length_of_elements = [[len(item[0]),len(item[1]),len(item[2])] for item in table_of_objs_to_print]
        column_widths = list(map(list, zip(*length_of_elements)))
        max_column_widths = [max(width) for width in column_widths]

        # print out the list of lists, padding each string with the right amount of blank space
        entire_representation = ''
        for row in table_of_objs_to_print:
            for idx,elem in enumerate(row):
                entire_representation += elem.ljust(max_column_widths[idx] + 2)
            entire_representation += "\n"

        return entire_representation


if __name__ == '__main__':
    main()


    