#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 11:39:19 2021
@author: stefaniecg
@orcid: 0000-0001-8091-0706
@description: library - gui for data extraction phase
"""

# ----- import packages -----
import db_lib as dblib # database library
import sqlite3

# ---------- constants ----------
c_db_fn = dblib.path_db+dblib.db_name_wos
c_db_dd_items = dblib.c_data_items
c_pub_data = dblib.c_pub_data
# c_file_dir = '/Users/xxx/Documents/PAPERS/' // location of papers in your computer

# [txt,row,col,colspan,sticky]
c_btn_list = (('query one',1,1,1,'n'),
              ('prev',2,0,1,'n'),
              ('next',2,1,1,'n'),
              ('DOI search',5,2,1,'e'),
              ('update record',0,5,1,'e'),
              ('file open',0,2,1,'e'),
              ('edit toc',1,2,1,'e'))
c_optmenu_list = (('db table',3,0,2)) #,('dummy',2,3))
c_optmenu_opt = dblib.db_tables_wos
c_pub_data_xtra = (('SNT','Screening notes'),
                   ('SLN','Selection notes'),
                   ('SLC','Selection category'),
                   ('FN','File name'))
c_pub_data_local = c_pub_data_xtra[0:3] + c_pub_data + c_pub_data_xtra[3:4]

c_pubdatalocal_height = (('OID', 1,1), # id, height, rowspan
                         ('TI', 2.5,2),
                         ('AU', 1,1),
                         ('C1', 3,2),
                         ('WC', 1,1),
                         ('DE', 1,1),
                         ('ID', 1,1),
                         ('PY', 1,1),
                         ('UT', 1,1),
                         ('PT', 1,1),
                         ('PU', 1,1),
                         ('SO', 1,1),
                         ('CT', 1,1),
                         ('DI', 1,1),
                         ('AB', 15,9),
                         ('SNT', 2.5,2),
                         ('SLN', 2.5,2),
                         ('SLC', 1,1),
                         ('FN',  1,1))
# [txt,row,col,hght,wdth,rowspan]
c_txt_info = (('to review',2,2,1,40,1),
              ('all selected',4,2,1,40,1)) #,('dummy',2,2,2.5,50,2))
# ---------- dictionary ----------
# [hight,rowspan]
d_txtdd_height = {'D00':[3,2],
                  'D10':[3,2],'D11':[3,2],'D12':[3,2],'D13':[3,2],
                  'D20':[3,2],'D21':[3,2],'D22':[3,2],
                  'D30':[3,2],'D31':[3,2],'D32':[3,2],'D33':[3,2],
                  'D40':[3,2],'D41':[3,2],'D42':[3,2],'D43':[3,2],'D44':[3,2],'D45':[3,2],
                  'D50':[5,4],'D51':[5,4]}
# ---------- variables ----------
v_optmenu = [None,None] #* len(c_optmenu_list)
# db variables
v_oid = 1
v_db_current_table = dblib.db_tables_wos[0]
v_db_all_col = []
v_db_dd_col = []

# ---------- objects ----------
o_txt_pub = []
o_txt_dd = []
o_txt_xtra_data = []
o_txt_info = []
o_entry_bx = []
o_btn = []

# search tags
c_tag_ids = ['TI','AB','DE','ID','PU','SO','WC']
c_tag_colors = ['yellow','plum','gold','greenyellow','tomato','cyan']
c_tag_search_items = [['quantum','comput'], # BASIC TERMS: yellow
                    ['ion trap','ion-trap','trapped ion','trapped-ion','paul trap'], # TYPE OF QC TERMS: pink
                    ['electronic','architecture','hardware','control','fpga',' asic ','processor','voltage','current','electrode','ieee','channel'], # ELECTRONIC TERMS: orange
                    ['we ','this paper','propose',' here ','here,','this work',' present ','presented','manuscript',' work '], #PAPER TERMS: green
                    ['penning','diamond','quantum dot','superconducting','spectroscopy','spectrometer','chemi','astronomy',' theor'], #EXCLUDED TERMS: red
                    ['cryo','vacuum','shuttling','shuttle','qccd','transport','rotation']] #HIGHLIGHT TERMS: blue


# ---------- Def ----------
def f_query_db_info():
    # -- db part
    conn = sqlite3.connect(c_db_fn)
    c = conn.cursor() # create a cursor
    sql = f'PRAGMA table_info({v_db_current_table})'
    c.execute(sql)
    table_info = c.fetchall()
    conn.close() # close connection
    for [i,code,dtype,a,b,c] in table_info:
        v_db_all_col.append(code)

def f_query_one():
    v_oid = int(o_entry_bx.get())
    # -- db part
    f_query_db_info()
    conn = sqlite3.connect(c_db_fn)
    c = conn.cursor()
    sql = f'SELECT * FROM {v_db_current_table} WHERE oid = {v_oid}'
    c.execute(sql)
    record = c.fetchone()
    conn.close()
    # -- build record plus
    record_plus = list(zip(v_db_all_col,record))
    # -- fill in PUB publication fields
    for i,[dbid,desc] in enumerate(c_pub_data_local):
        index = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == dbid)
        texto = record[index]
        if texto is not None:
            o_txt_pub[i].insert(1.0,texto)
            if dbid == 'TI':
                ix_rep = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == 'REP')
                if record_plus[ix_rep][1]:
                    o_txt_pub[i]['bg'] = 'red'
                else:
                    o_txt_pub[i]['bg'] = 'systemTextBackgroundColor'
        else:
            o_txt_pub[i].insert(1.0,'-')
    # -- fill in DD data fields
    # for i,dbid in enumerate(v_db_dd_col):
    #     index = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == dbid)
    #     texto = record[index]
    #     if texto is not None:
    #         o_txt_dd[i].insert(1.0,texto)
    # index = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == 'EXC')
    # texto = record[index]
    # if texto is not None: o_txt_xtra_data.insert(1.0,texto)
    # -- disable interface for non selected
    idx = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == 'FN')
    if record_plus[idx][1] is None or (record_plus[idx][1]==''): #81-slc
        for i in [4,5,6]:
            o_btn[i].config(state='disabled')
        for o in o_txt_pub:
            o['bg'] = 'gainsboro'
        for o in o_txt_dd:
            o['bg'] = 'gainsboro'
        o_txt_xtra_data['bg'] = 'gainsboro'
    else:
        # -- highligt tags
        f_tag_highlight(o_txt_pub)
        # --disable buttons
        for i in [4,5,6]:
            o_btn[i].config(state='normal')
        for o in o_txt_pub:
            o['bg'] = 'systemTextBackgroundColor'
        for o in o_txt_dd:
            o['bg'] = 'systemTextBackgroundColor'
        o_txt_xtra_data['bg'] = 'systemTextBackgroundColor'

def f_update_one():
    v_oid = int(o_entry_bx.get())
    # start DB
    conn = sqlite3.connect(c_db_fn)
    c = conn.cursor()
    c.execute(f"""UPDATE {v_db_current_table} SET
              D00=:d00, D01=:d01, D02=:d02, D03=:d03, D04=:d04, D05=:d05, D06=:d06, D07=:d07,
              D10=:d10, D11=:d11, D12=:d12,
              D20=:d20, D21=:d21, D22=:d22, D23=:d23,
              D30=:d30, D31=:d31, D32=:d32, D33=:d33,
              D40=:d40, D41=:d41, D42=:d42, D43=:d43, D44=:d44, D45=:d45,
              D50=:d50, D51=:d51,
              EXC=:exc
              WHERE oid = :oid""",
              {'d00':o_txt_dd[0].get('1.0', 'end').rstrip(),'d01':o_txt_dd[1].get('1.0', 'end').rstrip(),'d02':o_txt_dd[2].get('1.0', 'end').rstrip(),'d03':o_txt_dd[3].get('1.0', 'end').rstrip(),'d04':o_txt_dd[4].get('1.0', 'end').rstrip(),'d05':o_txt_dd[5].get('1.0', 'end').rstrip(),'d06':o_txt_dd[6].get('1.0', 'end').rstrip(),'d07':o_txt_dd[7].get('1.0', 'end').rstrip(),
               'd10':o_txt_dd[8].get('1.0', 'end').rstrip(),'d11':o_txt_dd[9].get('1.0', 'end').rstrip(),'d12':o_txt_dd[10].get('1.0', 'end').rstrip(),
               'd20':o_txt_dd[11].get('1.0', 'end').rstrip(),'d21':o_txt_dd[12].get('1.0', 'end').rstrip(),'d22':o_txt_dd[13].get('1.0', 'end').rstrip(),'d23':o_txt_dd[14].get('1.0', 'end').rstrip(),
               'd30':o_txt_dd[15].get('1.0', 'end').rstrip(),'d31':o_txt_dd[16].get('1.0', 'end').rstrip(),'d32':o_txt_dd[17].get('1.0', 'end').rstrip(),'d33':o_txt_dd[18].get('1.0', 'end').rstrip(),
               'd40':o_txt_dd[19].get('1.0', 'end').rstrip(),'d41':o_txt_dd[20].get('1.0', 'end').rstrip(),'d42':o_txt_dd[21].get('1.0', 'end').rstrip(),'d43':o_txt_dd[22].get('1.0', 'end').rstrip(),'d44':o_txt_dd[23].get('1.0', 'end').rstrip(),'d45':o_txt_dd[24].get('1.0', 'end').rstrip(),
               'd50':o_txt_dd[25].get('1.0', 'end').rstrip(),'d51':o_txt_dd[26].get('1.0', 'end').rstrip(),
               'exc':o_txt_xtra_data.get('1.0', 'end').rstrip(),
               'oid':v_oid})
    conn.commit() # commit changes
    conn.close() # close connection

def f_query_crit(): #v_to_review
    # -- db part
    conn = sqlite3.connect(c_db_fn)
    c = conn.cursor() # create a cursor
    #sql = f"SELECT * FROM {v_db_current_table} WHERE (IN0=1 and IN1=1 and IN2=1 and IN3=1 and IN4=1 and IN5=1 and IN6=1 and IN7=1 and IN8=1 and IN9=1 and D50!=D50 and D51!=D51)"
    sql = f"SELECT * FROM {v_db_current_table} WHERE (IN0=1 and IN1=1 and IN2=1 and IN3=1 and IN4=1 and IN5=1 and IN6=1 and IN7=1 and IN8=1 and IN9=1)" # and D50!=' '
    c.execute(sql)
    records_all = c.fetchall()
    #sql = f"SELECT * FROM {v_db_current_table} WHERE (IN0=1 and IN1=1 and IN2=1 and IN3=1 and IN4=1 and IN5=1 and IN6=1 and IN7=1 and IN8=1 and IN9=1)"
    #c.execute(sql)
    c.execute('SELECT * FROM '+str(v_db_current_table)+" WHERE (IN0=1 and IN1=1 and IN2=1 and IN3=1 and IN4=1 and IN5=1 and IN6=1 and IN7=1 and IN8=1 and IN9=1) AND ((D50='' OR D50 IS ?) OR (D51='' OR D51 IS ?))",(None,None)) # screening
    records = c.fetchall()
    conn.close() # close connection
    # -- extract data
    all_selected = [item[0] for item in records_all]
    to_review = [item[0] for item in records]
    return to_review, all_selected

#----
def search_tag(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, 'end',nocase=True)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)

def f_tag_highlight(list_txt):
    for i, idtag in enumerate(c_tag_ids):
        index = next(ids for ids, [dbid,name] in enumerate(c_pub_data_local) if  dbid == idtag)
        for j,color in enumerate(c_tag_colors):
            list_txt[index].tag_config(color, background=color)
            for z, stag in enumerate(c_tag_search_items[j]):
                search_tag(list_txt[index], stag, color)
