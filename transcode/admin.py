import os

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget, AdminTextInputWidget
from django.utils.safestring import mark_safe
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from transcode.models import Video, CharFileField, OutputFileField
from transcode.forms import VideoAdminForm
from transcode import conf

class AjaxFileWidget(AdminTextInputWidget):
    def __init__(self, attrs={}):
        super(AjaxFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value:
            output.append(_('<div id="id_file"></div></p><p class="file-upload">Current: %s</p>') % value)
        else:
            output.append('<div id="id_file"></div>')

        output.append(super(AjaxFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

    class Media:
        css = {
            'all': ('js/fineuploader-3.5.0.css',)
        }
        js = (
            'js/jquery.min.js',
            'js/jquery.fineuploader-3.5.0.min.js',
            'js/qlmedia.js',
        )

class OutputFileWidget(AdminTextInputWidget):
    def __init__(self, attrs={}):
        super(OutputFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value:
            output.append('<p><a href="/play/?f=/media/%s" target="_blank">%s</a></p>' % (value, value))
        else:
            output.append('<p>-</p>')
        output.append(super(OutputFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ('title', 'source_size', 'resulting_size', 'uploader', 'profile', 'upload_datetime', 'get_encode_status', 'get_transfer_status', 'get_publish_status')
    formfield_overrides = {
        CharFileField: {'widget': AjaxFileWidget},
        OutputFileField: {'widget': OutputFileWidget},
    }

    def source_size(self, obj):
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, obj.file)):
            return "%.2f Mbytes" % (os.path.getsize(os.path.join(settings.MEDIA_ROOT, obj.file))/1024.0/1024.0)
        else:
            return "-"

    def resulting_size(self, obj):
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, obj.output_file)):
            return "%.2f Mbytes" % (os.path.getsize(os.path.join(settings.MEDIA_ROOT, obj.output_file))/1024.0/1024.0)
        else:
            return "-"

    def get_encode_status(self, obj):
        """
        if obj.encode_status == 2:
            status = conf.ENCODE_STATUS[obj.encode_status] + '<span class="encoding_progress" id="pk-%s"></span><script>$("#pk-%s").get_progress({});</script>' % (obj.pk, obj.pk)
        else:
            status = conf.ENCODE_STATUS[obj.encode_status]
        return status
        """
        return '<span class="encode_status" id="es-%s"></span>' % obj.pk
    get_encode_status.allow_tags = True

    def get_transfer_status(self, obj):
        return '<span class="transfer_status" id="ts-%s"></span>' % obj.pk
    get_transfer_status.allow_tags = True

    def get_publish_status(self, obj):
        return '<span class="publish_status" id="ps-%s"></span>' % obj.pk
    get_publish_status.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
        obj.save()

    class Media:
        js = (
            'js/jquery.min.js',
            'js/encode_progress.js',
            'js/media-list.js',
        )

admin.site.register(Video, VideoAdmin)
