

import sqlite3


class Database():

    def __init__(self, db_file):
        self.conn = self.create_connection(db_file=db_file)
        self.create_database()
    
    

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            return self.conn
        except sqlite3.Error as e:
            print(e)

        return self.conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)
        
    def create_database(self):
        database = 'database.db'

        sql_create_reports_table = """ CREATE TABLE IF NOT EXISTS Report (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            date text,
                                            bssid text NOT NULL,
                                            essid text,
                                            protocol text NOT NULL,
                                            channel integer
                                        ); """

        sql_create_attack_table = """CREATE TABLE IF NOT EXISTS Attack (
                                        id integer PRIMARY KEY,
                                        type text NOT NULL,
                                        info text,
                                        risk text,
                                        report_id integer NOT NULL,
                                        FOREIGN KEY (report_id) REFERENCES Report (id)
                                    );"""

        # create a database connection
        self.conn = self.create_connection(database)

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_reports_table)
            self.create_table(sql_create_attack_table)
        else:
            print("Error! cannot create the database connection.")
    
    def create_report(self, report):
        """
        Create a new report
        :param conn:
        :param report:
        :return:
        """

        sql = ''' INSERT INTO Report(name,date,bssid,essid,protocol,channel)
                VALUES(?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, report)
        self.conn.commit()

        return cur.lastrowid
    
    def create_attack(self, attack):
        """
        Create a new attack
        :param attack:
        :return:
        """

        sql = ''' INSERT INTO Attack (type, info, risk, report_id)
                VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, attack)
        self.conn.commit()

        return cur.lastrowid

    def filter_reports(self, filter=None) -> list:
        with self.conn:
            c = self.conn.cursor()
            if not filter:
                c.execute("SELECT * FROM Report")
                return c.fetchmany(10)

            