import requests
from bs4 import BeautifulSoup


class GHContributions:
    url = 'https://github.com/users/{}/contributions'
    
    def __init__(self, username: str) -> None:
        r = requests.get(self.url.format(username))
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
