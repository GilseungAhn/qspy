import numpy as np

def ror_using_buy_and_hold(data,
                            period,
                            buy_arr,
                            buy_col = "Close",
                            sell_col = "Close",
                            fee_rate = 0.015,
                            tax_rate = 0.3):

    '''
    특정 패턴 발생 후 특정 기간 동안 해당 주식을 보유했다 매도할 때의 수익률 계산

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
        raise ValueError("패턴 배열과 data의 길이가 일치하지 않습니다: {}, {}".format(len(patt_arr), len(data)))
    if set(buy_arr).union(set([True, False])) != set([True, False]):
        raise ValueError("patt_arr이 부울 배열이 아닙니다.")
    if fee_rate > 100 or fee_rate < 0:
        raise ValueError("fee_rate는 0과 100사이어야 합니다.")

    patt_arr = np.array(buy_arr)
    patt_idx_list = data.loc[patt_arr].index
    max_idx = max(data.index)

    patt_bidx_list = patt_idx_list[patt_idx_list + period < max_idx] + 1
    patt_sidx_list = patt_bidx_list + period

    # 패턴 발생 후 수익률 계산
    patt_bp_list = data.loc[patt_bidx_list, buy_col].values
    patt_sp_list = data.loc[patt_sidx_list, sell_col].values

    buy_fee = patt_bp_list * fee_rate / 100
    sell_fee = patt_sp_list * fee_rate / 100
    sell_tax = patt_sp_list * tax_rate / 100

    patt_ror_list = (patt_sp_list - patt_bp_list - buy_fee - sell_fee - sell_tax) / patt_bp_list
    return patt_ror_list.tolist()