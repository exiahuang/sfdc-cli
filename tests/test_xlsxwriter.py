#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from unittest import TestCase as PythonTestCase
import xlsxwriter


class XlsxwriterTestCase(PythonTestCase):

    def test_xlsx(self):

        #test.xlsxを作成
        book = xlsxwriter.Workbook('test.xlsx')
        #段落用のフォーマット
        titleformat = book.add_format({
            'bold': True,
            'font_color': 'black',
            'font_size': '14',
            'bg_color': '#FFB900'
        })
        #通常の文字用フォーマット
        textformat = book.add_format({'bold': False, 'font_size': '14'})

        #ワークシートテスト用を作成
        sheet = book.add_worksheet('テスト用')

        sheet.write(1, 0, 'xlxswriteのテスト', titleformat)
        sheet.set_column(1, 0, 50)
        sheet.write(2, 0, 'こんにちはこんにちは', textformat)

        sheet.write(4, 0, 'サーバ一覧とか', titleformat)
        sheet.set_column(3, 0, 50)
        sheet.write(5, 0, '192.168.0.1', textformat)
        sheet.write(6, 0, '192.168.0.2', textformat)
        sheet.write(7, 0, '192.168.0.3', textformat)
        sheet.write(8, 0, '192.168.0.4', textformat)

        sheet.write(10, 0, 'URLとか', titleformat)
        #urlの入力
        sheet.write_url(11, 0, 'https://www.yahoo.co.jp', string='Yahoo')
        sheet.write_url(12, 0, 'https://google.co.jp')
        sheet.write_url(13, 0, 'https://xlsxwriter.readthedocs.io/index.html')

        book.close()
