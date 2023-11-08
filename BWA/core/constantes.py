import enum

from django.core.validators import MinValueValidator, MaxValueValidator


class CoreConstantes:
    class Environnement:
        LOCAL = 'local'
        RECETTE = 'recette'
        PREPRODUCTION = 'preproduction'
        PRODUCTION = 'production'

    class Choix_Oui_Non:
        OUI = 'O'
        NON = 'N'

        tuples = [
            (OUI, 'Oui'),
            (NON, 'Non')
        ]

    class Email:
        NOREPLY_MGL = 'andrew@revolucy.fr'

    class Utilisateur:
        MASCULIN = 'M'
        FEMININE = 'F'

        tuples_civilite = [
            (MASCULIN, 'M'),
            (FEMININE, 'Mme')
        ]

        tuples_sexe = [
            (MASCULIN, 'Homme'),
            (FEMININE, 'Femme')
        ]

    class Extension(enum.Enum):

        def __init__(self, nom, content_type):
            self.nom = nom
            self.content_type = content_type

        def extension(self):
            return f'.{self.nom}'

        CSV = 'csv', 'text/csv'
        DOC = 'doc', 'application/msword'
        DOCX = 'docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        PDF = 'pdf', 'application/pdf'

    class Field:
        TIME_FIELD_FORMATS = ['%H:%M', '%Hh%M']

    class PAYS:
        FR = 'FR'

    class Mode(enum.Enum):

        def __init__(self, nom, passe):
            self.nom = nom
            self.passe = passe

        CREATION = 'Création', 'créé'
        MODIFICATION = 'Modification', 'modifié'
        VISUALISATION = 'Visualisation', 'visualisé'

    class Forms:
        FIELD_DELETE = 'DELETE'

    class Validator:
        ANNEE = [MinValueValidator(1900), MaxValueValidator(2100)]
        POURCENT = [MinValueValidator(0), MaxValueValidator(100)]
