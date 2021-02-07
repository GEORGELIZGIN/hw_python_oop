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
        return f'Сегодня можно съесть что-нибудь ещё, ' \
               f'но с общей калорийностью не более {remained} кКал'


class CashCalculator(Calculator):
    USD_RATE = 74.67
    EURO_RATE = 89.92

    def get_today_cash_remained(self, currency):
        remained = 0
        currency_for_ans = {
            'rub': ('руб', 1),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }
        if currency not in currency_for_ans:
            raise KeyError
        remained = super().get_today_remained() / currency_for_ans[currency][1]
        if remained == 0:
            return 'Денег нет, держись'
        elif remained > 0:
            return f'На сегодня осталось ' \
                   f'{round(remained, 2)} {currency_for_ans[currency][0]}'
        elif remained < 0:
            return f'Денег нет, держись: твой долг - ' \
                   f'{round(abs(remained), 2)} {currency_for_ans[currency][0]}'


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб