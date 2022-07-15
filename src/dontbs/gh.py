import requests
from bs4 import BeautifulSoup


class GHContributions:
    url = 'https://github.com/users/{}/contributions'
    
    def __init__(self, username: str) -> None:
        r = requests.get(self.url.format(username))
        if r.status_code != requests.codes.ok:
            raise ValueError('Incorrect GitHub Username')
        self.soup = BeautifulSoup(r.content, 'html.parser')
        self.year = []
        table = self.soup.find('svg').find('g')

        for column in table.find_all('g'):
            week = []
            for cell in column.find_all('rect'):
                week.append(
                    {
                        'count': int(cell['data-count']),
                        'date': cell['data-date'],
                        'level': int(cell['data-level'])
                    }
                )
            self.year.append(week)

    @property
    def today(self) -> int:
        return self.year[-1][-1]['count']

    @property
    def this_week(self) -> int:
        return sum([day['count'] for day in self.year[-1]])

    @property
    def this_year(self) -> int:
        h2 = self.soup.find('h2')
        if h2:
            contributions = h2.text.split()[0]
            if contributions.isdigit():
                return int(contributions)

        contributions = 0
        for week in self.year:
            for day in week:
                contributions += day['count']
        return contributions

    @property
    def current_level(self) -> int:
        return self.year[-1][-1]['level']

    @property
    def to_level_up(self) -> int:
        return {
            0: 1,
            1: 3 - self.today,
            2: 5 - self.today,
            3: 10 - self.today,
            4: 0
        }[self.current_level]

    @property
    def streak(self) -> int:
        s = 0
        for week in reversed(self.year):
            for day in reversed(week):
                if day['count'] == 0:
                    return s
                s += 1
        return s
                
