# Cheat Sheet for Midterm IT 440 Spring 2019

### Remember that the midterm is on Thursday, March 14th.

### Recommended Resources:
All the stuff here is basically from the D2L page. The RDBMS manager I use is a really good one called DataGrip from JetBrains, it's free and a lot better than Oracle's in my opinion

## General Oracle Specific Commands

### Shows all the column names in a certain table

select column_name from all_tab_columns Where TABLE_NAME = 'your_table_here' ;


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

Lots of Joins in this one, should probably clean it up but ¯\_(ツ)_/¯


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

### List the top 10 percent of customers in terms of total number of orders (customer number, customer last name, and state) 

### List top city in each state in terms of total gross sales (exclude shipping charges and taxes) 

### List every product number and their total sales for each year (product number, year, total gross sale)

### List all customers that have more than two orders (customer number, number of orders) in desc order based on number of orders 

### List all employees that have not had any sales (employee number, last name, position title) 

### List total gross sales for each month (Hint: use substr to get the month). Order the result based on month from Jan to Dec. 

### List unique pairs of customers that are form the same city 

### List total sales for each product and calculate the percentage of their sale compared to total sale. 

### List customers (customer number, full name (last name, first name)) that have not placed any order yet 

### List customers (customer number, last name) with highest total purchase (rank one) for each state. 
