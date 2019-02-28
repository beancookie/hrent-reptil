import re
import datetime

ERROR_VALUE = -1
PATTERN = re.compile('.*?(\d+).*')

CITY_DICT = {
    'sh': '上海',
    'sz': '深圳',
    'hz': '杭州',
    'nj': '南京',
    'cd': '成都',
    'wh': '武汉',
    'gz': '广州',
    'tj': '天津'
}

def get_int(value, verify=True):
    """字符串转为int"""
    match_re = re.match(PATTERN, value)
    if match_re:
        if verify and len(match_re.group(1)) != len(value):
            num = ERROR_VALUE
        else:
            num = int(match_re.group(1))
    else:
        num = -1
    return num


def get_float(value, verify=True):
    """字符串转为float"""
    match_re = re.match(PATTERN, value)
    if match_re:
        if verify and len(match_re.group(1)) != len(value):
            num = ERROR_VALUE
        else:
            num = float(match_re.group(1))
    else:
        num = ERROR_VALUE
    return num


def get_city_from_url(url):
    split = re.split('[/.]', url)
    if len(split) >= 2:
        return CITY_DICT[split[2]]
    else:
        return ''


def get_date(value):
    now = datetime.datetime.now()
    before_time = now
    if value is None:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    if '天' in value:
        before_time = now + datetime.timedelta(days=get_int(value))
    elif '小时' in value:
        before_time = now + datetime.timedelta(hours=get_int(value))
    elif '分钟' in value:
        before_time = now + datetime.timedelta(minutes=get_int(value))
    return before_time.strftime("%Y-%m-%d %H:%M:%S")
