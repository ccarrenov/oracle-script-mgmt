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
config.read('config/recovery-dump.properties')

length_parameters = len(sys.argv)
current_time = datetime.datetime.now().strftime(config.get('FORMATE_DATE', 'formate.log'))

if length_parameters == 19 :

    HOST_NAME = sys.argv[1]
    HOST_PORT = sys.argv[2]
    USER_NAME = sys.argv[3]
    SERVER_PASS = sys.argv[4]
    EVN_ORACLE_SID = sys.argv[5]
    ORACLE_USER=sys.argv[6]
    ORACLE_PORT=sys.argv[7]
    ORACLE_PASS=sys.argv[8]
    ORACLE_SCHEME_ORIGIN=sys.argv[9]
    ORACLE_SCHEME_SEND=sys.argv[10]
    TABLE_SPACE_ORIGIN=sys.argv[11]
    TABLE_SPACE_SEND=sys.argv[12]
    TABLE_SPACE_ORIGIN_TEMP=sys.argv[13]
    TABLE_SPACE_SEND_TEMP=sys.argv[14]
    DATA_PUMP_DIR=sys.argv[15]
    DUMP_FILE=sys.argv[16]
    LOG_FILE=sys.argv[17]
    ORACLE_HOME=sys.argv[18]

    print('################################################################')
    print('############### RECOVERY DUMP - DIPRES - 2019 ###############')
    print('################################################################')
    print('###############       AUTHOR: CCARRENOV         ################')
    print('################################################################\n\n')
    print('INIT SHELL SCRIPT.....\n\n\n')


    SSH_REMOTE_CONNECTION_COMMAND = 'sshpass -p \'{0}\' ssh {1}@{2} -p {3} \'{4}\''
    ECHO_ORACLE_SID= config.get('COMMAND_ENVIRONMENT', 'oracle.oraclesid.echo')
    SET_ORACLE_SID= config.get('COMMAND_ENVIRONMENT', 'oracle.oraclesid')
    ORACLE_HOME='export ORACLE_HOME={0}'.format(ORACLE_HOME)
    ORACLE_HOME_EXPORT_PATH=config.get('COMMAND_ENVIRONMENT', 'oracle.home.export.path')
    ORACLE_HOME_ECHO=config.get('COMMAND_ENVIRONMENT', 'oracle.home.echo')
    ORACLE_EXPORT_BD=config.get('COMMAND_IMPORT_BD', 'oracle.import.bd').format(ORACLE_USER, 
                ORACLE_PASS, HOST_NAME, ORACLE_PORT, ORACLE_SCHEME_ORIGIN, ORACLE_SCHEME_SEND, TABLE_SPACE_ORIGIN, TABLE_SPACE_SEND, TABLE_SPACE_ORIGIN_TEMP, 
                TABLE_SPACE_SEND_TEMP, DATA_PUMP_DIR, DUMP_FILE, LOG_FILE)
    ORACLE_EXPORT_LOG=config.get('COMMAND_IMPORT_BD', 'oracle.import.bd').format(ORACLE_USER, 
                '*********', HOST_NAME, ORACLE_PORT, ORACLE_SCHEME_ORIGIN, ORACLE_SCHEME_SEND, TABLE_SPACE_ORIGIN, TABLE_SPACE_SEND, TABLE_SPACE_ORIGIN_TEMP, 
                TABLE_SPACE_SEND_TEMP, DATA_PUMP_DIR, DUMP_FILE, LOG_FILE)

    command_execute = '{0};{1};{2};{3};{4};{5}'.format(SET_ORACLE_SID.format(EVN_ORACLE_SID),ECHO_ORACLE_SID,
                            ORACLE_HOME,ORACLE_HOME_ECHO,ORACLE_HOME_EXPORT_PATH,ORACLE_EXPORT_BD)
    command_execute_log = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(SET_ORACLE_SID.format(EVN_ORACLE_SID),ECHO_ORACLE_SID,
                            ORACLE_HOME,ORACLE_HOME_ECHO,ORACLE_HOME_EXPORT_PATH,ORACLE_EXPORT_LOG)
    print('REMOTE COMMAND: ')
    print(command_execute_log)

    print('################################################################')
    print('##################       SERVER BD          ####################')
    print("TIME: {0}".format(current_time))
    print("HOST NAME: {0}".format(HOST_NAME))
    print("USER: {0}".format(USER_NAME))
    print('################################################################\n\n')
    open_execute= SSH_REMOTE_CONNECTION_COMMAND.format(SERVER_PASS, USER_NAME, HOST_NAME, HOST_PORT, command_execute)
    command_execute_log=SSH_REMOTE_CONNECTION_COMMAND.format('*********', USER_NAME, HOST_NAME, HOST_PORT, command_execute)
    out_put_ssh = os.popen(open_execute).read()
    print(command_execute_log)
    print(out_put_ssh)
else:
    print('ERROR -> DEFINED 10 PARAMETERS TO EXECUTE SCRIPT: HOST_NAME, PORT_HOST_NAME, USER_NAME_HOST, PASS_HOST, ORACLE_SID, ORACLE_HOME, USER_NAME_BD, PASS_BD SCHEME, PORT_BD, DATA_PUMP_DIR')
    print('FINISH SHELL SCRIPT.....')



