import numpy as np

def ror_buy_and_hold(data,
                    period,
                    buy_arr,
                    buy_col = "Close",
                    sell_col = "Close",
                    fee_rate = 0.015,
                    tax_rate = 0.3):

    '''
    매수 시점을 입력받아 특정 기간만큼 보유한 뒤 매도했을 때의 수익률을 계산

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    period: int
        보유 기간 (영업일)
    buy_arr: array-like
        매수 시점을 나타내는 부울 배열 (True: 매수, False: 매수 X)
    buy_col: str, default: "Close"
        패턴 발생 다음 날 매수 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    sell_col: str, default: "Close"
        보유 기간 이후 매도 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    fee_rate: float, default: 0.15
        매매 수수료 (%)
    tax_rate: float, default: 0.3
        세금 (%)
    '''

    if len(buy_arr) != len(data):
        raise ValueError("buy_arr과 data의 길이가 일치하지 않습니다: {}, {}".format(len(buy_arr), len(data)))
    if set(buy_arr).union(set([True, False])) != set([True, False]):
        raise ValueError("buy_arr이 부울 배열이 아닙니다.")
    if fee_rate > 100 or fee_rate < 0:
        raise ValueError("fee_rate는 0과 100사이어야 합니다.")

    data = data.reset_index(drop = True)
    buy_arr = np.array(buy_arr)
    buy_idx_list = data.loc[buy_arr].index
    max_idx = max(data.index)

    buy_idx_list = buy_idx_list[buy_idx_list + period < max_idx]
    sell_idx_list = buy_idx_list + period

    # 수익률 계산
    buy_price_list = data.loc[buy_idx_list, buy_col].values
    sell_price_list = data.loc[sell_idx_list, sell_col].values

    buy_fee = buy_price_list * fee_rate / 100
    sell_fee = sell_price_list * fee_rate / 100
    sell_tax = sell_price_list * tax_rate / 100

    ror_list = (sell_price_list - buy_price_list - buy_fee - sell_fee - sell_tax) / buy_price_list
    ror_list = ror_list.tolist()
    return ror_list


def ror_buy_and_sell(data,
                    buy_arr,
                    sell_arr,
                    buy_col = "Close",
                    sell_col = "Close",
                    fee_rate = 0.015,
                    tax_rate = 0.3):

    '''
    매수 시점 목록과 매도 시점 목록을 입력받아, 각 매수 시점에서 매수해서 가장 가까운 매도 시점에 매도했을 때의 수익률을 계산하여 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    buy_arr: array-like
        매수 시점을 나타내는 부울 배열 (True: 매수, False: 매수 X)
    sell_arr: array-like
        매도 시점을 나타내는 부울 배열 (True: 매도, False: 매도 X)
    buy_col: str, default: "Close"
        패턴 발생 다음 날 매수 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    sell_col: str, default: "Close"
        보유 기간 이후 매도 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    fee_rate: float, default: 0.15
        매매 수수료 (%)
    tax_rate: float, default: 0.3
        세금 (%)
    '''

    if len(buy_arr) != len(data):
        raise ValueError("buy_arr과 data의 길이가 일치하지 않습니다: {}, {}".format(len(buy_arr), len(data)))
    if len(sell_arr) != len(data):
        raise ValueError("sell_arr과 data의 길이가 일치하지 않습니다: {}, {}".format(len(sell_arr), len(data)))
    if set(buy_arr).union(set([True, False])) != set([True, False]):
        raise ValueError("buy_arr이 부울 배열이 아닙니다.")
    if set(sell_arr).union(set([True, False])) != set([True, False]):
        raise ValueError("sell_arr이 부울 배열이 아닙니다.")
    if fee_rate > 100 or fee_rate < 0:
        raise ValueError("fee_rate는 0과 100사이어야 합니다.")

    buy_arr = np.array(buy_arr)
    sell_arr = np.array(sell_arr)

    buy_idx_list = data.loc[buy_arr].index.sort_values()
    sell_idx_list = data.loc[sell_arr].index.sort_values()

    # 수익률 계산
    ror_list = []
    for buy_idx in buy_idx_list:
        if sum(sell_idx_list > buy_idx) == 0:
            break
        else:
            if buy_col == "Open" and sell_col == "Close":
                sell_idx = sell_idx_list[sell_idx_list >= buy_idx][0]
            else:
                sell_idx = sell_idx_list[sell_idx_list > buy_idx][0]
            buy_price = data.loc[buy_idx, buy_col]
            sell_price = data.loc[sell_idx, sell_col]
            buy_fee = buy_price * fee_rate / 100
            sell_fee = sell_price * fee_rate / 100
            sell_tax = sell_price * tax_rate / 100
            ror = (sell_price - buy_price - buy_fee - sell_fee - sell_tax) / buy_price
            ror_list.append(ror)

    return ror_list