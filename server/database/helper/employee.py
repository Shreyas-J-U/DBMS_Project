import pymysql
from pymysql import Error
from database.helper.authentication import *


def insert_employee_cred(db_resources,owner_cred):

    connection,cursor= db_resources
    

    try:

        if(len(owner_cred) == 5):

            query = """
                INSERT INTO employee (first_name, last_name, role, email, phone)
                VALUES (%s, %s, %s, %s, %s)
            """
        else:
            query = """
                INSERT INTO employee (first_name, last_name, role, email, phone,store_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

        cursor.execute(query, owner_cred)
        connection.commit()
        new_id = cursor.lastrowid
        return (True,new_id)

    except Error as e:
        print(e)
        connection.rollback()
        return (False,-1)

def store_hashed_passwords(db_resources,user,id,raw_password) -> bool:

    connection,cursor=db_resources
    hash_pass = hash_password(raw_password)
    query = """
        insert into passwords(user_name,employee_id,hash_pass) values(
            %s,
            %s,
            %s
            );
        """
    try : 
        cursor.execute(query,(user,id,hash_pass))
        connection.commit()
        return True
    except Error as e:
        print(e)
    
        connection.rollback()
        return False
    

def get_all_unassigned_managers(db_resources):

    connection,cursor = db_resources
    try:
        query = """
            SELECT e.employee_id, e.first_name, e.last_name
            FROM employee e
            WHERE e.role = 'manager'
            AND e.employee_id NOT IN (
            SELECT s.manager_id FROM store s WHERE s.manager_id IS NOT NULL
            );
            """
        cursor.execute(query)
        result = cursor.fetchall()
        return (True,result)
    
    except Exception as e:
        print(e)
        return (False,None)


def remove_employee_cred(db_resources,employee_id):

    connection,cursor = db_resources
    try:
        query = """
                delete from employee where employee_id = %s;
                """
        cursor.execute(query,employee_id)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False
    

def create_check_attendance_func(db_resources):

    connection,cursor=db_resources

    try:
        query = """

            CREATE FUNCTION has_attendance_today(emp_id INT)
            RETURNS BOOLEAN
            DETERMINISTIC
            BEGIN
                DECLARE count_att INT;
                SELECT COUNT(*) INTO count_att
                FROM attendance
                WHERE employee_id = emp_id AND attendance_date = CURDATE();
                
                RETURN count_att > 0;
            END
        """

        cursor.execute(query)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False
    
def create_attendance_helper(db_resources):

    connection,cursor = db_resources

    try:
        query = """
                CREATE FUNCTION has_attendance_today(emp_id INT)
                RETURNS BOOLEAN
                DETERMINISTIC
                BEGIN
                    DECLARE count_att INT;
                    SELECT COUNT(*) INTO count_att
                    FROM attendance
                    WHERE employee_id = emp_id AND attendance_date = CURDATE();
                    
                    RETURN count_att > 0;
                END
                """
        
        cursor.execute(query)

        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False
    

def create_checkin_procedure(db_resources):

    connection,cursor = db_resources

    try:
        query = """

            CREATE PROCEDURE mark_checkin(IN emp_id INT)
            BEGIN
                IF NOT has_attendance_today(emp_id) THEN
                    INSERT INTO attendance (employee_id, attendance_date, check_in, status)
                    VALUES (emp_id, CURDATE(), NOW(), 'present');
                END IF;
            END 
        """
        cursor.execute(query)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False
    
def create_checkout_procedure(db_resources):

    connection,cursor = db_resources
    try:
        query = """

            CREATE PROCEDURE mark_checkout(IN emp_id INT)
            BEGIN
                DECLARE existing_id INT;
                DECLARE existing_checkout DATETIME;

                SELECT attendance_id, check_out INTO existing_id, existing_checkout
                FROM attendance
                WHERE employee_id = emp_id AND attendance_date = CURDATE()
                LIMIT 1;

                IF existing_id IS NOT NULL THEN
                    IF existing_checkout IS NULL THEN
                        UPDATE attendance
                        SET check_out = NOW()
                        WHERE attendance_id = existing_id;
                    END IF;
                END IF;
            END 
           
            """
    
        cursor.execute(query)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False
    
        
def check_todays_attendance(db_resources, employee_id):
    connection, cursor = db_resources
    try:
        query = "SELECT has_attendance_today(%s);"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()
        print("Attendance check result:", result)
        return result[list(result.keys())[0]] if result else False 
    except Exception as e:
        print("Error in check_todays_attendance:", e)
        return False


def employee_checkin(db_resources, employee_id):
    connection, cursor = db_resources
    try:
        query = "CALL mark_checkin(%s);"
        cursor.execute(query, (employee_id,))  
        connection.commit()  
        return True
    except Exception as e:
        print("Error in employee_checkin:", e)
        connection.rollback()
        return False


def employee_checkout(db_resources, employee_id):
    connection, cursor = db_resources
    try:
        query = "CALL mark_checkout(%s);"
        cursor.execute(query, (employee_id,))  
        connection.commit()  
        return True
    except Exception as e:
        print("Error in employee_checkout:", e)
        connection.rollback()
        return False

def get_employee_id(db_resources, username):
    connection, cursor = db_resources
    try:
        query = "SELECT employee_id FROM passwords WHERE user_name = %s"
        cursor.execute(query, (username,))  
        result = cursor.fetchone()
        
        if result:
            # if using DictCursor, extract the value from the dict
            return result["employee_id"]
        else:
            return None 
        
    except Exception as e:
        print("Error in get_employee_id:", e)
        return -1

