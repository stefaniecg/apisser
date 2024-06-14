#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 11:39:19 2021
@author: stefaniecg
@orcid: 0000-0001-8091-0706
@description: gui for data extraction phase
"""

# ---------- import packages ----------
import tkinter as tk
import ex_lib as clib # current file library
import webbrowser
import subprocess

# ---------- Def ----------

def f_clear_pub_boxes():
    for o in clib.o_txt_pub:
        o.delete('1.0', tk.END)
    for o in clib.o_txt_dd:
        o.delete('1.0', tk.END)
    clib.o_btn[4]['highlightbackground'] = 'systemWindowBackgroundColor'
    clib.o_txt_info[0].delete('1.0', tk.END)
    clib.o_txt_info[1].delete('1.0', tk.END)
    clib.o_txt_xtra_data.delete('1.0', tk.END)

def f_update_pub_list():
    l_review, l_selected = clib.f_query_crit()
    clib.o_txt_info[0].insert(1.0,l_review)
    clib.o_txt_info[1].insert(1.0,l_selected)

def f_prev_next_item(arrow):
    if (arrow=='left'):
        clib.v_oid = int(clib.o_entry_bx.get())-1
    elif(arrow=='right'):
        clib.v_oid = int(clib.o_entry_bx.get())+1
    clib.o_entry_bx.delete(0,tk.END)
    clib.o_entry_bx.insert(0,str(clib.v_oid))
    f_query_one()

def f_query_one():
    f_clear_pub_boxes()
    clib.f_query_one()
    f_update_pub_list()

def f_btn_prev():
    f_prev_next_item('left')

def f_btn_nxt():
    f_prev_next_item('right')

def f_btn_doi():
    idx = next(i for i,[dbid,desc] in enumerate(clib.c_pub_data_local) if dbid=='DI')
    doi = clib.o_txt_pub[idx].get('1.0','end')
    url = 'https://doi.org/'+doi
    webbrowser.open(url)

def f_change_db_table(callback):
    clib.v_oid = 1
    clib.o_entry_bx.delete(0,tk.END)
    clib.o_entry_bx.insert(0,str(clib.v_oid))
    clib.v_db_current_table = callback
    f_query_one()

def f_update_record():
    clib.f_update_one()
    f_query_one()
    clib.o_btn[4]['highlightbackground'] = 'green'

def f_btn_openfile():
    idx = next(i for i,[dbid,desc] in enumerate(clib.c_pub_data_local) if dbid=='FN')
    file_name = clib.o_txt_pub[idx].get('1.0', 'end').rstrip()
    subprocess.call(['open', clib.c_file_dir+file_name])

def f_btn_toc():
    idx = next(i for i,[dbid,desc] in enumerate(clib.c_pub_data_local) if dbid=='FN')
    file_name = clib.o_txt_pub[idx].get('1.0', 'end').rstrip()
    subprocess.call(['open','-a','pdfoutliner.app',clib.c_file_dir+file_name])

# dictionary
d_func_match = {clib.c_btn_list[0][0]:f_query_one,
                clib.c_btn_list[1][0]:f_btn_prev,
                clib.c_btn_list[2][0]:f_btn_nxt,
                clib.c_btn_list[3][0]:f_btn_doi,
                clib.c_btn_list[4][0]:f_update_record,
                clib.c_btn_list[5][0]:f_btn_openfile,
                clib.c_btn_list[6][0]:f_btn_toc,
                clib.c_optmenu_list[0]:f_change_db_table}


def f_db_col_names():
    for [rq_id,rq_des,rq_data] in clib.c_db_dd_items:
        if type(rq_data[0])==tuple:
            for [data_id,data_des] in rq_data:
                clib.v_db_dd_col.append(data_id)
        else:
            clib.v_db_dd_col.append(rq_data[0])

def f_gui_place_labels():
    tk.Label(frame_gui, text='SLR publications', font='Helvetica 18 bold').grid(row=0,column=0,columnspan=3)
    tk.Label(frame_gui, text='To review:').grid(row=1,column=2,sticky='w')
    tk.Label(frame_gui, text='All selected:').grid(row=3,column=2,sticky='w')

def f_gui_place_interface():
    # buttons
    clib.o_btn = [None] * len(clib.c_btn_list)
    for i,[txt,row,col,clsp,stk] in enumerate(clib.c_btn_list):
        clib.o_btn[i] = tk.Button(frame_gui,text=txt,command=d_func_match[txt])
        clib.o_btn[i].grid(row=row,column=col,columnspan=clsp,sticky=stk)
    # option menus
    #___for i,[txt,row,col] in enumerate(c_optmenu_list):
    i = 0; [txt,row,col,clsp] = clib.c_optmenu_list
    if 1:
        clib.v_optmenu[i] = tk.StringVar(frame_gui)
        clib.v_optmenu[i].set(clib.c_optmenu_opt[0])
        tk.OptionMenu(frame_gui, clib.v_optmenu[i], *clib.c_optmenu_opt, command=f_change_db_table).grid(row=row,column=col,columnspan=clsp)
    # entry box
    clib.o_entry_bx = tk.Entry(frame_gui,width=5,justify='center')
    clib.o_entry_bx.grid(row=1,column=0)
    clib.o_entry_bx.insert(0,str(clib.v_oid))
    # info texts
    clib.o_txt_info = [None] * len(clib.c_txt_info)
    for i,[txt,row,col,hght,wdth,rwsp] in enumerate(clib.c_txt_info):
    #i = 0; [txt,row,col,hght,wdth,rwsp] = clib.c_txt_info
        clib.o_txt_info[i] = tk.Text(frame_gui,width=wdth,height=hght,font=(None,13))
        clib.o_txt_info[i].grid(row=row,column=col,rowspan=rwsp)

def f_gui_place_pub_data(start_row,start_col):
    v_start_row = start_row
    c_start_col = start_col
    clib.o_txt_pub = [None] * len(clib.c_pub_data_local)
    tk.Label(frame_gui, text='Publication Data', font='Helvetica 18 bold').grid(row=v_start_row,column=c_start_col,columnspan=3)
    for i,[db_id,db_des] in enumerate(clib.c_pub_data_local):
        tk.Label(frame_gui,text=db_id).grid(row=v_start_row+i+1,column=c_start_col)
        tk.Label(frame_gui,text=db_des).grid(row=v_start_row+i+1,column=c_start_col+1)
        idx = next(i for i,[dbid,hgt,rowspan] in enumerate(clib.c_pubdatalocal_height) if dbid==db_id)
        [dbid,hght,rowspan] = clib.c_pubdatalocal_height[idx]
        clib.o_txt_pub[i] = tk.Text(frame_gui,width=40,height=hght,font=(None,13))
        clib.o_txt_pub[i].grid(row=v_start_row+i+1,column=c_start_col+2,rowspan=rowspan)
        v_start_row = v_start_row+rowspan-1

def f_gui_place_data_items(start_row,start_col):
    # -- add EXC
    clib.o_txt_xtra_data = [None]
    tk.Label(frame_gui,text='EXC').grid(row=start_row,column=start_col)
    tk.Label(frame_gui,text='DataExtract class').grid(row=start_row,column=start_col+1)
    clib.o_txt_xtra_data = tk.Text(frame_gui,width=40,height=1,font=(None,13))
    clib.o_txt_xtra_data.grid(row=start_row,column=start_col+2,rowspan=1,sticky='w')
    #-- all data fields
    v_start_row = start_row+1
    c_start_col = start_col
    clib.o_txt_dd = [None] * len(clib.v_db_dd_col)
    for i,[rq_id,rq_des,rq_data] in enumerate(clib.c_db_dd_items):
        tk.Label(frame_gui, text=f'{rq_id} - {rq_des}', font='Helvetica 18 bold').grid(row=v_start_row,column=c_start_col,columnspan=3)
        v_start_row = v_start_row + 1
        # ---
        if type(rq_data[0])==tuple:
            for j,[data_id,data_des] in enumerate(rq_data):
                tk.Label(frame_gui,text=data_id).grid(row=v_start_row+j,column=c_start_col)
                tk.Label(frame_gui,text=data_des).grid(row=v_start_row+j,column=c_start_col+1)
                index = next(idx for idx,cid in enumerate(clib.v_db_dd_col) if cid == data_id)
                [hgt,rspn] = clib.d_txtdd_height.get(data_id,[1,1])
                clib.o_txt_dd[index] = tk.Text(frame_gui,width=60,height=hgt,font=(None,13))
                clib.o_txt_dd[index].grid(row=v_start_row+j,column=c_start_col+2,rowspan=rspn)
                v_start_row = v_start_row+rspn-1
        else:
            tk.Label(frame_gui,text=rq_data[0]).grid(row=v_start_row+i,column=c_start_col)
            tk.Label(frame_gui,text=rq_data[1]).grid(row=v_start_row+i,column=c_start_col+1)
            index = next(idx for idx,cid in enumerate(clib.v_db_dd_col) if cid == rq_data[0])
            [hgt,rspn] = clib.d_txtdd_height.get(rq_data[0],[1,1])
            clib.o_txt_dd[index] = tk.Text(frame_gui,width=60,height=hgt,font=(None,13))
            clib.o_txt_dd[index].grid(row=v_start_row+i,column=c_start_col+2,rowspan=rspn)
            v_start_row = v_start_row+rspn-1
        # ---
        v_start_row = v_start_row + len(rq_data)

def f_gui_left_key(event):
    #f_prev_next_item('left')
    return 1

def f_gui_right_key(event):
    #f_prev_next_item('right')
    return 1

# ---------- GUI ----------
gui = tk.Tk()
gui.title('SLR Data extraction GUI')
gui.geometry("1370x800") # (X * Y)
# key binding
gui.bind('<Left>', f_gui_left_key)
gui.bind('<Right>', f_gui_right_key)

# ---------- scrowl ----------
# create things
main_frame = tk.Frame(gui)
main_frame.pack(fill=tk.BOTH,expand=1)

my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

my_scrollbar = tk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview,width=30)
my_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

frame_gui = tk.Frame(my_canvas)

# configure things
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox('all')))
my_canvas.create_window((0,0),window=frame_gui,anchor='nw')

# ---------- work ----------
f_db_col_names()
f_gui_place_labels()
f_gui_place_interface()
f_gui_place_pub_data(start_row=5,start_col=0)
f_gui_place_data_items(start_row=0,start_col=3)

f_query_one()

# ---------- open WINDOW --------
gui.mainloop()
