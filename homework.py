import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, record):
        self.records.append(record)

    def __get_date_stats__(self, date):  # ф-ия вычисляет amount за определнную дату
        date_stats = 0
        for record in self.records:
            if record.date == date:
                date_stats += record.amount
        return date_stats

    def get_today_stats(self):
        now = dt.datetime.now()
        current_date = now.date()
        return self.__get_date_stats__(current_date)

    def get_today_remained(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        week_stats = 0
        now = dt.datetime.now()
        current_date = now.date()
        for i in range(7):
            week_stats += self.__get_date_stats__(current_date - dt.timedelta(days=i))
        return week_stats


class Record:
    def __init__(self, amount, comment, date=dt.date.today()):
        if isinstance(date, str):
            date_format = '%d.%m.%Y'
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = date
        self.amount = amount
        self.comment = comment


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained = super().get_today_remained()
        if remained <= 0:
            return 'Хватит есть!'
        else:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал'


class CashCalculator(Calculator):
    USD_RATE = 74.67
    EURO_RATE = 89.92

    def get_today_cash_remained(self, currency):
        remained = 0
        currency_for_answer = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        if currency == 'rub':
            remained = super().get_today_remained()
        elif currency == 'usd':
            remained = super().get_today_remained() / self.USD_RATE
        elif currency == 'eur':
            remained = super().get_today_remained() / self.EURO_RATE
        if remained == 0:
            return 'Денег нет, держись'
        elif remained > 0:
            return f'На сегодня осталось {round(remained, 2)} {currency_for_answer[currency]}'
        elif remained < 0:
            return f'Денег нет, держись: твой долг - {round(abs(remained), 2)} {currency_for_answer[currency]}'
