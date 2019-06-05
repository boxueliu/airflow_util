# -*- coding: utf-8 -*-
from Util import util
import os

# 需要比对的表名
# table_ = [
# 'ARCH_CITY'
# ,'ARCH_PROVINCE'
# ,'ARCH_TEMPLATE'
# ,'CFL_BANK_CITY_MP'
# ,'CFL_BANK_PROV_MP'
# ,'CFL_DIC_MP'
# ,'ODS_AP_PRELOAN_ARJ_OVERRIDE'
# ,'ODS_AP_PRELOAN_ELE_AUTH'
# ,'ODS_AP_PRELOAN_LENDINGPOOL'
# ,'ODS_BK_CONT_TRANS_INFO_CFL'
# ,'ODS_BKPF'
# ,'ODS_C_VM_IPOUTINFO'
# ,'ODS_CFL_001_SP_APP'
# ,'ODS_CFL_001_SP_RESP'
# ,'ODS_CFL_001_ZY_APP'
# ,'ODS_CFL_001_ZY_RESP'
# ,'ODS_CFL_BATCH_DAILY_BAL'
# ,'ODS_CFL_BATCH_REPAY_APP'
# ,'ODS_CFL_BATCH_REPAY_PLAN'
# ,'ODS_CM_CFL_BANK_INFO'
# ,'ODS_CM_FINPRT_FJD_ASSET_MP'
# ,'ODS_CM_FINPRT_FJD_RATE'
# ,'ODS_CR_PY_PHONE'
# ,'ODS_FAGLFLEXA'
# ,'ODS_I_CM_RECORDREG'
# ,'ODS_LN_CFL_SETTLE_BK_TRIAL'
# ,'ODS_LN_CS_CONT_CFL'
# ,'ODS_LN_CS_CONT_EXT'
# ,'ODS_R_APP_COBORWINFO'
# ,'ODS_R_APP_CRLINKADDR'
# ,'ODS_R_APP_DESTASK'
# ,'ODS_R_APP_IDLINKADDR'
# ,'ODS_R_COL_EARLYTASK'
# ,'ODS_R_COL_FIELDCOREG'
# ,'ODS_R_COL_LAWSUITREG'
# ,'ODS_R_COL_MIDDREG'
# ,'ODS_R_COL_OUTTRAILREG'
# ,'ODS_R_CUS_VEHFPREG'
# ,'ODS_R_DF_CHARGEINFO'
# ,'ODS_R_DLR_DLRGRPINFO'
# ,'ODS_R_PRT_INTRATE'
# ,'ODS_R_PRT_PBOCRATE'
# ,'ODS_R_PRT_PRTFINCRGE'
# ,'ODS_R_PRT_PRTINFO'
# ,'ODS_R_PRT_PRTLOANOBJ'
# ,'ODS_R_PRT_PRTTRMRELA'
# ,'ODS_R_PRT_PRTVEHCOND'
# ,'ODS_R_VEH_BRANDINFO'
# ,'ODS_R_VEH_MODELINFO'
# ,'ODS_R_VEH_SERIESINFO'
# ,'ODS_R_VER_VERIFICATIONINFO'
# ,'ODS_S_RET_SMSDETAIL'
# ,'ODS_SKA1'
# ,'ODS_SKAT'
# ,'ODS_ZUPLOADLOG'
# ,'ODS_ZUPLOADV'
# ]

table_ = [
'ARCH_CITY'
]
# table_ = ['ODS_CM_CD_M']

# minus data sql
data_minus_ = """
SELECT 
    WHO,
    %s
FROM 
(
    SELECT
        WHO,
        %s
    FROM 	
    (
        SELECT
            '%s' WHO,
            %s
        FROM %s.%s ORDER BY %s ASC
    ) A
) B
"""
# data minus 字段处理1
data_col1_ = "CASE WHEN %s IS NULL THEN ' ' ELSE TRIM(%s) END %s"
# data minus 字段处理2
data_col2_ = "CASE WHEN %s LIKE '%%?%%' OR %s LIKE '%%？%%' THEN ' ' ELSE TRIM(%s) END %s"
# data_minus 字段处理3
data_col3_ = "TRIM(REPLACE(REPLACE(%s,CHR(10),''),CHR(13),'')) %s"

# data_minus 字段处理3  for mysql
data_col3_m = "REPLACE(REPLACE(%s,CHAR(10),''),CHAR(13),'') %s"

# data_minus 字段处理4
data_col4_ = "CASE WHEN %s IS NULL THEN 0 ELSE %s END %s"

#
data_col5_ ="TO_CHAR(%s,'YYYY-MM-DD HH24:mi:ss') %s"


# minus 字段 sql
# column_minus_ = """
# (
# 	SELECT * FROM (select '%s' WHO,COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_columns where Table_Name='%s' ORDER BY COLUMN_NAME DESC)
# 	MINUS
# 	SELECT * FROM (select '%s' WHO,COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_columns where Table_Name='%s' ORDER BY COLUMN_NAME DESC)
# )
# 	UNION
# (
# 	SELECT * FROM (select '%s' WHO,COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_columns  where Table_Name='%s' ORDER BY COLUMN_NAME DESC)
# 	MINUS
# 	SELECT * FROM (select '%s' WHO,COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_columns where Table_Name='%s' ORDER BY COLUMN_NAME DESC)
# )
# """

class minusutil:
    # 比较两张表字段是否一致
    @staticmethod
    def minus_column(**kwargs):
        # 获取全字段 sql  ,DATA_TYPE,DATA_LENGTH
        colnum_minus1 = "SELECT COLUMN_NAME,DATA_TYPE FROM dba_tab_columns WHERE OWNER = '%s' AND TABLE_NAME='%s' ORDER BY COLUMN_NAME"
        colnum_minus2 = "SELECT COLUMN_NAME,DATA_TYPE FROM dba_tab_columns WHERE OWNER = '%s' AND TABLE_NAME='%s' ORDER BY COLUMN_NAME"
        cursor1 = kwargs['cursor_1']
        cursor2 = kwargs['cursor_2']
        try:
            sheet = util.xlsx("table.xlsx")
            for row in range(1, sheet.nrows):
                table = sheet.cell(row, 0).value
                table1 = sheet.cell(row, 1).value
                schema = sheet.cell(row, 2).value
                # index = sheet.cell(row, 3).value

                cursor1.execute(colnum_minus1 % (schema, table))
                cursor2.execute(colnum_minus2 % (schema, table1))
                column_data1 = cursor1.fetchall()
                column_data2 = cursor2.fetchall()

                for i in range(len(column_data2)):
                    # print(column_data1[i])
                    # print(column_data2[i])
                    if column_data1[i][0] == column_data2[i][0]:
                        continue
                    else:
                        print(table + ":" + column_data1[i][0] + "\n" + table1 +
                              ":" + column_data2[i][0])
        except Exception as e:
            print(e)
        finally:
            cursor1.close()
            cursor2.close()

    # 比较表数据量是否一致
    @staticmethod
    def minus_count(**kwargs):
        cursor1 = kwargs['cursor_1']
        cursor2 = kwargs['cursor_2']
        count_sql = "SELECT COUNT(*) FROM %s"
        try:
            for table in table_:
                # table1 = table.replace("ODS_", "", 1)
                table1 = table + '1'
                cursor1.execute(count_sql % table)
                cursor2.execute(count_sql % table1)
                count_1 = cursor1.fetchall()
                count_2 = cursor2.fetchall()
                # print(count_1[0][0])
                # print(count_2[0][0])
                if count_1[0][0] == count_2[0][0]:
                    print("%s:NICE|%s" % (table, count_1[0][0]))
                    continue
                else:
                    print("%s:%s" % (table, count_1[0][0]) + "=====%s:%s" %
                          (table1, count_2[0][0]))
        except Exception as e:
            print(e)
        finally:
            cursor1.close()
            cursor2.close()

    # 比较两张表数据是否一致(读取数据逐个字段对比)
    @staticmethod
    def minus_data(**kwargs):
        cursor1 = kwargs['cursor_1']
        cursor2 = kwargs['cursor_2']
        # cursor3 = kwargs['cursor_3']
        # 记录处理数量
        all_num = 0
        # 记录成功数量
        success_num = 0
        try:
            # result_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'result')
            sheet = util.xlsx("table.xlsx")
            for row in range(1, sheet.nrows):
                all_num += 1
                table = sheet.cell(row, 0).value
                table1 = sheet.cell(row, 1).value
                schema = sheet.cell(row, 2).value
                index = sheet.cell(row, 3).value
                colb_num = 0

                if index == 42:
                    print("%s no pk" % table)
                    continue
                else:
                    print("%s 正在处理：" % table)
                    # replace列逻辑
                    columns1 = ''
                    columns2 = ''
                    columns3 = ''
                    sql = "SELECT COLUMN_NAME,DATA_TYPE FROM dba_tab_columns WHERE OWNER = '%s' AND TABLE_NAME='%s'" % (
                    schema, table)
                    cursor1.execute(sql)
                    column_data_ = cursor1.fetchall()
                    length = len(column_data_) - 1
                    if len(column_data_) == 0:
                        print("not found colnum")
                        continue
                    else:
                        for data in column_data_:
                            if data[0] == column_data_[length][0]:
                                if data[1] == 'DATE':
                                    columns1 = columns1 + data[0]
                                    columns2 = columns2 + data[0]
                                    columns3 = columns3 + data[0]
                                elif data[1] == "CLOB":
                                    colb_num += 1
                                    pass
                                elif 'TIMESTAMP' in data[1]:
                                    columns1 = columns1 + data_col5_ % (data[0], data[0])
                                    columns2 = columns2 + data[0]
                                    columns3 = columns3 + data[0]
                                elif data[1] == 'NUMBER':
                                    columns1 = columns1 + data_col4_ % (data[0], data[0],
                                                                        data[0])
                                    columns2 = columns2 + data[0]
                                    columns3 = columns3 + data[0]
                                else:
                                    columns1 = columns1 + data_col1_ % (data[0], data[0],
                                                                        data[0])
                                    columns2 = columns2 + data_col2_ % (data[0], data[0],
                                                                        data[0], data[0])
                                    columns3 = columns3 + data_col3_ % (data[0], data[0])
                            else:
                                if data[1] == 'DATE':
                                    columns1 = columns1 + data[0] + ",\n\t\t\t"
                                    columns2 = columns2 + data[0] + ",\n\t\t"
                                    columns3 = columns3 + data[0] + ",\n\t"
                                elif data[1] == "CLOB" or data[0] == 'MOPER' and table == 'CFL_BANK_CITY_MP':
                                    colb_num += 1
                                    pass
                                elif 'TIMESTAMP' in data[1]:
                                    columns1 = columns1 + data_col5_ % (data[0], data[0]) + ",\n\t\t\t"
                                    columns2 = columns2 + data[0] + ",\n\t"
                                    columns3 = columns3 + data[0] + ",\n\t"
                                elif data[1] == 'NUMBER':
                                    columns1 = columns1 + data_col4_ % (data[0], data[0],
                                                                        data[0]) + ",\n\t\t\t"
                                    columns2 = columns2 + data[0] + ",\n\t\t"
                                    columns3 = columns3 + data[0] + ",\n\t"
                                else:
                                    columns1 = columns1 + data_col1_ % (data[0], data[0],
                                                                        data[0]) + ",\n\t\t\t"
                                    columns2 = columns2 + data_col2_ % (
                                        data[0], data[0], data[0], data[0]) + ",\n\t\t"
                                    columns3 = columns3 + data_col3_ % (data[0],
                                                                        data[0]) + ",\n\t"
                        end_sql1 = data_minus_ % (columns3, columns2, table, columns1,
                                                  schema, table, index)
                        end_sql2 = data_minus_ % (columns3, columns2, table1, columns1,
                                                  schema, table1, index)
                        # print(end_sql1,end_sql2)
                        # break
                        c1 = cursor1.execute(end_sql1)
                        c2 = cursor2.execute(end_sql2)
                        flag = True
                        while True:
                            data1 = c1.fetchmany(1000)
                            data2 = c2.fetchmany(1000)
                            if data1 and flag:
                                for i in range(len(data1)):
                                    for j in range(length + 1 - colb_num):
                                        j = j + 1
                                        if data1[i][j] == data2[i][j]:
                                            continue
                                        else:
                                            print(data1[i])
                                            print(data2[i])
                                            print(end_sql1, end_sql2)
                                            flag = False
                                            break
                                    if not flag:
                                        break
                            elif not flag:
                                break
                            else:
                                print('nice')
                                success_num += 1
                                break
        except Exception as e:
            print(end_sql1, end_sql2)
            print(e)
        finally:
            print("总数：%s 成功数：%s" % (all_num, success_num))
            cursor1.close()
            cursor2.close()



if __name__ == '__main__':
    cursor1 = util.oracleconn("DMT_ADMIN/dmt_admin@10.20.201.101:1521/DDMPRTDB")
    cursor2 = util.oracleconn("DMT_ADMIN/dmt_admin@10.20.201.101:1521/DDMPRTDB")
    # cursor3 = util.oracleconn("DMT_ADMIN/dmt_admin@10.20.201.101:1521/DDMPRTDB")
    # cursor3 = dbutil.mysqlconn("10.20.202.184", "mysql", "2wsx*IK<", "cbb")
    # minusutil.minus_column(cursor_1= cursor1, cursor_2= cursor2)
    # minusutil.minus_count(cursor_1=cursor1, cursor_2=cursor2)
    minusutil.minus_data(cursor_1=cursor1, cursor_2=cursor2)
