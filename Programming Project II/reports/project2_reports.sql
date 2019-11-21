/*
 * @author: Luke Malloy
 * @brief:	CS5300 Programming Project 2 Reports
 */

/*
 * Report 1:  List of authors and number of books they have,
 * 			  in descending order: report_1.csv
 */  
SELECT AUTHOR, COUNT(TITLE) AS BOOK_COUNT
FROM CAO346.BOOK_EDITIONS
WHERE 1=1 
GROUP BY AUTHOR
ORDER BY BOOK_COUNT DESC; --> exported to .csv


/*
 * Report 2: List of publishing companies and number of books
 * 		     they have, in descending order: report_2.csv
 */
SELECT PUBLISHER, COUNT(TITLE) AS BOOK_COUNT
FROM CAO346.PUBLISHER_BOOKS
WHERE 1=1
GROUP BY PUBLISHER
ORDER BY BOOK_COUNT DESC; -- exported to .csv


/*
 * Report 3: List of books newer than 2000: report_3.csv
 * 		     (Books with missing year exempt)
 */
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.BOOK_EDITIONS
WHERE PUBLISH_YEAR > 2000
ORDER BY TITLE; --> exported to .csv

/*
 * Report 4: Book list for those with missing data: report_4.csv
 * 
 * Assumptions: 
 * -- Books with missing notes are withdrawn from inquiry,
 * 	  as most books would be included and is not considered 
 * 	  critical unless otherwise requested by the customer
 * 	  
 * 
*/

-- Booklist
CREATE TABLE books AS 
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.BOOK_EDITIONS;

-- Books that are missing data in BOOK_EDITIONS
CREATE TABLE missing_1 AS 
SELECT TITLE, AUTHOR, EDITION 
FROM CAO346.BOOK_EDITIONS
-- Missing either ISBN, Page count or year published
-- Individual attribute reports availiable upon customer request
WHERE ISBN = 'nan' OR PAGES = 'nan' OR PUBLISH_YEAR = 'nan';

/*
 * Book data exists for the following attributes in the tables with FK:
 *	--binding type
 *	--jacket condition
 *	--book type
 *	--publisher
 *	--book grade
 *  
*/

-- Extract books missing this data with set difference of book_editions and FK tables
-- Books - binding_type
CREATE TABLE missing_binding_types AS
SELECT TITLE, AUTHOR, EDITION
FROM LDM437.BOOKS
MINUS
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.BOOK_BINDING_TYPES;

-- Books - jacket_condition
CREATE TABLE missing_conditions AS
SELECT TITLE, AUTHOR, EDITION
FROM LDM437.BOOKS
MINUS
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.BOOK_CONDITION;

-- Books - book_type
CREATE TABLE missing_book_types AS
SELECT TITLE, AUTHOR, EDITION
FROM LDM437.BOOKS
MINUS
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.BOOK_TYPE;

-- Books - publisher
CREATE TABLE missing_publishers AS
SELECT TITLE, AUTHOR, EDITION
FROM LDM437.BOOKS
MINUS
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.PUBLISHER_BOOKS;

-- Books - book_grade
CREATE TABLE missing_book_grades AS
SELECT TITLE, AUTHOR, EDITION
FROM LDM437.BOOKS
MINUS
SELECT TITLE, AUTHOR, EDITION
FROM CAO346.BOOK_GRADE;

-- Union all results from above
CREATE TABLE fk_missing AS 
SELECT * 
FROM LDM437.MISSING_BINDING_TYPES
UNION
SELECT *
FROM LDM437.MISSING_CONDITIONS
UNION
SELECT * 
FROM LDM437.MISSING_BOOK_TYPES
UNION
SELECT * 
FROM LDM437.MISSING_PUBLISHERS
UNION 
SELECT * 
FROM LDM437.MISSING_BOOK_GRADES

/* report_4.csv */
-- Union missing_1 (books with 'nan' values of interest) results with table created above
SELECT * 
FROM LDM437.FK_MISSING
UNION 
SELECT * 
FROM LDM437.MISSING_1 --> exported to .csv # 1172 books with important missing data!




