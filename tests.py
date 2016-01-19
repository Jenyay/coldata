# -*- coding: utf-8 -*-

import os.path
import shutil
import tempfile
import unittest
import codecs

import coldata


class ColdataReaderTest (unittest.TestCase):
    def testFileEmpty (self):
        fname = u'testdata/sample_empty.txt'
        data = coldata.ColdataReader (fname)
        self.assertEqual (len (data), 0)


    def testFileNotExists (self):
        fname = u'testdata/sample_not_exists.txt'
        self.assertRaises (IOError, coldata.ColdataReader, fname)


    def testFiles (self):
        files = [
            u'testdata/sample_no_header.txt',
            u'testdata/sample_rus.txt',
            u'testdata/sample_comma.txt',
            u'testdata/sample_invalid_end.txt',
            u'testdata/sample_length.txt',
            u'testdata/sample_tabs.txt',
        ]

        testColumn1 = [0.0000, -1.1280, 2.3500, -1.2580, -0.3300]
        testColumn2 = [1.2512, 5.2687, 9.1576, -1.2457, 95.3654]

        for fname in files:
            data = coldata.ColdataReader (fname)
            self.assertEqual (len (data), 2)
            self.assertEqual (data[0], testColumn1, fname)
            self.assertEqual (data[1], testColumn2, fname)


    def testSingleColumn (self):
        fname = u'testdata/sample_single.txt'
        data = coldata.ColdataReader (fname)
        self.assertEqual (len (data), 1)
        self.assertEqual (data[0], [0.0, 1.128, 2.35, -1.258, -3.33e-1])


    def testSkip_01 (self):
        fname = u'testdata/sample_single.txt'
        data = coldata.ColdataReader (fname, skiprows=1)
        self.assertEqual (len (data), 1)
        self.assertEqual (data[0], [1.128, 2.35, -1.258, -3.33e-1])


    def testSkip_02 (self):
        fname = u'testdata/sample_no_header.txt'
        data = coldata.ColdataReader (fname, skiprows=1)

        testColumn1 = [-1.1280, 2.3500, -1.2580, -0.3300]
        testColumn2 = [5.2687, 9.1576, -1.2457, 95.3654]

        self.assertEqual (len (data), 2)
        self.assertEqual (data[0], testColumn1)
        self.assertEqual (data[1], testColumn2)


    def testSkip_03 (self):
        fname = u'testdata/sample_rus.txt'
        data = coldata.ColdataReader (fname, skiprows=1)

        testColumn1 = [0.0000, -1.1280, 2.3500, -1.2580, -0.3300]
        testColumn2 = [1.2512, 5.2687, 9.1576, -1.2457, 95.3654]

        self.assertEqual (len (data), 2)
        self.assertEqual (data[0], testColumn1)
        self.assertEqual (data[1], testColumn2)


    def testSkip_04 (self):
        fname = u'testdata/sample_rus.txt'
        data = coldata.ColdataReader (fname, skiprows=3)

        testColumn1 = [0.0000, -1.1280, 2.3500, -1.2580, -0.3300]
        testColumn2 = [1.2512, 5.2687, 9.1576, -1.2457, 95.3654]

        self.assertEqual (len (data), 2)
        self.assertEqual (data[0], testColumn1)
        self.assertEqual (data[1], testColumn2)


    def testSkip_05 (self):
        fname = u'testdata/sample_rus.txt'
        data = coldata.ColdataReader (fname, skiprows=4)

        testColumn1 = [-1.1280, 2.3500, -1.2580, -0.3300]
        testColumn2 = [5.2687, 9.1576, -1.2457, 95.3654]

        self.assertEqual (len (data), 2)
        self.assertEqual (data[0], testColumn1)
        self.assertEqual (data[1], testColumn2)


    def testSkip_06 (self):
        fname = u'testdata/sample_rus.txt'
        data = coldata.ColdataReader (fname, skiprows=1000)

        self.assertEqual (len (data), 0)


    def testHeader_01 (self):
        fname = u'testdata/sample_rus.txt'
        data = coldata.ColdataReader (fname, skiprows=3)

        header = u'''Пример данных ASCII
Значение1    Значение2
-------------------'''

        self.assertEqual (len (data), 2)
        self.assertEqual (data.header, header)



class ColdataWriterTest (unittest.TestCase):
    def setUp (self):
        self._tempDirName = None


    def tearDown (self):
        if self._tempDirName is not None:
            shutil.rmtree (self._tempDirName)


    def testEmpty (self):
        writer = coldata.ColdataWriter()
        result = list (writer.iteritems ([]))
        self.assertEqual (result, [])


    def testEmptyHeader_01 (self):
        header = u'Бла-бла-бла'

        writer = coldata.ColdataWriter (header=header)
        result = list (writer.iteritems ([]))
        self.assertEqual (result, [header])


    def testEmptyHeader_02 (self):
        header = u'Бла-бла-бла'
        writer = coldata.ColdataWriter ()
        writer.header = header

        result = list (writer.iteritems ([]))
        self.assertEqual (result, [header])


    def testNone (self):
        writer = coldata.ColdataWriter()
        result = list (writer.iteritems (None))
        self.assertEqual (result, [])


    def testNoneHeader_01 (self):
        header = u'Бла-бла-бла'
        writer = coldata.ColdataWriter (header=header)

        result = list (writer.iteritems (None))
        self.assertEqual (result, [header])


    def testNoneHeader_02 (self):
        header = u'Бла-бла-бла'
        writer = coldata.ColdataWriter ()
        writer.header = header

        result = list (writer.iteritems (None))
        self.assertEqual (result, [header])


    def testSingle_01 (self):
        col1 = [0.5]
        data = [col1]

        writer = coldata.ColdataWriter ()
        result = list (writer.iteritems (data))

        self.assertEqual (result, [u'0.5'])


    def testSingle_02 (self):
        col1 = [0.5, -1.0, 0, 1]
        data = [col1]

        writer = coldata.ColdataWriter ()
        result = list (writer.iteritems (data))

        self.assertEqual (result, [u'0.5', u'-1', u'0', u'1'])


    def testSingle_header_01 (self):
        header = u'Бла-бла-бла'
        col1 = [0.5, -1.0, 0, 1]
        data = [col1]

        writer = coldata.ColdataWriter (header=header)
        result = list (writer.iteritems (data))

        self.assertEqual (result, [header, u'0.5', u'-1', u'0', u'1'])


    def testSingle_header_02 (self):
        header = u'Бла-бла-бла'
        col1 = [0.5, -1.0, 0, 1]
        data = [col1]

        writer = coldata.ColdataWriter ()
        writer.header = header
        result = list (writer.iteritems (data))

        self.assertEqual (result, [header, u'0.5', u'-1', u'0', u'1'])


    def testSingle_format_01 (self):
        col1 = [0.5, -1.0, 0, 1]
        data = [col1]

        writer = coldata.ColdataWriter (format=u'{:05.2f}')
        result = list (writer.iteritems (data))

        self.assertEqual (result, [u'00.50', u'-1.00', u'00.00', u'01.00'])


    def testSingle_format_02 (self):
        col1 = [0.5, -1.0, 0, 1]
        data = [col1]

        writer = coldata.ColdataWriter ()
        writer.format = u'{:05.2f}'
        result = list (writer.iteritems (data))

        self.assertEqual (result, [u'00.50', u'-1.00', u'00.00', u'01.00'])


    def testColumns_01 (self):
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter ()
        result = list (writer.iteritems (data))

        validResult = [
            u'0.5\t42',
            u'-1\t11.5',
            u'0\t20',
            u'1\t20.5',
        ]

        self.assertEqual (result, validResult)


    def testColumns_format_01 (self):
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter (format=u'{:g}     {:05.2f}')
        result = list (writer.iteritems (data))

        validResult = [
            u'0.5     42.00',
            u'-1     11.50',
            u'0     20.00',
            u'1     20.50',
        ]

        self.assertEqual (result, validResult)


    def testColumns_format_02 (self):
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter ()
        writer.format = u'{:g}     {:05.2f}'
        result = list (writer.iteritems (data))

        validResult = [
            u'0.5     42.00',
            u'-1     11.50',
            u'0     20.00',
            u'1     20.50',
        ]

        self.assertEqual (result, validResult)


    def testColumns_header_01 (self):
        header = u'Бла-бла-бла'
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter (header=header)
        result = list (writer.iteritems (data))

        validResult = [
            header,
            u'0.5\t42',
            u'-1\t11.5',
            u'0\t20',
            u'1\t20.5',
        ]

        self.assertEqual (result, validResult)


    def testColumns_header_02 (self):
        header = u'Бла-бла-бла'
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter ()
        writer.header = header
        result = list (writer.iteritems (data))

        validResult = [
            header,
            u'0.5\t42',
            u'-1\t11.5',
            u'0\t20',
            u'1\t20.5',
        ]

        self.assertEqual (result, validResult)


    def testCommonFormat_01 (self):
        commonFormat = u'{:05.2f}'
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter (commonFormat=commonFormat)
        result = list (writer.iteritems (data))

        validResult = [
            u'00.50\t42.00',
            u'-1.00\t11.50',
            u'00.00\t20.00',
            u'01.00\t20.50',
        ]

        self.assertEqual (result, validResult)


    def testCommonFormat_02 (self):
        commonFormat = u'{:05.2f}'
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter()
        writer.commonFormat = commonFormat
        result = list (writer.iteritems (data))

        validResult = [
            u'00.50\t42.00',
            u'-1.00\t11.50',
            u'00.00\t20.00',
            u'01.00\t20.50',
        ]

        self.assertEqual (result, validResult)


    def testCommonFormat_03_tofile (self):
        self._tempDirName = tempfile.mkdtemp (prefix=u'coldata_')
        fname = os.path.join (self._tempDirName, u'write_01.txt')

        commonFormat = u'{:05.2f}'
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter()
        writer.commonFormat = commonFormat
        writer.tofile (data, fname)

        self.assertTrue (os.path.exists (fname))

        with codecs.open (fname, "r", "utf-8") as fp:
            result = fp.readlines ()

        validResult = [
            u'00.50\t42.00\n',
            u'-1.00\t11.50\n',
            u'00.00\t20.00\n',
            u'01.00\t20.50',
        ]

        self.assertEqual (result, validResult)


    def testCommonFormat_04_tofile_header (self):
        self._tempDirName = tempfile.mkdtemp (prefix=u'coldata_')
        fname = os.path.join (self._tempDirName, u'write_01.txt')

        commonFormat = u'{:05.2f}'
        header = u'Бла-бла-бла'
        col1 = [0.5, -1.0, 0, 1]
        col2 = [42, 11.5, 20, 20.5]
        data = [col1, col2]

        writer = coldata.ColdataWriter()
        writer.commonFormat = commonFormat
        writer.header = header
        writer.tofile (data, fname)

        self.assertTrue (os.path.exists (fname))

        with codecs.open (fname, "r", "utf-8") as fp:
            result = fp.readlines ()

        validResult = [
            header + u'\n',
            u'00.50\t42.00\n',
            u'-1.00\t11.50\n',
            u'00.00\t20.00\n',
            u'01.00\t20.50',
        ]

        self.assertEqual (result, validResult)



if __name__ == '__main__':
    unittest.main()
