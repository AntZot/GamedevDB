import mysql.connector
from mysql.connector import Error

class dbController():

    def create_connection(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='azot'
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE gamedev;")
        return self.connection

    def create_database(self):
        self.cursor.close()
        file = open("Resources/DataBase.sql", 'r')
        sql_script_string = file.read()
        file.close()
        self.cursor.executescript(sql_script_string)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print('Execute sql script complete.')
        """with open('Resources/DataBase.sql') as f:
            with self.connection.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
            self.connection.commit()"""

    def add_project(self,platform,project_name,github_url):
        print(f"INSERT INTO project (platform_id,project_name,guthub_url) VALUES ('{platform}','{project_name}','{github_url}') ")
        self.cursor.execute(f"INSERT INTO project (platform_id,project_name,guthub_url) VALUES ('{platform}','{project_name}','{github_url}') ")
        self.connection.commit()

    def get_project_list(self):
        self.cursor.execute("SELECT * FROM project")
        return self.cursor.fetchall()

    def add_department(self):
        pass

    def get_department_list(self):
        pass

    def add_employee(self):
        print("INSERT INTO employee (employee_name,employee_second_name,position) VALUES ('%s') ")

    def get_employee_list(self):
        pass

    def add_platform(self,platform_name):
        print("INSERT INTO platform (platform) VALUES ('%s') " % platform_name)
        self.cursor.execute("INSERT INTO platform (platform) VALUES ('%s') " % platform_name)
        self.connection.commit()

    def add_state(self, state):
        print("INSERT INTO state (state) VALUES ('%s') " % state)
        self.cursor.execute("INSERT INTO state (state) VALUES ('%s') " % state)
        self.connection.commit()

    def get_state(self):

        pass

