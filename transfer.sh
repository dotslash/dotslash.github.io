#!/bin/sh

rsync -avr --rsh='ssh' --delete-after --delete-excluded   _site/ aws-personal-1:~/nginx/ytp_static
