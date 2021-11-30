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
        try:
            self.cursor.execute("USE gamedev;")
        except Error as e:
            print(f"The error '{e}' occurred")
            self.create_database()
        finally:
            self.cursor.execute("USE gamedev;")
        return self.connection

    def create_database(self):
        file = open("Resources\gamedev.sql", 'r')
        while True:
            # считываем строку
            sql_script_string = file.readline().strip()
            # прерываем цикл, если строка пустая
            if not sql_script_string:
                break

            if sql_script_string.find(";") == -1:
                sql_script_string += " " + file.readline().strip()
                while sql_script_string.find(";") == -1:
                    sql_script_string += " " + file.readline().strip()
            else:
                print(sql_script_string.find(";"))
            self.cursor.execute(sql_script_string)
            self.connection.commit()
        file.close()
        print('Execute sql script complete.')

    def add_project(self, project_name, platform, **kwargs):
        request = "INSERT INTO project (platform_id,project_name"
        for key in kwargs.keys():
            request += "," + str(key)
        request += f") VALUES ({self.get_platform(platform = platform)[0][0]},"
        request += f"'{project_name}\'"
        for key in kwargs.keys():
            if key == 'github_url':
                request += f",'{kwargs[key]}'"
            if key == 'state_id':
                request += f",{self.get_state(state = kwargs[key])[0][0]}"
            if key == 'project_version':
                request += f""
        request += ")"
        print(request)
        self.cursor.execute(request)
        self.connection.commit()

    def get_project_list(self):
        self.cursor.execute("SELECT * FROM project")
        return self.cursor.fetchall()

    def add_platform(self,platform_name):
        print("INSERT INTO platform (platform) VALUES ('%s') " % platform_name)
        self.cursor.execute("INSERT INTO platform (platform) VALUES ('%s') " % platform_name)
        self.connection.commit()

    def get_platform(self, **kwargs):
        if len(kwargs) > 0:
            request = f"SELECT * FROM platform WHERE"
        else:
            request = f"SELECT * FROM platform"
        for key in kwargs.keys():
            if isinstance(kwargs[key],str):
                request += " " + key + " = '" + kwargs[key] + "'"
            else:
                request += " " + key + " = " + str(kwargs[key]) + ""

        self.cursor.execute(request)
        return self.cursor.fetchall()

    def add_state(self, state):
        print("INSERT INTO state (state) VALUES ('%s') " % state)
        self.cursor.execute("INSERT INTO state (state) VALUES ('%s') " % state)
        self.connection.commit()

    def get_state(self, **kwargs):
        if len(kwargs) > 0:
            request = f"SELECT * FROM state WHERE"
        else:
            request = f"SELECT * FROM state"
        for key in kwargs.keys():
            if isinstance(kwargs[key], str):
                request += f" {key} = '{kwargs[key]}'"
            else:
                request += f" {key} = {kwargs[key]}"

        self.cursor.execute(request)
        return self.cursor.fetchall()

    def add_department(self):
        pass

    def get_department_list(self):
        pass

    def add_employee(self):
        print("INSERT INTO employee (employee_name,employee_second_name,position) VALUES ('%s') ")

    def get_employee_list(self):
        pass

