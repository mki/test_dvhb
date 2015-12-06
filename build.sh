#!/bin/bash

#PATH=$PATH:/opt/python266/bin:/opt/python266
#export PATH

pip install virtualenv

#Если ругается при pip install lxml
#yum install libxml2-devel libxslt-devel

virtualenv .env --no-site-packages -p python3.4
./.env/bin/pip install -r requirements.txt
