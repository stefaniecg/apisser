#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 10:07:53 2021
@author: stefaniecg
@orcid: 0000-0001-8091-0706
@description: library definitions access to DB
"""
# ----- import packages -----
import db_lib as dblib # database library
import sqlite3

# ---------- variables --------
current_table = dblib.db_tables_wos[0]

# ----- constants (tuples) -----
# display data of publication (id,db_code,desc, row, height, rowspan)
row_start = 3
pub_data = (('OID','DB OID',row_start,1,1),
            ('TI','Title',row_start+1,2,1),
            ('AU','Author',row_start+2,1,1),
            ('C1','Affiliation',row_start+3,3,1),
            #('LA','Language',row_start+4,1,1),
            ('WC','WOS cathegory',row_start+4,1,1),
            ('DE','Keywords author',row_start+5,2,1),
            ('ID','Keywords wos',row_start+6,2,1),
            ('PY','Year',row_start+7,1,1),
            #('SC','Research Area',row_start+8,1,1),
            ('UT','Accession Number',row_start+8,1,1),
            ('PT','Publication Type',row_start+9,1,1),
            ('PU','Publisher',row_start+10,1,1),
            ('SO','Publication Name',row_start+11,1,1),
            ('CT','Conference Title',row_start+12,1,1),
            ('DI','DOI',row_start+13,1,1),
            ('AB','Abstract',row_start+14,18,5))

# inclusion criteria (name,criteria,row,desc,height)
row_start = 1
inc_crit = (('IN0','Type of publication',row_start,'journal OR series OR book OR patent OR thesis',1),
            ('IN1','Years considered',row_start+1,'2000-2021',1),
            ('IN2','Language',row_start+2,'English',1),
            ('IN3','Peer reviewed',row_start+3,'Yes',1),
            ('IN4','Quality',row_start+4,'Published in WOS OR Espacenet OR Uni',1),
            ('IN5','Topic',row_start+5,'ITQCs with electronic design, implementation AND/OR verification',2),
            ('IN6','Accessiblity',row_start+6,'full paper accessible by UIBK libraries',1),
            ('IN7','Type of electronics',row_start+7,'control OR shuttling OR cryogenic OR vacuum',1),
            ('IN8','Min included content',row_start+8,'minimal description of the electronic system',1),
            ('IN9','Use-case',row_start+9,'control: execution quantum algorithm OR shuttling',2))

scr_notes = ('SNT','Screening notes',17,'Screening Notes',5)
sel_notes = ('SLN','Selection notes',18,'Selection Notes',5)
fn_pub = ('FN','File name',15,'file name',1)

# display_text[str], row[int], column[int]
info_notes = (('To review:',19,4),
              ('Screened IN0-IN5:',20,4),
              ('Selected IN0-IN9:',21,4))

# inclusion options (name,value,column)
inc_opt = (('False',0,5),('True',1,6),('Null',2,7))

# search tags
tag_ids = ['TI','AB','DE','ID','PU','SO','WC']
tag_colors = ['yellow','plum','gold','greenyellow','tomato','cyan']
tag_search_items = [['quantum comput','quantum information','quantum processor'], # BASIC TERMS: yellow
                    ['ion trap','ion-trap','trapped ion','trapped-ion','paul trap'], # TYPE OF QC TERMS: pink
                    ['electronic','architecture','hardware','control','fpga',' asic ','processor','voltage','current','electrode','ieee','channel'], # ELECTRONIC TERMS: orange
                    ['we ','this paper','propose',' here ','here,','this work',' present ','presented','manuscript',' work '], #PAPER TERMS: green
                    ['penning','diamond','quantum dot','superconducting','spectroscopy','spectrometer','chemi','astronomy',' theor'], #EXCLUDED TERMS: red
                    ['cryo','vacuum','shuttling','shuttle','qccd','transport','rotation']] #HIGHLIGHT TERMS: blue

# radio button for phase selection: name[str], value[int], row[int], col[int]
phases_opt = (('screening: IN0-5',0,20,0),('selection: IN6-9',1,21,0))

c_sel_cat = (' ','ElSys - described','ElSys - used','Review - ElSys ref')

# ----- functions -----

def query_db_info():
    # -- db part
    conn = sqlite3.connect(dblib.path_db+dblib.db_name_wos)
    c = conn.cursor() # create a cursor
    sql = f'PRAGMA table_info({current_table})'
    c.execute(sql)
    table_info = c.fetchall()
    sql = f'SELECT * from {current_table}'
    c.execute(sql)
    rowcount = len(c.fetchall())
    conn.close() # close connection
    # -- work
    col_names_raw = [None] * len(table_info)
    for i,cname in enumerate(table_info):
        col_names_raw[i] = table_info[i][1]
    colnames = [None] * len(col_names_raw)
    for i, colname in enumerate(col_names_raw):
        colnames[i] = colname
    # -- search query --
    index = int(dblib.df_wos_sq[dblib.df_wos_sq['id'] == current_table].index[0])
    df_sq = dblib.df_wos_sq['query'][index]
    return colnames, rowcount, df_sq

def query_one(oid,pub_info_txt,inc_v,snt_txt,sln_txt,fn_txt,v_option_cat):
    # -- db part
    conn = sqlite3.connect(dblib.path_db+dblib.db_name_wos)
    c = conn.cursor() # create a cursor
    sql = f'SELECT * FROM {current_table} WHERE oid = {oid}'
    c.execute(sql) # query the table
    record = c.fetchone()
    conn.close() # close connection
    # -- work
    record_plus = list(zip(db_colnames,record))
    # fill in data in fields
    for i,[dbid,desc,row,hgt,rows] in enumerate(pub_data):
        indices = [ids for ids, [cid,data] in enumerate(record_plus) if cid == dbid]
        index = indices[0]
        texto = record_plus[index][1]
        if texto is not None:
            pub_info_txt[i].insert(1.0,texto)
            if dbid == 'TI':
                ix_rep = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == 'REP')
                if record_plus[ix_rep][1]:
                    #pub_info_txt[i].config(bg='red')
                    pub_info_txt[i]['bg'] = 'red'
                else:
                    pub_info_txt[i]['bg'] = 'systemTextBackgroundColor'
        else:
            pub_info_txt[i].insert(1.0,'-')
    # extract inclusion criteria
    for i,[dbid,crit,row,desc,hgt] in enumerate(inc_crit):
        index = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == dbid)
        texto = record_plus[index][1]
        if texto == 0 or texto == '0':
            inc_v[i].set(0)
        elif texto == 1 or texto == '1':
            inc_v[i].set(1)
        else:  # texto is None
            inc_v[i].set(2)
    # extract screening notes
    [dbid,crit,row,desc,hgt] = scr_notes
    texto = next(b for a, b in record_plus if a == dbid)
    if texto is not None:
        snt_txt.insert(1.0,texto)
    # extract selection notes
    [dbid,crit,row,desc,hgt] = sel_notes
    texto = next(b for a, b in record_plus if a == dbid)
    if texto is not None:
        sln_txt.insert(1.0,texto)
    # extract file name
    [dbid,crit,row,desc,hgt] = fn_pub
    texto = next(b for a, b in record_plus if a == dbid)
    if texto is not None:
        fn_txt.insert(1.0,texto)
    # extract selection category
    ix_rep = next(ids for ids, [cid,data] in enumerate(record_plus) if cid == 'SLC')
    for i,category in enumerate(c_sel_cat):
        if category == record_plus[ix_rep][1]:
            v_option_cat.set(c_sel_cat[i])
    # highligt tags
    tag_highlight(pub_info_txt)

def update_one(oid,inc_v,snt_txt,sln_txt,fn_txt,v_option_cat):
    # start DB
    conn = sqlite3.connect(dblib.path_db+dblib.db_name_wos)
    c = conn.cursor()
    c.execute(f"""UPDATE {current_table} SET
              IN0 = :in0,
              IN1 = :in1,
              IN2 = :in2,
              IN3 = :in3,
              IN4 = :in4,
              IN5 = :in5,
              IN6 = :in6,
              IN7 = :in7,
              IN8 = :in8,
              IN9 = :in9,
              SNT = :snt,
              SLN = :sln,
              SLC = :slc,
              FN = :fn
              WHERE oid = :oid""",
              {'in0':inc_v[0].get(),
               'in1':inc_v[1].get(),
               'in2':inc_v[2].get(),
               'in3':inc_v[3].get(),
               'in4':inc_v[4].get(),
               'in5':inc_v[5].get(),
               'in6':inc_v[6].get(),
               'in7':inc_v[7].get(),
               'in8':inc_v[8].get(),
               'in9':inc_v[9].get(),
               'snt':snt_txt.get('1.0', 'end').rstrip(),
               'sln':sln_txt.get('1.0', 'end').rstrip(),
               'slc':v_option_cat.get(),
               'fn':fn_txt.get('1.0', 'end').rstrip(),
               'oid':oid})
    conn.commit() # commit changes
    conn.close() # close connection

def query_crit(phase_v):
    # -- db part
    conn = sqlite3.connect(dblib.path_db+dblib.db_name_wos)
    c = conn.cursor() # create a cursor
    sql = f"SELECT OID FROM {current_table} WHERE (IN0=1 and IN1=1 and IN2=1 and IN3=1 and IN4=1 and IN5=1)"
    c.execute(sql) # query the table
    record_scr = c.fetchall()
    sql = f"SELECT * FROM {current_table} WHERE (IN0=1 and IN1=1 and IN2=1 and IN3=1 and IN4=1 and IN5=1 and IN6=1 and IN7=1 and IN8=1 and IN9=1)"
    c.execute(sql) # query the table
    record_sel = c.fetchall()
    # choose one of the following depending on stage: (0) screening (1) Selection
    if phase_v == phases_opt[0][1]:
        #c.execute('SELECT * FROM '+str(current_table)+' WHERE REP=0 AND (IN5==2 OR IN5 IS ?)',(None,)) # screening
        c.execute('SELECT * FROM '+str(current_table)+' WHERE REP=0 AND ((IN0=2 OR IN0 IS ?) OR (IN1=2 OR IN1 IS ?) OR (IN2=2 OR IN2 IS ?) OR (IN3=2 OR IN3 IS ?) OR (IN4=2 OR IN4 IS ?) OR (IN5=2 OR IN5 IS ?))',(None,None,None,None,None,None)) # screening
    else:
        #c.execute('SELECT * FROM '+str(current_table)+' WHERE IN5=1 AND IN6=2') # selection
        c.execute('SELECT * FROM '+str(current_table)+" WHERE (IN0=1 AND IN1=1 AND IN2=1 AND IN3=1 AND IN4=1 AND IN5=1) AND ((IN6=2 OR IN6 IS ?) OR (IN7=2 OR IN7 IS ?) OR (IN8=2 OR IN8 IS ?) OR (IN9=2 OR IN9 IS ?) OR (SLC='   ' OR SLC IS ?))",(None,None,None,None,None)) # selection
    record_open = c.fetchall()
    conn.close() # close connection
    # -- work --
    scr_list = [None] * len(record_scr)
    for i,item in enumerate(record_scr):
        scr_list[i] = item[0]
    sel_list = [None] * len(record_sel)
    for i,item in enumerate(record_sel):
        sel_list[i] = item[0]
    open_list = [None] * len(record_open)
    for i,item in enumerate(record_open):
        open_list[i] = item[0]
    return scr_list, sel_list, open_list

#----
def search_tag(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, 'end',nocase=True)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)

def tag_highlight(pub_info_txt):
    for i, idtag in enumerate(tag_ids):
        index = next(ids for ids, [dbid,name,row,hgt,rows] in enumerate(pub_data) if  dbid == idtag)
        for j,color in enumerate(tag_colors):
            pub_info_txt[index].tag_config(color, background=color)
            for z, stag in enumerate(tag_search_items[j]):
                search_tag(pub_info_txt[index], stag, color)

# ----- execute once -----
db_colnames, db_rowcount, df_searchquery = query_db_info()
