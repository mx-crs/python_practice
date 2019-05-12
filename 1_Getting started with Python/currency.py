from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")  # Использовать переданный requests

    soup = BeautifulSoup(response.content, 'xml')

    amount = float(amount)
    from_nom = int(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string.replace(',', '.'))
    from_cur = float(soup.find('CharCode', text=cur_from).find_next_sibling('Value').string.replace(',', '.')) / from_nom * amount
    to_nom = int(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string.replace(',', '.'))
    to_cur = float(soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.')) / to_nom

    result = Decimal(from_cur / to_cur).quantize(Decimal('.0001'))
    return result  # не забыть про округление до 4х знаков после запятой
