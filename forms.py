from flask_wtf import FlaskForm
import fields
from fields import FIELDS



class Poll1Form(FlaskForm):
    ages = FIELDS['ages']
    coef_not_preg_period = FIELDS['coef_not_preg_period']
    coef_ovulation = FIELDS['coef_ovulation']
    coef_fert_sperm = FIELDS['coef_fert_sperm']
    coef_pipes_wellbeing = FIELDS['coef_pipes_wellbeing']


class Poll2Form(FlaskForm):
    rodi_v_anamnez = FIELDS['rodi_v_anamnez']
    aborts = FIELDS['aborts']
    vikidish = FIELDS['vikidish']
    vnematochnaya_beremennost = FIELDS['vnematochnaya_beremennost']
    bezplidie_u_rodstvennikov = FIELDS['bezplidie_u_rodstvennikov']
    previously_applied_treatments = FIELDS['previously_applied_treatments']
    smoking = FIELDS['smoking']
    harakter_bezplodiya = FIELDS['harakter_bezplodiya']
    night_shifts = FIELDS['night_shifts']
    infertility_reasons = FIELDS['infertility_reasons']
    chlamydial_trace = FIELDS['chlamydial_trace']
    frequent_inflammatory_diseases = FIELDS['frequent_inflammatory_diseases']
    narugniy_genitalniy_endometrioz = FIELDS['narugniy_genitalniy_endometrioz']
    adenomyos = FIELDS['adenomyos']
    myoma_matki = FIELDS['myoma_matki']
    giperplasticheskiy_process = FIELDS['giperplasticheskiy_process']
    SPKYA = FIELDS['SPKYA']
    narushenya_menstr = FIELDS['narushenya_menstr']
    sinehii_matki = FIELDS['sinehii_matki']
    anomaliya_razvitiya_matki = FIELDS['anomaliya_razvitiya_matki']
    operacii_na_matichnih_trubah = FIELDS['operacii_na_matichnih_trubah']
    apopleksiya_yaichnika = FIELDS['apopleksiya_yaichnika']
    rezekciya_yaichnika = FIELDS['rezekciya_yaichnika']
    andeksektomiya = FIELDS['andeksektomiya']
    time_after_operation = FIELDS['time_after_operation']
    nalichie_obrazovaniya = FIELDS['nalichie_obrazovaniya']
    height_patient = FIELDS['height_patient']
    weight_patient = FIELDS['weight_patient']
    height_partner = FIELDS['height_partner']
    weight_partner = FIELDS['weight_partner']
    girsutizm = FIELDS['girsutizm']
    autimunniy_tireodit = FIELDS['autimunniy_tireodit']
    gipertireoz = FIELDS['gipertireoz']
    gipOtireoz = FIELDS['gipOtireoz']
    diabet = FIELDS['diabet']
    gypergonadotropnoe_sostoyanie = FIELDS['gypergonadotropnoe_sostoyanie']
    koncentraciya_FSG = FIELDS['koncentraciya_FSG']
    koncentraciya_LG = FIELDS['koncentraciya_LG']
    koncentraciya_AMG = FIELDS['koncentraciya_AMG']
    gyperprolaktinemiya = FIELDS['gyperprolaktinemiya']
    gyperandrogeniya = FIELDS['gyperandrogeniya']
    postkoitalniy_test = FIELDS['postkoitalniy_test']
    count_antral_folliculs = FIELDS['count_antral_folliculs']
    gipoplaziya_endometriya = FIELDS['gipoplaziya_endometriya']

#

class AdditionalForm(FlaskForm):
    pass

    # def __init__(self, fields_list, **kwargs):
    #     for field in fields_list:
    #         self[field] = fields[field]
    #     super().__init__(**kwargs)
