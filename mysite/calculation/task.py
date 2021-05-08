from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import GetData

# @shared_task 데코레이터는 어떤 구체화된 app 인스턴스 없이도 task를 만들 수 있게 해줍니다.


@shared_task(name="check_test")
def test():
    print(" Hello world")
    return "test"


@shared_task(name="data_checking")
def data_add():
    json_data = GetData.objects.get_data_from_db()
    return json_data
