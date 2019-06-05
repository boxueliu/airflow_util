import cx_Oracle
import pymysql
import xlrd
import os


class util:
    # 连接mysql
    @staticmethod
    def mysqlconn(host, user, passwd, database):
        try:
            # db = pymysql.connect("10.20.202.184", "mysql", "2wsx*IK<", "cbb")
            db = pymysql.connect(host, user, passwd, database)
            cursor = db.cursor()
            return cursor
        except Exception as e:
            print(e)

    # 连接Oracle
    @staticmethod
    def oracleconn(conn):
        try:
            connect = cx_Oracle.connect(conn, encoding='utf-8')
            cursor = connect.cursor()
            return cursor
        except Exception as e:
            print(e)

    @staticmethod
    def xlsx(name,path=os.path.dirname(os.path.realpath(__file__)), index=0):
        """
        :param name: name of execl
        :param path: path of execl
        :param index: index of sheet, default 0
        :return: Object of sheet
        """
        try:
            path = os.path.join(path,name)
            xlsx = xlrd.open_workbook(path)
            sheet = xlsx.sheet_by_index(index)
            return sheet
        except Exception as e:
            print(e)


    @staticmethod
    def getpk(cursor, tablename):
        # 获取主键字段 sql
        colnum_pri = "select COLUMN_NAME from user_tab_columns where Table_Name='%s' ORDER BY COLUMN_NAME DESC"
        # 主键
        pri_column = ''
        # replace的根据实际情况修改 如没有需要修改 ：cursor_m.execute(colnum_pri %  table)
        # cursor.execute(colnum_pri % tablename.replace('ODS_', '', 1))
        cursor.execute(colnum_pri % tablename + "1")
        colnum_pris = cursor.fetchall()
        for pri in colnum_pris:
            if pri == colnum_pris[len(colnum_pris) - 1]:
                pri_column = pri_column + pri[0]
            else:
                pri_column = pri_column + pri[0] + ','
        return pri_column

if __name__ == '__main__':
    sql_file_name='/opt/aaa'
    print(os.path.join(sql_file_name))