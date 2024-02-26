# STR_FIND = ".txt"
# STR_REPLACE = ".md"

EXT_REF = ".txt"  # 참고 할 이름을 가진 파일들의 확장자
EXT_MODIFY = ".md"  # 수정 할 파일들의 확장자
log_file_path = "task_result.csv"  # 로그 파일 경로


import os
import pandas as pd
import datetime
import csv


# 경로에 있는 모든 파일 목록 리스트업
dir_list = os.listdir()
dir_list.sort()  # 정렬
# print(dir_list)


ref_data = []
to_data = []
# 참고 할 이름을 가진 파일들의 확장자만 추출
for item in dir_list:
    if item.endswith(EXT_REF):
        ref_data.append(item.replace(EXT_REF, ""))

# 수정 할 파일 목록 추출
for item in dir_list:
    if item.endswith(EXT_MODIFY):
        to_data.append(item)

print("<< File List >>", end="\n\n")
print("< Reference Data >")
print(ref_data, end="\n\n")
print("< Modify Data >")
print(to_data)


# 파일 개수 맞는지 확인
len1 = len(ref_data)
len2 = len(to_data)
print(len1, len2)
if not len1 == len2:
    # print("파일 개수가 맞지 않습니다. 계속하시겠습니까? (y/n) >> ")
    user_yes = "y"
    userinput = input("파일 개수가 맞지 않습니다. 계속하시겠습니까? (y) >> ")
    if not userinput == user_yes:
        raise RuntimeError("사용자가 작업을 중단하였습니다. \nUser Prevented Task. ")


# 작업 정상 처리 되었을 시, 메시지
MSG = "OK"
MSG_ERR = "Failed"
TASK_START = "Task Start"
TASK_END = "Task Done"

TimeNow = lambda: datetime.datetime.now()


def save_log(obj) -> bool:
    try:
        log_f = open(log_file_path, "a", encoding="utf-8", newline="")
        wr = csv.writer(log_f)
        wr.writerow(obj)
        log_f.close()
        return True
    except:
        raise RuntimeError("Log File Write Failed")


# 로그 파일 존재하지 않을 때, 파일 생성
if log_file_path not in dir_list:
    # 작업 정상 처리 되었는지 확인하기 위한 header array
    task_list = [["time", "State", "Before Name", "Changed Name"]]
    # 작업 목록 저장
    df = pd.DataFrame(task_list)  # create dataframe
    df.to_csv(f"{log_file_path}", index=False, header=False, encoding="UTF-8")


save_log(["\n"])
save_log([TimeNow(), TASK_START])


ERR_COUNT: int = 0
# ERR_LIST: list = []
# 데이터 처리 시작
for i in range(len(ref_data)):
    data1 = to_data[i]
    data2 = ref_data[i]

    try:
        # 이름 바꾸기
        os.rename(data1, f"{data2}{EXT_MODIFY}")
        # 정상 완료 기록
        save_log([TimeNow(), MSG, data1, f"{data2}{EXT_MODIFY}"])
    except:
        # 작업 오류 기록
        ERR_COUNT += 1
        obj = [TimeNow(), MSG_ERR, data1, f"{data2}{EXT_MODIFY}"]
        save_log(obj)
        print(obj)


save_log([TimeNow(), TASK_END])

print(f"작업이 완료되었습니다. (오류: {ERR_COUNT} 건)")
