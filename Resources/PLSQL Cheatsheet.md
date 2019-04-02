# PLSQL Cheatsheet for DB Phase 4 and Test

### General Structure for "For Loops"
<b>Note</b>: We will never have to use the "While Loop" implementation for loops as selecting a cursor, determining if a record is found etc is done for us using a For loop anyways.

``` 
set serveroutput on 
DECLARE
    BEGIN
    dbms_output.put_line('someting here'||' '||'another column');
    
    for count_var in (select some fields
                    FROM a_table)
    LOOP
        do you thingshere;
    END LOOP;
END;
    

```