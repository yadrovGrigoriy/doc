import json

from flask import Flask, render_template, flash, url_for, request
from werkzeug.utils import redirect
from flask import session
import forms
from fields import ADDITIONAL_FIELDS
from utils import calc_weight_by_IMT,  calc_finally_result

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'


# /home/zarezenko/mysite/flask_app.py

def calc_res_with_combinations(data, result):
    """расчет понижающего коэффициента"""
    if (
            data.get('narugniy_genitalniy_endometrioz') in ['1', '0'] and
            data.get('rezekciya_yaichnika') in ['1', '-2'] and
            data.get('time_after_operation') == '-5'
    ):
        result = result * 0.3

    if (
            data.get('SPKYA') in ['1', '0'] and
            data.get('narushenya_menstr') == '1' and
            data.get('rezekciya_yaichnika') in ['1', '-2'] and
            data.get('time_after_operation') == '-5' and
            data.get('lishniy_ves') == '1' and
            data.get('girsutizm') in ['0', '-2'] and
            data.get('gyperandrogeniya') == '0'
    ):
        result = result * 0.3

    if (
            data.get('СПКЯ') == '1' and
            data.get('narushenya_menstr') == '0' and
            data.get('rezekciya_yaichnika') in ['1', '-2'] and
            data.get('time_after_operation') == '-5' and
            data.get('lishniy_ves') == '1' and
            data.get('gyperandrogeniya') == '0'
    ):
        result = result * 0.2

    if (


    ):
        pass

    print(result)
    return result


def fields_weight_correction(data):
    """
        корректировка значений исходя из значений других элементов
        '0.0' - значение нужно расчитать исходя из других показателей
    """



    return data

def update_row_results_for_poll_1(data: dict):
    """ Пересчет части полей и удаление лишних(дополнительных) вернет модифицированый второй опрос для формы 1
     @param FIELDS['coef_ovulation']
    """

    # пересчет коэффициента овуляции
    if data.get('coef_ovulation') == 'specify':
        if float(data.get('ages')) < 0.7:
            data['coef_ovulation'] = 0.5
        elif float(data.get('ages')) <= 0.2:
            data['coef_ovulation'] = 0.3
        else:
            data['coef_ovulation'] = 0.5


    # Пересчет фертильности спермы
    sperm_fields = [
        'spermotozoid_count',
        'spermotozoid_concentration',
        'spermotozoid_mobility',
        'spermotozoid_viability',
        'spermotozoid_morfology',
    ]
    if any(float(data[item]) == 0.3 for item in sperm_fields):
        data['coef_fert_sperm'] = 0.3
    elif any(float(data[item]) == 0.5 for item in sperm_fields):
        data['coef_fert_sperm'] = 0.3
    elif all(float(data[item]) > 0.5 for item in sperm_fields):
        data['coef_fert_sperm'] = 1
    elif all(float(data[item]) == 0 for item in sperm_fields):
        data['coef_fert_sperm'] = 0

    [data.pop(item) for item in sperm_fields]

    # пересчет коффициента продолжительности бесплодия
    if data.get('coef_not_preg_period') == 'specify':
        data['coef_not_preg_period'] = 1  # default
        if float(data.get('ages')) <= 0.2:
            data['coef_not_preg_period'] = 0
        else:
            if float(data.get('coef_fert_sperm')) <= 0.5:
                data['coef_not_preg_period'] = data.get('coef_fert_sperm')

    return data




def update_row_results_for_poll_2(data: dict):
    """ Пересчет части полей и удаление лишних(дополнительных) вернет модифицированый второй опрос для формы 2
    """
    polls = session.get('polls')

    if not polls.get('poll_2'):
        res = data.copy()
    else:
        res = json.loads(polls['poll_2'])
    # корректировка коэффициента овуляции FIELDS['coef_ovulation']

    #Расчет ИМТ
    if data.get('weight_patient') and data.get('height_patient'):
        res['lishniy_ves'] = calc_weight_by_IMT(int(data['weight_patient']), int(data['height_patient']))
    if data.get('weight_partner') and data.get('height_partner'):
        res['lishniy_ves_partner'] = calc_weight_by_IMT(int(data['weight_partner']), int(data['height_partner']))
    try:
        [res.pop(item) for item in ['weight_patient', 'weight_partner', 'height_patient', 'height_partner'] ]
    except: pass
    #Расчет степени гирсутизма
    try:
        girsutizm_form_values = [data[f'girsutizm_ad_{number}'] for number in range(1, 12)]

        girsutizm_sum = 0
        for item in girsutizm_form_values:
            girsutizm_sum += int(item)

        if girsutizm_sum < 25:
            res['girsutizm'] = 0
        else:
            res['girsutizm'] = -2
        # уточнить по умеренной
        [res.pop(f'girsutizm_ad_{number}') for number in range(1, 12)]
    except Exception as e:    # Если это уже сделано то идем дальше
        print(e)

    return res


def generate_additional_form(data):
    """формирует дополнительную форму на основе второй формы"""
    res = []
    if data['previously_applied_treatments'] == '1':
        res.append('previously_applied_treatments_ad_1')
    if data['infertility_reasons'] == 'af':
        res.append('infertility_reasons_ad_1')
    if data['SPKYA'] in ['1', '0']:
        res.extend(['SPKYA_ad_1', 'SPKYA_ad_2', 'SPKYA_ad_3', 'SPKYA_ad_3'])
    if data['girsutizm'] == 'af':
        res.extend([f'girsutizm_ad_{number}' for number in range(1, 12)])# всего 11 полей дополниельной формы
    return res


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/poll_1', methods=['get', 'post'])
def poll_1():
    form = forms.Poll1Form()
    # handle submit =====================================
    if form.validate_on_submit():
        updated_data = update_row_results_for_poll_1(form.data)
        session['polls'] = {}
        session['polls']['poll_1'] = json.dumps(updated_data)
        return redirect(url_for('poll_2'))
    # end handle submit ==================================
    return render_template('poll_1.html', form=form)


@app.route('/poll_2', methods=['get', 'post'])
def poll_2():
    polls = session['polls']
    form = forms.Poll2Form()
    # handle submit
    if form.validate_on_submit():
        polls = session['polls']
        updates_data = update_row_results_for_poll_2(form.data)  # расчет индекса массы тела и прочих преобразованй с зменой полей
        polls['poll_2'] = json.dumps(updates_data)
        polls = session['polls']
        # generate additional poll
        fields_list = generate_additional_form(updates_data)
        if len(fields_list) > 0:
            session['fields_list'] = fields_list
            return redirect(url_for('poll_3'))


        # end all polls
        res = calc_finally_result()
        return redirect(url_for('confirmed', res=json.dumps(res)))
        # end handle submit
    return render_template('poll_2.html', form=form)


@app.route('/poll_3', methods=['get', 'post'])
def poll_3():
    fields_list = session['fields_list']
    for field in fields_list:
        setattr(forms.AdditionalForm, field, ADDITIONAL_FIELDS[field])
    form = forms.AdditionalForm()
    if form.validate_on_submit():
        updates_res = update_row_results_for_poll_2(form.data)  # расчет индекса массы тела и прочих преобразованй с зменой полей
        session['polls']['poll_2'] = json.dumps(updates_res)
        # calc finaly  result for KRA and PRZ
        res = calc_finally_result()
        return redirect(url_for('confirmed', res=json.dumps(res)))
    return render_template('poll_2.html', form=form)


@app.route('/confirmed')
def confirmed():
    res = json.loads(request.args.get('res'))
    return render_template('confirmed.html', res=res)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
