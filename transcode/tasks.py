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
        logger.info("Encoding command: %s" % video.encode_cmd)
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
        subtask(callback).delay(video.id)

@task(max_retries=3)
def upload_file(video_id, callback=None):
    video = Video.objects.get(pk=video_id)
    logger.info("Upload %s" % video)
    try:
        video.transfer_status = 2
        video.save()
        logger.info("Uploading command: %s" % video.upload_cmd)
        file_url = video.upload_file()
        video.transfer_status = 3
        video.save()
        logger.info("Done upload for %s" % video)
    except Exception, exc:
        video.transfer_status = 4
        video.save()
        logger.info("Upload file failed for %s - retrying " % video)

    if callback:
        subtask(callback).delay(video.id)
