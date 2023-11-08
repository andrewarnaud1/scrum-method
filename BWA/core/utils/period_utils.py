from datetime import datetime

from dateutil.relativedelta import relativedelta

"""
Classe générique de gestion des périodes : 2023/01 pour janvier 2023
"""


class PeriodUtils:
    FRENCH_LABEL_MONTH = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']

    # Retourne la période courante.
    @staticmethod
    def current():
        return datetime.now().strftime('%Y/%m')

    # Génère une liste de tuple représentant une période de temps : [('2022/12', 'décembre 2022), ...]
    @staticmethod
    def generate_tuples(months=1, years=1):
        current_day = datetime.now()
        first_day_of_month = datetime(current_day.year, current_day.month, 1)
        start_month = first_day_of_month - relativedelta(months=months)
        end_month = first_day_of_month + relativedelta(years=years)

        periods = []
        while start_month <= end_month:
            month_year = start_month.strftime('%Y/%m')
            month_name = f'{PeriodUtils.FRENCH_LABEL_MONTH[start_month.month - 1]} {start_month.year}'
            periods.append((month_year, month_name))
            start_month += relativedelta(months=1)
        return periods

    @staticmethod
    def get_label(period):
        year, month = period.split('/')
        date = datetime(int(year), int(month), 1)
        return f'{PeriodUtils.FRENCH_LABEL_MONTH[date.month - 1]} {date.year}'
