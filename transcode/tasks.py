from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.task.sets import subtask

from transcode.models import Video

logger = get_task_logger(__name__)

@task(max_retries=3)
def encode_video(video_id, callback=None):
    video = Video.objects.get(pk=video_id)
    logger.info("Encoding %s" % video)
    try:
        video.encode_status = 2
        video.save()
        output_file = video.encode_file()
        video.output_file = output_file
        video.encode_status = 3
        video.save()
        logger.info("Done encoding for %s" % video)
    except Exception, exc:
        video.encode_status = 4
        video.save()
        logger.info("Encode Media failed for %s - retrying " % video)

    if callback:
        ubtask(callback).delay(video.id)
