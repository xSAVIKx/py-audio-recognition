# coding=utf-8
__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'


class Language(object):
    languages = {
        'russian': 'ru_RU',
        'english': 'en_US'
    }
    festival_languages = {
        'russian': 'msu_ru_nsh_clunits',
        'english': 'kal_diphone'
    }


    @classmethod
    def get_festival_language(cls, language):
        return cls.festival_languages.get(language, 'english')

    @classmethod
    def get_language(cls, language):
        return cls.languages.get(language, 'english')