# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:05:59 2019

@author: charles.tan
"""

import tkinter as tk
from functions import create_sql_file

class Application(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.init_window()
        
    def init_window(self):
        self.master.title('PLU Script Generator')
        self.variables = Variables(self.master)
        self.buttons = Buttons(self.master, self.variables)
        self.body = Body(self.master, self.buttons, self.variables)
        
class Buttons(tk.Frame):
    def __init__(self, master, variables):
        self.generate_sql_button = tk.Button(master, text='Generate SQL', command=
                                                lambda: create_sql_file(variables.filename_preview_var.get(), variables.start_date_var.get(),
                                                                        variables.end_date_var.get(), variables.contact_name_var.get(), variables.region_var.get(),
                                                                        variables.plu_names_var.get(), variables.plu_ids_var.get(),variables.ad_ids_var.get()))
        self.generate_sql_button.grid(row=7, column=0, columnspan=3, sticky=tk.E+tk.W)

class Body(tk.Frame):
    def __init__(self, master, buttons, variables):
        # ANALYST NAME and REGION
        self.contact_name_label = tk.Label(master, text='Contact Name')
        self.contact_name_label.grid(row=0, column=0)
        self.contact_name_entry = tk.Entry(master, textvariable=variables.contact_name_var)
        self.contact_name_entry.grid(row=0, column=1)
        #######
        # have to manually assign regions now because OptionMenu is broken on python 3
        self.region_optionmenu = tk.OptionMenu(master, variables.region_var, 'APAC', 'EMEA', 'NA')
        self.region_optionmenu.grid(row=0, column=2)
        
        # CAMPAIGN START/END DATES
        self.start_date_label = tk.Label(master, text='Campaign Start Date')
        self.start_date_label.grid(row=1, column=0)
        self.start_date_entry = tk.Entry(master, textvariable=variables.start_date_var,
                                         justify=tk.CENTER)
        self.start_date_entry.grid(row=1, column=1)
        self.end_date_label = tk.Label(master, text='End Date')
        self.end_date_label.grid(row=2, column=0)
        self.end_date_entry = tk.Entry(master, textvariable=variables.end_date_var,
                                       justify=tk.CENTER)
        self.end_date_entry.grid(row=2, column=1)
        
        def get_plu_names_stringvar(event):
            variables.plu_names_var.set(self.plu_name_text.get('1.0', 'end'))
        
        # PLU NAMES
        self.plu_name_label = tk.Label(master, text='PLU Names')
        self.plu_name_label.grid(row=3, column=0)
        self.plu_name_text = tk.Text(master, height=10, width=50)
        self.plu_name_text.grid(row=4, column=0)
        # bind it such that anytime a key is release (i.e. a letter is typed)
        # we update the stringVar for plu_names.
        self.plu_name_text.bind('<KeyRelease>', get_plu_names_stringvar)
        
        def get_plu_ids_stringvar(event):
            variables.plu_ids_var.set(self.plu_id_text.get('1.0', 'end'))
        
        # PLU IDS
        self.plu_id_label = tk.Label(master, text='PLU/List IDs')
        self.plu_id_label.grid(row=3, column=1)
        self.plu_id_text = tk.Text(master, height=10, width=12)
        self.plu_id_text.grid(row=4, column=1)
        self.plu_id_text.bind('<KeyRelease>', get_plu_ids_stringvar)
        
        def get_ad_ids_stringvar(event):
            variables.ad_ids_var.set(self.ad_id_text.get('1.0', 'end'))
        
        # AD IDS
        self.ad_id_label = tk.Label(master, text='Ad IDs')
        self.ad_id_label.grid(row=3, column=2)
        self.ad_id_text = tk.Text(master, height=10, width=12)
        self.ad_id_text.grid(row=4, column=2)
        self.ad_id_text.bind('<KeyRelease>', get_ad_ids_stringvar)
        
        # DECIDE FILENAME
        self.decide_filename_label = tk.Label(master, text='Filename:')
        self.decide_filename_label.grid(row=5, column=0)
        self.decide_filename_entry = tk.Entry(master, textvariable=variables.decide_filename_var)
        self.decide_filename_entry.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E)
        self.filename_preview_label = tk.Label(master, text='Preview:')
        self.filename_preview_label.grid(row=6, column=0)
        self.filename_preview = tk.Label(master, textvariable=variables.filename_preview_var)
        self.filename_preview.grid(row=6, column=1)
        
class Variables(tk.Frame):
    def __init__(self, master):
        self.contact_name_var = tk.StringVar()
        self.region_var = tk.StringVar()
        self.region_var.set('APAC')
        self.start_date_var = tk.StringVar()
        self.start_date_var.set('MM/DD/YYYY')
        self.end_date_var = tk.StringVar()
        self.end_date_var.set('MM/DD/YYYY')
        self.plu_names_var = tk.StringVar()
        self.plu_ids_var = tk.StringVar()
        self.ad_ids_var = tk.StringVar()
        self.decide_filename_var = tk.StringVar()
        self.decide_filename_var.set('CHOOSE FILENAME')
        self.filename_preview_var = tk.StringVar()
        def change_label(*args):
            name_string = self.decide_filename_var.get()
            name_string = name_string.replace(' ', '_')
            final_string = '2542116_'+self.end_date_var.get().replace('/', '')+'_PLU_'+name_string+'.sql'
            self.filename_preview_var.set(final_string)
        self.end_date_var.trace('w', change_label)
        self.decide_filename_var.trace('w', change_label)

    

root = tk.Tk()
app = Application(master=root)
app.mainloop()
        