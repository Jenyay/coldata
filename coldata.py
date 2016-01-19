# -*- coding: utf-8 -*-
"""Класс для подготовки текстовых данных в виде столбцов
© 2008-2015 Jenyay (jenyay.ilin@gmail.com)
Домашняя страница: http://jenyay.net
Страница скрипта: http://jenyay.net/Programming/Coldata
"""

__version__ = "2.0.1"
__versionTime__ = "19 Jan 2016"
__author__ = "Eugeniy Ilin <jenyay.ilin@gmail.com>"

import codecs


class ColdataReader (object):
    def __init__ (self, fname = None, skiprows=0):
        self._encoding = u'utf-8'

        self.data = []
        self.header = u''
        if fname:
            self.load (fname, skiprows)


    def __getitem__ (self, colindex):
        """Получить список, представляющий собой столбец с индексом colindex"""
        return self.data[colindex]


    def __len__ (self):
        """Для получения количества столбцов с помощью функции len() """
        return len (self.data)


    def addcolumn (self, column):
        """Добавить столбец в массив данных"""
        self.data.append (column)


    def load (self, fname, skiprows=0):
        """Загрузить столбцы из файла"""
        self.data = []

        # Массив еще не заполнялся данными
        res_empty = True

        # Массив из строк
        result_rows = []
        header_lines = []

        with codecs.open (fname, 'r', self._encoding) as fp:
            n = 0
            for line in fp:
                n += 1
                if n <= skiprows:
                    header_lines.append (line.rstrip())
                    continue

                try:
                    row = self.parseline (line)

                    if len (row) == 0:
                        continue

                    if res_empty:
                        res_empty = False
                        result_rows.append (row)
                    else:
                        if len (row) == len (result_rows[0]):
                            result_rows.append (row)
                        else:
                            break
                except ValueError:
                    if not res_empty:
                        # Ошибка разбора очередной строки,
                        # но до этого уже были успешно разобранные строки
                        break

        self.data = self.transpose (result_rows)
        self.header = u'\n'.join (header_lines)


    @staticmethod
    def transpose (rows):
        """Транспонировать массив"""
        rows_count = len (rows)
        if not len (rows):
            return rows

        cols_count = len (rows[0])

        result = []
        for i in range (cols_count):
            column = [rows[n][i] for n in range (rows_count)]
            result.append (column)

        return result


    def parseline (self, line):
        elements = line.split()
        row = [float (element.replace (',', '.')) for element in elements]
        return row


class ColdataWriter (object):
    """
    Класс для записи табличных данных в файл или вывода в виде строк
    """
    def __init__ (self,
                  format=None,
                  header=None,
                  commonFormat=u'{:g}'):
        self._format = format
        self._header = header
        self._separator = u'\t'
        self._commonFormat = commonFormat
        self._encoding = u'utf-8'


    @property
    def format (self):
        return self._format


    @format.setter
    def format (self, value):
        self._format = value


    @property
    def header (self):
        return self._header

    @header.setter
    def header (self, value):
        self._header = value


    @property
    def commonFormat (self):
        return self._commonFormat


    @commonFormat.setter
    def commonFormat (self, value):
        self._commonFormat = value


    def iteritems (self, data):
        if self._header is not None:
            yield self._header

        if data is not None:
            iterators = [iter (column) for column in data]
            for row in zip (*iterators):
                yield self._formatRow (*row)


    def tofile (self, data, filename):
        with codecs.open (filename, 'w', self._encoding) as fp:
            for n, line in enumerate (self.iteritems (data)):
                if n != 0:
                    fp.write (u'\n' + line)
                else:
                    fp.write (line)


    def _formatRow (self, *args):
        if self._format is not None:
            template = self._format
        else:
            template = self._separator.join (
                [self._commonFormat] * len (args)
            )

        result = template.format (*args)

        return result
