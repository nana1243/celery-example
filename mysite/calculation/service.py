from celery import chain, group
from . import task as celery_task
from pydantic import BaseModel


class TaskInfo(BaseModel):
    task_id: str


class CalculationHandler:
    def handle(self, a: int, b: int):
        task_chain = chain(
            celery_task.get_random_numbers.si(a, b),
            celery_task.catpure_res.s(),
            group(
                *(chain(
                    celery_task.add.si(a, b),
                    celery_task.subtract.si(a, b),
                    celery_task.multiply.si(a, b),
                    celery_task.divide.si(a, b)
                )
                )
            )
        )
        result = task_chain.apply_async()

        return TaskInfo(
            task_id=result.id
        )
