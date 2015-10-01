# -*- coding: utf-8 -*-
"""Класс для подготовки текстовых данных в виде столбцов
© 2008-2015 Jenyay (jenyay.ilin@gmail.com)
Домашняя страница: http://jenyay.net
Страница скрипта: http://jenyay.net/Programming/Coldata
Версия 2.0
"""


class ColdataReader (object):
    def __init__ (self, fname = None, skiprows=0):
        self.data = []
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

        fp = file (fname)
        lines = fp.readlines()
        fp.close()

        # Массив еще не заполнялся данными
        res_empty = True

        # Массив из строк
        result_rows = []

        for line in lines[skiprows:]:
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
        row = [float (element.replace (",", ".")) for element in elements]
        return row
