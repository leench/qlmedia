from django import forms
from django.utils.translation import ugettext_lazy as _

from transcode.models import Video
from transcode.conf import VIDEO_PROFILES

VIDEO_PROFILES  = [ (k, v.get("name",k)) for k,v in VIDEO_PROFILES.iteritems()]

ENCODE_STATUS   = [
    (0, _('none')),
    (1, _('encoding')),
    (2, _('encoded')),
]

UPLOAD_STATUS   = [
    (0, _('none')),
    (1, _('uploading')),
    (2, _('uploaded')),
]

class VideoAdminForm(forms.ModelForm):
    profile         = forms.ChoiceField(choices=VIDEO_PROFILES)
    #encode_status   = forms.ChoiceField(choices=ENCODE_STATUS)
    #upload_status   = forms.ChoiceField(choices=UPLOAD_STATUS)

    class Meta:
        model = Video
