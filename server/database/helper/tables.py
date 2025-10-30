import pymysql


def create_employee_table(cursor):
    
    cursor.execute(
        """
            CREATE TABLE employee (
                employee_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                role enum('owner','manager','employee','supplier') NOT NULL,
                email VARCHAR(100),
                phone BIGINT NOT NULL
            );
        """
            
    )


def create_store_table(cursor):

    cursor.execute(
        """
            CREATE TABLE store(
                store_id INT AUTO_INCREMENT PRIMARY KEY ,
                store_name varchar(50) NOT NULL,
                location POINT NOT NULL,
                manager_id INT,
                FOREIGN KEY (manager_id) REFERENCES employee(employee_id)
            );
        """
    )

def create_customer_table(cursor):

    cursor.execute(
        """
            CREATE TABLE customer(
	            customer_id INT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                email VARCHAR(100),
                phone BIGINT,
                address VARCHAR(100)
            );
        """
    );    

def create_order_table(cursor):

    cursor.execute(
        """
            CREATE TABLE orders(
            order_id INT PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            amount float NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customer(customer_id) 
            ); 
        """
    )


def create_order_item_table(cursor):

    cursor.execute(
        """
            CREATE TABLE order_item(
                order_item_id INT PRIMARY KEY,
                order_id INT ,
                product_id INT,
                quantity INT,
                unit_price FLOAT,
                FOREIGN KEY(order_id) REFERENCES orders(order_id),
                FOREIGN KEY(product_id) REFERENCES product(product_id)
            );  
        """
    )


def create_payment_table(cursor):
    cursor.execute(
        """
            CREATE TABLE payment(
                payment_id INT PRIMARY KEY,
                order_id INT,
                payment_date DATE,
                amount float,
                payment_method ENUM('CARD','NETBANK','CASH','OTHERS') NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(order_id)
            );    
        """
    )


def create_product_table(cursor):

    cursor.execute(
            """
                CREATE TABLE product(
                product_id INT PRIMARY KEY,
                product_name VARCHAR(50) NOT NULL,
                product_description VARCHAR(150),
                price FLOAT NOT NULL,
                stock_quantity INT,
                category_id INT,
                supplier_id INT,
                FOREIGN KEY(category_id) REFERENCES product_category(category_id),
                FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id)
                );
            """
    )

def create_product_category(cursor):

    cursor.execute(
        """
            CREATE TABLE product_category(
                category_id INT PRIMARY KEY,
                category_name VARCHAR(100)
        );
        """
    )
    
def create_supplier_table(cursor):


    cursor.execute(
        """
            CREATE TABLE supplier(
                supplier_id INT PRIMARY KEY,
                supplier_name VARCHAR(50) NOT NULL,
                email VARCHAR(150) NOT NULL,
                phone BIGINT UNSIGNED NOT NULL
            ); 
        """ 
    )

def create_inventory_transactions(cursor):

    cursor.execute(
        """ 
            CREATE TABLE inventory_transactions(
                transaction_id INT PRIMARY KEY,
                product_id INT NOT NULL,
                transaction_type VARCHAR(100),
                quantity  INT NOT NULL,
                transaction_date DATE NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product(product_id)
            );
        """
    )   


def create_passwords_table(cursor):

    cursor.execute(

        """
            CREATE TABLE passwords (          
                user_name varchar(100) PRIMARY KEY,
                employee_id INT UNIQUE NOT NULL,
                hash_pass VARCHAR(100) NOT NULL,
                FOREIGN KEY (employee_id) 
                    REFERENCES employee(employee_id)
                    ON DELETE CASCADE
            );
        """
    )


def create_attendance_table(cursor):
    
    cursor.execute(
        """
            CREATE TABLE attendance (
                attendance_id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT NOT NULL,
                attendance_date DATE NOT NULL,
                check_in DATETIME,
                check_out DATETIME,
                status ENUM('present', 'absent', 'leave', 'half-day') DEFAULT 'absent',
                FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE,
                UNIQUE (employee_id, attendance_date)
            );

        """
    )





def link_employee_store(cursor):

    cursor.execute(
        """
            ALTER TABLE employee
            ADD COLUMN store_id INT;
        """
    )

    cursor.execute(

        """
            ALTER TABLE employee
            ADD CONSTRAINT fk_employee_store
            FOREIGN KEY (store_id)
            REFERENCES store(store_id);
        """
    )


