# -*- coding: utf-8 -*-

import unittest

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



class ColdataWriterTest (unittest.TestCase):
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





if __name__ == '__main__':
    unittest.main()
