import requests
import json
from datetime import datetime
from time import time


bookmaker_id = 11
domain = 'https://1-xbet7835678.top/ru'

def get_sport_url(sport, domain):
    data = {
    '1': '1',
    '2': '4',
    '3': '3',
    '4': '5',
    '5': '6',
    '6': '2',
    '7': '8',
    }


    return f'{domain}/LineFeed/Get1x2_VZip?sports={data[sport]}&count=100&tf=2200000&tz=4&mode=4&country=1&getEmpty=true&virtualSports=true&menuSection=1%7C7'

def get_name(sports):
    data = {
    '1': 'Football',
    '2': 'Tennis',
    '3': 'Basketball',
    '4': 'Baseball',
    '5': 'Volleyball',
    '6': 'Hockey',
    '7': 'Handball',
    }
    return data[sports]


def get_match_url(match_id, domain):
    return f'{domain}/LineFeed/GetGameZip?id={match_id}&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&grMode=2&marketType=1'


def start_app(sports, domain):
    start_time = time()

    sport = get_sport_url(sports, domain)
    r = requests.get(sport)
    res = r.text
    res = json.loads(res)

    table = res['Value']
    legue_list = []


    for match_id in table:

        liga_id = match_id['LI']
        league_name = match_id['LE']

        if liga_id not in legue_list:
            legue_list.append( {'id': liga_id,
                'matches': [],
                'name': league_name} )


        matches_list = []
        w = []

        MID = match_id['CI']

        matches, league_name, team1, team2, start_times, liga_id = get_W1W2X(MID, domain)

        if matches == '':
            continue

        _W1, _W2, _X, _1X, _12, _2X = outcome_match(match_id, sports)

        f1, bet_value_f1, f2, bet_value_f2 = get_all_kf_fora(match_id)
        bet_value1, to, bet_value2, tu  = get_all_total(match_id)

        lgs = league_name.replace(' ', '-').replace('.', '')
        tmt = team1.replace(' ','-')
        tmt2 = team2.replace(' ', '-')
        rrr = f'{tmt}-{tmt2}'.replace(')', '').replace('(', '').replace('.', '')

        NAME_SPORT = get_name(sports)
        match_uri = f'https://1xbet.com/line/{NAME_SPORT}/{liga_id}-{lgs}/{MID}-{rrr}'  #get_match_url(MID, domain)

        if sports != '1' or sports == '3':
            if _W1 != '':
                w.append([{'bet_link': match_uri,
                    'bet_rate': _W1,
                    'bet_value': 0,
                    'team': 'team1',
                    'bettype': 1
                    },
                    {'bet_link': match_uri,
                    'bet_rate': _W2,
                    'bet_value': 0,
                    'team': 'team2',
                    'bettype': 2
                    }
                    ])

        if f1 != '' or sports == '3':
            w.append([{'bet_link': match_uri,
                'bet_rate': f2,
                'bet_value': bet_value_f2,
                'team': 'team1',
                'bettype': 3
                }
                ,{'bet_link': match_uri,
                'bet_rate': f1,
                'bet_value': bet_value_f1,
                'team': 'team2',
                'bettype': 4
                }])
                
        if to != '' or sports == '3':
            w.append([{'bet_link': match_uri,
                'bet_rate': bet_value2,
                'bet_value': tu,
                'team': 'both',
                'bettype': 5
                },
                {'bet_link': match_uri,
                'bet_rate': bet_value1,
                'bet_value': to,
                'team': 'both',
                'bettype': 6
                }])


        if sports != '1':
            if _X != '':
                xxx = []
                xxx.append({'bet_link': match_uri,
                    'bet_rate': _X,
                    'bet_value': 0,
                    'team': 'both',
                    'bettype': 7})

                if _12 != '':
                    xxx.append({'bet_link': match_uri,
                    'bet_rate': _12,
                    'bet_value': 0,
                    'team': 'both',
                    'bettype': 8
                    })

                w.append(xxx)

        if _2X != '':
            w.append([{'bet_link': match_uri,
                'bet_rate': _W1,
                'bet_value': 0,
                'team': 'both',
                'bettype': 9
                },
                {'bet_link': match_uri,
                'bet_rate': _2X,
                'bet_value': 0,
                'team': 'both',
                'bettype': 10
                }
                ])



        if _1X != '':
            w.append([{'bet_link': match_uri,
                'bet_rate': _1X,
                'bet_value': 0,
                'team': 'both',
                'bettype': 11
                },
                {'bet_link': match_uri,
                'bet_rate': _W2,
                'bet_value': 0,
                'team': 'both',
                'bettype': 12
                }
                ])



        data = {'id': MID, 'is_live': 0, 'start_time': start_times, 'team1': team1, 'team2': team2, 'markets': w}
        for ms in legue_list:
            if liga_id == ms['id']:
                ms['matches'].append(data)


        

    data = {'bookmaker_id': 11,
        'sport_id': sports,
        'leagues': legue_list}


    print(f'Request time: {round(time() - start_time, 1)} sec.')
    return data


def get_all_total(match_id):
    try:

        rest = match_id['AE'][1]['ME']

        TB_total = []
        TM_total = []
        
        for tb in rest:
            if len(TB_total) >= 1 and len(TM_total) >= 1:
                break

            if 'CE' in tb:
                if tb['T'] == 9:
                    TB_total.append([tb['C'], tb['P']])

                if tb['T'] == 10:
                    TM_total.append([tb['C'], tb['P']])



        return TM_total[0][0], TM_total[0][1], TB_total[0][0], TB_total[0][1]
    except:
        return '','','',''



def get_all_kf_fora(match_id):
    try:
        rest = match_id['AE'][0]['ME']
        TB = []
        TM = []
        for tb in rest:
            if len(TB) >= 1 and len(TM) >= 1:
                break

            if 'CE' in tb:
                if tb['T'] == 7:
                    TB.append([tb['C'], tb['P']])

                if tb['T'] == 8:
                    TM.append([tb['C'], tb['P']])

        return TM[0][0], TM[0][1], TB[0][0], TB[0][1]

    except:
        return '', '', '', ''


def outcome_match(match_id, sports = None):
    if sports == '3':
        # r = requests.get(f'{domain}/LineFeed/GetGameZip?id={match_id["CI"]}&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&grMode=2&marketType=1')
        # res = r.text
        # res = json.loads(res)

        # _W1 = res['Value']['GE'][0]['E'][0][0]['C']
        # _W2 = res['Value']['GE'][0]['E'][1][0]['C']
        return '', '', '','', '', '' #_W1, _W2, '', '', '' , ''

    else:
        try:
            rest = match_id['E']

            _W1 = ''
            _W2 = ''
            _X = ''
            _1X = ''
            _12 = ''
            _2X = ''

            for es in rest:
                if es['T'] == 1:
                    _W1 = es['C']

                if es['T'] == 3:
                    _W2 = es['C']

                if es['T'] == 2:
                    _X = es['C']

                if es['T'] == 5:
                    _12 = es['C']

                if es['T'] == 6:
                    _2X = es['C']

                if es['T'] == 4:
                    _1X = es['C']


            return _W1, _W2, _X, _1X, _12, _2X
        except:
            return '', '', '','', '', ''

def get_date(time_date):
    return datetime.fromtimestamp(int(time_date)).strftime('%Y-%m-%d %H:%M:%S')

def get_W1W2X(MID, domain):

        r = requests.get(get_match_url(MID, domain))
        res = r.text
        res = json.loads(res)

        if res['Error'] == 'Нет игры в линии!':
            return '', '', '','','',''

        res = res['Value']
        if 'O2' not in res:
            return '', '', '','','','',

        name_1 = res['O1E']
        name_2 = res['O2E']
        liga_name = res['LE']
        liga_id = res['LI']
        time_date = res['S']
        
        if len(str(name_1).strip()) <= 0 or len(str(name_2).strip()) <= 0 or len(str(liga_name).strip()) <= 0 or len(str(liga_id).strip()) <= 0:
            return '', '', '','','',''

        return MID, liga_name, name_1, name_2, get_date(time_date), liga_id

def save_json(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return


from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/scrap", methods=['GET'])
def index():
    print(get_name(request.args.get('sport_id')))
    data = start_app(request.args.get('sport_id'), 'https://1xstavka.ru')
    return data
    
    
if __name__ == '__main__':
    app.run(host='45.128.205.156', port=7771)
    #app.run()



