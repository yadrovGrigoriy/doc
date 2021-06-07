import json

from flask import Flask, render_template, flash, url_for, request
from werkzeug.utils import redirect

import forms

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
        # data = field_weight_correction(form.data)
        return redirect(url_for('poll_2', prev_poll=json.dumps(form.data)))
    # end handle submit ==================================
    return render_template('poll_1.html', form=form)


def calc_weight(data):
    res = 0
    for key, value in data.items():
        if key != 'csrf_token':
            res += round(float(value), 3)
    return res


@app.route('/poll_2', methods=['get', 'post'])
def poll_2():
    prev_poll = json.loads(request.args.get('prev_poll'))
    form = forms.Poll2Form()
    # handle submit
    if form.validate_on_submit():
        flash(u'Сведения обновлены!')
        PRZ = calc_weight(form.data)
        KRA = calc_weight(prev_poll)
        # result = calc_res_with_combinations(form.data, res)
        res = {
            "PRG": KRA * PRZ,
            "KRA": KRA,
            "PRZ": PRZ
        }

        return redirect(url_for('confirmed', res=json.dumps(res)))
    # end handle submit
    return render_template('poll_2.html', form=form, prev_poll=prev_poll)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)