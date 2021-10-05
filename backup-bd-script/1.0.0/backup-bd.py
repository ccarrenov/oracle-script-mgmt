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
config.read('config/backup-bd.properties')

length_parameters = len(sys.argv)


if length_parameters == 12 :

    HOST_NAME = sys.argv[1]
    HOST_PORT = sys.argv[2]
    USER_NAME = sys.argv[3]
    SERVER_PASS = sys.argv[4]
    EVN_ORACLE_SID = sys.argv[5]
    current_time = datetime.datetime.now().strftime(config.get('FORMATE_DATE', 'formate.log'))
    sufix=datetime.datetime.now().strftime(config.get('FORMATE_DATE', 'formate.folder'))

    print('################################################################')
    print('############### SCRIPT BACKUP BD - DIPRES - 2019 ###############')
    print('################################################################')
    print('###############       AUTHOR: CCARRENOV         ################')
    print('################################################################\n\n')
    print('INIT SHELL SCRIPT.....\n\n\n')


    #SSH_REMOTE_CONNECTION_COMMAND = 'ssh {0}@{1} -p {2} \'{3}\''
    SSH_REMOTE_CONNECTION_COMMAND = 'sshpass -p \'{0}\' ssh {1}@{2} -p {3} \'{4}\''
    ECHO_ORACLE_SID= config.get('COMMAND_ENVIRONMENT', 'oracle.oraclesid.echo')
    SET_ORACLE_SID= config.get('COMMAND_ENVIRONMENT', 'oracle.oraclesid')
    ORACLE_HOME='export ORACLE_HOME={0}'.format(sys.argv[6])
    ORACLE_HOME_EXPORT_PATH=config.get('COMMAND_ENVIRONMENT', 'oracle.home.export.path')
    ORACLE_HOME_ECHO=config.get('COMMAND_ENVIRONMENT', 'oracle.home.echo')
    ORACLE_USER=sys.argv[7]
    ORACLE_PASS=sys.argv[8]
    ORACLE_SCHEME=sys.argv[9]
    NAME_DUMP_FILE="{0}-{1}.dmp".format(sufix,ORACLE_SCHEME)
    NAME_DUMP_LOG="{0}-{1}.log".format(sufix,ORACLE_SCHEME)
    ORACLE_PORT=sys.argv[10]
    DATA_PUMP_DIR=sys.argv[11]
    ORACLE_EXPORT_BD=config.get('COMMAND_EXPORT_BD', 'oracle.export.bd').format(ORACLE_USER, 
                ORACLE_PASS, HOST_NAME, ORACLE_PORT, EVN_ORACLE_SID,ORACLE_SCHEME, NAME_DUMP_FILE, NAME_DUMP_LOG)
    ORACLE_EXPORT_LOG=config.get('COMMAND_EXPORT_BD', 'oracle.export.bd').format(ORACLE_USER, 
                '**********', HOST_NAME, ORACLE_PORT, EVN_ORACLE_SID,ORACLE_SCHEME, NAME_DUMP_FILE, NAME_DUMP_LOG)

    #VALIDATE PAREMETER PASS
    if not(HOST_NAME is None) and not(USER_NAME is None) and not(SERVER_PASS is None) and not(EVN_ORACLE_SID is None):

        print('################################################################')
        print('##################       SERVER BD          ####################')
        print("TIME: {0}".format(current_time))
        print("HOST NAME: {0}".format(HOST_NAME))
        print("USER: {0}".format(USER_NAME))
        print('################################################################\n\n')

        command_execute = '{0};{1};{2};{3};{4};{5}'.format(SET_ORACLE_SID.format(EVN_ORACLE_SID),ECHO_ORACLE_SID,
                                ORACLE_HOME,ORACLE_HOME_ECHO,ORACLE_HOME_EXPORT_PATH,ORACLE_EXPORT_BD)
        command_execute_log = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(SET_ORACLE_SID.format(EVN_ORACLE_SID),ECHO_ORACLE_SID,
                                ORACLE_HOME,ORACLE_HOME_ECHO,ORACLE_HOME_EXPORT_PATH,ORACLE_EXPORT_LOG)
        print('REMOTE COMMAND: ')
        print(command_execute_log)
        open_execute= SSH_REMOTE_CONNECTION_COMMAND.format(SERVER_PASS, USER_NAME, HOST_NAME, HOST_PORT, command_execute)
        out_put_ssh = os.popen(open_execute).read()
        print('DATA_PUMP_DIR = {0}'.format(DATA_PUMP_DIR))
        open_execute= SSH_REMOTE_CONNECTION_COMMAND.format(SERVER_PASS, USER_NAME, HOST_NAME, HOST_PORT, 'ls -la {0}'.format(DATA_PUMP_DIR))
        out_put_ssh = os.popen(open_execute).read()
        print(out_put_ssh)
        EXECUTE_OK=out_put_ssh.find(NAME_DUMP_FILE)

        if (EXECUTE_OK > -1):
            print('CREATE DUMP SUCCESSFULLY')
        else:
            print('CREATE DUMP ERROR')
            open_execute= SSH_REMOTE_CONNECTION_COMMAND.format(SERVER_PASS, USER_NAME, HOST_NAME, HOST_PORT, 'cat {0}{1}'.format(DATA_PUMP_DIR, NAME_DUMP_LOG))
            print(open_execute)
    else:
        print('ERROR -> SET PARAMETERS')
        print('FINISH SHELL SCRIPT.....')

else:
    print('ERROR -> DEFINED 10 PARAMETERS TO EXECUTE SCRIPT: HOST_NAME, PORT_HOST_NAME, USER_NAME_HOST, PASS_HOST, ORACLE_SID, ORACLE_HOME, USER_NAME_BD, PASS_BD SCHEME, PORT_BD, DATA_PUMP_DIR')
    print('FINISH SHELL SCRIPT.....')



