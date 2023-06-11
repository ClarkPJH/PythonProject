# coding: utf-8
from .config import *
from akshare import stock_zh_a_hist_min_em as get_min_dt
import tushare as ts
import datetime


def initBS(strategy, main_code):
    basic_v, refer_v = strategy[1], strategy[2]

    L.log('INFO', f'{main_code} -- 初始化BS')
    if basic_v >= refer_v:
        BS = 0
        L.log('TIPS', f'{main_code} -- 下次将触发SELL操作')
    else:
        BS = 1
        L.log('TIPS', f'{main_code} -- 下次将触发BUY操作')
    L.log('INFO', f'{main_code} -- BS：{BS}')
    return BS


def get_data_to_csv(main_code, period):
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    before_date = datetime.date.today() + datetime.timedelta(days=-20)
    try:
        df = get_min_dt(symbol=main_code, period=str(period), start_date=f"{before_date} 09:30:00", end_date=localtime)
        df.to_csv(f'Data/{main_code}.csv')
    except Exception as e:
        L.log('ERROR', e)
        L.log('ERROR', f'{main_code} -- 获取k线数据失败')


def get_price(main_code):
    try:
        price = float(ts.get_realtime_quotes(str(main_code)).iloc[0, 3])
        return price
    except Exception as e:
        L.log('ERROR', e)
