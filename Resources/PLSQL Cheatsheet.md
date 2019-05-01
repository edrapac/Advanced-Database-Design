# PLSQL Cheatsheet for DB Phase 4 and Test

## General Structure for "For Loops"
<b>Note</b>: We will never have to use the "While Loop" implementation for loops as selecting a cursor, determining if a record is found etc is done for us using a "For loop" anyways.

```sql
set serveroutput on 
DECLARE
    BEGIN
    dbms_output.put_line('column 1 here'||' '||'another column');
    
    for count_var in (select some fields
                    FROM a_table)
    LOOP
        do your things here;
    END LOOP;
END;
    

```

## 15 SP Queries (Odd Numbered) using PLSQL

### 1)	Give the top 2 and bottom 2 parts based on their shipped quantity.
```
set serveroutput on;
declare
  BEGIN
  dbms_output.put_line('Quantity'||' '||'Rank');
  for cnt_var in (SELECT S2.QTY, NTILE(10)
  
  OVER( ORDER BY COUNT (S.SNAME) DESC) AS Ranges
  FROM S
  JOIN SP S2 on S.S# = S2.S#
  JOIN P P2 on S2.P# = P2.P#
  GROUP BY S2.QTY )
  LOOP
    dbms_output.put_line(cnt_var.QTY||' '||cnt_var.Ranges);
  end LOOP;
end;
```

### 3.) Give the name of the supplier whose supplies red parts and whose weight > 10.

```
set serveroutput on;
declare
BEGIN
    dbms_output.put_line('Supplier Name');
    for cnt_var in (SELECT DISTINCT S.SNAME
    FROM S
    JOIN SP S2 on S.S# = S2.S#
    JOIN P P2 on S2.P# = P2.P#
    WHERE P2.COLOR LIKE 'Red' AND P2.WEIGHT > 10)
    LOOP
        dbms_output.put_line(cnt_var.SNAME);
    end loop;
end;
```

### 5.)Give the supplier and part that come from the same city

```
set serveroutput on;
declare
    BEGIN
    dbms_output.put_line('Supplier 1'||' '||'Supplier 2'||' '|| 'Part Name');
    for cnt_var in (SELECT S1.SNAME SNAME1, S2.SNAME SNAME2, P1.PNAME
    FROM S S1, S S2
    JOIN SP SP3 on S2.S# = SP3.S#
    JOIN P P1 on SP3.P# = P1.P#
    WHERE S1.CITY <= S2.CITY)
    LOOP
        dbms_output.put_line(cnt_var.SNAME1||' '||cnt_var.SNAME2||' '||cnt_var.PNAME);
    end loop;
end;
```

### 7.)Give how many parts each supplier has and the total qty each part has.

```
set serveroutput ON;
declare
    BEGIN
    dbms_output.put_line('S#'||' '||'Quantity');
    for cnt_var in (SELECT S#,SUM(QTY) SQTY
                    FROM sp
                    GROUP BY S#)
    LOOP
        dbms_output.put_line(cnt_var.S#||' '|| cnt_var.SQTY);
    end loop;
end;
```

### 9.) Give the total quantity of all the blue parts

```
set serveroutput ON;
declare
    BEGIN
    dbms_output.put_line('Quantity');
    for cnt_var in (SELECT SUM(QTY) SQTY 
                    FROM SP
                    JOIN P ON sp.p# = P.P#
                    WHERE P.COLOR = 'Blue')
    LOOP
        dbms_output.put_line(cnt_var.SQTY);
    end loop;
end;
```

### 11.) Change all the parts that come from London to as those coming from Mankato

<b>NA this is an update statement</b>

### 13.) Give the top 3 parts that weigh the most.

```
set serveroutput on;
declare
    BEGIN
    dbms_output.put_line('Partname'||' '||'Weight'||' ' ||'Ranking');
    for cnt_var in (WITH RTable AS (SELECT P#, WEIGHT,RANK() over (ORDER BY WEIGHT) Ranking

                    FROM P)
                    SELECT RTable.P# RP,RTable.Ranking RR , RTable.WEIGHT RW
                    FROM RTable
                    WHERE Ranking <=4
                    GROUP BY P#,RTable.Ranking, RTable.WEIGHT
                    ORDER BY Ranking)
                LOOP
                    dbms_output.put_line(RPAD(cnt_var.RP,10)||''||rpad(cnt_var.RW,8)||''||cnt_var.RR);
                
                end loop;
end;
```

### 15.) Give the total quantity supplied by each supplier and his name

```
set serveroutput on;
declare
    BEGIN
    dbms_output.put_line('Supplier Num'||' '||'Supplier Name'||' ' ||'Total Quantity');
    for cnt_var in (SELECT S.S#,S.SNAME, SUM(S2.QTY) SumQTY
                    FROM S
                    JOIN SP S2 on S.S# = S2.S#
                    JOIN P P2 on S2.P# = P2.P#
                    GROUP BY S.S#, S.SNAME
                                            )
                LOOP
```

### 17.) Give the name of parts from supplier from Paris with qty>100 and part is from Paris

```
set serveroutput on;
declare
    BEGIN
    dbms_output.put_line('Partname');
    for cnt_var in (SELECT DISTINCT P2.PNAME
                FROM S
                JOIN SP S2 on S.S# = S2.S#
                JOIN P P2 on S2.P# = P2.P#
                WHERE S2.QTY > 100 AND P2.CITY LIKE 'Paris')
                LOOP
                    dbms_output.put_line(cnt_var.PNAME);
                
                end loop;
```
### 19.) Give the names of the suppliers that are from the same city

```
set serveroutput on;
declare
    BEGIN
    dbms_output.put_line('Supplier 1 Name'||' '||'Supplier 2 Name'||' '||'City Name');
    for cnt_var in (SELECT S1.SNAME S1NAME ,S2.SNAME S2NAME, S1.CITY S1CITY
                FROM S S1, S S2
                WHERE S1.CITY <= S2.CITY AND S1.SNAME >= S2.SNAME)
            LOOP
                dbms_output.put_line(rpad(cnt_var.S1NAME,15)||' '||rpad(cnt_var.S2NAME,15)||' '||cnt_var.S1CITY);
            end loop;
    end;
```

### 21.)Give the total quantity present for each part

```
set serveroutput on;
declare
BEGIN
    dbms_output.put_line('Part Name'||' '||'Total QTY');
    for cnt_var in (SELECT DISTINCT P2.PNAME,SUM(S2.QTY) TotalQty
            FROM S
            JOIN SP S2 on S.S# = S2.S#
            JOIN P P2 on S2.P# = P2.P#
            GROUP BY P2.PNAME)
    LOOP
        dbms_output.put_line(rpad(cnt_var.PNAME,12)||' '||cnt_var.TotalQty);
    end loop;
end;
```

### 23) Give the suppliers and parts that come from the London

```
set serveroutput on;
declare
BEGIN
    dbms_output.put_line('Part Name'||' '||'Supplier');
    for cnt_var in (SELECT P.PNAME P1,stuff.SNAME S1
                    FROM P
                    JOIN S stuff on stuff.S# = P.P#
                    )
    LOOP
        dbms_output.put_line(rpad(cnt_var.P1,8)||' '||cnt_var.S1);
    end loop;
end;
```

### 25) Give the max number of parts supplied by a supplier

```
set serveroutput on;
declare
BEGIN
    dbms_output.put_line('Max Qty'||' '||'PNumber');
    for cnt_var in (SELECT MAX(QTY) MAXqty, P#
                    FROM SP
                    GROUP BY P#
                    ORDER BY MAXqty DESC)
    LOOP
        dbms_output.put_line(rpad(cnt_var.MAXqty,8)||' '||cnt_var.P#);
    end loop;
end;
```

### 27 Give the name of the supplier that supplies both red part and weight is 14

```
set serveroutput on;
declare
BEGIN
    dbms_output.put_line('Supplier Name');
    for cnt_var in (SELECT S.SNAME
FROM S 
JOIN P ON P.P# = S.S#
WHERE P.WEIGHT = 14 and P.COLOR = 'Red'
)
    LOOP
        dbms_output.put_line(rpad(cnt_var.SNAME,8));
    end loop;
end;
```

### 29 Give the subtotals of the total part weights of the all the parts supplied by a supplier and give the final total weight.

```
set serveroutput on 
declare
    BEGIN
    dbms_output.put_line('SNAME'||' '||'Num Parts'||' '||'Quantity'||' '||'Rank');
    for count_var in (select sname,no_of_parts,qt,rank
                from (select s#,count(distinct p#) as no_of_parts,sum(qty) as qt,
                rank() over(order by count(distinct p#) desc,sum(qty) desc) as rank
                from sp.sp
                group by s#) s1,sp.s s2
                where s1.s#=s2.s#)
    LOOP
        dbms_output.put_line(rpad(count_var.sname,8)||' '||rpad(count_var.no_of_parts,8)||' '||rpad(count_var.qt,8)||' '||count_var.rank);
    end loop;
end;
```
