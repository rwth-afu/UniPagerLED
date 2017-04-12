#!/bin/sh -x

cp unipagerled.py /usr/local/bin/unipagerled.py
cp config.py.example /etc/unipagerledconfig.py
mkdir -p /usr/local/lib/systemd/system
cp unipagerled.service /usr/local/lib/systemd/system/unipagerled.service

systemctl daemon-reload
