import re
import datetime

ERROR_VALUE = -1
PATTERN = re.compile('.*?(\d+).*')


def get_int(value, verify=True):
    """字符串转为int"""
    match_re = re.match(PATTERN, value)
    if match_re and len(match_re.group(1)) == len(value):
        nums = int(match_re.group(1))
    elif verify:
        nums = ERROR_VALUE
    else:
        nums = int(match_re.group(1))

    return nums


def get_float(value, verify=True):
    """字符串转为float"""
    match_re = re.match(PATTERN, value)
    if match_re and len(match_re.group(1)) == len(value):
        num = float(match_re.group(1))
    elif verify:
        num = ERROR_VALUE
    else:
        num = float(match_re.group(1))

    return num


def get_city_from_url(url):
    split = re.split('[/.]', url)
    if len(split) >= 2:
        return split[2]
    else:
        return ''

def get_date(value):
    now = datetime.datetime.now()
    before_time = now
    if '天' in value:
        before_time = now + datetime.timedelta(days=get_int(value))
    elif '小时' in value:
        before_time = now + datetime.timedelta(hours=get_int(value))
    elif '分钟' in value:
        before_time = now + datetime.timedelta(minutes=get_int(value))
    return before_time.strftime("%Y-%m-%d %H:%M:%S")


