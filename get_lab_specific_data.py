import requests
import json
import os
import click
token = "ujmu8QMbzOReaZc5pGDxYibWWw900yMi"


def get_baserow_data(uri):
    r = requests.get(
        uri,
        headers={
            "Authorization": f"Token {token}"
        }
    )
    data = json.loads(r.content)
    for n in data['results']:
        yield n
    if data['next']:
        yield from get_baserow_data(data['next'])


basepath = 'sv'
files = os.listdir(basepath)

survey_map = {
    "likelihood": {
        1: {
            "female_young": 42,
            "female_old": 41,
            "male_young": 43,
            "male_old": 40,
            "unisex": 44}

    },
    "social": {
        1: {
            "female_young": 42,
            "female_old": 43,
            "male_young": 44,
            "male_old": 45,
            "unisex": 46
        },
        2: {
            "female_young": 63,
            "female_old": 62,
            "male_young": 61,
            "male_old": 60,
            "unisex": 64
        }
    },
    "spatial": {
        1: {
            "female_young": 51,
            "female_old": 50,
            "male_young": 53,
            "male_old": 52,
            "unisex": 54
        }
    },
    "temporal": {
        1: {
            "female_young": 57,
            "female_old": 56,
            "male_young": 59,
            "male_old": 58,
            "unisex": 60
        }
    }
}

for f in files:
    if not f.endswith('.qsf'):
        continue
    flist = f.split('_')
    survey_name = flist[1]

    with open(os.path.join(basepath, f), encoding='utf-8') as cs:
        qsf = json.loads(cs.read())

        for i in get_baserow_data("https://baserow-backend-psykcom.apps.k8s.gu.se/api/database/rows/table/11069/?user_field_names=true"):
            lab_id = i['Lab ID'][0]['value']
            if lab_id == 'SE_01':

                data = {
                    "female_young": {
                        "1": {
                            "Display": i['female young 1']
                        },
                        "2": {
                            "Display": i['female young 2']
                        },
                        "3": {
                            "Display":i['female young 3']
                        },
                        "4": {
                            "Display": i['female young 4']
                        },
                        "5": {
                            "Display": i['female young 5']
                        },
                        "6": {
                            "Display": i['female young 6']
                        }
                    },
                    "female_old": {
                        "1": {
                            "Display": i['female old 1']
                        },
                        "2": {
                            "Display": i['female old 2']
                        },
                        "3": {
                            "Display": i['female old 3']
                        },
                        "4": {
                            "Display": i['female old 4']
                        },
                        "5": {
                            "Display": i['female old 5']
                        },
                        "6": {
                            "Display": i['female old 6']
                        }
                    },
                    "male_young": {
                        "1": {
                            "Display": i['male young 1']
                        },
                        "2": {
                            "Display": i['male young 2']
                        },
                        "3": {
                            "Display": i['male young 3']
                        },
                        "4": {
                            "Display": i['male young 4']
                        },
                        "5": {
                            "Display": i['male young 5']
                        },
                        "6": {
                            "Display": i['male young 6']
                        }
                    },
                    "male_old": {
                        "1": {
                            "Display": i['male old 1']
                        },
                        "2": {
                            "Display": i['male old 2']
                        },
                        "3": {
                            "Display": i['male old 3']
                        },
                        "4": {
                            "Display": i['male old 4']
                        },
                        "5": {
                            "Display": i['male old 5']
                        },
                        "6": {
                            "Display": i['male old 6']
                        }
                    },
                    "unisex": {
                        "1": {
                            "Display": i['unisex 1']
                        },
                        "2": {
                            "Display": i['unisex 2']
                        },
                        "3": {
                            "Display": i['unisex 3']
                        },
                        "4": {
                            "Display": i['unisex 4']
                        },
                        "5": {
                            "Display": i['unisex 5']
                        },
                        "6": {
                            "Display": i['unisex 6']
                        }
                    }
                }
                print(survey_name)
                var_female_young =  {k:v['Display'] for (k,v) in data['female_young'].items()}
                var_female_old = {k: v['Display'] for (k, v) in data['female_old'].items()}
                var_male_young = {k: v['Display'] for (k, v) in data['male_young'].items()}
                var_male_old = {k: v['Display'] for (k, v) in data['male_old'].items()}
                var_unisex = {k: v['Display'] for (k, v) in data['unisex'].items()}

                rec = {str(k): str(k) for (k) in range(1, 7)}
                ChoiceOrder = [str(i) for i in range(1, 7)]

                for key in survey_map[survey_name]:
                    id = survey_map[survey_name][key]['female_young']
                    qsf['SurveyElements'][id]['Payload']['Choices'] = data['female_young']
                    qsf['SurveyElements'][id]['Payload']['VariableNaming'] = var_female_young
                    qsf['SurveyElements'][id]['Payload']['RecodeValues'] = rec
                    qsf['SurveyElements'][id]['Payload']['ChoiceOrder'] = ChoiceOrder

                    id = survey_map[survey_name][key]['female_old']
                    qsf['SurveyElements'][id]['Payload']['Choices'] = data['female_old']
                    qsf['SurveyElements'][id]['Payload']['VariableNaming'] = var_female_old
                    qsf['SurveyElements'][id]['Payload']['RecodeValues'] = rec
                    qsf['SurveyElements'][id]['Payload']['ChoiceOrder'] = ChoiceOrder

                    id = survey_map[survey_name][key]['male_young']
                    qsf['SurveyElements'][id]['Payload']['Choices'] = data['male_young']
                    qsf['SurveyElements'][id]['Payload']['VariableNaming'] = var_male_young
                    qsf['SurveyElements'][id]['Payload']['RecodeValues'] = rec
                    qsf['SurveyElements'][id]['Payload']['ChoiceOrder'] = ChoiceOrder

                    id = survey_map[survey_name][key]['male_old']
                    qsf['SurveyElements'][id]['Payload']['Choices'] = data['male_old']
                    qsf['SurveyElements'][id]['Payload']['VariableNaming'] = var_male_old
                    qsf['SurveyElements'][id]['Payload']['RecodeValues'] = rec
                    qsf['SurveyElements'][id]['Payload']['ChoiceOrder'] = ChoiceOrder

                    id = survey_map[survey_name][key]['unisex']
                    qsf['SurveyElements'][id]['Payload']['Choices'] = data['unisex']
                    qsf['SurveyElements'][id]['Payload']['VariableNaming'] = var_unisex
                    qsf['SurveyElements'][id]['Payload']['RecodeValues'] = rec
                    qsf['SurveyElements'][id]['Payload']['ChoiceOrder'] = ChoiceOrder


        for i in get_baserow_data("https://baserow-backend-psykcom.apps.k8s.gu.se/api/database/rows/table/11070/?user_field_names=true"):
            lab_id = i['Lab ID'][0]['value']
            if lab_id == 'SE_01':
                current_lower = i['[Current Location]'].replace('[','').replace(']','')
                current_upper = current_lower.upper()

                distant_lower = i['[Distant Location]'].replace('[', '').replace(']', '')
                distant_upper = distant_lower.upper()

                alternative_location = i['[Alternative Distant Location]'].replace('[', '').replace(']', '')

                miles_km = i['[miles/km]']['value']

                xxx_distans = ''.join(x for x in i['[XXX miles/XXX km]'] if x.isdigit())
                xxxx_distans = ''.join(x for x in i['[XXXX miles/XXXX km]'] if x.isdigit())
                xxxx_distans_miles_km = f"{xxxx_distans} {miles_km}"
                xxx_distans_miles_km = f"{xxx_distans} {miles_km}"

                close_country = i['[a different country closest to the current location]'].replace('[', '').replace(']', '')
                far_country = i['[a different country far away from the current location]'].replace('[', '').replace(']', '')

                #Spatial
                if survey_name == 'spatial':
                    # QID6_QuestionText
                    QID6 = qsf['SurveyElements'][65]['Payload']['QuestionText']
                    QID6 = QID6.replace('[CURRENT LOCATION]', current_upper)
                    QID6 = QID6.replace('[3 miles/5 km]', '3 miles' if miles_km == 'miles' else '5 km')
                    QID6 = QID6.replace('[Current Location]', current_lower)

                    QID101 = qsf['SurveyElements'][64]['Payload']['QuestionText']
                    QID101 = QID101.replace('[DISTANT LOCATION]', distant_upper)

                    QID101 = QID101.replace('[XXXX miles/XXXX km]', xxxx_distans_miles_km)
                    QID101 = QID101.replace('[Distant Location]', distant_lower)

                    QID112 = qsf['SurveyElements'][43]['Payload']['QuestionText']
                    QID112 = QID112.replace('[Distant Location]', distant_lower)

                    QID72 = qsf['SurveyElements'][42]['Payload']['QuestionText']
                    QID72 = QID72.replace('[Current Location]', current_lower)

                    ### CHOICES ####
                    QID71C1 = qsf['SurveyElements'][84]['Payload']['Choices']["1"]['Display']
                    QID71C1 = QID71C1.replace('[Current Location]', current_lower)
                    QID71C1 = QID71C1.replace('[3 miles/5 km]', '3 miles' if miles_km == 'miles' else '5 km')
                    QID71C2 = qsf['SurveyElements'][84]['Payload']['Choices']["2"]['Display']
                    QID71C2 = QID71C2.replace('[Distant Location]', distant_lower)
                    QID71C2 = QID71C2.replace('[XXXX miles/XXXX km]', xxxx_distans_miles_km)
                    QID71C3 = qsf['SurveyElements'][84]['Payload']['Choices']["3"]['Display']
                    QID71C3 = QID71C3.replace('[Current Location]', current_lower)
                    QID71C3 = QID71C3.replace('[15 miles/25 km]', '15 miles' if miles_km == 'miles' else '25 km')
                    QID71C4 = qsf['SurveyElements'][84]['Payload']['Choices']["4"]['Display']
                    QID71C4 = QID71C4.replace('[Alternative Distant Location]', alternative_location)
                    QID71C4 = QID71C4.replace('[XXX miles/XXX km]', xxx_distans_miles_km)

                    QID71C6 = qsf['SurveyElements'][84]['Payload']['Choices']["6"]['Display']
                    QID71C6 = QID71C6.replace('[a different country closest to the current location]', close_country)

                    QID71C7 = qsf['SurveyElements'][84]['Payload']['Choices']["7"]['Display']
                    QID71C7 = QID71C7.replace('[a different country far away from the current location]', far_country)

                    ### CHOICES ###

                    QID129C1 = qsf['SurveyElements'][85]['Payload']['Choices']["1"]['Display']
                    QID129C1 = QID129C1.replace('[Current Location]', current_lower)
                    QID129C1 = QID129C1.replace('[3 miles/5 km]', '3 miles' if miles_km == 'miles' else '5 km')
                    QID129C2 = qsf['SurveyElements'][85]['Payload']['Choices']["2"]['Display']
                    QID129C2 = QID129C2.replace('[Distant Location]', distant_lower)
                    QID129C2 = QID129C2.replace('[XXXX miles/XXXX km]', xxxx_distans_miles_km)
                    QID129C3 = qsf['SurveyElements'][85]['Payload']['Choices']["3"]['Display']
                    QID129C3 = QID129C3.replace('[Current Location]', current_lower)
                    QID129C3 = QID129C3.replace('[15 miles/25 km]', '15 miles' if miles_km == 'miles' else '25 km')
                    QID129C4 = qsf['SurveyElements'][85]['Payload']['Choices']["4"]['Display']
                    QID129C4 = QID129C4.replace('[Alternative Distant Location]', alternative_location)
                    QID129C4 = QID129C4.replace('[XXX miles/XXX km]', xxx_distans_miles_km)

                    QID129C6 = qsf['SurveyElements'][85]['Payload']['Choices']["6"]['Display']
                    QID129C6 = QID129C6.replace('[a different country closest to the current location]', close_country)

                    QID129C7 = qsf['SurveyElements'][85]['Payload']['Choices']["7"]['Display']
                    QID129C7 = QID129C7.replace('[a different country far away from the current location]', far_country)

                elif survey_name == 'social':
                    QID1211340211 = qsf['SurveyElements'][40]['Payload']['QuestionText']
                    QID1211340211 = QID1211340211.replace('[Current Location]', current_lower)
                    QID1211340211 = QID1211340211.replace('[3 miles/5 km]',
                                                          '3 miles' if miles_km == 'miles' else '5 km')

                    QID1211340228 = qsf['SurveyElements'][41]['Payload']['QuestionText']
                    QID1211340228 = QID1211340228.replace('[Distant Location]', distant_lower)
                    QID1211340228 = QID1211340228.replace('[XXXX miles/XXXX km]', xxxx_distans_miles_km)

                elif survey_name == 'temporal':
                    QID1211339847 = qsf['SurveyElements'][52]['Payload']['QuestionText']
                    QID1211339847 = QID1211339847.replace('[Current Location]', current_lower)
                    QID1211339847 = QID1211339847.replace('[3 miles/5 km]',
                                                          '3 miles' if miles_km == 'miles' else '5 km')

                    QID1211339848 = qsf['SurveyElements'][53]['Payload']['QuestionText']
                    QID1211339848 = QID1211339848.replace('[Distant Location]', distant_lower)
                    QID1211339848 = QID1211339848.replace('[XXXX miles/XXXX km]', xxxx_distans_miles_km)

                elif survey_name == 'likelihood':
                    QID1211340641 = qsf['SurveyElements'][32]['Payload']['QuestionText']
                    QID1211340641 = QID1211340641.replace('[Current Location]', current_lower)
                    QID1211340641 = QID1211340641.replace('[3 miles/5 km]',
                                                          '3 miles' if miles_km == 'miles' else '5 km')
                    QID1211340642 = qsf['SurveyElements'][33]['Payload']['QuestionText']
                    QID1211340642 = QID1211340642.replace('[Distant Location]', distant_lower)
                    QID1211340642 = QID1211340642.replace('[XXXX miles/XXXX km]', xxxx_distans_miles_km)


                # newfile = f'{flist[0]}_{survey_name}_{lab_id}_{flist[2]}'
                # if not os.path.exists(lab_id):
                #     os.makedirs(lab_id)
                # with open(os.path.join(lab_id,newfile), 'w', encoding='utf-8') as outfile:
                #     outfile.write(json.dumps(qsf,indent=4,ensure_ascii=False))


