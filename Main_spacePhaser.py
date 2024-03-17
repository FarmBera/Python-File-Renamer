# STR_FIND = ".txt"
# STR_REPLACE = ".md"

DIRECTORY = "CONVERTER/"  # 파일 경로
TO_DIRECTORY = "COMPLETE/"
EXT_FIND = ".png"  # 찾을 확장자명
log_file_path = "task_result_date.csv"  # 로그 파일 경로


import os
import pandas as pd
import datetime
import csv
import re


# 로그 기록을 위한 현재 시간 return
TimeNow = lambda: datetime.datetime.now()


TimeNowStr = lambda: f"[{TimeNow()}] "


# 함수: 프로그램 종료
def StopProgram(msg=None) -> None:
    if not msg:  # 입력된 메시지가 없다면
        msg = TimeNowStr()
        msg += f"사용자가 작업을 중단하였습니다. "  # User Prevented Task.
    else:
        msg = TimeNowStr() + msg
    exit(msg)
    # raise RuntimeError(msg)


# 함수: 유저 입력 받아서 처리
def UserInput(msg) -> bool:
    user_yes = "y"
    msg += " (y/n) >> "
    usrinput = input(msg)
    if not usrinput == user_yes:
        StopProgram()
    print(TimeNowStr() + "작업을 시작합니다. ")
    return True


def CalcuTime(START, END):
    time_diff = TIME_END - TIME_START
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    seconds = time_diff.seconds % 60
    microseconds = time_diff.microseconds
    return f"{hours}h {minutes}m {seconds}.{microseconds}s"


TIME_START = TimeNow()
# 경로에 있는 모든 파일 목록 리스트업
dir_list = os.listdir(DIRECTORY)
dir_list.sort()
# print(dir_list)


data_list = []
# 참고 할 이름을 가진 파일들의 확장자만 추출
for item in dir_list:
    if item.endswith(EXT_FIND):
        data_list.append(item)
        # data_list.append(item.replace(EXT_FIND, ""))


# 빈 데이터인지 확인
if not data_list:
    StopProgram("data_list 에 추출된 데이터가 없습니다. ")

TIME_END = TimeNow()
print("데이터 추출 성공", CalcuTime(TIME_START, TIME_END))


# 데이터 정렬
try:
    DataSort = lambda data: sorted(
        data, key=lambda s: int(re.search(r"\d+", s).group())
    )
    data_list = DataSort(data_list)
except:
    StopProgram("정렬에 오류가 발생하였습니다. 데이터를 확인하십시오. ")


len1 = len(data_list)
print()
print("< Pharse Data >", len1)
print(data_list, end="\n\n")


UserInput("파일 이름을 바꾸시겠습니까?")


# 작업 정상 처리 되었을 시, 메시지
MSG = "OK"
MSG_ERR = "Failed"
TASK_START = "TASK START"
TASK_END = "TASK END"


def save_log(obj) -> bool:
    try:
        log_f = open(log_file_path, "a", encoding="utf-8", newline="")
        wr = csv.writer(log_f)
        wr.writerow(obj)
        log_f.close()
        return True
    except:
        msg = TimeNowStr() + "Log File Write Failed"
        print(msg)
        # StopProgram(msg)


# 로그 파일 존재하지 않을 때, 파일 생성
if log_file_path not in dir_list:
    # 작업 정상 처리 되었는지 확인하기 위한 header array
    task_list = [["time", "State", "Before Name", "Changed Name", "Other Info"]]
    # 작업 목록 저장
    df = pd.DataFrame(task_list)  # create dataframe
    df.to_csv(f"{log_file_path}", index=False, header=False, encoding="UTF-8")


# save_log(["\n"])
save_log([TimeNow(), TASK_START])


# 데이터 처리 시작
ERR_COUNT: int = 0
ERR_LIST: list = []
TIME_START: datetime = TimeNow()

for item in data_list:
    try:
        # 공백 제거
        new_name = item.replace(" ", "_")

        # 파일 이름 변경
        os.rename(f"{DIRECTORY}{item}", f"{TO_DIRECTORY}{new_name}")  # 이름 바꾸기
        save_log([TimeNow(), MSG, item, new_name])  # 정상 완료 기록
    except:  # 작업 오류 기록
        ERR_COUNT += 1
        obj = [TimeNowStr(), MSG_ERR, item, "?"]
        ERR_LIST.append(obj)
        save_log(obj)
        # print(obj)


save_log([TimeNow(), TASK_END])

TIME_END: datetime = TimeNow()

TOTAL_TIME = CalcuTime(TIME_START, TIME_END)
print(
    f"""{TimeNowStr()}작업이 완료되었습니다.
오류: {ERR_COUNT} 건, Estimated Time: {TOTAL_TIME}
    """
)
if ERR_COUNT > 0:
    for item in ERR_LIST:
        print(item)
