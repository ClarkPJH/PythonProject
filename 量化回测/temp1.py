# coding :utf-8
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#####     一个量化回测框架至少包含那几部分：
'''
1、  数据   
2、账户（股票账户、期货账户，账户中：资金，持仓，转账）  
3、交易过程(回测过程)、及交易结果   -------   交易逻辑，交易结果输出-------文字输出、图表数据

'''


class Account:
    """
        账户类：存放股票、期货等证券账户信息；以及银证转账操作（资金转入转出）
    """

    def __init__(self):
        self.account_1 = {'name': 'stock_1', 'password': '123456', 'capital': 1000000, 'position': {},
                          'gjcapital': 1000000}
        self.account_2 = {'name': 'future_1', 'password': '123456', 'capital': 1000000, 'position': {}}
        self.bank_1 = {'name': 'bank1', 'password': 123456, 'capital': 1000000}

    def bank2security(self, account, bank, amount):
        ''' 银转证 '''
        if bank['capital'] >= amount:
            account['capital'] += amount
            bank['capital'] -= amount
        else:
            print('银行卡资金不足,请重新设置金额！')

    def security2bank(self, account, bank, amount):
        if account['gjcapital'] >= amount:
            account['capital'] -= amount
            account['gjcapital'] -= amount
            bank['capital'] += amount
        else:
            print('可转出资金不足,请重新设置！')


class trade(Account):
    ''' 交易类 '''

    def __init__(self):
        '''
        初始化函数中，先初始化父类的初始化变量
        声明回测的证券列表、回测时间
        '''
        super(trade, self).__init__()
        # code_df = pd.read_table(r'C:\Users\PC\Desktop\1.txt',converters={'代码':str})
        # code_list = list(code_df.iloc[:,0][:-5].values)
        # print(code_list)
        code_list = ['600519', '000001']
        self.security_list = code_list  ####  回测的股票列表    以这两个为例
        self.start_date = '2021-11-02'
        self.end_date = '2022-06-24'
        self.short = 10
        self.long = 30
        # self.handle_data()
        self.plot_curve()

    def handle_data(self):  ####    交易函数
        '''
        在这里编写交易策略，并调用数据进行回测-----
        先编写一个简单的例子：双均线策略
        '''
        ###   双均线策略，首先需要计算一些，均线数据。比如  5日、20日均线吧。
        ###   首先定义一个，存放数据的字典.把每只票的数据都存放进去，方便后面回测使用。
        data_dict = {}
        ###   使用for循环遍历每一只票，把所有数据都存进data
        for i in self.security_list:
            df = ts.get_hist_data(i, self.start_date, self.end_date)  ####   获取   时间段内的日线数据
            ###  由于我们使用的是收盘价回测，所以只取收盘价。并且排序一下。tushare默认是倒序
            close = df.close.sort_index(ascending=True)
            ###  然后计算均线数据   可以使用talib库，也可以直接计算
            ma5 = close.rolling(self.short).mean()  ###   使用rolling函数，5为时间窗口，滚动计算5日均线。
            ma20 = close.rolling(self.long).mean().dropna()  ###   由于计算的均线数据，前n个数据会计算为一个，所以有（n-1)个数据缺失。
            ###  两个均线取相同长度.而且必须是取长均线的长度
            len_ = len(ma20)
            ma5 = ma5[-len_:]
            ###  现在我们获取了，收盘价、5日均线、10日均线数据。可以传入  data_dict字典了
            data_dict[i] = (close, ma5, ma20)

        ###   处理完上面的数据之后，我们就可以进行，回测了
        ###   回测 ：  就是对我们设置的 回测日期的每一天 每只股票  进行判断  符合策略的买入卖出

        ###   把我们的回测日期，单独作为一个列表，用来循环遍历。我们在这里解直接取data_dict中收盘价的索引作为，日期列表
        date_list = data_dict[self.security_list[0]][0].index
        # return date_list

        ###   回测过程：
        ###   定义一个账户资金记录 Series 和成交记录 方便最后绘制收益曲线、查看成交记录
        account_df = pd.Series()
        log_list = []
        for i in range(1, len(date_list)):
            date1 = date_list[i - 1]
            date2 = date_list[i]
            for code in self.security_list:
                data = data_dict[code]  ###  取出该股票的 数据
                if date1 not in data[1].index:
                    pass
                else:
                    close = data[0]
                    ma5 = data[1]
                    ma20 = data[2]
                    if code not in self.account_1['position'].keys():
                        if ma5.loc[date1] < ma20.loc[date1] and ma5.loc[date2] > ma20.loc[
                            date2]:  ###  金叉买入    假设每次买入   10000股
                            ###   首先判断账户资金，够不够买10000股，不够的话，调整为 可买入的最大股数
                            ###   手续费假设为1手5元
                            need_capital = 10000 * close.loc[date2] + 100 * 5

                            ###   假设使用账户一
                            if self.account_1['capital'] >= need_capital:
                                self.account_1['capital'] -= need_capital
                                self.account_1['position'][code] = [close.loc[date2], 10000]
                                log_list.append([date2, code, 'B', close.loc[date2], 10000])
                            elif self.account_1['capital'] < need_capital:  ###  资金不够 买10000股，需要调整
                                if self.account_1['capital'] >= 100 * close.loc[date2] + 5:  ####   至少得够买一手的钱吧，不够的话就买不了
                                    ###  判断 账户资金  能买几手
                                    num = self.account_1['capital'] // (100 * close.loc[date2] + 5)  ###   整除取整
                                    need_capital = num * 100 * close.loc[date2] + num * 5
                                    self.account_1['capital'] -= need_capital
                                    self.account_1['position'][code] = [close.loc[date2], 100 * num]
                                    log_list.append([date2, code, 'B', close.loc[date2], 100 * num])
                                else:
                                    print('可用资金不足，请查看账户余额！')

                    else:
                        if ma5.loc[date1] > ma20.loc[date1] and ma5.loc[date2] < ma20.loc[date2]:
                            hold_num = self.account_1['position'][code][1]
                            self.account_1['capital'] += close.loc[date2] * hold_num - hold_num // 100 * 5
                            del self.account_1['position'][code]
                            log_list.append([date2, code, 'S', close.loc[date2], hold_num])

            account_df[date2] = self.account_1['capital']
            for k in self.account_1['position'].keys():
                close = data_dict[k][0].loc[date2]
                hold_num = self.account_1['position'][k][1]
                account_df[date2] += close * hold_num
        trade_log = pd.DataFrame(columns=['date', 'code', 'BS', 'price', 'num'], data=log_list)
        return (account_df, trade_log)

    def plot_curve(self):
        account_assets = self.handle_data()[0]
        ret_all = (account_assets - account_assets[0]) / account_assets[0]
        account_assets_shift = account_assets.shift(1)
        account_assets_shift[0] = account_assets[0]
        ret_day = account_assets / account_assets_shift - 1
        # print(ret_day)
        fig, (ax0, ax1) = plt.subplots(2, 1)
        ax0.plot(ret_all.index, ret_all, 'r', alpha=1)
        ax0.plot([0] * len(ret_all), c='k', alpha=0.5)
        ax0.set_title(label='收益曲线', size=9)
        ax0.xaxis.set_major_locator(ticker.MultipleLocator(base=len(ret_all) // 8))  #
        ax0.grid(color='k', linestyle='--', linewidth=0.5, alpha=0.4)
        ax1.bar(ret_day.index, ret_day, color=['r' if ret_day[x] >= 0 else 'g' for x in range(0, len(ret_day))])
        ax1.plot([0] * len(ret_day), c='y', alpha=0.2)
        ax1.set_title(label='每日收益', size=9)
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(base=len(ret_day) // 8))  #
        ax1.grid(color='k', linestyle='--', linewidth=0.5, alpha=0.4)
        plt.show()


a = trade()
