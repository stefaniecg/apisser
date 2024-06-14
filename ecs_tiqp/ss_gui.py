#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 14:15:35 2021
@author: stefaniecg
@orcid: 0000-0001-8091-0706
@description: display databases,GUI display only
"""
# ----- import packages -----
import tkinter as tk
import ss_lib as clib # current file library
import db_lib as dblib # database library
import webbrowser

# ---------- variables --------
oid = 1

# ---------- Def ----------
def clear_pub_boxes():
    enable_interface()
    for i in range(len(pub_info_txt)):
        pub_info_txt[i].delete('1.0', tk.END)
    snt_txt.delete('1.0', tk.END)
    sln_txt.delete('1.0', tk.END)
    fn_txt.delete('1.0', tk.END)
    scr_lab.delete('1.0', tk.END)
    sel_lab.delete('1.0', tk.END)
    open_lab.delete('1.0', tk.END)
    up_btn['highlightbackground'] = 'systemWindowBackgroundColor'
    v_option_cat.set(clib.c_sel_cat[0])

def update_pub_list():
    screened_list, selection_list, open_list = clib.query_crit(phase_v.get())
    scr_lab.insert(1.0,screened_list)
    sel_lab.insert(1.0,selection_list)
    open_lab.insert(1.0,open_list)
    disable_interface()

def query_one():
    clear_pub_boxes()
    clib.query_one(id_bx.get(),pub_info_txt,inc_v,snt_txt,sln_txt,fn_txt,v_option_cat)
    update_pub_list()

def next_item():
    oid = int(id_bx.get()) + 1
    id_bx.delete(0,tk.END)
    id_bx.insert(0,str(oid))
    query_one()

def prev_item():
    oid = int(id_bx.get()) - 1
    id_bx.delete(0,tk.END)
    id_bx.insert(0,str(oid))
    query_one()

def update_one():
    clib.update_one(id_bx.get(),inc_v,snt_txt,sln_txt,fn_txt,v_option_cat)
    query_one()
    up_btn['highlightbackground'] = 'green'

def btn_nni(): # changes only gui
    if phase_v.get()==0: # mode: screening
        for i in range(5):
            inc_v[i].set(1)
        inc_v[5].set(0)
        snt_txt.insert(1.0,'nni;')
    elif phase_v.get()==1: # mode: selection
        inc_v[6].set(1)
        inc_v[7].set(0); inc_v[8].set(0); inc_v[9].set(0)
        sln_txt.insert(1.0,'nni; no electronic design described;')

def btn_ssi(): # changes only gui
    text = 'ssi; (iff) electronic design is included;'
    if phase_v.get()==0: # mode: screening
        snt_txt.insert(1.0,text)
    elif phase_v.get()==1: # mode: selection
        sln_txt.insert(1.0,text)


def btn_doi():
    idx = next(i for i,[code,desc,row,hght,span] in enumerate(clib.pub_data) if code=='DI')
    doi = pub_info_txt[idx].get('1.0','end')
    url = 'https://doi.org/'+doi
    webbrowser.open(url)

def left_key(event):
    prev_item()

def right_key(event):
    next_item()

def radio_opt():
    query_one()

def change_table(callback):
    clib.current_table = callback
    clib.db_colnames, clib.db_rowcount, clib.df_searchquery = clib.query_db_info()
    v_lab_db.set(f'DB name and table: {dblib.db_name_wos}/{clib.current_table}    Range: 1 - {clib.db_rowcount}')
    v_lab_sq.set(f'SQ {clib.current_table}: {clib.df_searchquery}')
    oid = 1
    id_bx.delete(0,tk.END)
    id_bx.insert(0,str(oid))
    query_one()

def enable_interface():
    # list labels
    open_lab.config(state='normal')
    scr_lab.config(state='normal',bg='systemTextBackgroundColor')
    sel_lab.config(state='normal',bg='systemTextBackgroundColor')
    # option menu
    o_opt_men_cat.config(state='normal')
    # notes
    snt_txt.config(state='normal')
    sln_txt.config(state='normal')
    fn_txt.config(state='normal')
    snt_txt['bg'] = 'systemTextBackgroundColor'
    sln_txt['bg'] = 'systemTextBackgroundColor'
    fn_txt['bg'] = 'systemTextBackgroundColor'
    # radio buttons
    for rbs_row in rad_btn:
        for rb in rbs_row:
            rb.configure(state='normal')

def disable_interface():
    # list labels
    open_lab.config(state='disable')
    scr_lab.config(state='disable')
    sel_lab.config(state='disable')
    # notes + radio butttons + cat option menu: acoding to mode
    if phase_v.get()==0: # mode: screening
        sel_lab.config(bg='gainsboro')
        o_opt_men_cat.config(state='disabled')
        snt_txt.config(state='normal')
        sln_txt.config(bg='gainsboro')
        sln_txt.config(state='disabled')
        fn_txt.config(bg='gainsboro')
        fn_txt.config(state='disabled')
        for rbs_row in rad_btn[6:10]:
            for rb in rbs_row:
                rb.configure(state='disable')
    elif phase_v.get()==1: # mode: selection
        scr_lab.config(bg='gainsboro')
        o_opt_men_cat.config(state='normal')
        snt_txt.config(bg='gainsboro')
        snt_txt.config(state='disabled')
        sln_txt.config(state='normal')
        fn_txt.config(state='normal')
        for rbs_row in rad_btn[0:6]:
            for rb in rbs_row:
                rb.configure(state='disable')

# ---------- GUI --------
gui = tk.Tk()
gui.title('SLR of Doctoral thesis')
gui.geometry("1400x825") # (X * Y)

# --- publication information ---
tk.Label(gui, text='SLR of publications', font='Helvetica 18 bold').grid(row=0,column=0,columnspan=3)
pub_info_txt = [None] * len(clib.pub_data)
for i,[dbid,name,row,hgt,rows] in enumerate(clib.pub_data):
    tk.Label(gui,text=dbid).grid(row=row,column=0)
    tk.Label(gui,text=name).grid(row=row,column=1)
    pub_info_txt[i] = tk.Text(gui,width=62,height=hgt,font=(None,13))
    pub_info_txt[i].grid(row=row,column=2,rowspan=rows)

# --- inclusion criteria ---
tk.Label(gui, text='Inclusion Criteria', font='Helvetica 18 bold').grid(row=0,column=3,columnspan=2)
# display labels
for optn,val,col in clib.inc_opt:
    tk.Label(gui,text=optn).grid(row=0,column=col)
tk.Label(gui,text='Criteria description').grid(row=0,column=8)
for i,[dbid,crit,row,desc,hgt] in enumerate(clib.inc_crit):
    tk.Label(gui,text=dbid).grid(row=row,column=3)
    tk.Label(gui,text=crit).grid(row=row,column=4)
# display radio buttons
inc_v = [None] * len(clib.inc_crit)
inc_txt = [None] * len(clib.inc_crit)
rad_btn = [[None]*len(clib.inc_opt) for item in clib.inc_crit]
for i,[dbid,crit,row,desc,hgt] in enumerate(clib.inc_crit):
    inc_v[i] = tk.IntVar(); inc_v[i].set(2)
    for j,[optn,val,col] in enumerate(clib.inc_opt):
        rad_btn[i][j] = tk.Radiobutton(gui,variable=inc_v[i],value=val)
        rad_btn[i][j].grid(row=row,column=col)
    inc_txt[i] = tk.Text(gui,width=30,height=hgt,font=(None,13))
    inc_txt[i].grid(row=row,column=8,rowspan=hgt)
    inc_txt[i].insert(1.0,desc)
    inc_txt[i].config(state='disabled')
# screening notes
[dbid,crit,row,desc,hgt] = clib.scr_notes
tk.Label(gui,text=dbid).grid(row=row,column=3,sticky='nw')
tk.Label(gui,text=crit).grid(row=row,column=4,sticky='n')
snt_txt = tk.Text(gui,width=60,height=hgt)
snt_txt.grid(row=row,column=5,columnspan=4,rowspan=1,sticky='nw')
# selection notes
[dbid,crit,row,desc,hgt] = clib.sel_notes
tk.Label(gui,text=dbid).grid(row=row,column=3,sticky='nw')
tk.Label(gui,text=crit).grid(row=row,column=4,sticky='n')
sln_txt = tk.Text(gui,width=60,height=hgt)
sln_txt.grid(row=row,column=5,columnspan=4,rowspan=1,sticky='nw')
# file location
[dbid,crit,row,desc,hgt] = clib.fn_pub
tk.Label(gui,text=dbid).grid(row=row,column=3,sticky='nw')
tk.Label(gui,text=crit).grid(row=row,column=4,sticky='n')
fn_txt = tk.Text(gui,width=60,height=hgt)
fn_txt.grid(row=row,column=5,columnspan=4,rowspan=1,sticky='nw')


# buttons
tk.Button(gui,text="Query one",command=query_one).grid(row=1,column=1)
tk.Button(gui,text="Prev",command=prev_item).grid(row=2,column=0)
tk.Button(gui,text="Next",command=next_item).grid(row=2,column=1)
up_btn = tk.Button(gui,text="Update INx",command=update_one)
up_btn.grid(row=12,column=5,columnspan=3)
tk.Button(gui,text='Mark NNI',command=btn_nni).grid(row=12,column=8, sticky='e')
tk.Button(gui,text='Mark SSI',command=btn_ssi).grid(row=12,column=8, sticky='w')
tk.Button(gui,text='DOI search',command=btn_doi).grid(row=2,column=2,sticky='e')

# entry box
id_bx = tk.Entry(gui,width=5,justify='center')
id_bx.grid(row=1,column=0)
id_bx.insert(0,str(oid))

# info label
v_lab_db = tk.StringVar()
v_lab_db.set(f'DB name and table: {dblib.db_name_wos}/{clib.current_table}    Range: 1 - {clib.db_rowcount}')
tk.Label(gui,textvariable=v_lab_db).grid(row=1,column=2)
tk.Label(gui,text='VVI (Very-interesting) - SSI (Somewhat-interesting) - NNI (Non-interesting)').grid(row=16,column=4,columnspan=6)
v_lab_sq = tk.StringVar()
v_lab_sq.set(f'SQ {clib.current_table}: {clib.df_searchquery}')
tk.Label(gui,textvariable=v_lab_sq,wraplength=600).grid(row=13,column=4,columnspan=6,rowspan=2)
for i,[text,row,col] in enumerate(clib.info_notes):
    tk.Label(gui,text=text).grid(row=row,column=col)

# texts
open_lab = tk.Text(gui,width=60,height=3)
open_lab.grid(row=19,column=5,columnspan=4)
scr_lab = tk.Text(gui,width=60,height=3)
scr_lab.grid(row=20,column=5,columnspan=4)
sel_lab = tk.Text(gui,width=60,height=3)
sel_lab.grid(row=21,column=5,columnspan=4)

# key binding
gui.bind('<Left>', left_key)
gui.bind('<Right>', right_key)

# option menus
# --db table
option_list = dblib.db_tables_wos
option = tk.StringVar(gui)
option.set(dblib.db_tables_wos[0])
opt_men =tk.OptionMenu(gui, option, *option_list, command=change_table)
opt_men.grid(row=2,column=2)
# --category
option_list_cat = clib.c_sel_cat
v_option_cat = tk.StringVar(gui)
v_option_cat.set(clib.c_sel_cat[0])
o_opt_men_cat =tk.OptionMenu(gui, v_option_cat, *option_list_cat) #, command=f_set_sel_cat
o_opt_men_cat.grid(row=18,column=3,columnspan=2)

# radio butons for phase selection
tk.Label(gui,text='Phase selection',font='Helvetica 15 bold').grid(row=19,column=0,columnspan=2)
phase_v = tk.IntVar(); phase_v.set(0)
for i,[optn,val,row,col] in enumerate(clib.phases_opt):
    tk.Radiobutton(gui,variable=phase_v,value=val,command=radio_opt).grid(row=row,column=col)
    tk.Label(gui,text=optn).grid(row=row,column=col+1,sticky='w')

# ---------- Databases ----------
query_one()

# ---------- open WINDOW --------
gui.mainloop()
