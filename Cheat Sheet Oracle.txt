# Cheat Sheet for Midterm IT 440 Spring 2019

### Remember that the midterm is on Thursday, March 14th.

### Recommended Resources:
All the stuff here is basically from the D2L page. The RDBMS manager I use is a really good one called DataGrip from JetBrains, it's free and a lot better than Oracle's in my opinion

## General Commands (Some are Oracle Specific)

### Shows all the column names in a certain table

select column_name from all_tab_columns Where TABLE_NAME = 'your_table_here' ;

### Convert an average to decimal and filter on condition 

HAVING CONVERT(DECIMAL(5,2), AVG(PRICE)) > 10

### Is how to alter tables, in this instance it adds a column

ALTER TABLE table_name
  ADD column_name datatype;

### Updates the table customer, inserts the value 'M' for gender where customer_id = 00001

UPDATE CUSTOMER SET Gender = 'M' WHERE "Customer_ID"='00001';

### Adds a constraint that checks if the value entered for State is uppercase
ALTER TABLE CUSTOMER
  ADD CONSTRAINT STATE_CHECK CHECK ("State" = upper("State"));

### NVL tells us what to do with NULL Values, if there is a null value for Tell_Number, reply with Not Available

SELECT Tell_Number, NVL(Tell_Number,'Not available') as NVL_USE
From CUSTOMER

### General Constraint for checking a condition
ALTER TABLE table_name 
ADD CONSTRAINT MyUniqueConstraint CHECK (CONDITION);

SELECT * from v$version -- provides the installed version of oracle as well as install info

### A "WHERE NOT IN" Scenario
Sometimes you may be asked to write a query that asks you to select fields from a group of joined tables that are not in another group of joined tables (See example 5 at the very bottom for an example). While this initially seems like a good use for building a subquery along the lines of :
WITH SUBQUERY1 AS ()
SELECT ...
Or a NOT EXISTS Subquery, be warned. It is computationally very slow to do this and you are better off using Left and Right joins to filter information (See example 5) they're much faster! 

## Database Specific, May need to be altered slightly for your specific database

### The following are taken from Azarbods file Contents > SQL > SQL Basics using my database (populate for that also found in this repo)

I've ommitted some of the really basic questions...

### SQL I.2: Produce a list of commission for all employee, showing only employee number, first and last names, and commission. 

SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               (SUM(P.PRICE) * SALES_COMISSION) TotalComission

FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME,JT.SALES_COMISSION,JT.JOB_ID;

Lots of Joins in this one, should probably clean it up but "¯\_(ツ)_/¯


### SQL I.3: List the product number of all the products those have been ordered. 

SELECT DISTINCT(P.PAINTING_ID), P.TITLE
FROM PAINTING P;


### SQL I.4: Produce a list of monthly commission for all employee, showing employee number, first and last names, and  commission details.

SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               ROUND(((SUM(P.PRICE) * SALES_COMISSION)/12),2) TotalComission


FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME,JT.SALES_COMISSION,JT.JOB_ID;

### SQL I.5: List all employee with a commission greater than 80,000.

A note on this one: Since total comission per employee is an aggregate field for me I had to use a HAVING field to filter on TotalComission

SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               (SUM(P.PRICE) * SALES_COMISSION) TotalComission


FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
HAVING (SUM(P.PRICE) * SALES_COMISSION) > 80000
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME, JT.SALES_COMISSION, JT.JOB_ID;

### SQL I.7: List all employee with a commission between 60,000 and 80,000. 

SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,  JT.SALES_COMISSION,JT.JOB_ID, SUM(P.PRICE) TotalSales,
               (SUM(P.PRICE) * SALES_COMISSION) TotalComission


FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
WHERE JT.SALES_COMISSION IS NOT NULL
HAVING (SUM(P.PRICE) * SALES_COMISSION) BETWEEN 60000 AND 80000
GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME, JT.SALES_COMISSION, JT.JOB_ID;

### SQL I.8: List all employees from Chicago and Boston 

SELECT E.FIRST_NAME, E.LAST_NAME, E.CITY
FROM EMPLOYEE E
WHERE E.CITY IN ('Chicago','Boston');


### List the names of employees who receive comission as part of their salary. For those that don't, use NVL to display "Not a comissioned position"

SELECT DISTINCT(E.EMPLOYEE_ID), E.FIRST_NAME, E.LAST_NAME,
                NVL(to_char(JT.SALES_COMISSION),'Not a comissioned position') Comission_Status,
                JT.JOB_ID, SUM(P.PRICE) TotalSales

FROM EMPLOYEE E
JOIN JOB_HISTORY JH on E.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID

GROUP BY E.EMPLOYEE_ID, E.FIRST_NAME, E.LAST_NAME,JT.SALES_COMISSION,JT.JOB_ID;

## The following is also related to the Midterm, according to a student who had Azarbod over the summer these are very similar questions to ones he asks on the test

### 1. List the top 10 percent of customers in terms of total number of orders (customer number, customer last name, and state) 

WITH Percentiles AS
       (SELECT DISTINCT(C.CUSTOMER_ID), C.FIRST_NAME, C.LAST_NAME, C.STATE, COUNT(CO.ORDER_ID) OrderCount,
                NTILE(10) OVER (ORDER BY COUNT(CO.ORDER_ID) DESC) AS Range
         FROM CUSTOMER C
         JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
         GROUP BY C.CUSTOMER_ID, FIRST_NAME, LAST_NAME, STATE
         )

SELECT *
FROM Percentiles
WHERE Range in (1);


### 2. List top city in each state in terms of total gross sales (exclude shipping charges and taxes) 
SELECT DISTINCT CITY,STATE, OrderTotal
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
ORDER BY STATE;


### 3. List every product number and their total sales for each year (product number, year, total gross sale)
WITH Percentiles AS
       (SELECT DISTINCT(C.CUSTOMER_ID), C.FIRST_NAME, C.LAST_NAME, C.STATE, COUNT(CO.ORDER_ID) OrderCount,
                NTILE(10) OVER (ORDER BY COUNT(CO.ORDER_ID) DESC) AS Range
         FROM CUSTOMER C
         JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
         GROUP BY C.CUSTOMER_ID, FIRST_NAME, LAST_NAME, STATE
         )

SELECT *
FROM Percentiles
WHERE Range in (1);

### 4. List all customers that have more than two orders (customer number, number of orders) in desc order based on number of orders 
SELECT DISTINCT(C.CUSTOMER_ID), COUNT(CO.ORDER_ID) Number_Orders
FROM CUSTOMER C
JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
HAVING COUNT(CO.ORDER_ID) > 2
GROUP BY C.CUSTOMER_ID
ORDER BY Number_Orders DESC ;

### 5. List all employees that have not had any sales (employee number, last name, position title) 

A note about this one: The WHERE clause at the end is used just to clean up the output. Since an employee's ID won't change, it is possible an employee could start out in a non-sales role and then move onto a sales role. Without the WHERE clause at the end an employee that had been in a different role first would appear twice, which still isn't incorrect as they were the one who did make the sale. It just makes it look nicer

SELECT DISTINCT(CO.EMPLOYEE_ID), E.LAST_NAME, JT.JOB_NAME
FROM EMPLOYEE E
RIGHT JOIN CUSTOMER_ORDER CO on E.EMPLOYEE_ID = CO.EMPLOYEE_ID
JOIN JOB_HISTORY JH on CO.EMPLOYEE_ID = JH.EMPLOYEE_ID
JOIN JOB_TITLE JT on JH.JOB_ID = JT.JOB_ID
WHERE JT.JOB_NAME LIKE '%Sales%';

### 6. List total gross sales for each month (Hint: use substr to get the month). Order the result based on month from Jan to Dec. 
SELECT SUBSTR(CO.DATE_CREATED,4,3) MONTH, SUM(P.PRICE) Total_Sales_Per_Month
/**
First number indicates where to start second number indicates how many characters after that
 */
FROM CUSTOMER C
JOIN CUSTOMER_ORDER CO ON CO.CUSTOMER_ID = C.CUSTOMER_ID
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
GROUP BY SUBSTR(CO.DATE_CREATED,4,3)

### 7. List unique pairs of customers that are from the same city 

Will ask Azarbod about this one...

### 8. List total sales for each product and calculate the percentage of their sale compared to total sale. 
SELECT P.TITLE,SUM(P.PRICE) as TotalPrice,
       ROUND((SUM(P.PRICE)/(SELECT SUM(P2.PRICE)
        FROM CUSTOMER_ORDER CO2
        JOIN PAINTING_ORDER PO2 on CO2.ORDER_ID = PO2.ORDER_ID
        JOIN PAINTING P2 on PO2.PAINTING_ID = P2.PAINTING_ID
       ) *100),2)Percentage_Total_Revenue


FROM CUSTOMER_ORDER CO
JOIN PAINTING_ORDER PO on CO.ORDER_ID = PO.ORDER_ID
JOIN PAINTING P on PO.PAINTING_ID = P.PAINTING_ID
GROUP BY P.TITLE;

### 9. List customers (customer number, full name (last name, first name)) that have not placed any order yet 

SELECT C.CUSTOMER_ID, C.FIRST_NAME, C.LAST_NAME
FROM CUSTOMER C
LEFT JOIN CUSTOMER_ORDER CO on C.CUSTOMER_ID = CO.CUSTOMER_ID
WHERE CO.CUSTOMER_ID IS NULL;

### 10. List customers (customer number, last name) with highest total purchase (rank one) for each state. 
