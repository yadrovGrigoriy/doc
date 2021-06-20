import json

from flask import Flask, render_template, flash, url_for, request
from werkzeug.utils import redirect
from flask import session
import forms
from fields import ADDITIONAL_FIELDS

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


def field_weight_correction(data):
    """
        корректировка значений исходя из значений других элементов
        '0.0' - значение нужно расчитать исходя из других показателей
    """

    if data.get('coef_ovulation') == '0.0':
        if float(data.get('ages')) < 0.7:
            data['coef_ovulation'] = 0.5
        elif float(data.get('ages')) <= 0.2:
            data['coef_ovulation'] = 0.3
        else:
            data['coef_ovulation'] = 0.5

    if data.get('coef_not_preg_period') == '0.0':
        if float(data.get('ages')) > 0.2:
            data['coef_not_preg_period'] = 0.5
        if float(data.get('coef_fert_sperm')) < 0.5:
            data['coef_not_preg_period'] = data.get('coef_fert_sperm')
        else:
            data['coef_ovulation'] = 1
    return data


def calc_weight(data):
    res = 0
    for key, value in data.items():
        if key != 'csrf_token':
            res += round(float(value), 3)
    return res


def update_row_results(data):
    res = data.copy()
    polls = session['polls']
    poll_1 = json.loads(polls['poll_1'])
    poll_2 = json.loads(polls['poll_2'])# пофиксить запись этого словаря

    #Расчет ИМТ

    def calc_weight_by_IMT(IMT):
        if IMT <= 30:
            return 2
        elif IMT > 30 and IMT < 35:
            return -1
        elif IMT > 35:
            return -2
        elif IMT >= 40:
            return 0
    try:
        IMT = float(data['weight_patient']) / (float(data['height_patient']) * float(data['height_patient']))
        IMT_partner = float(data['weight_partner']) / (float(data['height_partner']) * float(data['height_partner']))
        res['lishniy_ves'] = calc_weight_by_IMT(IMT)
        res['lishniy_ves_partner'] = calc_weight_by_IMT(IMT_partner)
        [res.pop(item) for item in ['weight_patient', 'weight_partner', 'height_patient', 'height_partner'] ]
    except: pass # Если это уже сделано то идем дальше
        ##
    #Расчет степени гирсутизма
    try:
        girsutizm_form_values = [data[f'girsutizm_ad_{number}'] for number in range(1, 12)]

        girsutizm_sum = 0
        for item in girsutizm_form_values:
            girsutizm_sum += int(item)
        res['girsutizm'] = -5
        [res.pop(f'girsutizm_ad_{number}') for number in range(1, 12)]
        print(girsutizm_sum)
        res = {**res, **poll_1, **poll_2}
        print(res)
    except Exception as e:    # Если это уже сделано то идем дальше
        print(e)

    return res


def need_additional_form(data):
    res = []
    poll_2 = json.loads(data['poll_2'])

    if poll_2['previously_applied_treatments'] == '1':
        res.append('previously_applied_treatments_ad_1')
    if poll_2['infertility_reasons'] == 'af':
        res.append('infertility_reasons_ad_1')
    if poll_2['SPKYA'] in ['1', '0']:
        res.extend(['SPKYA_ad_1', 'SPKYA_ad_2', 'SPKYA_ad_3', 'SPKYA_ad_3'])
    if poll_2['girsutizm'] == 'af':
        res.extend([f'girsutizm_ad_{number}' for number in range(1, 12)])# всего 11 полей дополниельной формы
    return res


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/confirmed')
def confirmed():
    res = json.loads(request.args.get('res'))
    return render_template('confirmed.html', res=res)


@app.route('/poll_1', methods=['get', 'post'])
def poll_1():
    form = forms.Poll1Form()
    # handle submit =====================================
    if form.validate_on_submit():
        print('submit')
        session['polls'] = {}
        session['polls']['poll_1'] = json.dumps(form.data)
        # data = field_weight_correction(form.data)
        return redirect(url_for('poll_2'))
    # end handle submit ==================================
    return render_template('poll_1.html', form=form)


@app.route('/poll_2', methods=['get', 'post'])
def poll_2():
    polls = session['polls']
    form = forms.Poll2Form()
    # handle submit
    if form.validate_on_submit():
        updates_res = update_row_results(form.data)  # расчет индекса массы тела и прочих преобразованй с зменой полей
        polls['poll_2'] = json.dumps(updates_res)
        # generate additional poll
        fields_list = need_additional_form(polls)
        if len(fields_list) > 0:
            session['fields_list'] = fields_list
            return redirect(url_for('poll_3'))
        # result = calc_res_with_combinations(form.data, res)

        # end all polls
        PRZ = calc_weight(form.data)
        KRA = calc_weight(json.loads(polls['poll_1']))

        res = {
            "PRG": KRA * PRZ,
            "KRA": KRA,
            "PRZ": PRZ
        }
        return redirect(url_for('confirmed', res=json.dumps(res)))
        # end handle submit
    return render_template('poll_2.html', form=form, prev_poll=polls['poll_1'])


@app.route('/poll_3', methods=['get', 'post'])
def poll_3():
    fields_list = session['fields_list']
    for field in fields_list:
        setattr(forms.AdditionalForm, field, ADDITIONAL_FIELDS[field])
    form = forms.AdditionalForm()
    if form.validate_on_submit():
        updates_res = update_row_results(form.data)  # расчет индекса массы тела и прочих преобразованй с зменой полей
        # calc finaly  result for KRA and PRZ
        print('done')
    return render_template('poll_2.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
