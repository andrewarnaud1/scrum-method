import itertools
import locale
import re
from datetime import date, datetime, timedelta

from django.utils import timezone

"""
Classe générique de gestion des dates : date courante, trimestre, ...
"""


class DateUtils:

    # Retourne la date du jour.
    @staticmethod
    def today():
        return date.today()

    # Retourne la date du jour.
    @staticmethod
    def now():
        return timezone.now()

    # Retourne l'année courante.
    @staticmethod
    def current_year():
        return date.today().year

    # Retourne le mois courante.
    @staticmethod
    def current_month():
        return date.today().month

    # Retourne le trimestre courante.
    @staticmethod
    def current_quarter():
        return DateUtils.current_month() // 4 + 1

    # Retourne le mois et l'année sous le format mm/yyyy avec un date yyyy-mm-jj en entrée
    @staticmethod
    def truncate_month_year(date):
        if date is None:
            return

        year, month, day = str(date).split("-")
        return f"{month}/{year}"

    # Retourne les trimestres sous forme de tuple ex: (01/2022, 1er trimestre 2022) pour les 5 ans à venir.
    @staticmethod
    def tuple_next_quarters():
        label_quarter = ['1er trimestre', '2eme trimestre', '3eme trimestre', '4eme trimestre']
        result = [(f'0{str(trimestre)}/{str(DateUtils.current_year())}',
                   f'{label_quarter[trimestre - 1]} {str(DateUtils.current_year())}') for trimestre in
                  range(DateUtils.current_quarter(), 5)]

        result.extend((f'0{str(trimestre)}/{str(DateUtils.current_year() + year)}',
                       f'{label_quarter[trimestre - 1]} {str(DateUtils.current_year() + year)}') for year, trimestre in
                      itertools.product(range(1, 6), range(1, 5)))

        return result

    # Retourne le trimestre courant de l'année ex: (01/2022, 1er trimestre 2022).
    @staticmethod
    def current_quarter_of_year():
        return f'0{str(DateUtils.current_quarter())}/{str(DateUtils.current_year())}'

    # Retourne la date du jour + 7j.
    @staticmethod
    def limit_date_7days():
        return date.today() + timedelta(days=7)

    # Retourne l'année courante.
    @staticmethod
    def range_10_years():
        return [(y, y) for y in range((DateUtils.current_year() - 5), (DateUtils.current_year() + 5))]

    # Converti un timpstamp en chaine de caractère.
    @staticmethod
    def timestamp_to_basic_str(timestamp):
        return timestamp.strftime("%Y%m%d%H%M%S")

    # Converti une date au format dd/mm/YYYY.
    @staticmethod
    def date_to_dd_mm_yyyy(date):
        return date.strftime("%d/%m/%Y") if date else None

    @staticmethod
    def format_dd_mm_yyyy_to_date(date):
        if date is None:
            return None

        # Remplace les caractères de séparation par un '/'
        date = re.sub('[-.:]', '/', date)
        # Split de la date en tableau par '/'
        splited_date = date.split('/')
        # Reconstruction de la date pour avoir dd/mm/yyyy
        date = str(f'{splited_date[0]}/{splited_date[1]}/{splited_date[2]}')

        return datetime.strptime(date, '%d/%m/%Y').date()

    @staticmethod
    def date_to_AA_dd_BB_YYYY(date):
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        return date.strftime('%A %d %B %Y')
