from scraper import GHScraper

s = GHScraper('Graphity')
year = s.fetch_contributions()

for week in year:
    for day in week:
        print(day['count'])
        print(day['date'])
        print(day['level'])
        print()

print(s.contributions)
