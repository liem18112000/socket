import mysql.connector
from mysql.connector import errorcode


DB_NAME = 'socket'
USER = 'root'
PASSWORD = ''
HOST = '127.0.0.1'


class Database:
    def __init__(self, u=USER, p=PASSWORD, h=HOST, dbname=DB_NAME):
        self.dbname = dbname
        self.user = u
        self.password = p
        self.host = h
        self.connectDatabase()

    def connectDatabase(self):
        """
        Create new connection
        """
        try:

            self.conn = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.dbname
            )

            self.cursor = self.conn.cursor()

            print("Database connect done")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(-1)

    def createDatabase(self, dbname=DB_NAME):
        """
        Create Database
        :param dbname:
        :return:
        """
        try:
            self.cursor.execute("USE {}".format(dbname))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(dbname))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    self.cursor.execute(
                        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbname)
                    )
                except mysql.connector.Error as err:
                    print("Failed creating database: {}".format(err))
                    exit(1)
                print("Database {} created successfully.".format(dbname))
                self.conn.database = dbname
            else:
                print(err)
                exit(1)

    def createAllTables(self, tables):
        """
        Create all tables
        :param tables:
        :return:
        """
        for table_name in tables:
            table_description = tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        self.cursor.close()

    def execute(self, sql, data=None):
        """
        Execute sql code
        :param sql:
        :param data:
        :return:
        """

        # Execute information
        self.cursor.execute(sql, data)
        print("Execute done")

        # Commit change
        self.conn.commit()

    def getData(self, sql, where=None):
        """
        :param sql:
        :param where:
        :return:
        """

        # Execute information
        self.cursor.execute(sql, where)
        print("Get data done")
        return self.cursor


# db = Database()
#
# sql = (
#     "SELECT route, ticket_type, quantity, price FROM ticket"
# )
#
# for (route, ticket_type, quantity, price) in db.getData(sql):
#     print(str(route) + " " + str(ticket_type) + " " + str(quantity) + " " + str(price))
