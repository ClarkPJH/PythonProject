# coding: utf-8
import datetime
import time
import akshare as ak
import csv
from Lib import *
from _Lib import *
# from _Lib.config import *


# 5分钟k线，双均线策略
def get_data(main_code, start_date, freq, basic_c, refer_c):
    path = 'Data/{}.csv'.format(main_code)
    # 获取上一天开盘到当前时间的5分钟k线数据
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    df = ak.stock_zh_a_hist_min_em(symbol=str(main_code), period=freq,
                                   start_date="{} 09:30:00".format(start_date), end_date=localtime)
    df.to_csv(path)

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        amount_list = [row[3] for row in reader]
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        time_list = [row[1] for row in reader]

    basic_list = get_MA_list(amount_list, basic_c)
    refer_list = get_MA_list(amount_list, refer_c)

    return time_list, amount_list, basic_list, refer_list


def get_MA_list(column_data, length):
    MA_list = []
    start = 1
    for i in range(0, len(column_data)-length):
        end = start + length
        close_list = [float(x) for x in column_data[start:end]]
        MA = round(sum(close_list)/len(close_list), 2)
        start += 1
        MA_list.append(MA)
    return MA_list


def back_test(main_code, trans_count, start_date, freq, basic_c, refer_c, b_dv, s_dv):
    L.mik_log()
    time_list, amount_list, basic_list, refer_list = get_data(main_code, start_date, freq, int(basic_c), int(refer_c))

    b_amt = s_amt = b_ct = s_ct = sxf = 0
    BS = 1
    for i in range(0, len(refer_list)):
        data_time = time_list[i + int(refer_c)]
        new_amt = amount_list[i + int(refer_c)]
        basic_v = basic_list[i + (int(refer_c) - int(basic_c))]
        bf_basic_v = basic_list[i + (int(refer_c) - int(basic_c)) - 1]
        refer_v = refer_list[i]
        bf_refer_v = refer_list[i - 1]

        dv = round(basic_v - refer_v, 2)
        bf_dv = round(bf_basic_v - bf_refer_v, 2)

        L.log(data_time, '{0} -- newAmt:{1} | MA5m:{2} | MA10m:{3} | DV:{4}'
              .format(main_code, new_amt, basic_v, refer_v, dv))
        # if basic_v > refer_v and abs(dv) >= float(b_dv) and BS == 1:
        # if dv-bf_dv > 0 and BS == 1:
        if float(new_amt) - basic_v >= b_dv and BS == 1:
            L.log(data_time, '{0} -- B 卖一价{1}买入{2}股'.format(main_code, new_amt, trans_count))
            BS = 0
            print(data_time + '-- {0} -- 卖一价{1}买入{2}股'.format(main_code, new_amt, trans_count))
            b_amt += float(new_amt)*trans_count
            sxf += 5
            b_ct += 1
        # elif basic_v < refer_v and abs(dv) >= float(s_dv) and BS == 0:
        # elif dv-bf_dv < 0 and BS == 0:
        elif basic_v - float(new_amt) >= s_dv and BS == 0:
            L.log(data_time, '{0} -- S 买一价{1}卖出{2}股'.format(main_code, new_amt, trans_count))
            BS = 1
            print(data_time + '-- {0} -- 买一价{1}卖出{2}股'.format(main_code, new_amt, trans_count))
            s_amt += float(new_amt) * trans_count
            s_ct += 1

    # s_amt += float(amount_list[-1]) * trans_count
    # s_ct += 1
    print('\n\n总买入次数: {0} \n总买入金额: {1} \n总卖出次数: {2} \n总卖出金额: {3} \n产生手续费: {4} \n总收益(含手术费):{5}'
          .format(b_ct, b_amt, s_ct, s_amt, sxf, s_amt-b_amt-sxf))


# back_test(main_code='002603',
#           trans_count=100,
#           start_date=20230608,
#           freq=5,
#           basic_c=5,
#           refer_c=10,
#           b_dv=0.01,
#           s_dv=0.1
#           )

