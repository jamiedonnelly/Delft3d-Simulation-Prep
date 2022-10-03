from numpy import insert
import mysql.connector
from functools import wraps

class sql_api():

    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()
    
    def connect(self):
        self.conn = mysql.connector.connect(host=self.host, user=self.user, database=self.database, password=self.password)
        self.cursor = self.conn.cursor()

    def _commit(func):
        @wraps(func)
        def wrap(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.conn.commit()
            return result
        return wrap

    def _reconnect(func):
        @wraps(func)
        def rec(self,*args,**kwargs):
            try:
                result = func(self,*args,**kwargs)
                return result
            except (mysql.connector.Error, mysql.connector.Warning) as e:
                self.connect()
                result = func(self,*args,**kwargs)
                return result
        return rec   

    @_commit
    @_reconnect 
    def add_bc(self,table,data):
        value_placeholder = ''
        insert_str = '({})'
        for i in range(40):
            if i == max(list(range(40))):
                value_placeholder += '%s'
            else:
                value_placeholder += '%s,'
        cmd = 'INSERT INTO {table} VALUES {insert}'.format(table=table,insert=insert_str.format(value_placeholder))
        self.cursor.execute(cmd,params=data)



