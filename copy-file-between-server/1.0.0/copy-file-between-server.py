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
config.read('config/copy-file-between-server.properties')

length_parameters = len(sys.argv)


if length_parameters == 12 :

    HOST_NAME = sys.argv[1]
    HOST_PORT = sys.argv[2]
    USER_NAME = sys.argv[3]
    SERVER_PASS = sys.argv[4]
    FOLDER_PATH = sys.argv[5]
    FILE_NAME = sys.argv[6]
    HOST_NAME_SEND = sys.argv[7]
    HOST_PORT_SEND = sys.argv[8]
    USER_NAME_SEND = sys.argv[9]
    SERVER_PASS_SEND = sys.argv[10]
    FOLDER_PATH_SEND = sys.argv[11]

    print('################################################################')
    print('######## SCRIPT COPY BETWEEN SERVER - DIPRES - 2019 ############')
    print('################################################################')
    print('###############       AUTHOR: CCARRENOV         ################')
    print('################################################################\n\n')
    print('INIT SHELL SCRIPT.....\n\n\n')


    SSH_REMOTE_CONNECTION_COMMAND = config.get('COPY', 'ssh.copy')
    SSH_REMOTE_COPY_FILE_COMMAND = config.get('COPY', 'scp.copy')
    SSH_REMOTE_LIST_COMMAND = config.get('COPY', 'ssh.copy')
    command_execute = SSH_REMOTE_COPY_FILE_COMMAND.format(SERVER_PASS_SEND, HOST_PORT_SEND, FOLDER_PATH + FILE_NAME, USER_NAME_SEND, HOST_NAME_SEND, FOLDER_PATH_SEND)
    command_execute_log = SSH_REMOTE_CONNECTION_COMMAND.format('********', USER_NAME, HOST_NAME, HOST_PORT,
								SSH_REMOTE_COPY_FILE_COMMAND.format('********', HOST_PORT_SEND, FOLDER_PATH + FILE_NAME, USER_NAME_SEND, HOST_NAME_SEND, FOLDER_PATH_SEND))
    command_list_execute_log = SSH_REMOTE_LIST_COMMAND.format('********', USER_NAME_SEND, HOST_NAME_SEND, HOST_PORT, 'ls {0}'.format(FOLDER_PATH_SEND))
    print('REMOTE COMMAND: ')
    print('COPY FILE: {0} SERVER {1} TO SERVER {2}'.format(FILE_NAME, HOST_NAME, HOST_NAME_SEND))
    print(command_execute_log)
    open_execute= SSH_REMOTE_CONNECTION_COMMAND.format(SERVER_PASS, USER_NAME, HOST_NAME, HOST_PORT, command_execute)
    #print(open_execute)
    out_put_ssh = os.popen(open_execute).read()
    print(out_put_ssh)
    print('LIST {0} TO SERVER {1}'.format(FOLDER_PATH_SEND, HOST_NAME_SEND))
    open_execute= SSH_REMOTE_LIST_COMMAND.format(SERVER_PASS_SEND, USER_NAME_SEND, HOST_NAME_SEND, HOST_PORT, 'ls -la {0}'.format(FOLDER_PATH_SEND))
    #print(open_execute)	
    print(command_list_execute_log)
    out_put_ssh = os.popen(open_execute).read()
    print(out_put_ssh)
else:
        print('ERROR -> DEFINED 10 PARAMETERS TO EXECUTE SCRIPT: HOST_NAME, PORT_HOST_NAME, USER_NAME_HOST, PASS_HOST, ORACLE_SID, ORACLE_HOME, USER_NAME_BD, PASS_BD SCHEME, PORT_BD')
        print('FINISH SHELL SCRIPT.....')



