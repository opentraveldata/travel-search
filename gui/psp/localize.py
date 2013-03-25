#!/usr/bin/python

import socket

# Log files
www_log_filename = '/var/log/webapps/airports/www.log'
trep_log_filename = '/var/log/webapps/airports/opentrep.log'
tmp_trep_log_filename = '/var/log/webapps/airports/tmp_opentrep.log'

# Airport service
airport_service_path = '/var/www/webapps/airport_service'
airport_service_path_dict = {
        'www': '/var/www/webapps/airport_service'
        }

# OpenTREP path (see http://github.com/opentraveldata/optd)
traveldb_path = '/var/www/webapps/opentrep/trep/traveldb'
libpyopentrep_path = '/var/www/webapps/opentrep/trep/lib'

# Specific configuration for some servers
hostname = socket.gethostname()
main_name = hostname.split('.')[0]

if main_name in airport_service_path_dict.keys():
    airport_service_path = airport_service_path_dict[main_name]

