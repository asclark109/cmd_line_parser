"""tests for task.py"""
import pytest
from main import task


def test_task_objcreation():
    # testing for functionality
    task1 = task.Task('get basic exercise (30 min)',r'8/20/2021')
    task2 = task.Task('read book',r'10/2/2021')
    task3 = task.Task('visit sister',r'09/10/2021')
    task4 = task.Task('write some code',r'11/01/2021')

    # confirm ID counter works
    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3

    # confirm date parser works (converts everything to MM/DD/YYYY)
    assert task1.due_date == r'08/20/2021'
    assert task2.due_date == r'10/02/2021'
    assert task3.due_date == r'09/10/2021'
    assert task4.due_date == r'11/01/2021'

    # test for failure (bad inputs, like bad dates):
    bad_dates = [
        "/20/2000",
        "1//2000",
        "1/2/200",
        "10/20/",
    ]
    for bad_date in bad_dates:
        with pytest.raises(Exception):
            task.Task('some task description',bad_date)