import datetime
import json
import locale
from os import path

import jinja2

from models.month import Month
from utils.format_currency import format_currency

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

months = list[Month]()


with open(path.normpath(COLLECTION_FILE_PATH)) as file:
    for set in json.load(file)['sets']:
        stats['count'] += 1

        pieces = set['info']['pieces']
        price_paid = set['price']['paid']
        full_price = set['price']['full']
        bought_at = datetime.date.fromisoformat(set['boughtAt'])
        budgeted_for = datetime.date.fromisoformat(
            f'{set['budgetedFor']}-01',
        ).strftime('%B %Y')

        savings = round(full_price - price_paid, 2)

        stats['pieces'] += pieces
        stats['pricePaid'] += price_paid
        stats['fullPrice'] += full_price
        stats['savings'] += savings

        if not any(month.id == budgeted_for for month in months):
            months.append(Month(budgeted_for))

        month = list(filter(lambda m: m.id == budgeted_for, months))[0]

        month.add_set(
            id=set['id'],
            theme=set['info']['theme'],
            name=set['info']['name'],
            pieces=pieces,
            price_paid=price_paid,
            full_price=full_price,
            bought_at=bought_at,
        )

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
