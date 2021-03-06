#!/usr/bin/env python
# coding: utf-8
import openpyxl
import pandas as pd
import json
import yaml

def english_countries() :
    filename = "ISO국가코드.xlsx"
    book = openpyxl.load_workbook(filename)
    sheet = book.worksheets[0]
    countries = []
    for row in sheet.rows:
        countries.append([row[3].value, row[1].value])
    del countries[:4]
    
    countries = dict(countries)
    return countries

def load_excel():
    filename = "test.xlsx"
    book = openpyxl.load_workbook(filename)
    return book

def add_data(sheets):
    data = []
    for sheetNum, sheet in enumerate(sheets) :
        for idx, row in enumerate(sheet.rows):
            data.append([row[1].value, row[2].value])
    return data

def del_garbages(data, dataf):
    for index, row in enumerate(data) :
        if row[1] == None or row[1] == '조  치  사  항':
            continue
          
        #엑셀 페이지 때문에 잘린 것들 처리
        if row[0] == None:
            try :
                dataf.loc[index-2, 'detail'] += row[1]
            except :
                dataf.loc[index-1, 'detail'] += row[1]
            continue;
        
        #개행 문자 없애기 (국가명)
        row[0] = row[0].replace("\n", "")

        dataf.loc[index, 'nation_kr'] = row[0]
        dataf.loc[index, 'detail'] = row[1]
    dataf = dataf.reset_index(drop = True)
    return data, dataf


def add_nation_eng(dataf) : 
    countries = english_countries()
    for index, row in enumerate(dataf['nation_kr']):
        if row in countries :
            dataf.loc[index, 'nation_eng'] = countries[row]
            dataf.loc[index, 'marker'] = False
        else :
            dataf.loc[index, 'marker'] = True
    return dataf