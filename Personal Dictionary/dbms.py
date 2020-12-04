import sqlite3
from sqlite3 import Error


class dbms():
    def __init__(self, table_name, database_name_and_path):
        self.table_name = table_name
        database = database_name_and_path
        # database = r":memory:"
        # database = r"C:\Users\ronakjai\Documents\Docs\DFD\Experiments\python_sql\Dict_personal.db"
        self.conn = self.create_connection(database)
        
    def create_connection(self, db_file):
        """ 
        Create a database connection to the SQLite database
        specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'connection stablished to database. version: {sqlite3.version}')
            return conn
        except Error as e:
            print(e)
            
        return conn
        
    def create_table(self, create_table_sql):
        """     
        Create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        conn = self.conn
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            conn.commit()
            print("table created")
        except Error as e:
            print(e)
        
    def create_entry(self, sql, entry):
        """
        Create a new entry
        :param conn:
        :param entry:
        :return:
        """
        conn = self.conn                  
        # sql = ''' INSERT INTO crqram(Valid,CreqID,Addr,Addr_Full,AfuId,VirtualAFU,Ial_attr,Mdata,NeedReIssue,BBSOpcode,Op_Type,RdbufAddr,Target,WaitDfc,WaitExtCmp,WaitGo,WrBufI)
                  # VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        # with conn:
        cur = conn.cursor()
        cur.execute(sql, entry)
        conn.commit()
        print("entry added")
        return cur.lastrowid
        
    def update_entry(self, entry):
        """
        update priority, begin_date, and end date of a entry
        :param conn:
        :param entry:
        :return: project id
        """
        conn = self.conn
        sql = ''' UPDATE entries
                  SET priority = ? ,
                      begin_date = ? ,
                      end_date = ?
                  WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, entry)
        conn.commit()
        
    def select_entries(self, query):
        """
        Query all rows in the entry table
        :param conn: the Connection object
        :param query: sql query to operate
        :return:
        """
        conn = self.conn
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
            
    def delete_entry(self, id):
        """
        Delete a entry by entry id
        :param conn:  Connection to the SQLite database
        :param id: id of the entry
        :return:
        """
        conn = self.conn
        sql = 'DELETE FROM {entries} WHERE id=?'.format(entries = self.table_name)
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()


    def delete_all_entries(self):
        """
        Delete all rows in the entries table
        :param conn: Connection to the SQLite database
        :return:
        """
        conn = self.conn
        sql = 'DELETE FROM {entries}'.format(entries = self.table_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        
    def get_sql_for_creating_table(self, header):
        table_name = self.table_name
        sql = r'CREATE TABLE IF NOT EXISTS' + ' ' + table_name + r'(' + \
         'id integer PRIMARY KEY,\n'+ \
         " text,\n".join(header) + " text"+ \
        r');'
        return sql
        
    def get_sql_for_creating_entry(self, header):
        table_name = self.table_name
        sql = r' INSERT INTO' + ' ' + table_name + '('+\
                ",".join(header) + r')'+\
                '\n'+r'VALUES('+ "?,"*(len(header)-1) + "?" +r');'
        return sql
        
def main():
    # initialize (connection established to the database)
    dbms_inst = dbms("dictionary")
    
    # create a new table
    list = ["Word", "Meaning"]    
    
    sql_create_table = dbms_inst.get_sql_for_creating_table(list)        
    print(sql_create_table)
    print()
    dbms_inst.create_table(sql_create_table)
    
    # insert data            
    sql = dbms_inst.get_sql_for_creating_entry(list)            
    print(sql)
    print()
    entry = ("word1","meaning1")
    cursor = dbms_inst.create_entry(sql, entry)
    print(f'cursor at {cursor}')
    entry = ("word2","meaning2")
    cursor = dbms_inst.create_entry(sql, entry)
    print(f'cursor at {cursor}')
    entry = ("word3","meaning3")
    cursor = dbms_inst.create_entry(sql, entry)
    print(f'cursor at {cursor}')
    entry = ("word4","meaning4")
    cursor = dbms_inst.create_entry(sql, entry)
    print(f'cursor at {cursor}')
    
    dbms_inst.select_entries("SELECT * FROM dictionary")
    print()
    # dbms_inst.select_entries("SELECT * FROM dictionary WHERE Valid LIKE 'V%'")
    dbms_inst.delete_all_entries()    

if __name__ == '__main__':
    main()