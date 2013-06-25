from django.utils.translation import ugettext_lazy as _

# ffmpeg profile
VIDEO_PROFILES = {
    'mp4': {
        'encode_cmd': 'ffmpeg -y -i "%(input)s" "%(output)s"',
        'name': 'MPEG-4',
        'container': 'mp4',
        'thumbnail_cmd': '',
    },
    'flv_w640': {
        'encode_cmd': 'ffmpeg -y -i "%(input)s" -ab 96 -ar 22050 -acodec libmp3lame -ac 1 -r 29.97 -qscale 2 -vf scale=640:-1 "%(output)s"',
        'name': 'Flash video',
        'container': 'flv',
        'thumbnail_cmd': '',
    }
}

# rsync or other cms
# rsync -avP OUT.mp4 -e 'ssh -p 4040' leen@219.151.7.29:/home/leen/tmp/
TRANSPORT_CMD = 'rsync -avz -e "ssh -p 4040" --progress %(file)s leen@219.151.7.24:/home/leen/mediatmp/%(path)s'
#TRANSPORT_CMD = 'script -q /dev/stdout -c "scp -P 4040 %(file)s leen@219.151.7.24:/home/leen/mediatmp/%(path)s"'

REMORE_ROOT = '/home/leen/mediatmp/'
REMOTE_MKDIR_CMS = 'ssh -p 4040 leen@219.151.7.24 mkdir -p %(dir)s'

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

PUBLISH_URL = 'http://219.151.7.28:8000/pubentry/'