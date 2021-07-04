import json

from flask import session




def calc_res_with_combinations(data, result):
    polls = session['polls']
    poll_1= json.loads(polls['poll_1'])
    """расчет понижающего коэффициен=та"""
    if (
            data.get('narugniy_genitalniy_endometrioz') in ['1', '0'] and
            data.get('rezekciya_yaichnika') in ['0', '-2'] and
            data.get('time_after_operation') == '-1'
    ):
        result = result * 0.3

    if (
            data.get('SPKYA') in ['1', '0'] and
            data.get('narushenya_menstr') == '-1' and
            data.get('rezekciya_yaichnika') in ['0', '-2'] and
            data.get('time_after_operation') == '-1' and
            data.get('lishniy_ves') == '-1' and
            data.get('girsutizm') in ['0', '-2'] and
            data.get('gyperandrogeniya') == '0'
    ):
        result = result * 0.2

    if (
            float(poll_1.get('ages')) <= 0.2 and
            data.get('coef_not_preg_period') == '0.3' and
            data.get('previously_applied_treatments') == '-1' and
            data.get('gypergonadotropnoe_sostoyanie') == '-2' and
            data.get('koncentraciya_FSG') == '0' and
            data.get('koncentraciya_AMG') == '0' and
            data.get('count_antral_folliculs') in ['0', '1']
    ):
        result = result * 0.1


    # if (data.get('frequent_inflammatory_diseases') == '0' and
    #     poll_1.get('coef_pipes_wellbeing') in ['0.3', '1'] and
    #      data.get('operacii_na_matichnih_trubah') in ['1', '0', '-4']
    #
    # ):
    #     result = result * 0.1
    return result



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
    return calc_res_with_combinations(data, res)


def calc_KRA_weight(data):
    res = 1
    for key, value in data.items():
        if key != 'csrf_token':
            res *= float(value)
    return round(res, 3)


def calc_finally_result():
    print('done')
    polls = session.get('polls')
    KRA = calc_KRA_weight(json.loads(polls['poll_1']))
    PRZ = calc_PRZ_weight(json.loads(polls['poll_2']))


    # result = calc_res_with_combinations(form.data, res)

    return {
        "PRG": KRA * PRZ,
        "KRA": KRA,
        "PRZ": PRZ
    }
