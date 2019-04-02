# Cheat Sheet for Midterm IT 440 Spring 2019

### Remember that the midterm is on Thursday, March 14th.

### Recommended Resources:
All the stuff here is basically from the D2L page. The RDBMS manager I use is a really good one called DataGrip from JetBrains, it's free and a lot better than Oracle's in my opinion

## General Commands (Some are Oracle Specific)

### Shows all the column names in a certain table

`select column_name from all_tab_columns Where TABLE_NAME = 'your_table_here' ;`

### Convert an average to decimal and filter on condition 

`HAVING CONVERT(DECIMAL(5,2), AVG(PRICE)) > 10`

### Is how to alter tables, in this instance it adds a column

`ALTER TABLE table_name
  ADD column_name datatype;`

### Updates the table customer, inserts the value 'M' for gender where customer_id = 00001

`UPDATE CUSTOMER SET Gender = 'M' WHERE "Customer_ID"='00001';`

### Adds a constraint that checks if the value entered for State is uppercase
`ALTER TABLE CUSTOMER
  ADD CONSTRAINT STATE_CHECK CHECK ("State" = upper("State"));`

### NVL tells us what to do with NULL Values, if there is a null value for Tell_Number, reply with Not Available

`SELECT Tell_Number, NVL(Tell_Number,'Not available') as NVL_USE
From CUSTOMER`

### Ranking Stuff

`SELECT rs.Field1,rs.Field2 
    FROM (
        SELECT Field1,Field2, Rank() 
          over (Partition BY Section
                ORDER BY RankCriteria DESC ) AS Rank
        FROM table
        ) rs WHERE Rank = Something`

### General Constraint for checking a condition
`ALTER TABLE table_name 
ADD CONSTRAINT MyUniqueConstraint CHECK (CONDITION);`

`SELECT * from v$version -- provides the installed version of oracle as well as install info`

### A "WHERE NOT IN" Scenario
Sometimes you may be asked to write a query that asks you to select fields from a group of joined tables that are not in another group of joined tables (See example 5 at the very bottom for an example). While this initially seems like a good use for building a subquery along the lines of :

`WITH SUBQUERY1 AS ()
SELECT ...`
Or a NOT EXISTS Subquery, be warned. It is computationally very slow to do this and you are better off using Left and Right joins to filter information (See example 5) they're much faster! 

## Database Specific, May need to be altered slightly for your specific database

### The following are taken from Azarbods file Contents > SQL > SQL Basics using my database (populate for that also found in this repo)

I've ommitted some of the really basic questions...

### SQL I.2: Produce a list of commission for all employee, showing only employee number, first and last names, and commission. 

`SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               (SUM(P.PRICE) * SALES_COMISSION) TotalComission
FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME,JT.SALES_COMISSION,JT.JOB_ID;`

Lots of Joins in this one, should probably clean it up but `¯\_(ツ)_/¯`

### SQL I.3: List the product number of all the products those have been ordered. 

`SELECT DISTINCT(P.PAINTING_ID), P.TITLE
FROM PAINTING P;`


### SQL I.4: Produce a list of monthly commission for all employee, showing employee number, first and last names, and  commission details.

`SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               ROUND(((SUM(P.PRICE) * SALES_COMISSION)/12),2) TotalComission
FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME,JT.SALES_COMISSION,JT.JOB_ID;`

### SQL I.5: List all employee with a commission greater than 80,000.

A note on this one: Since total comission per employee is an aggregate field for me I had to use a HAVING field to filter on TotalComission

`SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               (SUM(P.PRICE) * SALES_COMISSION) TotalComission
FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
HAVING (SUM(P.PRICE) * SALES_COMISSION) > 80000
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME, JT.SALES_COMISSION, JT.JOB_ID;`

### SQL I.7: List all employee with a commission between 60,000 and 80,000. 

`SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               (SUM(P.PRICE) * SALES_COMISSION) TotalComission
FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
HAVING (SUM(P.PRICE) * SALES_COMISSION) BETWEEN 60000 AND 80000
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME, JT.SALES_COMISSION, JT.JOB_ID;`

### SQL I.8: List all employees from Chicago and Boston 
`SELECT E.FIRST_NAME, E.LAST_NAME, E.CITY
FROM EMPLOYEE E
WHERE E.CITY IN ('Chicago','Boston');`


### List the names of employees who receive comission as part of their salary. For those that don't, use NVL to display "Not a comissioned position"

`SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,
                NVL(to_char(JT.SALES_COMISSION),'Not a comissioned position') Comission_Status,
                JT.JOB_ID, SUM(P.PRICE) TotalSales
FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME,JT.SALES_COMISSION,JT.JOB_ID;`

## The following is also related to the Midterm based on questions Azarbod has asked in class

### 1. List the top 10 percent of customers in terms of total number of orders (customer number, customer last name, and state) 

`WITH Percentiles AS
       (SELECT DISTINCT(C.CUSTOMER_ID), C.FIRST_NAME, C.LAST_NAME, C.STATE, COUNT(CO.ORDER_ID) OrderCount,
                NTILE(10) OVER (ORDER BY COUNT(CO.ORDER_ID) DESC) AS Range
         FROM CUSTOMER C
         JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
         GROUP BY C.CUSTOMER_ID, FIRST_NAME, LAST_NAME, STATE
         )
SELECT *
FROM Percentiles
WHERE Range in (1);`


### 2. List top city in each state in terms of total gross sales (exclude shipping charges and taxes) 
`SELECT DISTINCT CITY,STATE, OrderTotal
FROM (
  SELECT C.CITY, C.STATE, SUM(P.PRICE) AS OrderTotal,
  ROW_NUMBER() over (PARTITION BY C.CITY ORDER BY SUM(P.PRICE)) AS RowNumber
  FROM CUSTOMER C
  JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
  JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
  JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
  GROUP BY C.CITY, C.STATE
  ) Selection
WHERE RowNumber = 1
ORDER BY STATE;`


### 3. List every product number and their total sales for each year (product number, year, total gross sale)
`WITH Percentiles AS
       (SELECT DISTINCT(C.CUSTOMER_ID), C.FIRST_NAME, C.LAST_NAME, C.STATE, COUNT(CO.ORDER_ID) OrderCount,
                NTILE(10) OVER (ORDER BY COUNT(CO.ORDER_ID) DESC) AS Range
         FROM CUSTOMER C
         JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
         GROUP BY C.CUSTOMER_ID, FIRST_NAME, LAST_NAME, STATE
         )
SELECT *
FROM Percentiles
WHERE Range in (1);`

### 4. List all customers that have more than two orders (customer number, number of orders) in desc order based on number of orders 
`SELECT DISTINCT(C.CUSTOMER_ID), COUNT(CO.ORDER_ID) Number_Orders
FROM CUSTOMER C
JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
HAVING COUNT(CO.ORDER_ID) > 2
GROUP BY C.CUSTOMER_ID
ORDER BY Number_Orders DESC ;`

### 5. List all employees that have not had any sales (employee number, last name, position title) 

A note about this one: The WHERE clause at the end is used just to clean up the output. Since an employee's ID won't change, it is possible an employee could start out in a non-sales role and then move onto a sales role. Without the WHERE clause at the end an employee that had been in a different role first would appear twice, which still isn't incorrect as they were the one who did make the sale. It just makes it look nicer

`SELECT DISTINCT(CO.EMPLOYEE_ID), E.LAST_NAME, JT.JOB_NAME
FROM EMPLOYEE E
RIGHT JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN JOB_HISTORY JH on CO.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
WHERE JT.JOB_NAME LIKE '%Sales%';`

### 6. List total gross sales for each month (Hint: use substr to get the month). Order the result based on month from Jan to Dec. 
`SELECT SUBSTR(CO.DATE_CREATED,4,3) MONTH, SUM(P.PRICE) Total_Sales_Per_Month
/**
First number indicates where to start second number indicates how many characters after that
 */
FROM CUSTOMER C
JOIN CUSTOMER_ORDER CO ON CO.CUSTOMER_ID = C.CUSTOMER_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
GROUP BY SUBSTR(CO.DATE_CREATED,4,3)`

### 7. List unique pairs of customers that are from the same city 

`SELECT C1.FIRST_NAME, C1.LAST_NAME,
       C2.FIRST_NAME, C2.LAST_NAME,C1.CITY
FROM CUSTOMER C1, CUSTOMER C2
WHERE C1.CITY <= C2.CITY AND C1.FIRST_NAME > C2.FIRST_NAME
  AND C1.LAST_NAME > C2.LAST_NAME;`

### 8. List total sales for each product and calculate the percentage of their sale compared to total sale. 
`SELECT P.TITLE,SUM(P.PRICE) as TotalPrice,
       ROUND((SUM(P.PRICE)/(SELECT SUM(P2.PRICE)
        FROM CUSTOMER_ORDER CO2
        JOIN PAINTING_ORDER PO2 on CO2.ORDER_ID = PO2.ORDER_ID
        JOIN PAINTING P2 on PO2.PAINTING_ID = P2.PAINTING_ID
       ) *100),2)Percentage_Total_Revenue
FROM CUSTOMER_ORDER CO
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
GROUP BY P.TITLE;`

### 9. List customers (customer number, full name (last name, first name)) that have not placed any order yet 

`SELECT C.CUSTOMER_ID, C.FIRST_NAME, C.LAST_NAME
FROM CUSTOMER C
LEFT JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
WHERE CO.CUSTOMER_ID IS NULL;`

### 10. List customers (customer number, last name) with highest total purchase (rank one) for each state. 
`WITH Ranking_Table As (SELECT C.CUSTOMER_ID, C.FIRST_NAME, C.STATE, SUM(P.PRICE) TotalOrdered,
       Rank() over (PARTITION BY C.STATE ORDER BY SUM(P.PRICE)) as Top_Customer
FROM CUSTOMER C
JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
GROUP BY C.CUSTOMER_ID, C.FIRST_NAME, CO.CUSTOMER_ID, C.STATE)
Select Ranking_Table.CUSTOMER_ID, Ranking_Table.FIRST_NAME,
       Ranking_Table.STATE,
       Ranking_Table.TotalOrdered
FROM Ranking_Table
WHERE Ranking_Table.Top_Customer =1`


### Select Orders that are made within Discount Peroids
`SELECT CO.ORDER_ID,CO.DATE_CREATED, DS.START_DATE
FROM CUSTOMER_ORDER CO, DISCOUNT_SALES DS
WHERE CO.DATE_CREATED >= DS.START_DATE AND CO.DATE_CREATED <= DS.END_DATE`

## SP 30 Questions


Answer the following queries using SP database
1)  Give the top 2 and bottom 2 parts based on their shipped quantity.
`WITH RangeTable AS
  (SELECT S2.QTY, NTILE(10)
  OVER( ORDER BY COUNT (S.SNAME) DESC) AS Range
  FROM S
  JOIN SP S2 on S.S# = S2.S#
  JOIN P P2 on S2.P# = P2.P#
  GROUP BY S2.QTY )
SELECT *
FROM RangeTable
WHERE Range IN (1,2) OR Range IN (9,10)`

2)  Give the supplier name that supplies the maximum quantity of parts.
`SELECT S.SNAME, MAX(S2.QTY)
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE S2.QTY =
      (
        SELECT MAX(S2.QTY)
        FROM SP S2
        )`

3)  Give the name of the supplier whose supplies red parts and whose weight > 10.

`SELECT DISTINCT S.SNAME
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE P2.COLOR LIKE 'Red' AND P2.WEIGHT > 10;`

Give all the part numbers that are from the same city
`SELECT P1.PNAME, P2.PNAME, P1.CITY
FROM P P1, P P2
WHERE P1.PNAME <= P2.PNAME
  AND P1.CITY = P2.CITY`

6)  Give the supplier and part that come from the same city

`SELECT S1.SNAME, S2.SNAME, P1.PNAME
FROM S S1, S S2
JOIN SP SP3 on S2.S# = SP3.S#
JOIN P P1 on SP3.P# = P1.P#
WHERE S1.CITY <= S2.CITY`

7)  Give the part name that has the minimum quantity
8)  Give how many parts each supplier has and the total qty each part has.
9)  Give the names of the suppliers who supplies the most pats and least part
10) Give the total quantity of all the blue parts
11) Give the suppliers that are not from the city from which smith is.
`SELECT SNAME
FROM S
WHERE CITY NOT LIKE 'London'`
12) Change all the parts that come from London to as those coming from Mankato
`UPDATE S SET City = 'Mankato'
WHERE CITY = 'London';`
13) Give the top and bottom suppliers based on the quantity they supply.
`WITH RTable AS (SELECT S#, QTY,
                RANK() over (PARTITION BY QTY ORDER BY S# DESC) AS Ranking
                FROM SP)
SELECT DISTINCT RTable.S#
FROM RTable
HAVING MAX(RTable.Ranking) >2 OR MIN(RTable.Ranking) =1
GROUP BY S#;
OR
SELECT DISTINCT(S.SNAME), S2.QTY
FROM S
JOIN SP S2 on S.S# = S2.S#
WHERE S2.QTY =
      (SELECT MIN(S2.QTY)
        FROM SP S2)UNION
SELECT DISTINCT(S.SNAME), S2.QTY
FROM S
JOIN SP S2 on S.S# = S2.S#
WHERE S2.QTY =
      (SELECT MAX(S2.QTY)
        FROM SP S2)
ORDER BY 2;`

14) Give the top 3 parts that weigh the most.
`WITH RTable AS (SELECT P#, WEIGHT,RANK() over (ORDER BY WEIGHT) Ranking
                FROM P)
SELECT RTable.P#,  RTable.Ranking, RTable.WEIGHT
FROM RTable
WHERE Ranking <=4
GROUP BY P#,RTable.Ranking, RTable.WEIGHT
ORDER BY Ranking;`

15) Give all the parts that are not from London and whose color is not blue
`SELECT P2.PNAME
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE S.CITY NOT LIKE 'London'
AND P2.COLOR NOT LIKE 'Blue'`

16) Give the total quantity supplied by each supplier and his name
`SELECT S.S#,S.SNAME, SUM(S2.QTY) SumQTY
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
GROUP BY S.S#, S.SNAME`

17) Give the name of the supplier that supplies a red part.
`SELECT DISTINCT S.S#,S.SNAME
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE P2.COLOR LIKE 'Red'`

18) Give the name of parts from supplier from Paris with qty>100 and part is from Paris
`SELECT DISTINCT P2.PNAME
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE S2.QTY > 100 AND P2.CITY LIKE 'Paris'`

19) Give the total weight of all the red parts
`SELECT DISTINCT SUM(P2.WEIGHT) TotalWeight
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE P2.COLOR LIKE 'Red'`

20) Give the names of the suppliers that are from the same city
`SELECT S1.SNAME ,S2.SNAME, S1.CITY
FROM S S1, S S2
WHERE S1.CITY <= S2.CITY AND S1.SNAME >= S2.SNAME`

21) Give the supplier name that supplies the minimum quantity of parts
`SELECT DISTINCT S.SNAME
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
WHERE S2.QTY =
      (SELECT MIN(S2.QTY) as MinQty
        FROM SP S2)`

22) Give the total quantity present for each part
`SELECT DISTINCT P2.PNAME,SUM(S2.QTY) TotalQty
FROM S
JOIN SP S2 on S.S# = S2.S#
JOIN P P2 on S2.P# = P2.P#
GROUP BY P2.PNAME`