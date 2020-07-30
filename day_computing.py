import datetime


def get_date_str(bias=0):
    """
    get the date as a string only shows month/day
    [bias] * as days want to add on today(could be minus)
           * defaut is zero stands for today
    """
    today = datetime.datetime.today()  # 獲得今天的日期
    date = (today + datetime.timedelta(days=bias)).strftime("%m/%d")  # 格式化日期
    return ' ' + date[1:] if date[0] == '0' else date     # 把0換成空白

# print(get_date_str())       # today
# print(get_date_str(-3))     # 3 days ago
# print(get_date_str(-7))     # 7 days ago
# print(get_date_str(100))    # day after 100 days


def Is_within_Target_Date_2020(this_date, target_date):
    # replace ' ' by '0' for the first letter
    this_date = '0' + this_date[1:] if this_date[0] == ' ' else this_date
    target_date = '0' + target_date[1:] if target_date[0] == ' ' else target_date

    this = datetime.date(2020, int(this_date[0:2]), int(this_date[3:]))
    target = datetime.date(2020, int(target_date[0:2]), int(target_date[3:]))

    # print for debugging
    # print("{} >= {} : {}" .format(this.strftime("%m/%d"), target.strftime("%m/%d"), this >= target))

    return this >= target

# Is_within_Target_Date_2020('03/12', '03/11')
# Is_within_Target_Date_2020('03/11', '03/11')
# Is_within_Target_Date_2020('03/10', '03/11')
# Is_within_Target_Date_2020(get_date_str(), get_date_str(-7))
