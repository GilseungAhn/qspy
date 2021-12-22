import numpy as np
from .strategy import _ror_using_buy_and_hold


def bullish_engulfing(
    data,
    period,
    buy_col="Close",
    sell_col="Close",
    fee_rate=0.015,
    tax_rate=0.3,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="Low",
):

    """
    상승 장악형이 발생한 시점을 반환하는 함수

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    period: int
        보유 기간 (영업일)
    buy_arr: array-like
        매수 시점을 나타내는 부울 배열 (True: 매수, False: 매도)
    buy_col: str, default: "Close"
        패턴 발생 다음 날 매수 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    sell_col: str, default: "Close"
        보유 기간 이후 매도 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    fee_rate: float, default: 0.15
        매매 수수료 (%)
    tax_rate: float, default: 0.3
        세금 (%)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가 나타내는 컬럼명
    """

    cond_1 = (data[open_col] > data[close_col]).values[:-1]
    cond_2 = (data[open_col] < data[close_col]).values[1:]
    cond_3 = data[low_col].values[:-1] > data[open_col].values[1:]
    cond_4 = data[high_col].values[:-1] < data[close_col].values[1:]

    cond = cond_1 & cond_2 & cond_3 & cond_4
    cond = np.insert(cond, 0, False)

    ror_list = _ror_using_buy_and_hold(
        data, period, cond, buy_col, sell_col, fee_rate, tax_rate
    )
    return ror_list


def bearish_engulfing(
    data,
    period,
    buy_col="Close",
    sell_col="Close",
    fee_rate=0.015,
    tax_rate=0.3,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="Low",
):

    """
    하락 장악형이 발생한 시점을 반환하는 함수

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    period: int
        보유 기간 (영업일)
    buy_arr: array-like
        매수 시점을 나타내는 부울 배열 (True: 매수, False: 매도)
    buy_col: str, default: "Close"
        패턴 발생 다음 날 매수 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    sell_col: str, default: "Close"
        보유 기간 이후 매도 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    fee_rate: float, default: 0.15
        매매 수수료 (%)
    tax_rate: float, default: 0.3
        세금 (%)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가 나타내는 컬럼명
    """

    cond_1 = (data[open_col] < data[close_col]).values[:-1]
    cond_2 = (data[open_col] > data[close_col]).values[1:]
    cond_3 = data[low_col].values[:-1] < data[open_col].values[1:]
    cond_4 = data[high_col].values[:-1] > data[close_col].values[1:]

    cond = cond_1 & cond_2 & cond_3 & cond_4
    cond = np.insert(cond, 0, False)

    ror_list = _ror_using_buy_and_hold(
        data, period, cond, buy_col, sell_col, fee_rate, tax_rate
    )
    return ror_list


def three_black_crows(
    data,
    period,
    buy_col="Close",
    sell_col="Close",
    fee_rate=0.015,
    tax_rate=0.3,
    open_col="Open",
    close_col="Close",
):
    """
    흑삼병이 발생한 시점을 반환하는 함수

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    period: int
        보유 기간 (영업일)
    buy_arr: array-like
        매수 시점을 나타내는 부울 배열 (True: 매수, False: 매도)
    buy_col: str, default: "Close"
        패턴 발생 다음 날 매수 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    sell_col: str, default: "Close"
        보유 기간 이후 매도 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    fee_rate: float, default: 0.15
        매매 수수료 (%)
    tax_rate: float, default: 0.3
        세금 (%)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가 나타내는 컬럼명
    """
    cur_price = data[close_col].values[2:]
    pre_price = data[close_col].values[1:-1]
    sec_pre_price = data[close_col].values[:-2]

    cond_1 = (cur_price < pre_price) & (pre_price < sec_pre_price)
    cond_2 = (data[open_col] > data[close_col]).values[:-2]
    cond_3 = (data[open_col] > data[close_col]).values[1:-1]
    cond_4 = (data[open_col] > data[close_col]).values[2:]

    cond = cond_1 & cond_2 & cond_3 & cond_4
    cond = np.insert(cond, [0, 0], False)

    ror_list = _ror_using_buy_and_hold(
        data, period, cond, buy_col, sell_col, fee_rate, tax_rate
    )
    return ror_list


def three_white_soldiers(
    data,
    period,
    buy_col="Close",
    sell_col="Close",
    fee_rate=0.015,
    tax_rate=0.3,
    open_col="Open",
    close_col="Close",
):
    """
    적삼병이 발생한 시점을 반환하는 함수

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    period: int
        보유 기간 (영업일)
    buy_arr: array-like
        매수 시점을 나타내는 부울 배열 (True: 매수, False: 매도)
    buy_col: str, default: "Close"
        패턴 발생 다음 날 매수 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    sell_col: str, default: "Close"
        보유 기간 이후 매도 기준이 되는 컬럼 ("Close": 종가, "Open": 시가)
    fee_rate: float, default: 0.15
        매매 수수료 (%)
    tax_rate: float, default: 0.3
        세금 (%)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가 나타내는 컬럼명
    """
    cur_price = data[close_col].values[2:]
    pre_price = data[close_col].values[1:-1]
    sec_pre_price = data[close_col].values[:-2]

    cond_1 = (cur_price > pre_price) & (pre_price > sec_pre_price)
    cond_2 = (data[open_col] < data[close_col]).values[:-2]
    cond_3 = (data[open_col] < data[close_col]).values[1:-1]
    cond_4 = (data[open_col] < data[close_col]).values[2:]

    cond = cond_1 & cond_2 & cond_3 & cond_4
    cond = np.insert(cond, [0, 0], False)

    ror_list = _ror_using_buy_and_hold(
        data, period, cond, buy_col, sell_col, fee_rate, tax_rate
    )
    return ror_list
