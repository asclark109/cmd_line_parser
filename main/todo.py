"""main module for running cmd line task manager"""

# metadata
__author__ = 'Austin Clark'
__version__ = '1.0.0'

# import modules
import argparse
import task
import tasks


def main():
    # load up Tasks object
    task_mnger = tasks.Tasks()

    # get -h argument by default
    parser = argparse.ArgumentParser()

    # add optional arguments
    parser.add_argument("--add", type=str, help="a task string to add to your list")
    parser.add_argument('--due', type=str, required=False, help='due date in dd/MM/YYYY format')
    parser.add_argument("--delete", type=int, help="ID of task to delete")
    parser.add_argument("--priority",type=int, required=False, default=1, help="priority of task; default value is 1")
    parser.add_argument("--list", action='store_true', required=False, help="list all tasks that have not been completed")
    parser.add_argument("--report", action='store_true', required=False, help="list all tasks")
    parser.add_argument("--query",  type=str, required=False, nargs="+", help="priority of task; default value is 1")
    parser.add_argument("--done", type=int, help="ID of task to complete")

    # Parse the argument
    args = parser.parse_args()

    # handle arguments
    if args.add:
        if args.due:
            if args.priority:
                new_task = task.Task(args.add,args.due,args.priority)
            else:
                new_task = task.Task(args.add,args.due)
        else:
            new_task = task.Task(args.add)
        task_mnger.add(new_task)
    elif args.delete:
        task_mnger.delete(args.delete)
    elif args.list:
        task_mnger.list()
    elif args.report:
        task_mnger.report()
    elif args.query:
        task_mnger.query(args.query)
    elif args.done:
        task_mnger.done(args.done)
        
    task_mnger.pickle_tasks()


if __name__ == "__main__":
    main()