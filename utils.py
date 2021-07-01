import json

from flask import session


def calc_weight_by_IMT(weight: int, height: int):
    """
           Расчет индекса массы тела
           @param weight kg(целое число)
           @param height см(целое число)
           @return коеффициент
    """
    IMT  = weight / (height * height)
    if IMT <= 30:
        return 2
    elif IMT > 30 and IMT < 35:
        return -1
    elif IMT > 35:
        return -2
    elif IMT >= 40:
        return 0

def calc_PRZ_weight(data):
    res = 0
    for key, value in data.items():
        if key != 'csrf_token':
            res += round(float(value), 3)
    return res


def calc_KRA_weight(data):
    res = 1
    for key, value in data.items():
        if key != 'csrf_token':
            res *= float(value)
    return round(res, 3)


def calc_finally_result():
    print('done')
    polls = session.get('polls')
    print(polls)
    KRA = calc_KRA_weight(json.loads(polls['poll_1']))
    PRZ = calc_PRZ_weight(json.loads(polls['poll_2']))

    # result = calc_res_with_combinations(form.data, res)

    return {
        "PRG": KRA * PRZ,
        "KRA": KRA,
        "PRZ": PRZ
    }
