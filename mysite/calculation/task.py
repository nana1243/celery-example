from __future__ import absolute_import, unicode_literals

from celery import chain, group, shared_task

from .models import GetData

# @shared_task 데코레이터는 어떤 구체화된 app 인스턴스 없이도 task를 만들 수 있게 해줍니다.


@shared_task(name="check_test")
def test():
    res1 = chain(add.s(1, 2), subtract.s(5), add.s(8))()
    res2 = (add.si(100, 101) | add.si(102, 103) | add.si(104, 105))()
    res3 = group([multi(i, i) for i in range(1, 10)])
    print(res1)
    print(res2)
    print(res3)


@shared_task(name="data_checking")
def data_add():
    json_data = GetData.objects.get_data_from_db()
    return json_data


@shared_task()
def add(int1, int2):
    print("running add!")
    return int1 + int2


@shared_task()
def subtract(int1, int2):
    print("running subtract!")
    return abs(int1 - int2)


@shared_task()
def multi(int1, int2):
    print("running multi!")
    return int1 * int2
