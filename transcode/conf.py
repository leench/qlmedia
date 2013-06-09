from django.utils.translation import ugettext_lazy as _

# ffmpeg profile
VIDEO_PROFILES = {
    'mp4': {
        'encode_cmd': 'ffmpeg -y -i "%(input)s" "%(output)s"',
        'name': 'MPEG-4',
        'container': 'mp4',
        'thumbnail_cmd': '',
    },
}

TEMP_DIR = '/home/leen/media/temp/'

ENCODE_STATUS = [
    _('none'),      # 0
    _('queue'),     # 1
    _('encoding'),  # 2
    _('encoded'),   # 3
    _('failed'),    # 4
]

UPLOAD_STATUS = []

PUBLISH_STATUS = []
