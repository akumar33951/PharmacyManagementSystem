"""
author Akhil
"""


import sys
import datetime
import csv
import re
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


display_list = []
display_outs_list = []
display_expired = []
monthlist = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept',
             'oct', 'nov', 'dec']
monthdict = {'jan' : 1, 'feb' : 2, 'mar' : 3, 'apr' : 4, 'may' : 5, 'jun' : 6, 
             'jul': 7, 'aug': 8, 'sept' : 9, 'oct': 10, 'nov': 11, 'dec': 12}

# class defining the node's structure for the ternary tree 
class node:

    def __init__(self, data = None):
        self.key = data
        self.isLeaf = False
        self.comp_name = str
        self.expiry_date = str
        self.quan = int
        self.small = None
        self.equal = None
        self.big = None

    def expiry_date_upd(self, exp_date):
        self.expiry_date = exp_date

    def comp_name_upd(self,company_name):
        self.comp_name = company_name

    def quan_upd(self, quantity):
        self.quan = quantity

    def isleaf_upd(self, val):
        self.isLeaf = val

    def key_ret(self):
        return self.key  
    
    def small_ret(self):
        return self.small

    def equal_ret(self):
        return self.equal

    def big_ret(self):
        return self.big

    def expiry_date_ret(self):
        return self.expiry_date

    def comp_name_ret(self):
        return self.comp_name

    def quan_ret(self):
        return self.quan

    def isLeaf_ret(self):
        return self.isLeaf

#class defining methods for manipulating the ternary search tree
class med_rec:
    
    def __init__(self):
        self.root = node()

    def createNode(self,key):
        temp = node(key)
        return temp

    def insert_node(self, root, name, exp_date, company_name, quantity):   

        if not root:
            root = self.createNode(name[0])

        if name[0] < root.key_ret():
            root.small = self.insert_node(root.small, name, exp_date, company_name, quantity)

        elif name[0] > root.key_ret():
            root.big = self.insert_node(root.big_ret(), name, exp_date, company_name, quantity)

        elif name[0] == root.key_ret():
            if (name[1] == '.'): 
                root.expiry_date_upd(exp_date)
                root.comp_name_upd(company_name)
                root.quan_upd(quantity)
                root.isLeaf = True
                return root
            name = name[1:]
            root.equal = self.insert_node(root.equal_ret(), name, exp_date, company_name, quantity)
        return root

    def isLeaf(self, root):

        if root.isLeaf_ret():
            return True
        else:
            return False

    def isFreeNode(self, root):

        if root.small_ret() or root.equal_ret() or root.big_ret():
            return 0
        return 1

    def display(self, root, string, level): 

        if not root:
            return
        self.display(root.small_ret(), string, level)
        if level == 0:
            string = root.key_ret() + string[1:]
        else:
            string = string[:level] + root.key_ret() + string[level+1:]

        if root.isLeaf_ret():
            string = string[:level+1]
            med_dict = {"med_name": string, "comp_name": root.comp_name_ret(), "exp_date": root.expiry_date_ret(), "quantity": root.quan_ret()}
            global display_list
            display_list.append(med_dict)

        self.display(root.equal_ret(), string, level+1)
        self.display(root.big_ret(), string, level)
        
    def traverse(self, root, string, level, med_rec):

        if not root:
            return
        self.traverse(root.small_ret(), string, level, med_rec)
        if level == 0:
            string = root.key_ret() + string[1:]
        else:
            string = string[:level] + root.key_ret() + string[level+1:]
            
        if root.isLeaf_ret():
            string = string[:level+1] + '.'
            medlist = list()
            med_dict = {'Name': string, 'Company_Name':root.comp_name_ret(), 'Expiry_date':root.expiry_date_ret(), 'Quantity':root.quan_ret()}
            medlist.append(med_dict)
            med_rec.writerows(medlist)

        self.traverse(root.equal_ret(), string, level+1, med_rec)
        self.traverse(root.big_ret(), string, level, med_rec)

    def display_out_of_stock(self, root, string, level):

        if not root:
            return
        self.display_out_of_stock(root.small_ret(), string, level)
        if level == 0:
            string = root.key_ret() + string[1:]
        else:
            string = string[:level] + root.key_ret() + string[level+1:]
        
        if root.isLeaf_ret() and root.quan_ret() == 0:
            string = string[:level+1]
            med_dict = {"med_name": string, "comp_name": root.comp_name_ret(), "exp_date": root.expiry_date_ret(),
                        "quantity": root.quan_ret()}
            global display_outs_list
            display_outs_list.append(med_dict)

        self.display_out_of_stock(root.equal_ret(), string, level+1)
        self.display_out_of_stock(root.big_ret(), string, level)

    def display_expired(self, root, string, level):

        if not root:
            return
        self.display_expired(root.small_ret(), string, level)
        if level == 0:
            string = root.key_ret() + string[1:]
        else:
            string = string[:level] + root.key_ret() + string[level+1:]
                                
        if root.isLeaf_ret():
            """ extracts month and year from system's current time and date, and
                compares medicines Expiry date (month and year) with system's date 
            """
            date = str(datetime.datetime.now())
            date = date.split(" ")
            sys_year_month = date[0].split("-")
            med_month_num = int()
            med_month_year = root.expiry_date_ret().split(", ")
            med_month_name = med_month_year[0].lower() 
            for month_name in monthdict:
                if month_name == med_month_name:
                    med_month_num = monthdict[month_name]
            global display_expired
            if int(sys_year_month[0]) > int(med_month_year[1]):
                string = string[:level+1]
                med_dict = {"med_name": string, "comp_name": root.comp_name_ret(), "exp_date": root.expiry_date_ret(),
                            "quantity": root.quan_ret()}
                display_expired.append(med_dict)

            elif int(sys_year_month[0]) == int(med_month_year[1]):
                if med_month_num < int(sys_year_month[1]):
                    string = string[:level+1]
                    med_dict = {"med_name": string, "comp_name": root.comp_name_ret(), "exp_date": root.expiry_date_ret(),
                                "quantity": root.quan_ret()}
                    display_expired.append(med_dict)
                    
        self.display_expired(root.equal_ret(), string, level+1)
        self.display_expired(root.big_ret(), string, level)
        
    def search(self, root, string):

        if not root:
            return None

        if string[0] < root.key_ret():
            return self.search(root.small_ret(), string)
        elif string[0] > root.key_ret():
            return self.search(root.big_ret(), string)
        else:
            if (string[1] == '.'):
                if root.isLeaf_ret():
                    return root
                return None
            string = string[1:]
            return self.search(root.equal_ret(), string)

    def update(self, root, string = []):

        #creates a new window prompting user for updating medicine detail
        upd_med = Tk()
        upd_med.title("Update Window")
        upd_med.geometry("700x300")
        Label(upd_med, text="\t  UPDATE MEDICINE DETAIL").grid(row=1, column=0, columnspan=3)
        Label(upd_med, text=' ' * 16 + '*' * 120).grid(row=3, column=0, columnspan=3)

        if not root:
            Label(upd_med, text="Empty database").grid(row=5, column=1)
            return
        
        #method that is called when submit button on update window is pressed
        def updt(bt):
            root = self.search(medicines.root, med_name.get().strip().lower() + '.')
            if not root:
                messagebox.showinfo("Unknown medicine","' " + med_name.get().strip() + " ' is not present in the database") 
                return
            else:
                bt.grid_forget()
                def cpy():
                    root.comp_name_upd(comp_name.get().strip())
                    root.expiry_date_upd(exp_date.get().strip())
                    root.quan_upd(int(quan.get().strip()))

                    upd_med.destroy()

                Label(upd_med, text="Enter new Company name").grid(row=10, column=0)
                Label(upd_med, text="Enter new Expiry date").grid(row=11, column=0)
                Label(upd_med, text="Enter Quantity").grid(row=12, column=0)

                comp_name = Entry(upd_med, width=50)
                comp_name.focus()
                comp_name.grid(row=10, column=1)

                exp_date = Entry(upd_med, width=50)
                exp_date.focus()
                exp_date.grid(row=11, column=1)

                quan = Entry(upd_med, width=50)
                quan.focus()
                quan.grid(row=12, column=1)
                #To check if company name, quantity and expiry date are valid
                def chk():
                    if bool(re.search('^[a-zA-Z]*$', comp_name.get().strip())) is False:
                        messagebox.showwarning("Warning", "Enter a valid company name") 
                        return
                    
                    dtime = str(datetime.datetime.now()).split(" ")
                    date = dtime[0].split("-")
                    inpdate = exp_date.get().split(", ")
                    
                    if len(inpdate) < 2:
                        messagebox.showwarning("Warning", "Enter a valid expiry date") 
                        return
                    
                    global monthlist, monthdict
                    valid_exp_date = False
                    for month in monthlist:
                        if inpdate[0].lower() == month:
                            if int(date[0]) <= int(inpdate[1]) and int(inpdate[1]) <= int(date[0]) + 5:
                                if int(date[0]) == int(inpdate[1]):
                                    if monthdict[month] > int(date[1]):
                                        valid_exp_date = True
                                        break
                                else:
                                    valid_exp_date = True
                                    break
                    
                    if valid_exp_date is False:
                        messagebox.showwarning("Warning", "Enter a valid expiry date") 
                        return
                    
                    if quan.get().strip().lower().isdigit() == False or int(quan.get().strip()) < 0:
                        messagebox.showwarning("Warning", "Enter a valid number in quantity field") 
                        return
                    else:
                        cpy()

                Button(upd_med, width = 20, text="Submit", command=chk).grid(row=13, column=2)

        Label(upd_med, text="Enter medicine name to be updated").grid(row=6, column=0)

        med_name = Entry(upd_med, width=50)
        med_name.focus()   
        med_name.grid(row=6, column=1)

        bt = Button(upd_med, width = 20, text="Enter", command=lambda : updt(bt))
        bt.grid(row=6, column=2) 
        upd_med.mainloop()

    def update_quantity(self, root, string = []):
        
        #creates a new window prompting user for updating medicine quantity
        upd_med = Tk()
        upd_med.title("Update Window")
        upd_med.geometry("700x300")
        Label(upd_med, text="\t  UPDATE MEDICINE QUANTITY").grid(row=1, column=0, columnspan=3)
        Label(upd_med, text=' ' * 16 + '*' * 120).grid(row=3, column=0, columnspan=3)

        if not root:
            Label(upd_med, text="Empty database").grid(row=5, column=1)
            return

        def updt(bt):
            root = self.search(medicines.root, med_name.get().strip().lower() + '.')
            if not root:
                messagebox.showinfo("Unknown medicine","' " + med_name.get().strip() + " ' is not present in the database") 
                return
            else:
                bt.grid_forget()
                def cpy(new_quan):
                    root.quan_upd(new_quan)
                    upd_med.destroy()

                Label(upd_med, text="Enter quantity of medicine added/removed").grid(row=10, column=0)
                
                quan = Entry(upd_med, width=50)
                quan.focus()
                quan.grid(row=10, column=1)
                
                def chk():
                    if quan.get().strip()[0] == '-':
                        if quan.get().strip()[1:].isdigit():
                            if root.quan_ret() + int(quan.get().strip()) > 0:
                                cpy(root.quan_ret() + int(quan.get().strip()))
                            else:
                                messagebox.showwarning("Warning", "Not enough medicine in stock") 
                                return
                        else:
                            messagebox.showwarning("Warning", "Enter a valid number in quantity field") 
                            return
                    elif quan.get().strip().isdigit() is False:
                        messagebox.showwarning("Warning", "Enter a valid number in quantity field") 
                        return
                    else:
                        cpy(root.quan_ret() + int(quan.get().strip()))

                Button(upd_med, width = 20, text="Submit", command=chk).grid(row=13, column=2)

        Label(upd_med, text="Enter medicine name to be updated").grid(row=6, column=0)

        med_name = Entry(upd_med, width=50)
        med_name.focus()   
        med_name.grid(row=6, column=1)

        bt = Button(upd_med, width = 20, text="Enter", command=lambda : updt(bt))
        bt.grid(row=6, column=2) 
        upd_med.mainloop()

    def delete_node(self, root, string):
        
        tmp = self.search(root, string)
        if tmp == None:
            return tmp
        
        tmp.isleaf_upd(0)
        tmp.comp_name = [] 
        tmp.expiry_date = []  
        return tmp

#class containing methods for handling user interface
class user_menu:

    def insert_medicine(self):
        insrt_med = Tk()
        insrt_med.title("Insert Medicine")
        insrt_med.geometry("700x300")
        Label(insrt_med, text="\t  INSERT MEDICINE").grid(row=1, column=0, columnspan=3)
        Label(insrt_med, text=' ' * 16 + '*' * 120).grid(row=3, column=0, columnspan=3)
        Label(insrt_med, text="Enter Medcine name").grid(row=6, column=0)

        med_name = Entry(insrt_med, width=50)
        med_name.focus()
        med_name.grid(row=6, column=1)
        
        def search_in_lib(bt):
            if not re.search('^[a-zA-Z]*$', med_name.get().strip()):
                messagebox.showwarning("Warning", "Enter a valid medicine name")
                return
            
            bt.grid_forget()
            if medicines.search(medicines.root, med_name.get().strip().lower() + '.') != None:
                Label(insrt_med, text = "' " + med_name.get().strip()[:len(med_name.get().strip())] + "' is already present in the database").grid(row=7,column=1)
                Label(insrt_med, text="Do you want to update its record details instead?").grid(row=8,column=1)     # instead try yes/no message box
                def yes():
                    medicines.update(medicines.root, med_name.get().strip() + '.')
                    insrt_med.destroy()
                def no():
                    insrt_med.destroy()
                
                Button(insrt_med, width = 20, text="YES", command=yes).grid(row=9, column=0)
                Button(insrt_med, width = 20, text="NO", command=no).grid(row=9, column=2)
            
            else:

                Label(insrt_med, text="Enter Expiry date").grid(row=9, column=0)
                Label(insrt_med, text="Enter Company name of the medicine").grid(row=8, column=0)
                Label(insrt_med, text="Enter quantity of the medicine").grid(row=10, column=0)

                company_name = Entry(insrt_med, width=50)  
                company_name.focus()
                company_name.grid(row=8, column=1)

                exp_date = Entry(insrt_med, width=50)
                exp_date.focus()
                exp_date.grid(row=9, column=1)

                quan = Entry(insrt_med, width=50) 
                quan.focus()
                quan.grid(row=10, column=1)

                def chk():
                    if bool(re.search('^[a-zA-Z]*$', company_name.get().strip())) is False:
                        messagebox.showwarning("Warning", "Enter a valid company name") 
                        return
                    
                    dtime = str(datetime.datetime.now()).split(" ")
                    date = dtime[0].split("-")
                    inpdate = exp_date.get().split(", ")
                    
                    if len(inpdate) < 2:
                        messagebox.showwarning("Warning", "Enter a valid expiry date") 
                        return
                    
                    global monthlist, monthdict
                    valid_exp_date = False
                    for month in monthlist:
                        if inpdate[0].lower() == month:
                            if int(date[0]) <= int(inpdate[1]) and int(inpdate[1]) <= int(date[0]) + 5:
                                if int(date[0]) == int(inpdate[1]):
                                    if monthdict[month] > int(date[1]):
                                        valid_exp_date = True
                                        break
                                else:
                                    valid_exp_date = True
                                    break
                    
                    if valid_exp_date is False:
                        messagebox.showwarning("Warning", "Enter a valid expiry date") 
                        return
                    
                    if quan.get().strip().lower().isdigit() == False or int(quan.get().strip()) < 0:
                        messagebox.showwarning("Warning", "Enter a valid number in quantity field") 
                        return

                    else:
                        medicines.root = medicines.insert_node(medicines.root, med_name.get().strip().lower() + '.', exp_date.get().strip(), company_name.get().strip(), int(quan.get().strip()))

                        insrt_med.destroy()

                Button(insrt_med, width=20, text='Submit', command=chk).grid(row=11, column=2)
                
        bt = Button(insrt_med, width=20, text='Submit', command = lambda : search_in_lib(bt))
        bt.grid(row=6, column=2)
        insrt_med.mainloop()

    def delete_medicine(self):
        delete_win = Tk()
        delete_win.title("Delete iwndow")
        delete_win.geometry("700x300")
        Label(delete_win, text="\t  DELETE MEDICINE RECORD").grid(row=1, column=0, columnspan=3)
        Label(delete_win, text=' ' * 16 + '*' * 120).grid(row=3, column=0, columnspan=3)
        Label(delete_win, text="Enter Medcine name to be deleted").grid(row=6, column=0)

        if not medicines.root:
            messagebox.showinfo("No records", "Empty database") 
            return

        def dlt():
            if medicines.delete_node(medicines.root, med_name.get().strip().lower() + '.'):
                messagebox.showinfo("Success", "'" + med_name.get().strip() + "' has been deleted successfully") 
                return
            else:
                messagebox.showinfo("Unknown medicine", "'" + med_name.get().strip() + "' is not present in the database") 
                return
        med_name = Entry(delete_win, width=50)
        med_name.focus()
        med_name.grid(row=6, column=1)

        Button(delete_win, width = 20, text="Enter", command=dlt).grid(row=6, column=2)
        delete_win.mainloop()

    def update_medicine_info(self):
        medicines.update(medicines.root)
        
    def update_medicine_quantity(self):
        medicines.update_quantity(medicines.root)
        
    def search_medicine(self):

        search_win = Tk()
        search_win.title("Search Window")
        search_win.geometry("700x300")
        Label(search_win, text="\t  DELETE MEDICINE RECORD").grid(row=1, column=0, columnspan=3)
        Label(search_win, text=' ' * 16 + '*' * 120).grid(row=3, column=0, columnspan=3)
        Label(search_win, text="Enter Medcine name to be searched").grid(row=6, column=0)

        if not medicines.root:
            messagebox.showinfo("No records", "Empty database") 
            return
        
        def srch():
            tmp = medicines.search(medicines.root, med_name.get().strip().lower() + '.')
            if tmp != None:
                Label(search_win, text="Company name").grid(row=8, column=0)
                Label(search_win, text="Expiry date").grid(row=8, column=1)
                Label(search_win, text="Quantity").grid(row=8, column=2)

                Label(search_win, text=tmp.comp_name).grid(row=9, column=0)
                Label(search_win, text=tmp.expiry_date).grid(row=9, column=1)
                Label(search_win, text=tmp.quan).grid(row=9, column=2)

            else:
                messagebox.showinfo("Unknown medicine", "'" + med_name.get().strip() + "' is not present in the database") 
                return
            
        med_name = Entry(search_win, width=50)
        med_name.focus()
        med_name.grid(row=6, column=1)

        Button(search_win, width = 20, text="Enter", command=srch).grid(row=6, column=2)
        search_win.mainloop()

    def show_each_medicine(self):
        show_win = Tk()
        show_win.geometry("500x500")
        show_win.title("Medicine record")
        
        wrapper1 = LabelFrame(show_win, text="\tMEDICINE RECORDS\n\n" + "*" * 90 + "\n")
        wrapper1.pack(fill="both", expand="yes", padx = 10, pady = 10)
        
        trv = ttk.Treeview(wrapper1, columns = (1,2,3,4), show ="headings", height = "22")
        trv.pack()
        
        trv.heading(1, text = "Medicine name")
        trv.heading(2, text = "Company name")
        trv.heading(3, text = "Expiry date")
        trv.heading(4, text = "Quantity")
        trv.column("1", width = 100, anchor ='c')
        trv.column("2", width = 100, anchor ='c')
        trv.column("3", width = 100, anchor ='c')
        trv.column("4", width = 100, anchor ='c')
        
        string = str()
        
        global display_list
        display_list = []

        medicines.display(medicines.root, string, 0)

        for med_dict in display_list:
            med = med_dict["med_name"][0:1].upper() + med_dict["med_name"][1:]
            output_list = [ med, med_dict["comp_name"], med_dict["exp_date"], med_dict["quantity"]]
            trv.insert('', 'end', values=output_list)
        
        show_win.mainloop()

    def show_out_of_stock_medicines(self):
        show_win = Tk()
        show_win.geometry("500x500")
        show_win.title("Out of stock medicines")
        
        wrapper1 = LabelFrame(show_win, text="\tOUT OF STOCK MEDICINES\n\n" + "*" * 92 + "\n")
        wrapper1.pack(fill="both", expand="yes", padx = 10, pady = 10)
        
        trv = ttk.Treeview(wrapper1, columns = (1,2,3,4), show ="headings", height = "22")
        trv.pack()
        
        trv.heading(1, text = "Medicine name")
        trv.heading(2, text = "Company name")
        trv.heading(3, text = "Expiry date")
        trv.heading(4, text = "Quantity")
        trv.column("1", width = 105, anchor ='c')
        trv.column("2", width = 105, anchor ='c')
        trv.column("3", width = 100, anchor ='c')
        trv.column("4", width = 100, anchor ='c')
        
        string = str()
        
        global display_outs_list
        display_outs_list = []

        medicines.display_out_of_stock(medicines.root, string, 0)

        for med_dict in display_outs_list:
            med = med_dict["med_name"][0:1].upper() + med_dict["med_name"][1:]
            output_list = [ med, med_dict["comp_name"], med_dict["exp_date"], med_dict["quantity"]]
            trv.insert('', 'end', values=output_list)
        
        show_win.mainloop()

    def show_expired_medicines(self):
        show_win = Tk()
        show_win.geometry("500x500")
        show_win.title("Expired Medicines")
        
        wrapper1 = LabelFrame(show_win, text="\tEXPIRED MEDICINES\n\n" + "*" * 90 + "\n")
        wrapper1.pack(fill="both", expand="yes", padx = 10, pady = 10)
        
        trv = ttk.Treeview(wrapper1, columns = (1,2,3,4), show ="headings", height = "22")
        trv.pack()
        
        trv.heading(1, text = "Medicine name")
        trv.heading(2, text = "Company name")
        trv.heading(3, text = "Expiry date")
        trv.heading(4, text = "Quantity")
        trv.column("1", width = 100, anchor ='c')
        trv.column("2", width = 100, anchor ='c')
        trv.column("3", width = 100, anchor ='c')
        trv.column("4", width = 100, anchor ='c')
        
        string = str()
        
        global display_list
        display_list = []

        medicines.display_expired(medicines.root, string, 0)

        for med_dict in display_expired:
            med = med_dict["med_name"][0:1].upper() + med_dict["med_name"][1:]
            output_list = [ med, med_dict["comp_name"], med_dict["exp_date"], med_dict["quantity"]]
            trv.insert('', 'end', values=output_list)
        
        show_win.mainloop()

    def menu(self):

        menu_win = Tk()
        menu_win.title("Menu")
        Label(menu_win, text="CHEMIST AND DRUGSHOP").grid(row=0, column=0, columnspan=3)
        Label(menu_win, text='*' * 80).grid(row=1, column=0, columnspan=3)
        Label(menu_win, text='-' * 80).grid(row=3, column=0, columnspan=3)

        Label(menu_win, text="Stock Maintenance").grid(row=2, column=0)
        Button(menu_win, text='Add product to Stock', width=25, command=self.insert_medicine).grid(row=4, column=0)
        Button(menu_win, text='Update medicine detail', width=25, command=self.update_medicine_info).grid(row=5, column=0)
        Button(menu_win, text='Update medicine quantity', width=25, command=self.update_medicine_quantity).grid(row=6, column=0)
        Button(menu_win, text='Delete product from Stock', width=25, command=self.delete_medicine).grid(row=7, column=0)
 
        Label(menu_win, text="Access Database").grid(row=2, column=1)
        Button(menu_win, text='Search', width=25, command=self.search_medicine).grid(row=4, column=1)
        Button(menu_win, text='Medicine Record', width=25, command=self.show_each_medicine).grid(row=5, column=1)
        Button(menu_win, text='Out of stock medicines', width=25, command=self.show_out_of_stock_medicines).grid(row=6, column=1)
        Button(menu_win, text='Expired medicines', width=25, command=self.show_expired_medicines).grid(row=7, column=1)
        
        Label(menu_win, text='-' * 80).grid(row=12, column=0, columnspan=3)
        menu_win.mainloop()

#object for storing medicines details in ternary search tree 
medicines = med_rec()
medicines.root = []
med_rec = csv.DictReader(open("MedRecords.csv", mode = 'r'))
for lines in med_rec:
    medicines.root = medicines.insert_node(medicines.root, lines["Name"], lines["Expiry_date"], lines["Company_Name"], int(lines["Quantity"]))

ob = user_menu()
ob.menu()

headings = ['Name', 'Company_Name', 'Expiry_date', 'Quantity']
with open('MedRecords.csv', mode = 'w') as file:
    med_rec = csv.DictWriter(file, fieldnames = headings)
    med_rec.writeheader()
    string = str()
    medicines.traverse(medicines.root, string, 0, med_rec)
