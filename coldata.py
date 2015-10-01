# -*- coding: utf-8 -*-
"""Класс для подготовки текстовых данных в виде столбцов
© 2008-2015 Jenyay (jenyay.ilin@gmail.com)
Домашняя страница: http://jenyay.net
Страница скрипта: http://jenyay.net/Programming/Coldata
Версия 2.0
"""


class Coldata (object):
    def __init__ (self, fname = "", skiprows = 0):
        self.data = []
        if len(fname) != 0:
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


    def load (self, fname, skiprows = 0):
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


    def tostr (self, format = "%f", deliver = "\t"):
        """Преобразовать в строку
        format - вормат вывода (%f, %d, %.3f и т.д.)
        deliver - разделитель между столбцами"""
        length = [len (col) for col in self.data]
        maxlength = max (length)

        colcount = len (self.data)

        result = u""
        # Цикл по строкам
        for rownumber in xrange (maxlength):
            rowstr = ""

            # Перебираем столбцы
            for colnumber in xrange (colcount):
                # Если в этом столбце еще есть числа, добавим их
                if rownumber < len (self.data[colnumber]):
                    rowstr += format % (self.data[colnumber][rownumber])

                if colnumber != colcount - 1:
                    rowstr += deliver
                else:
                    rowstr += "\n"

            result += rowstr
        return result


    def save (self, fname, format = "%f", deliver = "\t", header=None):
        strval = self.tostr (format, deliver)

        fp = file (fname, "w")
        if header is not None:
            fp.write (header + "\n")
        fp.write (strval)
        fp.close()


def save (columns, fname, format = "%f", deliver = "\t", header=None):
    coldata_obj = Coldata ()
    for column in columns:
        coldata_obj.addcolumn (column)

    coldata_obj.save (fname, format, deliver, header)
