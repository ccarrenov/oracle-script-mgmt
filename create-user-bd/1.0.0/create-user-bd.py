#!/usr/bin/env python
#LOAD LIBRERY DATE TIME
import datetime
#IMPORT OS LIB
import os
#IMPORT RE LIB
import re
#IMPORT SYS LIB
import sys
#LOAD PROPERTIES
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config/create-user-bd.properties')

HOST_NAME_BD = sys.argv[1]
USER_NAME_BD = sys.argv[2]
PASS_BD = sys.argv[3]
PORT_BD = sys.argv[4]
SERVICE_NAME_BD = sys.argv[5]
USER_NAME = sys.argv[6]
PASS_BD_USER = sys.argv[7]
length_parameters = len(sys.argv)

SQL_PLUS_QUERY = config.get('SQL_PLUS', 'sql.plus.query')
open_execute= SQL_PLUS_QUERY.format(USER_NAME_BD, PASS_BD, HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, '@script-bd/01-info-tablespace.sql {0}'.format(USER_NAME))
command_execute_log  = SQL_PLUS_QUERY.format('*********', '*********', HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, '@script-bd/01-info-tablespace.sql {0}'.format(USER_NAME))
print(command_execute_log)
out_put_ssh = os.popen(open_execute).read()
print(out_put_ssh)

EXECUTE_OK=out_put_ssh.find('[[[OK]]]')

if not(EXECUTE_OK is None):

    print('EJECUCION 01-info-tablespace.sql ... CORRECTA')

    
    expresion_reg=re.compile('\[([\w*;]+)\]')
    matcher=expresion_reg.search(out_put_ssh)
    TABLE_SPACE=matcher.group(0)
    TABLE_SPACE=TABLE_SPACE.replace('[', '').replace(']', '')
    TABLE_SPACE = TABLE_SPACE.split(';')
    print('TABLESPACE DATA {0}'.format(TABLE_SPACE[0]))
    print('TABLESPACE TEMPORARY {0}'.format(TABLE_SPACE[1]))
    TABLESPACE_DATA=TABLE_SPACE[0]
    TABLESPACE_DATA_TEMPORARY=TABLE_SPACE[1]

    open_execute= SQL_PLUS_QUERY.format(USER_NAME_BD, PASS_BD, HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, '@script-bd/02-kill-session-user.sql {0}'.format(USER_NAME))
    command_execute_log  = SQL_PLUS_QUERY.format('*********', '*********', HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, '@script-bd/02-kill-session-user.sql {0}'.format(USER_NAME))
    print(command_execute_log)
    out_put_ssh = os.popen(open_execute).read()
    print(out_put_ssh)


    expresion_reg=re.compile('\[\[\[OK\]\]\]')
    matcher=expresion_reg.search(out_put_ssh)
    EXECUTE_OK=matcher.group(0)

    if not(EXECUTE_OK is None):

        print('EJECUCION 02-kill-session-user.sql ... CORRECTA')

        open_execute= SQL_PLUS_QUERY.format(USER_NAME_BD, PASS_BD, HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, 
            '@script-bd/03-create-user.sql {0} {1} {2} {3}'.format(USER_NAME, PASS_BD_USER, TABLESPACE_DATA, TABLESPACE_DATA_TEMPORARY))
        command_execute_log  = SQL_PLUS_QUERY.format('*********', '*********', HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, 
            '@script-bd/03-create-user.sql {0} {1} {2} {3}'.format(USER_NAME, PASS_BD_USER, TABLESPACE_DATA, TABLESPACE_DATA_TEMPORARY))
        print(command_execute_log)
        out_put_ssh = os.popen(open_execute).read()
        print(out_put_ssh)

        if not(EXECUTE_OK is None):

            print('EJECUCION 03-create-user.sql ... CORRECTA')

            open_execute= SQL_PLUS_QUERY.format(USER_NAME_BD, PASS_BD, HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, 
                '@script-bd/04-grant-user.sql {0} {1}'.format(USER_NAME, TABLESPACE_DATA))
            command_execute_log  = SQL_PLUS_QUERY.format('*********', '*********', HOST_NAME_BD, PORT_BD, SERVICE_NAME_BD, 
                '@script-bd/04-grant-user.sql {0} {1}'.format(USER_NAME, TABLESPACE_DATA))
            print(command_execute_log)
            out_put_ssh = os.popen(open_execute).read()
            print(out_put_ssh)
        else:

            print('EJECUCION 03-create-user.sql ... INCORRECTA')
    else:

        print('EJECUCION 02-kill-session-user.sql ... INCORRECTA')
else:

    print('EJECUCION 01-info-tablespace.sql ... INCORRECTA')



