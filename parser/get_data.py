import json
import re
import time
import requests

import undetected_chromedriver
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

from config import SERVER_API_URL_UPLOAD, SERVER_API_TOKEN
from parser.reference_Info import code_league


def get_points(team):
    if ':' in team:
        # totals = re.findall(r'\d+', team)
        totals = re.findall(r'\d{1} : \d{1}', team)
        if len(totals) == 1:
            total_1 = totals[0].split(':')
            scored_points_game1 = total_1[0].strip()
            missed_points_game1 = total_1[-1].strip()
            scored_points_game2 = None
            missed_points_game2 = None
            scored_points_game3 = None
            missed_points_game3 = None
            scored_points_game4 = None
            missed_points_game4 = None
            scored_points_game5 = None
            missed_points_game5 = None
        elif len(totals) == 2:
            total_1 = totals[0].split(':')
            total_2 = totals[-1].split(':')
            scored_points_game1 = total_1[0].strip()
            missed_points_game1 = total_1[-1].strip()
            scored_points_game2 = total_2[0].strip()
            missed_points_game2 = total_2[-1].strip()
            scored_points_game3 = None
            missed_points_game3 = None
            scored_points_game4 = None
            missed_points_game4 = None
            scored_points_game5 = None
            missed_points_game5 = None
        elif len(totals) == 3:
            total_1 = totals[0].split(':')
            total_2 = totals[1].split(':')
            total_3 = totals[-1].split(':')
            scored_points_game1 = total_1[0].strip()
            missed_points_game1 = total_1[-1].strip()
            scored_points_game2 = total_2[0].strip()
            missed_points_game2 = total_2[-1].strip()
            scored_points_game3 = total_3[0].strip()
            missed_points_game3 = total_3[-1].strip()
            scored_points_game4 = None
            missed_points_game4 = None
            scored_points_game5 = None
            missed_points_game5 = None
        elif len(totals) == 4:
            total_1 = totals[0].split(':')
            total_2 = totals[1].split(':')
            total_3 = totals[2].split(':')
            total_4 = totals[-1].split(':')
            scored_points_game1 = total_1[0].strip()
            missed_points_game1 = total_1[-1].strip()
            scored_points_game2 = total_2[0].strip()
            missed_points_game2 = total_2[-1].strip()
            scored_points_game3 = total_3[0].strip()
            missed_points_game3 = total_3[-1].strip()
            scored_points_game4 = total_4[0].strip()
            missed_points_game4 = total_4[-1].strip()
            scored_points_game5 = None
            missed_points_game5 = None
        else:
            total_1 = totals[0].split(':')
            total_2 = totals[1].split(':')
            total_3 = totals[2].split(':')
            total_4 = totals[3].split(':')
            total_5 = totals[-1].split(':')
            scored_points_game1 = total_1[0].strip()
            missed_points_game1 = total_1[-1].strip()
            scored_points_game2 = total_2[0].strip()
            missed_points_game2 = total_2[-1].strip()
            scored_points_game3 = total_3[0].strip()
            missed_points_game3 = total_3[-1].strip()
            scored_points_game4 = total_4[0].strip()
            missed_points_game4 = total_4[-1].strip()
            scored_points_game5 = total_5[0].strip()
            missed_points_game5 = total_5[-1].strip()
    else:
        scored_points_game1 = None
        missed_points_game1 = None
        scored_points_game2 = None
        missed_points_game2 = None
        scored_points_game3 = None
        missed_points_game3 = None
        scored_points_game4 = None
        missed_points_game4 = None
        scored_points_game5 = None
        missed_points_game5 = None
    return scored_points_game1, missed_points_game1, scored_points_game2, missed_points_game2, scored_points_game3, \
           missed_points_game3, scored_points_game4, missed_points_game4, scored_points_game5, missed_points_game5


# function get html in text form
def get_html(url, amount_team):
    options = undetected_chromedriver.ChromeOptions()
    # options.headless = True
    # options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = undetected_chromedriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, features='html.parser')

        result: list = []

        trs = soup.find('tbody').find_all('tr')
        for tr in trs:
            name = tr.find('td').find('span', class_='table-item__name').text.strip()
            data = {'team_id': name}
            tds = tr.find_all('td')
            for i in range(1, amount_team + 1):
                team = tds[int('{}'.format(i))].text.strip()
                get_points(team)
                data['td{}_1'.format(i)] = get_points(team)[0]
                data['td{}_2'.format(i)] = get_points(team)[1]
                data['td{}_3'.format(i)] = get_points(team)[2]
                data['td{}_4'.format(i)] = get_points(team)[3]
                data['td{}_5'.format(i)] = get_points(team)[4]
                data['td{}_6'.format(i)] = get_points(team)[5]
                data['td{}_7'.format(i)] = get_points(team)[6]
                data['td{}_8'.format(i)] = get_points(team)[7]
                data['td{}_9'.format(i)] = get_points(team)[8]
                data['td{}_10'.format(i)] = get_points(team)[-1]
            result.append(data)

        return result
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def get_data(result, league_name, amount_team):
    df = pd.DataFrame.from_records(result)
    df.replace('', np.nan, inplace=True)
    df.replace('?', np.nan, inplace=True)

    col_name = [i for i in df.columns]

    for i in col_name[1:]:
        df[i] = df[i].astype(np.float64)

    df['gh'] = df[col_name[1::2]].count(axis=1)
    df["gh"] = df["gh"].astype(np.float64)
    df['sh'] = df[col_name[1::2]].sum(axis=1)
    df['mh'] = df[col_name[2::2]].sum(axis=1)

    i, n = 0, 1
    for el in range(0, amount_team):
        df.at[i, 'gg'] = pd.to_numeric(df[f"td{n}_2"], errors='coerce').count()
        df.at[i, 'sg'] = pd.to_numeric(df[f"td{n}_2"], errors='coerce').sum()
        df.at[i, 'mg'] = pd.to_numeric(df[f"td{n}_1"], errors='coerce').sum()
        i += 1
        n += 1

    if league_name == "NHL":
        df['team_id'].replace(
            ["Анахайм Дакс", "Аризона Койотс", "Баффало Сэйбрз", "Бостон Брюинз", "Ванкувер Кэнакс",
             "Вашингтон Кэпиталз", "Вегас Голден Найтс", "Виннипег Джетс", "Даллас Старз", "Детройт Ред Уингз",
             "Калгари Флэймз", "Каролина Харрикейнз", "Коламбус Блю Джекетс", "Колорадо Эвеланш", "Лос-Анджелес Кингз",
             "Миннесота Уайлд", "Монреаль Канадиенс", "Нью-Джерси Дэвилз", "Нью-Йорк Айлендерс", "Нью-Йорк Рейнджерс",
             "Нэшвилл Предаторз", "Оттава Сенаторз", "Питтсбург Пингвинз", "Сан-Хосе Шаркс", "Сент-Луис Блюз",
             "Сиэтл Кракен", "Тампа-Бэй Лайтнинг", "Торонто Мэйпл Лифс", "Филадельфия Флайерз", "Флорида Пантерз",
             "Чикаго Блэкхоукс", "Эдмонтон Ойлерз"], [*range(1, 33)], inplace=True)
    else:
        df['team_id'].replace(
            ["Авангард", "Автомобилист", "Адмирал", "Ак Барс", "Амур", "Барыс", "Витязь", "Динамо М", "Динамо Мн",
             "Куньлунь Ред Стар", "Локомотив", "Металлург Мг", "Нефтехимик", "Салават Юлаев", "Северсталь", "Сибирь",
             "СКА", "Спартак", "Торпедо", "Трактор", "ХК Сочи", "ЦСКА"], [*range(41, 63)], inplace=True)

    """Average goals scored = (Home scored + in away) / for the total number of games
        (Среднее количество забитых голов = (забитые дома + забитые в гостях)/ на общее количество игр)"""
    df['avg_scored'] = ((df['sh'] + df['sg']) / (df['gh'] + df['gg'])).round(3)

    """Average goals conceded = (Homes conceded + away) / for the total number of games
        (Среднее кол-во пропущенных голов = (пропущенные дома + пропущенные в гостях)/ на общее  количество игр"""
    df['avg_conceded'] = ((df['mh'] + df['mg']) / (df['gh'] + df['gg'])).round(3)

    """Average number of goals scored at home = number of goals scored at home / per number of home games
            (Среднее количество забитых дома = количество забитых мячей дома / на количество домашних игр)"""
    df['avg_scored_home'] = (df['sh'] / df['gh']).round(3)

    """Average Away Scored = Away Goals Scored / Per Away Games
        (Среднее количество забитых в гостях = количество забитых мячей в гостях / на количество гостевых игр)"""
    df['avg_scored_away'] = (df['sg'] / df['gg']).round(3)

    """Average conceded home goals = conceded goals at home / per number of home games
        (Среднее количество пропущенных голов дома = количество пропущенных мячей дома / на количество домашних игр)"""
    df['avg_conceded_home'] = (df['mh'] / df['gh']).round(3)

    """Average Away conceded = Away goals conceded / Per away games
        (Среднее количество пропущенных в гостях = количество пропущенных мячей в гостях / на количество гостевых игр)"""
    df['avg_conceded_away'] = (df['mg'] / df['gg']).round(3)

    """home team average total = the sum of all goals scored and conceded at home / per number of home games
        (Средний тотал домашней команды = сумма всех забитых и пропущенных мячей дома / на количество домашних игр)"""
    df['avg_total_home'] = ((df['sh'] + df['mh']) / df['gh']).round(3)

    """average total of the away team = the sum of all goals scored and conceded away / per the number of away games
        (Средний тотал гостевой команды = сумма всех забитых и пропущенных мячей в гостях / на количество гостевых игр)"""
    df['avg_total_away'] = ((df['sg'] + df['mg']) / df['gg']).round(3)

    df.to_csv(f'csv/{league_name}_s22-23.csv', index=False, header=True)

    result = df.to_json(orient="records")
    parsed = json.loads(result)

    for line in parsed:
        resp = requests.post(url=SERVER_API_URL_UPLOAD, headers={"Authorization": SERVER_API_TOKEN},
                             json=line)
        # print(f'SENDING: {line} RESULT:{resp.text}')

    print(f'SEND: {league_name}_file')
