#!/usr/bin/env python

import os
import subprocess

command = ['ffmpeg', '-y', '-i', '1.avi', '1.mp4']

stdout = open("stdout.txt","wb")
stderr = open("stderr.txt","wb")
subprocess.call(command,stdout=stdout,stderr=stderr)
