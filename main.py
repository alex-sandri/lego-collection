import datetime
import json
import locale
from os import path

import jinja2

locale.setlocale(locale.LC_ALL, 'it_IT')

PROJECT_PATH = path.normpath(path.join(__file__, '..'))
TEMPLATE_PATH = path.join(PROJECT_PATH, 'template')
COLLECTION_FILE_PATH = path.join(PROJECT_PATH, 'collection.json')

environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))
template = environment.get_template('index.html')

stats = dict[str, float]({
    'count': 0,
    'pieces': 0,
    'pricePaid': 0,
    'fullPrice': 0,
    'savings': 0,
})

months = dict[str, list[dict[str, str]()]()]()


def format_currency(value: float) -> str:
    return '€ {:,.2f}'.format(value)


with open(path.normpath(COLLECTION_FILE_PATH)) as file:
    for set in json.load(file)['sets']:
        stats['count'] += 1

        pieces = set['info']['pieces']
        pricePaid = set['price']['paid']
        fullPrice = set['price']['full']
        boughtAt = datetime.date.fromisoformat(set['boughtAt'])
        budgetedFor = datetime.date.fromisoformat(
            f'{set['budgetedFor']}-01',
        ).strftime('%B %Y')

        savings = round(fullPrice - pricePaid, 2)

        stats['pieces'] += pieces
        stats['pricePaid'] += pricePaid
        stats['fullPrice'] += fullPrice
        stats['savings'] += savings

        if budgetedFor not in months:
            months[budgetedFor] = []

        months[budgetedFor].append({
            'id': set['id'],
            'theme': set['info']['theme'],
            'name': set['info']['name'],
            'pieces': pieces,
            'pricePaid': format_currency(pricePaid),
            'fullPrice': format_currency(fullPrice),
            'pricePerPiece': format_currency(pricePaid / pieces),
            'savings': format_currency(savings),
            'savingsPercentage': f'{round(savings * 100 / fullPrice)}%',
            'boughtAt': boughtAt.strftime('%d/%m/%Y'),
        })

formattedStats = {
    'count': str(stats['count']),
    'pieces': str(stats['pieces']),
    'pricePaid': format_currency(stats['pricePaid']),
    'fullPrice': format_currency(stats['fullPrice']),
    'pricePerPiece': format_currency(stats['pricePaid'] / stats['pieces']),
    'savings': format_currency(stats['savings']),
    'savingsPercentage': f'{round(stats['savings'] * 100 / stats['fullPrice'])}%',
}

with open(path.join(PROJECT_PATH, 'index.html'), 'w') as file:
    contents = template.render(months=months, stats=formattedStats)

    file.write(contents)
