# coding: utf-8
import datetime
import csv
from akshare import stock_zh_a_hist_min_em as get_min_dt
import tushare as ts
from .config import *
from .libs import *


# 5分钟k线，双均线策略
def two_avg_k(main_code, is_up):
    path = f'Data/{main_code}.csv'

    # 如果从未保存过当前股票数据则保存数据
    if not os.path.exists(path):
        L.log('TIPS', f'{main_code} -- 首次保存5分钟k线: {path}')
        get_data_to_csv(main_code, period=5)

    # 获取上一天开盘到当前时间的5分钟k线数据，更新到path
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if localtime[-4] in ['0', '5'] and '20' < localtime[-2:] < '40' and is_up == 1:
        L.log('TIPS', f'{main_code} -- 更新5分钟k线')
        get_data_to_csv(main_code, period=5)
        is_up = 0
        time.sleep(5)

    # 获取path保存的本地数据
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        amount_list = [row[3] for row in reader]
        file.close()

    # 获取当前代码的实时价格
    price = get_price(main_code)
    # 如果实时数据获取失败则使用文件中最新的5分钟k线数据
    if not price:
        price = float(amount_list[-1])
        L.log('WARN', f'{main_code} -- 将使用本地最新保存的k线数据作为实时数据 Price: {price}')

    # 通过最新4组和9组5分钟收盘价以及实时价格计算实时MA5和实时MA10
    df_basic_list = [float(x) for x in amount_list[-4:]]
    df_refer_list = [float(x) for x in amount_list[-9:]]
    df_basic_list.append(price), df_refer_list.append(price)
    basic_v = round(sum(df_basic_list) / len(df_basic_list), 2)
    refer_v = round(sum(df_refer_list) / len(df_refer_list), 2)

    return price, basic_v, refer_v, is_up
