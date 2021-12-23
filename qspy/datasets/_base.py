import FinanceDataReader as fdr
import pandas as pd
import time
import os
from pkg_resources import resource_filename
import numpy as np


def load_stock_list(
    market="all", including_futures=False, return_name_and_code_only=True
):

    """
    수집 가능한 종목 목록을 반환

    Parameters:
    ==========================
    market: str, default = "all"
        반환할 종목이 속한 시장 ("all", "KOSPI", "KOSDAQ")
        - "all": 전체 종목 (코스피 + 코스닥)
        - "KOSPI": 코스피 종목
        - "KOSDAQ": 코스닥 종목

    including_futures: bool, default = False
        선물 종목을 포함할 것인지 여부
        - True: 선물 종목을 포함
        - False: 선물 종목을 미포함

    return_name_only: bool, default = True
        출력 타입 결정
        - True: 종목 이름과 코드만 반환함
        - False: 종목 정보도 같이 포함

    :return: stock_list
        조건에 맞는 종목 정보 (자료형: 데이터프레임)
    """

    if market == "all":
        stock_list = pd.concat(
            [fdr.StockListing("KOSPI"), fdr.StockListing("KOSDAQ")],
            axis=0,
            ignore_index=True,
        )
    elif market == "KOSPI":
        stock_list = fdr.StockListing("KOSPI")
    elif market == "KOSDAQ":
        stock_list = fdr.StockListing("KOSDAQ")
    else:
        raise ValueError('market의 입력 값은 ("all", "KOSPI", "KOSDAQ") 중 하나여야 합니다')
    if not (including_futures):
        stock_list.dropna(inplace=True)
    if return_name_and_code_only == "name_only":
        return stock_list[["Code", "Name"]]
    else:
        return stock_list


def load_stock_data(stock_code, start_date=None, end_date=None, download=True):

    """
    하나의 종목 코드를 입력받아, 해당 데이터를 반환

    Parameters:
    ==========================
    stock_code: str,
        수집할 종목 코드
    start_date: str, default: None
        수집 시작 날짜: YYYY-MM-DD (None으로 입력시 상장일로 설정)
    end_date: str, default: None
        수집 종료 날짜: YYYY-MM-DD (None으로 입력시 최근 개장일로 설정)
    download: bool, default: True
        수집한 데이터를 다운로드받을지 여부로, 기존 데이터가 있으면 병합됨

    :return : data, type: DataFrame
        수집한 데이터
    """

    if not ((len(stock_code) == 6) and (stock_code.isdigit())):
        raise ValueError("적절한 종목 코드가 아닙니다. 종목 코드는 6자리 숫자입니다.")
    file_path = resource_filename(
        __name__, "pickle_data/stock_price/{}.pkl".format(stock_code)
    )
    file_path = file_path.replace("\\", "/")
    folder_path = "/".join(file_path.split("/")[:-1])
    if stock_code in os.listdir(folder_path):
        data = pd.read_pickle(file_path, compression = "xz")
        data["Date"] = pd.to_datetime(data["Date"])
        if (data["Date"].min() <= pd.to_datetime(start_date)) and (
            data["Date"].max() >= pd.to_datetime(start_date)
        ):
            data = data.loc[
                (data["Date"] <= pd.to_datetime(start_date))
                & (data["Date"].max() >= pd.to_datetime(start_date))
            ]
        else:
            data = fdr.DataReader(
                stock_code, start=start_date, end=end_date
            ).reset_index()
    else:
        data = fdr.DataReader(stock_code, start=start_date, end=end_date).reset_index()
    if len(data) == 0:
        raise ValueError("관련 데이터가 없습니다")
    if download:
        if stock_code + ".pkl" not in os.listdir(folder_path):
            data.to_pickle(file_path, compression = "xz")
        else:
            old_data = pd.read_pickle(file_path, compression="xz")
            old_data["Date"] = pd.to_datetime(old_data["Date"])
            data = pd.concat([data, old_data], axis=0, ignore_index=True)
            data = data.drop_duplicates().sort_values(by="Date").reset_index(drop=True)
            change_null_idx = data.loc[data["Change"].isnull()].index
            for idx in change_null_idx:
                if idx - 1 in data.index:
                    change_value = (
                        data.loc[idx + 1, "Close"] - data.loc[idx, "Close"]
                    ) / data.loc[idx, "Close"]
                    data.loc[idx, "Change"] = change_value
            data.to_pickle(file_path, compression = "xz")
    return data


def load_stock_data_list(
    stock_code_list,
    start_date=None,
    end_date=None,
    download=True,
    sleep_time_between_load=1,
    sleep_time_connection_out=15,
):
    """
    여러 종목 데이터를 수집하여 전달

    Parameters:
    ==========================
    stock_code_list: array-like,
        수집할 종목 코드로 구성된 배열
    start_date: str, default: None
        수집 시작 날짜: YYYY-MM-DD (None으로 입력시 상장일로 설정)
    end_date: str, default: None
        수집 종료 날짜: YYYY-MM-DD (None으로 입력시 최근 개장일로 설정)
    download: bool, default: True
        수집한 데이터를 다운로드받을지 여부로, 기존 데이터가 있으면 병합됨
    sleep_time_between_load: int, default: 1
        한 데이터를 수집하고 나서 기다리는 시간(초)
    sleep_time_connection_out: int, default: 15
        연결이 끊겼을 때 기다리는 시간(분)

    :return : data_list, type: list
        수집한 데이터 목록
    """

    data_list = []
    for code in stock_code_list:
        try:
            data = load_stock_data(code, start_date, end_date, download)
            data_list.append(data)
            time.sleep(sleep_time_between_load)
        except ValueError:
            break
        except:
            time.sleep(60 * sleep_time_connection_out)
    return data_list


def _read_fs_record(file_path, account_list, consolidated, _year, _quarter, add_date):

    """
    재무 제표 데이터에서 계정명만 뽑아서 반환

    Parameters:
    ==========================
    file_path: str
        재무제표 파일이 있는 폴더 경로
    account_list: array-like,
        수집할 계정명 목록: ["유동자산", "비유동자산", "자산총계", "유동부채", "비유동부채", "부채총계",
                         "자본금", "이익잉여금", "자본총계", "매출액", "영업이익", "법인세차감전 순이익", "당기순이익"]
    consolidate: bool, default: True
        연결 재무 제표를 사용할 것인지 여부 (단, True여도 연결 재무 제표를 발표하지 않는 기업은 개별 재무 제표를 사용)
    _year: int
        수집 연도
    _quarter: int
        수집 분기
    add_date: bool, default: False
        사업 보고서가 등록된 날짜를 포함할 것인지 여부
    :return : data, type: DataFrame
        행이 기업이고 열이 [계정명+날짜]인 데이터프레임
    """
    report_name = "{}Q".format(_quarter)
    file_name = [
        file
        for file in os.listdir(file_path)
        if (str(_year) in file) and (report_name in file)
    ][0]

    df = pd.read_pickle(file_path + "/" + file_name, compression = "xz")
    if (consolidated) and ("연결재무제표" in df["개별/연결"].values):
        fs_record = df.loc[
            (df["개별/연결"] == "연결재무제표") & (df["계정명"].isin(account_list)), "금액"
        ].values
    else:
        fs_record = df.loc[
            (df["개별/연결"] == "재무제표") & (df["계정명"].isin(account_list)), "금액"
        ].values
    if add_date:
        date = file_name.split("_")[0]
        fs_record = np.insert(fs_record, 0, date)
    return fs_record


def load_fs_data(
    stock_code_list,
    account_list,
    year,
    quarter,
    consolidated=True,
    period="1Y",
    add_date=False,
):
    """
    재무 제표 데이터를 반환

    Parameters:
    ==========================
    stock_code_list: array-like,
        수집할 종목 코드로 구성된 배열
    account_list: array-like,
        수집할 계정명으로 구성된 배열: ["유동자산", "비유동자산", "자산총계", "유동부채", "비유동부채", "부채총계",
                         "자본금", "이익잉여금", "자본총계", "매출액", "영업이익", "법인세차감전 순이익", "당기순이익"]
    year: int
        사업 연도
    quarter: int
        사업 분기
    consolidate: bool, default: True
        연결 재무 제표를 사용할 것인지 여부 (단, True여도 연결 재무 제표를 발표하지 않는 기업은 개별 재무 제표를 사용)
    period: str,
        누적 기간 (1Y, 2Q, 1Q)
        (예: quarter = "2021-2", period = "1Y"; 2020년 2분기부터 2021년 2분기까지 1년 동안의 누적 재무지표 (예: 매출액)
    missing: bool, default: "fillna"
        데이터가 없을 경우에 처리 방법
        - "fillna": 결측으로 채움
        - "raise": 오류 발생
    add_date: bool, default: False
        사업 보고서가 등록된 날짜를 포함할 것인지 여부

    :return : data, type: DataFrame
        행이 기업이고 열이 [계정명+날짜]인 데이터프레임
    """

    folder_path = resource_filename(__name__, "pickle_data/finance_state").replace('\\', '/')
    data = []

    for stock_code in stock_code_list:
        file_path = folder_path + "/{}".format(stock_code)
        if period == "1Y":
            if quarter == 4:
                record = _read_fs_record(
                    file_path, account_list, consolidated, year, 4, add_date
                )
            elif quarter == 3:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, 3, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 4, add_date
                )
                record3 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 3, add_date
                )
                record = record1 + record2 - record3
            elif quarter == 2:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, 2, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 4, add_date
                )
                record3 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 2, add_date
                )
                record = record1 + record2 - record3
            elif quarter == 1:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, 1, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 4, add_date
                )
                record3 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 1, add_date
                )
                record = record1 + record2 - record3
        elif period == "6M":
            if quarter == 4:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, 4, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year, 2, add_date
                )
                record = record1 - record2
            elif quarter == 3:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, 3, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year, 1, add_date
                )
                record = record1 - record2
            elif quarter == 2:
                record = _read_fs_record(
                    file_path, account_list, consolidated, year, 2, add_date
                )
            elif quarter == 1:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, 1, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 4, add_date
                )
                record3 = _read_fs_record(
                    file_path, account_list, consolidated, year - 1, 3, add_date
                )
                record = record1 + record2 - record3
        elif period == "3M":
            if quarter == 1:
                record = _read_fs_record(
                    file_path, account_list, consolidated, year, 1, add_date
                )
            else:
                record1 = _read_fs_record(
                    file_path, account_list, consolidated, year, quarter, add_date
                )
                record2 = _read_fs_record(
                    file_path, account_list, consolidated, year, quarter + 1, add_date
                )
                record = record2 - record1
        data.append(record)
    if add_date:
        data = pd.DataFrame(
            data, columns=["보고서_제출일"] + account_list, index=stock_code_list
        )
    else:
        data = pd.DataFrame(data, columns=account_list, index=stock_code_list)
    return data
