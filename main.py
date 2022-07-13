import requests
from bs4 import BeautifulSoup

username = 'Graphity'

url = f'https://github.com/users/{username}/contributions'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

h2 = soup.find('h2').text
h2 = ' '.join(h2.split())
print(h2)


year = []

table = soup.find('svg').find('g')
for column in table.find_all('g'):
    week = []
    for cell in column.find_all('rect'):
        week.append(
            {
                'count': cell['data-count'],
                'date': cell['data-date'],
                'level': cell['data-level']
            }
        )
    year.append(week)


for week in year:
    for day in week:
        print(day['count'])
        print(day['date'])
        print(day['level'])
        print()
