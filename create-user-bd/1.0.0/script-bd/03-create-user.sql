/
SET SERVEROUTPUT ON
DECLARE
    LOG_INFO VARCHAR(255);
BEGIN

    
    DBMS_OUTPUT.PUT_LINE(RPAD(LPAD('CREATE USER', 50, '#'), 75, '#'));

    LOG_INFO := 'create user &1 identified by &2 default tablespace &3 temporary tablespace &4 profile default account unlock';
    DBMS_OUTPUT.PUT_LINE(LOG_INFO);
    EXECUTE IMMEDIATE LOG_INFO;
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('[[[OK]]]');

EXCEPTION
WHEN OTHERS THEN

    DBMS_OUTPUT.PUT_LINE('[[[NOK]]]');
    DBMS_OUTPUT.PUT_LINE('ERROR CODE: ' || SQLCODE || ' DETAIL: ' || SQLERRM);
    DBMS_OUTPUT.PUT_LINE('BACKTRACE: ' || DBMS_UTILITY.format_error_backtrace);
END;
/
EXIT;
