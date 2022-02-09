import random
import time

from celery import shared_task, Task, chain
from celery.result import allow_join_result


@shared_task(bind=True)
def add(self, a, b):
    print("running add!")
    time.sleep(15)
    print(f"a +b : {a + b}")
    time.sleep(15)
    return a + b


@shared_task(bind=True)
def subtract(self, a, b):
    print(f"{self.request.id} running subtract!")
    time.sleep(15)
    print(f"a -b :{a - b}")
    time.sleep(15)
    return a - b


@shared_task(bind=True)
def multiply(self, a, b):
    print(f"{self.request.id} running multi!")
    # raise ValueError("Test Fail Error!")
    time.sleep(15)
    print(f"a * b :{a * b}")
    time.sleep(15)
    return a * b


@shared_task(bind=True)
def divide(self, a, b):
    print(f"{self.request.id} running divide!")
    time.sleep(15)
    print(f"a / b :{a / b}")
    time.sleep(15)
    return a / b


@shared_task(bind=True)
def _get_random_number(a, b):
    print("start running!")
    rand = random.choice(range(1, 10))
    return a + rand, b + rand


@shared_task(bind=True)
def catpure_res(self, value):
    result = []
    task = Task()
    task_obj = task.AsyncResult(task_id=value)
    with allow_join_result():
        for value in task_obj.get():
            result.append(value)
    return result


@shared_task()
def get_random_numbers(a, b):
    tasks = chain(_get_random_number.si(a, b),
                  _get_random_number.si(a + 2, b + 2),
                  _get_random_number.si(a + 4, b + 4)
                  )

    result = tasks.apply_async()
    return result.id
