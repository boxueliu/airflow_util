
# -*- coding:UTF-8 -*-
r"""
author: boxueliu
version: 0.1.0
description: airflow analysis sql and create file
"""
import os
import time
import cx_Oracle
import traceback2 as traceback


class AirflowUtil:

    def __init__(self):
        self.flag = ''

    def flag_creat(self, file_path):
        r"""
         cbb system to create success file flag
        :param file_path:
        :return:
        """
        flag_name = 'complete.log'
        with open(os.path.join(file_path, flag_name), 'w') as file:
            file.write('batch complete in %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def get_cut_time(self, taskid, conn):
        r"""
        get daily cut time by taskid
        :param taskid:
        :param conn:
        :return:
        """
        try:
            conenc = conn
            conn = cx_Oracle.connect(conenc)
            cursor = conn.cursor()
            sql = "SELECT TO_CHAR(LAST_FIN_DAILY_DATE,'YYYY-MM-DD_HH:MI:SS')," \
                  "TO_CHAR(THIS_FIN_DAILY_DATE,'YYYY-MM-DD_HH:MI:SS') " \
                  "FROM K_ODS.FIN_DAILY_TABLE   WHERE TASK_ID = '%s'  AND EFF_FLAG = '1'" \
                  % str(taskid)
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            return data[0][0], data[0][1]
        except Exception as e:
            print(e)

    def spool_csv(self, **kwargs):
        r"""
        to analysis sql file and create csv file to export data
        :param kwargs:
        :return: csv file
        """
        spool_path = kwargs['spool_path']
        data_path = kwargs['data_path']
        data_type = kwargs['data_type']
        sql_name = kwargs['sql_name']
        conn = kwargs['conn']
        daily_conn = kwargs['daily_conn']

        """
            get daily time
        """
        daily_start_time, daily_end_time = self.get_cut_time(data_type, daily_conn)
        connect = cx_Oracle.connect(conn, encoding='gb18030')
        cursor = connect.cursor()

        """     
            to analysis sql
        """
        for file_ in os.listdir(spool_path):
            try:
                if file_ == sql_name:
                    with open(os.path.join(spool_path, file_), 'r') as fp:
                        spool_source = fp.readlines()
                        file_flag = 0
                        sql_flag = 0
                        file_name = ''
                        sql_ = ''
                        for line_ in spool_source:
                            if (line_.find('spool ') >= 0) & (line_.find('set ') < 0) & (file_flag == 0):
                                # find file path
                                file_flag = 1
                                try:
                                    file_name = line_.replace('\n', '').split(' ')[1].split('/')[-1].replace("'", '')
                                except Exception:
                                    print('spool not formatted!')
                                    print(line_)
                                    print(traceback.format_exc())
                            elif (line_.upper().find('SELECT') >= 0) & (file_flag == 1) & (sql_flag == 0):
                                sql_flag = 1
                                sql_ += line_
                            elif line_.strip().find('spool off;') == 0:
                                sql_flag = 0
                            elif line_.strip().find('quit;') == 0:
                                sql_flag = 0
                            elif sql_flag == 1:
                                sql_ += line_

                    if sql_.find('&2') != -1:
                        sql_ = sql_.replace('&2', daily_start_time)
                    if sql_.find('&3') != -1:
                        sql_ = sql_.replace('&3', daily_end_time)

                    print(sql_.replace(';', ''))
                    cursor.execute(sql_.replace(';', ''))
                    with open(os.path.join(data_path, file_name), 'w', encoding='gb18030') as f:
                        while True:
                            data = cursor.fetchmany(1000)
                            if data:
                                for x in data:
                                    f.write(x[0])
                                    f.write('\n')
                            else:
                                break
                    cursor.close()
                else:
                    pass
            except Exception as e:
                print(e)


if __name__ == '__main__':
    a = AirflowUtil()

    print(a.get_cut_time('RTL1', 'ODSB_ADMIN/admin@10.20.201.99/DDMUATDB'))