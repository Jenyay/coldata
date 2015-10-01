# -*- coding: utf-8 -*-

import unittest
import os

import coldata


class ColdataTest (unittest.TestCase):
    def setUp (self):
        self._resultFile = None
        self._testColumn1 = [0.0000, -1.1280, 2.3500, -1.2580, -0.3300]
        self._testColumn2 = [1.2512, 5.2687, 9.1576, -1.2457, 95.3654]


    def tearDown (self):
        if self._resultFile:
            os.remove (self._resultFile)


    def testFileEmpty (self):
        fname = u'testdata/sample_empty.txt'
        data = coldata.Coldata (fname)
        self.assertEqual (len (data), 0)


    def testFileNotExists (self):
        fname = u'testdata/sample_not_exists.txt'
        self.assertRaises (IOError, coldata.Coldata, fname)


    def testFiles (self):
        files = [
            u'testdata/sample_no_header.txt',
            u'testdata/sample_rus.txt',
            u'testdata/sample_comma.txt',
            u'testdata/sample_invalid_end.txt',
            u'testdata/sample_length.txt',
            u'testdata/sample_tabs.txt',
        ]
        for fname in files:
            data = coldata.Coldata (fname)
            self.assertEqual (len (data), 2)
            self.assertEqual (data[0], self._testColumn1, fname)
            self.assertEqual (data[1], self._testColumn2, fname)


    def testSingleColumn (self):
        fname = u'testdata/sample_single.txt'
        data = coldata.Coldata (fname)
        self.assertEqual (len (data), 1)
        self.assertEqual (data[0], [0.0, 1.128, 2.35, -1.258, -3.33e-1])


if __name__ == '__main__':
    unittest.main()
