import numpy as np

def bullish_engulfing(
    data,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="Low",
):

    """
    상승 장악형이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가 나타내는 컬럼명

    returns:
    ==========================
    cond: ndarray
        상승 장악형이 발생한 시점이 True인 부울 배열
    """

    cond_1 = (data[open_col] > data[close_col]).values[:-1]
    cond_2 = (data[open_col] < data[close_col]).values[1:]
    cond_3 = data[low_col].values[:-1] > data[open_col].values[1:]
    cond_4 = data[high_col].values[:-1] < data[close_col].values[1:]

    cond = cond_1 & cond_2 & cond_3 & cond_4
    cond = np.insert(cond, 0, False)
    return cond


def bearish_engulfing(
    data,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="Low",
):

    """
    하락 장악형이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가 나타내는 컬럼명

    returns:
    ==========================
    cond: ndarray
        하락장악형이 발생한 시점이 True인 부울 배열
    """

    cond_1 = (data[open_col] < data[close_col]).values[:-1]
    cond_2 = (data[open_col] > data[close_col]).values[1:]
    cond_3 = data[low_col].values[:-1] < data[open_col].values[1:]
    cond_4 = data[high_col].values[:-1] > data[close_col].values[1:]

    cond = cond_1 & cond_2 & cond_3 & cond_4
    cond = np.insert(cond, 0, False)
    return cond


def three_black_crows(
    data,
    open_col="Open",
    close_col="Close",
):
    """
    흑삼병이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명

    returns:
    ==========================
    cond: ndarray
        흑삼병이 발생한 시점이 True인 부울 배열
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
    return cond


def three_white_soldiers(
    data,
    open_col="Open",
    close_col="Close",
):
    """
    적삼병이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명

    returns:
    ==========================
    cond: ndarray
        적삼병이 발생한 시점이 True인 부울 배열
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

    return cond


def hammer(
    data,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="low",
    min_len_tail=0,
    min_len_body=0,
    max_len_tail=30,
    max_len_body=30):

    """
    망치형이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가를 나타내는 컬럼명
    min_len_tail: float, default: 0
        최소 꼬리 길이
    min_len_body: float, default: 0
        최소 몸통 길이
    max_len_tail: float, default: 30
        최대 꼬리 길이
    max_len_body: float, default: 30
        최대 몸통 길이

    returns:
    ==========================
    cond: ndarray
        망치형이 발생한 시점이 True인 부울 배열
    """
    open_price = data[open_col].values
    close_price = data[close_col].values
    high_price = data[high_col].values
    low_price = data[low_col].values

    tail_len = (open_price - low_price) / low_price * 100
    body_len = (close_price - open_price) / open_price * 100

    cond = (high_price == close_price) & (close_price > open_price)
    cond = cond & (tail_len >= min_len_tail) & (tail_len <= max_len_tail) & (body_len >= min_len_body) & (body_len <= max_len_body)

    return cond


def inverted_hammer(
    data,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="low",
    min_len_tail=0,
    min_len_body=0,
    max_len_tail=30,
    max_len_body=30):

    """
    역망치형이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가를 나타내는 컬럼명
    min_len_tail: float, default: 0
        최소 꼬리 길이
    min_len_body: float, default: 0
        최소 몸통 길이
    max_len_tail: float, default: 30
        최대 꼬리 길이
    max_len_body: float, default: 30
        최대 몸통 길이

    returns:
    ==========================
    cond: ndarray
        망치형이 발생한 시점이 True인 부울 배열
    """

    open_price = data[open_col].values
    close_price = data[close_col].values
    high_price = data[high_col].values
    low_price = data[low_col].values

    tail_len = (high_price - close_price) / close_price * 100
    body_len = (close_price - open_price) / open_price * 100

    cond = (low_price == open_price) & (close_price > open_price)
    cond = cond & (tail_len >= min_len_tail) & (tail_len <= max_len_tail) & (body_len >= min_len_body) & (body_len <= max_len_body)

    return cond



def dragon_fly_doji(
    data,
    open_col="Open",
    close_col="Close",
    high_col="High",
    low_col="low",
    min_len_tail=0,
    max_len_tail=30):

    """
    잠자리형이 발생한 시점을 반환

    Parameters:
    ==========================
    data: DataFrame
        주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    open_col: str, default: "Open"
        시가를 나타내는 컬럼명
    close_col: str, default: "Close"
        종가를 나타내는 컬럼명
    high_col: str, default: "High"
        고가를 나타내는 컬럼명
    low_col: str, default: "Low"
        저가를 나타내는 컬럼명
    min_len_tail: float, default: 0
        최소 꼬리 길이
    max_len_tail: float, default: 30
        최대 꼬리 길이

    returns:
    ==========================
    cond: ndarray
        잠자리형이 발생한 시점이 True인 부울 배열
    """
    open_price = data[open_col].values
    close_price = data[close_col].values
    high_price = data[high_col].values
    low_price = data[low_col].values

    tail_len = (open_price - low_price) / low_price * 100

    cond = (high_price == close_price) & (high_price == open_price)
    cond = cond & (tail_len >= min_len_tail) & (tail_len <= max_len_tail)

    return cond
