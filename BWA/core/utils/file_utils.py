import hashlib
import string
import unicodedata

from .date_utils import DateUtils

"""
Liste de méthodes utiles liées à la gestion des fichiers
"""


class FileUtils:
    '''
    Nom: clean_filename
    Fonction: nettoyer le nom de fichier envoyé par l'utilisateur pour enlever les caractères spéciaux et remplacer les espaces
    src : https://www.programcreek.com/python/?CodeExample=clean+filename
    '''

    @staticmethod
    def clean_filename(p_filename):
        char_limit = 255

        # replace spaces
        p_filename.replace(' ', '_')

        # keep only valid ascii chars
        cleaned_filename = unicodedata.normalize('NFKD', p_filename).encode('ASCII', 'ignore').decode()

        # keep only whitelisted chars
        whitelist = f"-_.()[]{string.ascii_letters}{string.digits}"
        cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
        return cleaned_filename[:char_limit]

    @staticmethod
    def prepare_filename(filename):
        return f'{DateUtils.timestamp_to_basic_str(DateUtils.now())}_{FileUtils.clean_filename(filename)}'

    @staticmethod
    def get_filefield_checksum(filefield):
        md5 = hashlib.md5()
        for chunk in filefield.chunks():
            md5.update(chunk)
        return md5.hexdigest()

    @staticmethod
    def generic_image_directory_path(instance, filename):
        return f'{type(instance).__name__.lower()}/{instance.pk}/images/{FileUtils.prepare_filename(filename)}'

    """
    Méthode permettant d'enregistrer le document à l'endroit passé en paramètre
    """

    @staticmethod
    def document_file_directory_path(instance, filename):
        new_filename = FileUtils.clean_filename(filename)
        instance_name = type(instance).__name__

        if instance_name == 'Achat':
            return 'achat/{0}/{1}'.format(instance.pk, new_filename)
        if instance_name == 'Affaires':
            return 'affaire/{0}/{1}'.format(instance.objet, new_filename)
        if instance_name == 'Client':
            return 'client/{0}/{1}/{2}'.format(instance.type, instance.client, new_filename)
        if instance_name == 'Paie':
            return 'paie/{0}/{1}/{2}'.format(instance.type, instance.paie, new_filename)
        return None

    @staticmethod
    def readable_file_size(bytes):
        thresh = 1024
        units = ['Ko', 'Mo', 'Go', 'To']

        if abs(bytes) < thresh:
            return f'{bytes} B'

        u = -1
        r = 10

        while True:
            bytes /= thresh
            u += 1

            if round(abs(bytes) * r) / r < thresh or u >= len(units) - 1:
                break

        return ('%.1f' % bytes) + ' ' + units[u]
