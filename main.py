import yaml
from yaml import Loader
import requests
import json
import datetime

DATA = {'TOKEN': '', 'ACCOUNT': ''}

def load_params():

    global DATA

    try:
        with open('settings.yaml', 'r') as yaml_file:
            DATA.update(yaml.load(yaml_file, Loader))
    except Exception:
        print('Can\'t open file with settings')

def get_statement():

    auth_header = {'X-Token': DATA['TOKEN_MONO']}

    with requests.Session() as session:
        session.headers.update(auth_header)
        resp = session.get(f'https://api.monobank.ua/personal/statement/{DATA["ACCOUNT"]}/1648760400')
        client_data = json.loads(resp.text)

        for rec in client_data:
            date_time = datetime.date.fromtimestamp(rec['time'])
            print(f'date = {date_time.strftime("%d.%m.%Y")}, client EDRPOU = {rec["counterEdrpou"]}, client NAME = {rec["description"]}, '
                  f'sum = {int(rec["amount"])/100}, comment = {rec["comment"] if "comment" in rec else ""}')

if __name__ == '__main__':
    load_params()

    if DATA['TOKEN_MONO'] == '':
        exit()

    get_statement()
