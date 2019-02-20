import re

ERROR_VALUE = -1
PATTERN = re.compile('.*?(\d+).*')


def get_int(value):
    """字符串转为int"""
    match_re = re.match(PATTERN, value)
    if match_re and len(match_re.group(1)) == len(value):
        nums = int(match_re.group(1))
    else:
        nums = ERROR_VALUE

    return nums


def get_float(value):
    """字符串转为float"""
    match_re = re.match(PATTERN, value)
    if match_re and len(match_re.group(1)) == len(value):
            num = float(match_re.group(1))
    else:
        num = ERROR_VALUE

    return num


if __name__ == '__main__':
    print(get_int('12321s'))
