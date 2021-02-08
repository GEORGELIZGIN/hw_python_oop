import datetime as dt


DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, record):
        self.records.append(record)

    def __get_date_stats__(self, date):
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
            week_stats += (
                self.__get_date_stats__(current_date - dt.timedelta(days=i))
            )
        return week_stats


class Record:
    def __init__(self, amount, comment, date=None):
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
        elif date is None:
            self.date = dt.date.today()
        else:
            raise ValueError
        self.amount = amount
        self.comment = comment


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained = super().get_today_remained()
        if remained <= 0:
            return 'Хватит есть!'
        return (
            f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал'
        )


class CashCalculator(Calculator):
    USD_RATE = 74.67
    EURO_RATE = 89.92

    def get_today_cash_remained(self, currency):
        currency_for_ans = {
            'rub': ('руб', 1),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }
        if currency not in currency_for_ans:
            return 'Неправильный код валюты'
        name, rate = currency_for_ans[currency]
        remained = super().get_today_remained() / rate
        remained_rounded = round(remained, 2)
        if remained == 0:
            return 'Денег нет, держись'
        elif remained > 0:
            return (
                f'На сегодня осталось {remained_rounded} {name}'
            )
        elif remained < 0:
            return (
                f'Денег нет, держись: твой долг - {abs(remained_rounded)} {name}'
            )
