import hashlib
import time
import os
import shlex
import subprocess

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

from south.modelsinspector import add_introspection_rules

from celery.task.sets import subtask

from transcode import conf

class CharFileField(models.CharField):
    pass

class OutputFileField(models.CharField):
    pass

add_introspection_rules([], ["^transcode\.models\.CharFileField"])
add_introspection_rules([], ["^transcode\.models\.OutputFileField"])

class MediaBase(models.Model):
    title               = models.CharField(_('title'), max_length=255)
    description         = models.TextField(_("description"), max_length=1500, blank=True)
    file                = CharFileField(_('file'), max_length=255)
    output_file         = OutputFileField(_('output file'), max_length=255, blank=True)
    if_upload           = models.BooleanField(_('if upload'), default=True)
    uploader            = models.ForeignKey(User, verbose_name=_('uploader'), editable=False)
    upload_datetime     = models.DateTimeField(_('upload datetime'), auto_now_add=True, editable=False)
    if_encode           = models.BooleanField(_('if encode'), default=True, help_text=_("If encoding before send to remote server."))
    profile             = models.CharField(_('profile'), max_length=255)
    encode_status       = models.SmallIntegerField(_('encode status'), default=0, help_text=_("Indicates the status of encode this file."))
    encoded_datetime    = models.DateTimeField(_('encoded datetime'), blank=True, null=True, editable=False)
    transfer_status     = models.SmallIntegerField(_('transfer status'), default=0, help_text=_("Indicates the status of upload this file to remote server."))
    transfered_datetime = models.DateTimeField(_('transfered datetime'), blank=True, null=True, editable=False)
    publish_status      = models.BooleanField(default=False, editable=False, help_text=_("Indicates that this entry has publish on website."))
    published_datetime  = models.DateTimeField(_('published datetime'), blank=True, null=True, editable=False)

    class Meta:
        ordering = ('-upload_datetime',)
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")

    def __unicode__(self):
        return u'%s' % self.title

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

class Video(MediaBase):
    thumbnail_image     = models.ImageField(_('thumbnail image'), upload_to='images/%Y/%m/%d', blank=True, null=True, help_text=_("Set this to upload your own thumbnail image for a video"))
    auto_thumbnail      = models.BooleanField(_('auto thumbnail'), default=False, help_text=_("Will auto generate the thumbnail from the video file if checked"))
    thumbnail_offset    = models.PositiveIntegerField(blank=True, default=4, help_text=_("Number of seconds into the video to take the auto thumbnail"))

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")

    def get_profile(self):
        return conf.VIDEO_PROFILES[self.profile]

    @property
    def container(self):
        return self.get_profile().get("container", "media")

    @property
    def encode_cmd(self):
        encode_cmd = self.get_profile().get("encode_cmd")
        input_path = os.path.join(settings.MEDIA_ROOT, self.file)
        args = {"input": input_path, "output": self.output_path}
        return str(encode_cmd % args)

    @property
    def output_path(self):
        s = self.file.split('/')
        output_file = "%s.%s" % (s[-1].split('.')[0], self.container)
        output_dir = os.path.join(settings.MEDIA_ROOT, "OUTPUT", *s[0:-1])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, output_file)
        return output_path

    @property
    def block_path(self):
        return ''.join(self.output_path.split('.')[0:-1]) + '_block.txt'

    def encode_file(self):
        if self.if_encode:
            command = shlex.split(self.encode_cmd)

            # encode file
            block_file = open(self.block_path, "wb")
            # why output in stderr??
            process = subprocess.call(command, stdout=block_file, stderr=subprocess.STDOUT)
        else:
            import shutil
            shutil.copyfile(os.path.join(settings.MEDIA_ROOT, self.file), self.output_path)

        if os.path.isfile(self.output_path):
            return self.output_path.split(settings.MEDIA_ROOT)[-1]

    @property
    def datedir(self):
        return self.upload_datetime.strftime('%Y/%m/%d/')

    @property
    def upload_cmd(self):
        upload_cmd = conf.TRANSPORT_CMD
        args = {"path": self.datedir, "file": self.output_path}
        return str(upload_cmd % args)

    @property
    def transfer_path(self):
        return ''.join(self.output_path.split('.')[0:-1]) + '_transfer.txt'

    def upload_file(self):
        if self.if_upload:
            command = shlex.split(self.upload_cmd)

            remote_dir = conf.REMORE_ROOT + self.datedir
            # make remote dir
            mkdir_cmd = shlex.split(str(conf.REMOTE_MKDIR_CMS % {"dir": remote_dir}))
            process = subprocess.call(mkdir_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            transfer_file = open(self.transfer_path, "wb")
            process = subprocess.call(command, stdout=transfer_file, stderr=subprocess.PIPE)

        return "123"            

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)

        from transcode.tasks import encode_video
        from transcode.tasks import upload_file
        if self.encode_status == 0:
            encode_video.delay(self.id, callback=subtask(upload_file))
        #if self.transfer_status == 0:
        #    print self.upload_cmd
        #    upload_file.delay(self.id)
        """
        import urllib, urllib2
        import requests

        url = 'http://219.151.7.28:8000/pubentry/'
        values = {
            'a': 1,
            'b': 2,
        }
        headers = {
            'User-Agent': 'test',
        }
        r = requests.post(url, values, headers=headers)
        print r.text
        print r.request.headers
        """
