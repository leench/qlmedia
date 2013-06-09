import time
import os
import hashlib
import json
import re

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext

from django.conf import settings
from transcode.models import Video
from transcode import conf

@csrf_exempt
@login_required
def ajax_upload(request):
    if request.method == 'POST':
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]

            datedir = time.strftime('%Y/%m/%d/', time.localtime(time.time()))
            dest_dir = conf.TEMP_DIR + datedir

            if not os.path.exists(str(dest_dir)):
                os.makedirs(str(dest_dir))

            salt = str(time.time()) + uploaded_file.name
            if isinstance(salt, unicode):
                salt = salt.encode('utf8')
            filename = hashlib.md5(salt).hexdigest()
            fn_ext = uploaded_file.name.split('.')[-1]

            # save to temp dir
            dest_path = dest_dir + filename + '.' + fn_ext
            dest = open(str(dest_path), 'wb+')
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
            dest.close()

            # copy to media root
            media_path = time.strftime('uploads/media/%Y/%m/%d/', time.localtime(time.time())) + filename + '.' + fn_ext
            if not os.path.exists(settings.MEDIA_ROOT + time.strftime('uploads/media/%Y/%m/%d/', time.localtime(time.time()))):
                os.makedirs(settings.MEDIA_ROOT + time.strftime('uploads/media/%Y/%m/%d/', time.localtime(time.time())))

            import shutil
            shutil.copyfile(dest_path, settings.MEDIA_ROOT + media_path)

        ret_json = {'success': True, 'filename': media_path}        
        return HttpResponse(json.dumps(ret_json), mimetype="text/plain")
    else:
        response = HttpResponseNotAllowed(['POST'])
        response.write("ERROR: Only POST allowed")
        return response

def get_status(request):
    pk = request.GET.get("id", "")
    if pk:
        video = get_object_or_404(Video, pk=pk)
    else:
        raise Http404

    res_json = {
        'es': video.encode_status,
        'ts': video.transfer_status,
        'ps': video.publish_status,
    }
    return HttpResponse(json.dumps(res_json), mimetype="text/plain")

def get_encode_progress(request):
    pk = request.GET.get("id", "")
    if pk:
        video = get_object_or_404(Video, pk=pk)
    else:
        raise Http404

    bp = video.block_path
    if not os.path.isfile(bp):
        return HttpResponse('error')

    block_file = open(bp, "r")
    content = block_file.read()
    block_file.close()

    # http://stackoverflow.com/questions/11441517/ffmpeg-progress-bar-encoding-percentage-in-php
    rawDuration = re.findall(r"Duration: (.*?), start:", content)[0]

    # rawDuration is in 00:00:00.00 format. This converts it to seconds.
    duration = convtosec(rawDuration)

    # get the time in the file that is already encoded
    rawTime = re.findall(r"time=(.*?) bitrate", content)[-1]
    etime = convtosec(rawTime)

    progress = etime/duration*100
    if progress >= 100:
        progress = 100.00
    return HttpResponse("%.2f" % progress)

def convtosec(str):
    if str:
        ar = str.split(":")
        duration = float(ar[2])
        if ar[1]: duration += int(ar[1]) * 60
        if ar[0]: duration += int(ar[0]) * 60 * 60
    else:
        duration = 0.0
    return duration

def play(request, template_name="player.html"):
    file = request.GET.get("f", "")
    return render_to_response(template_name,
                              locals(),
                              context_instance=RequestContext(request))

