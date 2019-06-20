import os
import re
import traceback


def cerate_table_function(file_path):
    for file_ in os.listdir(file_path):
        flag = 0
        with open(os.path.join(file_), 'r') as fp:
            remark1 = 'create table'
            len_r1 = 2
            remark2 = ')organization external'
            output_string = ''
            try:
                _sqls = fp.readlines()
            except Exception:
                print('Modify sql error! file pointer cannot be used!')
                print(traceback.format_exc())
                raise Exception
            sql = ''
            stack_ = []
            for _sql in _sqls:
                st_remark1 = st_remark2 = st_remark3 = -1
                if _sql.find(remark1) >= 0:
                    st_remark1 = _sql.find(remark1)
                    stack_.append(1)
                if _sql.find(remark2) >= 0:
                    st_remark2 = _sql.find(remark2)
                    stack_.append(2)
                if len(stack_) == 0:
                    output_string += _sql
                elif st_remark1 >= 0:
                    if st_remark2 >= 0:
                        output_string += _sql[st_remark1: st_remark2]
                elif st_remark2 >= 0:
                    output_string += _sql[st_remark2 + len_r1:]
                else:
                    continue

                if st_remark2 >= 0:
                    stack_.pop()
                    if stack_.count(1) > stack_.count(2):
                        stack_.pop()
                if st_remark3 >= 0:
                    stack_.pop()