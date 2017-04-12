#!/bin/sh -x

rm /usr/local/bin/unipagerled.py
rm -i /etc/unipagerledconfig.py
rm /usr/local/lib/systemd/system/unipagerled.service

systemctl daemon-reload
