# coding: utf-8
from _Lib import *


def trader(main_code, trans_count, b_dv, s_dv):
    today = datetime.date.today()
    print(f' Tips: {main_code} 程序正在运行, 请勿中止进程! 如需了解详情请查看TransLogs/实时日志文件.')

    # 初始化下次买卖
    BS = initBS(two_avg_k(main_code, 1), main_code)
    is_set = is_up = 1

    # 在指定时间到之前循环运行
    while time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) < f'{today} 14:59:00':
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # 盘中交易时间进行数据实时监控及交易操作
        if not f'{today} 11:30:00' < localtime < f'{today} 12:59:00':

            """--循环获取实时价格及进行买卖点的参照数据--------------"""
            price, basic_v, refer_v, is_up = two_avg_k(main_code, is_up)
            # print(f'{localtime} : {main_code} -- {price}')
            # 每10次记录一次日志
            if is_set == 10:
                is_set = 0
                dv = round(basic_v - refer_v, 2)
                L.log('INFO', f'{main_code} -- Price:{price} | Basic:{basic_v} | Refer:{refer_v} | Dv:{dv}')
            # 每进行一次k线数据保存，分钟非0/5时初始化请求开关
            if localtime[-4] not in ['0', '5']:
                is_up = 1

            """--设置交易发生的条件-------------------------------"""
            # if basic_v > refer_v and BS == 1:
            if price > basic_v + b_dv and BS == 1:
                TD.mk_trans('B', main_code, trans_count)
                BS = 0
                L.log(' BUY', f'{main_code} -- B 卖一价{price}买入{trans_count}股')
                L.log('TIPS', '下次将触发SELL操作')
            # elif basic_v < refer_v and BS == 0:
            elif price < basic_v - s_dv and BS == 0:
                TD.mk_trans('S', main_code, trans_count)
                BS = 1
                L.log('SELL', f'{main_code} -- S 买一价{price}卖出{trans_count}股')
                L.log('TIPS', '下次将触发BUY操作')

            is_set += 1
            time.sleep(3)

        # 非盘中交易时间进行轮巡休息
        else:
            time.sleep(30)
    os.system('shutdown -s -t 120')


if __name__ == '__main__':
    L.mik_log()
    TD = Treader()

    multiprocessing.Process(target=trader, args=('600115', 500, 0.01, 0.01)).start()  # 中国东航
    time.sleep(2)
    # multiprocessing.Process(target=trader, args=('002603', 100, 0.03, 0.01)).start()  # 以岭药业
    time.sleep(2)
    multiprocessing.Process(target=trader, args=('002349', 300, 0.02, 0.01)).start()  # 精华制药
    # time.sleep(2)
    # multiprocessing.Process(target=trader, args=('002251', 100, 0.01, 0.01)).start()  # 步步高
    # time.sleep(2)
    # multiprocessing.Process(target=trader, args=('000983', 100, 0.02, 0.01)).start()  # 山西焦煤

    # TD.mk_trans('B', 600115, 100)
    # sleep(2)
    # TD.mk_trans('S', 600115, 100)
