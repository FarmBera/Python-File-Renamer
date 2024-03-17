from datetime import datetime


def convert_datetime_str(dt_str):
    """
    "2023-03-09 at 20.06.02" 형식의 문자열을 "230309 200602" 형식으로 변환합니다.

    Args:
      dt_str: 변환할 날짜 문자열

    Returns:
      변환된 날짜 문자열
    """
    try:
        # datetime 객체 생성
        dt = datetime.strptime(dt_str, "%Y-%m-%d at %H.%M.%S")
    except ValueError:
        # 올바른 형식이 아닌 경우 None 반환
        return None

    # 연, 월, 일, 시, 분 추출
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute

    # 문자열 조합
    converted_str = f"{year:02d}{month:02d}{day:02d} {hour:02d}{minute:02d}"

    return converted_str


# 예시
dt_str = "2023-03-09 at 20.06.02"
converted_str = convert_datetime_str(dt_str)

if converted_str is not None:
    print(f"변환된 문자열: {converted_str}")
else:
    print(f"입력 문자열 '{dt_str}'은 올바른 형식이 아닙니다.")
