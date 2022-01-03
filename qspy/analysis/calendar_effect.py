import numpy as np

def week_effect(data, buy_weekday = 0, sell_weekday = 4, date_col = "Date"):
    """
    요일에 따른 매수 시점 배열과 매도 시점 배열을 반환

    Parameters:
    ==========================
    data: DataFrame
     주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    buy_weekday: int, default: 0
     매수 요일 (0: 월요일, 1: 화요일, 2: 수요일, 3: 목요일, 4: 금요일)
    sell_weekday: int, default: 4
     매도 요일 (0: 월요일, 1: 화요일, 2: 수요일, 3: 목요일, 4: 금요일)
    date_col: str, default: Date
     data에서 날짜를 나타내는 컬럼명

    returns:
    ==========================
    (buy_arr, sell_arr): ndarray
     매수 시점 배열과 매도 시점 배열로 구성된 튜플
    """

    if buy_weekday not in [0, 1, 2, 3, 4]:
        raise ValueError("buy_weekday는 0, 1, 2, 3, 4 중 하나이어야 합니다")
    if sell_weekday not in [0, 1, 2, 3, 4]:
        raise ValueError("sell_weekday 0, 1, 2, 3, 4 중 하나이어야 합니다")

    buy_arr = (data[date_col].dt.weekday == buy_weekday).values
    sell_arr = (data[date_col].dt.weekday == sell_weekday).values

    return buy_arr, sell_arr


def month_effect(data, buy_day = "end", sell_day = "start", date_col = "Date"):
    """
    월중 시기에 따른 매수 시점 배열과 매도 시점 배열을 반환

    Parameters:
    ==========================
    data: DataFrame
     주가 데이터 (FinanceDataReader나 이 패키지를 통해 수집한 데이터 구조와 일치해야 함)
    buy_day: 특정 월의 매수 시기, default: "last"
     매수 시기 ("start": 월초, "mid": 월중, "end": 월말)
    sell_day: 특정 월의 매수 시기, default: "start"
     매도 시기 ("start": 월초, "mid": 월중, "end": 월말)

    returns:
    ==========================
    (buy_arr, sell_arr): ndarray
     매수 시점 배열과 매도 시점 배열로 구성된 튜플
    """

    if buy_day not in ["start", "mid", "end"]:
        raise ValueError('buy_day는 "start", "mid", "end"중 하나이어야 합니다')
    if sell_day not in ["start", "mid", "end"]:
        raise ValueError('sell_day는 "start", "mid", "end"중 하나이어야 합니다')
    if buy_day == sell_day:
        raise ValueError("buy_day와 sell_day가 같을 수 없습니다.")

    # 임시 데이터 생성: Year와 Month 컬럼 추가
    temp = data.copy()
    temp['Year'] = data[date_col].dt.year
    temp['Month'] = data[date_col].dt.month
    temp["Day"] = data[date_col].dt.day

    # 출력 초기화
    buy_arr = np.zeros(len(temp), dtype=bool)
    sell_arr = np.zeros(len(temp), dtype=bool)

    # year와 month를 순회하면서 매수/매도 시점 파악 및 출력 업데이트

    for year, month in temp[["Year", "Month"]].drop_duplicates().values:
        # 월별 매수/매도 시점 파악
        s_temp = temp.loc[(temp["Year"] == year) & (temp["Month"] == month)]
        if (buy_day == "start") and (s_temp["Day"].min() < 10):
            buy_idx = s_temp["Day"].idxmin()
            buy_arr[buy_idx] = True
        elif (buy_day == "mid") and (sum((s_temp["Day"] >= 10) & (s_temp["Day"] < 20)) >= 1):
            buy_idx = (s_temp["Day"] - 15).abs().idxmin()
            buy_arr[buy_idx] = True
        elif (buy_day == "end")  and (s_temp["Day"].max() >= 20):
            buy_idx = s_temp["Day"].idxmax()
            buy_arr[buy_idx] = True

        if (sell_day == "start") and (s_temp["Day"].min() < 10):
            sell_idx = s_temp["Day"].idxmin()
            sell_arr[sell_idx] = True
        elif (sell_day == "mid") and (sum((s_temp["Day"] >= 10) & (s_temp["Day"] < 20)) >= 1):
            sell_idx = (s_temp["Day"] - 15).abs().idxmin()
            sell_arr[sell_idx] = True
        elif (sell_day == "end")  and (s_temp["Day"].max() >= 20):
            sell_idx = s_temp["Day"].idxmax()
            sell_arr[sell_idx] = True

    return buy_arr, sell_arr