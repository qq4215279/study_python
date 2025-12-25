#encoding=utf-8

import MySQLdb

TEST_SQL = 'select CURRENT_DATE from dual'

class DBUtil:
    '''
    argument like this
    util = DBUitl(host="localhost", db="mysql", user="root", passwd="1234")
    '''
    def __init__(self, **args):
        self.args = args
        try:
            self._check()
            self._init()
        except KeyError, e:
            raise e
    def _check(self):
        if not self.args.has_key('host'):
            print ('need argument host')
            raise KeyError('need argument host')
        elif not self.args.has_key('db'):
            print ('need argument db')
            raise KeyError('need argument host')
        elif not self.args.has_key('user'):
            print ('need argument user')
            raise KeyError('need argument host')
        elif not self.args.has_key('passwd'):
            print ('need argument psw')
            raise KeyError('need argument host')
        
    def _init(self):
        try:
            self.db = MySQLdb.connect(host=self.args['host'], user=self.args['user'],
                                      passwd=self.args['passwd'], db=self.args['db'],
                                      charset="utf8")
            self.db.query(TEST_SQL)
            r = self.db.store_result() #一次全部拉去 use_result() 一行一行拉取
            print(r.fetch_row())
        except Exception, e:
            raise e

    '''
    查询结果
    '''
    def query(self, sql, *args):
        dc = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        dc.execute(sql, args)
        result = dc.fetchall()
        dc.close()
        return result

    def close(self):
        self.db.close()
        
