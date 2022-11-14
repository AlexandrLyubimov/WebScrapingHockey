import os

from parser.get_data import get_html, get_data
from parser.reference_Info import hockey_leagues


def main():
    if not os.path.exists('csv'):
        os.mkdir('csv')

    for league in hockey_leagues:
        print(f'{league}')
        if league == "NHL":
            amount_team = 32
        else:
            amount_team = 22
        result: list = get_html(url=hockey_leagues[league], amount_team=amount_team)
        get_data(result=result, league_name=league, amount_team=amount_team)
        print(f'READY {league}')
    print("DONE")


if __name__ == '__main__':
    main()
