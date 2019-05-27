# coding=utf-8
import random
import re
import string


#  验证参数不能为null
def verify(request, *args):
    msg = ""
    for arg in args:
        if request.data.get(arg) is None:
            msg = "%s 不能为null" % arg
            return msg
    return msg


#  生成26位token
def create_token(phone, size=26):
    tokens = [phone]
    for i in range(size):
        num = random.choice(string.ascii_letters + string.digits)
        tokens.append(num)
    token = "".join(tokens)
    return token


# 生成随机字符串
def create_random(size=26):
    nums = []
    for i in range(size):
        num = random.choice(string.ascii_letters + string.digits)
        nums.append(num)
    num_str = "".join(nums)
    return num_str


def verifyPhone(phone):
    if re.match(r'1[3,5,6,7,8]\d{9}', phone) and len(phone) <= 11:
        return ""
    else:
        return "请输入正确电话号码"


def verifyPassword(password):
    if len(password) < 6 or len(password) > 18:
        return "请输入6-18位密码"
    else:
        return ""
