from __future__ import absolute_import, unicode_literals

import enum
from dataclasses import asdict
from typing import Any, Dict, Iterable, Optional, Union

import celery
from celery import chain, chord, group, shared_task, signature
from celery.result import AsyncResult
from pydantic import BaseModel

from .models import GetData

# @shared_task 데코레이터는 어떤 구체화된 app 인스턴스 없이도 task를 만들 수 있게 해줍니다.


class GenerationState(enum.Enum):
    PENDING = "생성 전"
    STARTED = "생성 중"
    FINISHED = "생성 완료"
    SUCCEEDED = "성공"
    FAILED = "실패"


class GenerationTaskResult(BaseModel):
    idx: int
    sub_config: Dict
    generation_result: Dict


@shared_task()
def update_state(meta_data: Dict, state: str):
    meta_data["started"] = state
    return meta_data


@shared_task()
def search_samples(meta_data: Dict):
    result = {"sub_config": 1}, {"generation_result": "result!"}

    result = [
        GenerationTaskResult(
            idx=idx,
            sub_config=sub_config.dict(),
            generation_info=generation_info,  # noqa : E501
        ).dict()
        for idx, (sub_config, generation_info) in enumerate(result)
    ]
    return result


@shared_task()
def publish_notfound_error():
    print("not found Error!")
    raise ValueError


@shared_task()
def group_on_results(
    iterable: Iterable[Any],
    task_signature: Dict[str, Any],
    callback: Dict[str, Any],
    task_signature_errback: Dict[str, Any] = None,
    final: Optional[Dict[str, Any]] = None,
) -> Union[AsyncResult]:
    task_group = group(
        *(
            chain(
                signature(task_signature)
                .clone((item,))
                .set(link_error=task_signature_errback),
                signature(callback),
            )
            for item in iterable
        )
    )

    if final is not None:
        return chord(task_group)(signature(final))
    return task_group.apply_async()


@shared_task()
def mixmaster(
    generation_task_result: Dict[str, Any],
    mixmaster_base_url: str,
    output_bitrate: str,
    mix_before_arrangement: bool,
    # 에러 발생 시 정보를 확인하기 위한 메타데이터
    metadata: Dict[str, str],
) -> Dict[str, Any]:
    generation_task_result = GenerationTaskResult.parse_obj(
        generation_task_result
    )  # noqa : E501
    # mixmaster_delegate = "mixmaster_delegate"
    generation_info = generation_task_result.generation_info

    return GenerationTaskResult(
        idx=generation_task_result.idx,
        sub_config=generation_task_result.sub_config.dict(),
        generation_info=asdict(generation_info),
    ).dict()


@shared_task(name="check_test")
def test():
    task_id = celery.utils.uuid()
    metadata = {
        "user_email": "hennie92@naver.com",
        "template_name": "template_name",
        "task_id": task_id,
        "total": 2,
    }
    task_chain = chain(
        update_state.s(metadata, GenerationState.STARTED.value),
        search_samples.si(
            metadata,
        ).set(link_error=publish_notfound_error.s()),
    ).set(task_id=task_id)

    result = task_chain.apply_async()
    return result


@shared_task(name="data_checking")
def data_add():
    json_data = GetData.objects.get_data_from_db()
    return json_data
