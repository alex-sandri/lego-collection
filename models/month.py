from datetime import date

from utils.format_currency import format_currency


class Month:
    id: str

    sets: list[dict[str, str]]
    stats: dict[str, float]

    @property
    def formatted_stats(self) -> dict[str, str]:
        return {
            'count': str(self.stats['count']),
            'pieces': str(self.stats['pieces']),
            'pricePaid': format_currency(self.stats['pricePaid']),
            'fullPrice': format_currency(self.stats['fullPrice']),
            'pricePerPiece': format_currency(self.stats['pricePaid'] / self.stats['pieces']),
            'savings': format_currency(self.stats['savings']),
            'savingsPercentage': f'{round(self.stats['savings'] * 100 / self.stats['fullPrice'])}%',
        }

    def __init__(self, id: str) -> None:
        self.id = id
        self.sets = []
        self.stats = {
            'count': 0,
            'pieces': 0,
            'pricePaid': 0,
            'fullPrice': 0,
            'savings': 0,
        }

    def add_set(
        self,
        id: str,
        theme: str,
        name: str,
        pieces: int,
        price_paid: float,
        full_price: float,
        bought_at: date,
    ) -> None:
        savings = round(full_price - price_paid, 2)

        self.stats['count'] += 1
        self.stats['pieces'] += pieces
        self.stats['pricePaid'] += price_paid
        self.stats['fullPrice'] += full_price
        self.stats['savings'] += savings

        self.sets.append({
            'id': id,
            'theme': theme,
            'name': name,
            'pieces': str(pieces),
            'pricePaid': format_currency(price_paid),
            'fullPrice': format_currency(full_price),
            'pricePerPiece': format_currency(price_paid / pieces),
            'savings': format_currency(savings),
            'savingsPercentage': f'{round(savings * 100 / full_price)}%',
            'boughtAt': bought_at.strftime('%d/%m/%Y'),
        })
