#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 12:57:56 2021
@author: stefaniecg
@orcid: 0000-0001-8091-0706
@description: database information
"""
# ----- import packages -----
import datetime
import os
import pandas as pd # dataframe management

# ----- constants (data) -----
fn_wos_query = ('wos_0','wos_1','wos_2','wos_3',
                'wos_4','wos_5','wos_6','wos_7','wos_8','wos_9','wos_10',
                'wos_11','wos_12','wos_13','wos_14',
                'wos_15','wos_16','wos_17')
db_name_wos = 'slr_pub_WOS.db'
db_tables_wos = fn_wos_query # propagate file names from parsed database queries
fn_sq_wos = 'wos_queries.csv'
c_pub_data = (('OID','DB OID'),
              ('AU','Author'),
              ('TI','Title'),
              ('C1','Affiliation'),
              #('LA','Language'),
              ('WC','WOS cathegory'),
              ('DE','Keywords author'),
              ('ID','Keywords wos'),
              ('PY','Year'),
              #('SC','Research Area'),
              ('UT','Accession Number'),
              ('PT','Publication Type'),
              ('PU','Publisher'),
              ('SO','Publication Name'),
              ('CT','Conference Title'),
              ('DI','DOI'),
              ('AB','Abstract'))
c_data_items = (# ---
                ('RQ0','Use case',(
                    ('D00','Aim of publication'))),
                # ---
                ('RQ1','Physical requirements',(
                    ('D10','Type of ion trap'),
                    ('D11','Temperature'),
                    ('D12','In-Vacuum'),
                    ('D13','Size'))),
                # ---
                ('RQ2','Electric requirements',(
                    ('D20','Voltages'),
                    ('D21','Processing rate'),
                    ('D22','RF/DC channels'))),
                # ---
                ('RQ3','System-Level',(
                    ('D30','System Architecture'),
                    ('D31','Technologies used'))))

# ----- definitions -----
def write_df(df,fn,path,ix_write=True,ix_label=None):
    df.to_csv(path+fn, index=ix_write, header=True, index_label=ix_label)
    print(f'[INFO] generated: {fn}')

def init_dates():
    # define dates
    today = datetime.date.today()
    ctime = datetime.datetime.now()
    dtoday = today.strftime("%y%m%d")
    dtoday_long = today.strftime("%d %b %Y")
    dctime = ctime.strftime('%H%M')
    return dtoday, dtoday_long, dctime

def init_working_directories():
    # define project path
    path_project = os.getcwd()+'/'
    # new directories
    path_data = path_project+'data/'
    if not os.path.exists(path_data): os.makedirs(path_data)
    path_fig = path_project+'fig/'
    if not os.path.exists(path_fig): os.makedirs(path_fig)
    path_db = path_project+'db/'
    if not os.path.exists(path_db): os.makedirs(path_db)
    path_rep = path_project+'rep/'
    if not os.path.exists(path_rep): os.makedirs(path_rep)
    # return values
    return path_data, path_fig, path_db, path_rep #, path_db_ark

def get_sq():
    df_wos_sq = pd.read_csv(path_data+fn_sq_wos,sep=',',header=0)
    return df_wos_sq

def write_sq(df):
    write_df(df,fn_sq_wos,path_data,False)

def num2str(d):
    try:
        return str(int(d))
    except ValueError:
        return ''

def conv_col_num2str(df,col):
    for i,item in enumerate(df[col]):
        df.at[i,col] = num2str(item)

# ----- execute once -----
today, todayl, ctime = init_dates()
path_data, path_fig, path_db, path_rep = init_working_directories() # load working directories
df_wos_sq = get_sq()
