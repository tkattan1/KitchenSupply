from tkinter import *
from tkinter import ttk
import csv
import json
from tkinter import messagebox
from time import ctime


class Customer:
    def __init__(self, accNum, name, PIN, balance):
        self.__accNum = accNum
        self.__name = name
        self.__PIN = PIN
        self.__balance = balance

    @property
    def accNum(self):
        return self.__accNum

    @property
    def name(self):
        return self.__name.capitalize()

    @property
    def PIN(self):
        return self.__PIN

    @property
    def balance(self):
        return f'{self.__balance}'

    @balance.setter
    def balance(self, newBalance):
        self.__balance = newBalance

    def __str__(self):
        """Override the string representation of a student"""
        # Use the properties or you are not executing the formatting
        return f'{self.name}'

class Product:
    def __init__(self, ID, description, quantity, price):
        self.__ID = ID
        self.__description = description
        self.__quantity = quantity
        self.__price = price

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, id):
        self.__ID = id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, productName):
        self.__description = productName

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, newQuantity):
        self.__quantity = newQuantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, newPrice):
        self.__price = newPrice

    def __str__(self):
        """Override the string representation of a product"""
        # Use the properties or you are not executing the formatting
        return f'{self.__description}: {self.__quantity} in stock. ${self.__price}'

class Attachment(Product):
    def __init__(self, material, attachedTo, ID, description, quantity, price):
        super().__init__(ID, description, quantity, price)
        self.material  = material
        self.attachedTo = attachedTo


#Create and initialize global variables
customer_roster = list()
product_roster = list()
product_names = list()
cart = list()
quantityInStock = list()
employees = list()
customers = list()
totalBalance = 0
accNum = 0
balance = 0
attach = None
mater = None
pID = None
pDesc = None
quant = None
pri = None
isEmp = False
edit_mode = False
edit_index = 0
tot = 0
current_user = None
userBalance = None
quantityToBePurchased = 0

#read customers file and store in customer_roster
with open('customers.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        customer_roster.append(Customer(row[0], row[1], row[2], row[3]))

#read products file and store in product_roster
with open('products.json', 'r') as fp:
    products = json.load(fp)

#create objects for every key and value in the json file
for k,v in products.items():
    ID = k
    material = None
    attachedTo = None
    try:
        material = v['Material']
        attachedTo = v['AttachedTo']
    except KeyError:
        pass
    description = v['Description']
    qty = v['Quantity']
    prix = v['Price']
    if material == None and attachedTo == None:
        product_roster.append(Product(ID,description,qty,prix))
    else:
        product_roster.append(Attachment(material, attachedTo, ID, description, qty, prix))

#this function gets the name and returns it from the name combobox
def getName(event):
    newName = name.get()
    name.set(newName)
    return name

#function that executes when ok button next to name is clicked
def ok_click():
    global isEmp, total, tot, name, pin, att, mat, productID, productDesc, quantity, price, current_user, name_cmbx
    total.set("")
    tot = 0
    pin.set("")
    att.set("")
    mat.set("")
    productID.set("")
    productDesc.set("")
    quantity.set("")
    price.set("")
    indexOfCustomer = name_cmbx.current()
    current_user = customer_roster[indexOfCustomer]
    for c in customer_roster:
        if name.get() == c.name and c.balance == '0.00' and c.PIN == '4900':
            isEmp = True
            attachesTo['state'] = NORMAL
            product_id['state'] = NORMAL
            price_cmbx['state'] = NORMAL
            material_entry['state'] = NORMAL
            product_name_cmbx['state'] = NORMAL
            quantity_entry['state'] = NORMAL
            total_entry['state'] = DISABLED
            modify_button['relief'] = SUNKEN
            add_to_button['relief'] = SUNKEN
            Add_button['relief'] = SUNKEN
            purchase_button['relief'] = SUNKEN
            delete_product_button['relief'] = SUNKEN
            break
    for c in customer_roster:
        if name.get() == c.name and c.balance != '0.00' and c.PIN != '4900':
            isEmp = False
            total_entry['state'] = DISABLED
            attachesTo['state'] = DISABLED
            product_id['state'] = DISABLED
            price_cmbx['state'] = DISABLED
            material_entry['state'] = DISABLED
            product_name_cmbx['state'] = DISABLED
            quantity_entry['state'] = DISABLED
            add_to_button['relief'] = SUNKEN
            modify_button['relief'] = SUNKEN
            Add_button['relief'] = SUNKEN
            purchase_button['relief'] = SUNKEN
            delete_product_button['relief'] = SUNKEN
            break
    return isEmp

edit_prod = None

#this function executes when edit button is clicked by Employee
def edit_product(event):
    global edit_index, edit_mode,edit_prod, product_list, product_id
    # Get index from listbox to get reference to student object in roster
    edit_mode = True
    edit_index = product_list.curselection()[0]
    edit_prod = product_roster[edit_index]
    quantity_entry['state'] = NORMAL
    add_to_button['relief'] = RAISED
    if current_user.PIN == '4900' and current_user.balance == '0.00':
        add_to_button['relief'] = SUNKEN
    if isinstance(edit_prod, Attachment):
        att.set(edit_prod.attachedTo)
        mat.set(edit_prod.material)
        productID.set(edit_prod.ID)
        productDesc.set(edit_prod.description)
        quantity.set(edit_prod.quantity)
        price.set(edit_prod.price)
    else:
        att.set("")
        mat.set("")
        productID.set(edit_prod.ID)
        productDesc.set(edit_prod.description)
        quantity.set(edit_prod.quantity)
        price.set(edit_prod.price)

#this function executes to delete items from cart with every double click
#it adds back the quantity to the product list
def delete_cart_item(event):
    global edit_index, cart, cart_list, tot, total, product_roster
    edit_index = cart_list.curselection()[0]
    itemToBeDel = cart[edit_index]
    unformattedPrice = itemToBeDel.price
    formattedPrice = float(unformattedPrice)
    formattedQuant = int(itemToBeDel.quantity)
    tot = tot - (formattedPrice * formattedQuant)
    if tot >= 0:
        total.set(tot)
    else:
        total.set(0)

    for item in cart:
        for prod in product_roster:
            if item.description == prod.description:
                prod.quantity = int(prod.quantity) + int(item.quantity)
                if prod.quantity <= 0:
                    quantity.set(0)
                    prod.quantity = 0
                else:
                    quantity.set(prod.quantity)
    product_list.delete(0, END)
    for row in product_roster:
        product_list.insert(END, row)

    cart.pop(edit_index)
    cart_list.delete(edit_index)

#this function executes when adding items to cart (for customers only)
def add_item_click():
    global isEmp, newItem, tot, total, realquant, realprice,edit_prod, attach, edit_index
    attach = att.get()
    mater = mat.get()
    pID = productID.get()
    pDesc = productDesc.get()
    quant = quantity.get()
    pri = price.get()
    order_names = []
    try:
        if quantity.get() <= edit_prod.quantity and isinstance(edit_prod, Attachment):
            newOrder = Attachment(mater, attach, pID, pDesc, quant, pri)
            cart.append(newOrder)
            order_names.append(newOrder.description)
            order_names.append(newOrder.quantity)
            cart_list.insert(END, order_names)
        elif quantity.get() <= edit_prod.quantity:
            newOrder = Product(pID,pDesc,quant, pri)
            cart.append(newOrder)
            order_names.append(newOrder.description)
            order_names.append(newOrder.quantity)
            cart_list.insert(END, order_names)
        else:
            messagebox.showinfo("Error", "Quantity is too high")
        realprice = float(pri)
        realquant = int(quant)
        tot = tot + (realquant * realprice)
        total.set(tot)

        for item in cart:
            for prod in product_roster:
                if item.description == prod.description:
                    prod.quantity = int(prod.quantity) - int(item.quantity)
                    if prod.quantity <= 0:
                        quantity.set(0)
                        prod.quantity = 0
                    else:
                        quantity.set(prod.quantity)
        product_list.delete(0,END)
        for row in product_roster:
            product_list.insert(END,row)

        if realquant == 0:
            messagebox.showinfo("Error", "Must enter quantity greater than 0.")
            cart.pop(edit_index)
            cart_list.delete(edit_index)

    except IndexError:
        pass

#this function authenticates after clicking the ok button next to the pin_entry
def check_pin():
    global pin, name, current_user, userBalance, modify_button
    userBalance = current_user.balance
    if pin.get() == current_user.PIN:
      messagebox.showinfo("Logged In", f'Hello {current_user.name}\nCurrent Balance: ${userBalance}')
      purchase_button['relief'] = RAISED
      if pin.get() == '4900' and current_user.balance == '0.00':
          modify_button['relief'] = RAISED
          Add_button['relief'] = RAISED
          purchase_button['relief'] = SUNKEN
          delete_product_button['relief'] = RAISED
    else:
        messagebox.showinfo("Error", "Wrong PIN")

#this function executes when customer has been authenticated and proceeds to purchase product
def purchaseItems():
    global tot, total, current_user, userBalance, cart, newCustomerList, my_list, productsInCart, quantities
    customer_balance = float(userBalance)
    if customer_balance >= tot:
        current_user.balance = customer_balance - tot
        messagebox.showinfo("Success", f"{current_user.name}'s current balance: {current_user.balance}")

        newCustomerList = [[customer_roster[0].accNum, customer_roster[0].name, customer_roster[0].PIN,
                           customer_roster[0].balance],
                           [customer_roster[1].accNum, customer_roster[1].name, customer_roster[1].PIN,
                           customer_roster[1].balance],
                           [customer_roster[2].accNum, customer_roster[2].name, customer_roster[2].PIN,
                           customer_roster[2].balance],
                           [customer_roster[3].accNum, customer_roster[3].name, customer_roster[3].PIN,
                           customer_roster[3].balance],
                           [customer_roster[4].accNum, customer_roster[4].name, customer_roster[4].PIN,
                           customer_roster[4].balance]]
        productsInCart = []
        quantities = []
        for items in cart:
            productsInCart.append(items.description)
            quantities.append(items.quantity)

        with open('customers.csv', 'w', newline="") as f:
             writer = csv.writer(f)
             writer.writerows(newCustomerList)
        with open('receipt.csv', 'w') as f:
            writer = csv.writer(f)
            my_list = [current_user.name, tot, ctime(), productsInCart, quantities]
            writer.writerow(my_list)
    else:
        messagebox.showinfo("Error", "Insufficient funds.")

line = dict()

#this function executes when employee adds a brand new item to the product list
def addItems():
    global quantity, product_roster, attach, mater, pID, pDesc, quant, pri, edit_prod, product_list, line
    attach = att.get()
    mater = mat.get()
    pID = productID.get()
    pDesc = productDesc.get()
    quant = quantity.get()
    pri = price.get()
    if attach == "" and mater == "" and pID != "" and pDesc != "" and quant != "" and pri != "":
        newItem = Product(pID, pDesc, quant, pri)
        product_roster.append(newItem)
        product_list.insert(END, newItem)
    elif attach != "" and mater != "" and pID != "" and pDesc != "" and quant != "" and pri != "":
        newItem = Attachment(attach, mater, pID, pDesc, quant, pri)
        product_roster.append(newItem)
        product_list.insert(END, newItem)

    for p in product_roster:
        if isinstance(p, Attachment):
            material = p.material
            attachedTo = p.attachedTo
            ID = p.ID
            description = p.description
            qty = p.quantity
            prix = p.price
            line = {ID : {"Material" : material, "AttachedTo": attachedTo, "Description": description, "Quantity": qty, "Price": prix}}
        else:
            ID = p.ID
            description = p.description
            qty = p.quantity
            prix = p.price
            line = {ID: {"Description": description, "Quantity": qty, "Price": prix}}

#        line += line
#    print(line)
#    with open('products.json', 'w') as fp:
 #       json.dump(line, fp)

#this option is for editing products in the product list by employees
def modifyItems():
    global quantity, product_roster, attach, mater, pID, pDesc, quant, pri, edit_index, product_list, line
    product_roster.pop(edit_index)
    product_list.delete(edit_index)
    attach = att.get()
    mater = mat.get()
    pID = productID.get()
    pDesc = productDesc.get()
    quant = quantity.get()
    pri = price.get()
    if attach == "" and mater == "" and pID != "" and pDesc != "" and quant != "" and pri != "":
        newItem = Product(pID, pDesc, quant, pri)
    elif attach != "" and mater != "" and pID != "" and pDesc != "" and quant != "" and pri != "":
        newItem = Attachment(attach, mater, pID, pDesc, quant, pri)
    product_roster.append(newItem)
    product_list.insert(END, newItem)

#    with open('products.json', 'w') as fp:
#        json.dump(line, fp)

#this is a function that executes with save in the file menu bar
def save_app():
    with open('products.json', 'w') as fp:
        json.dump(line, fp)
    with open('customers.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(newCustomerList)
    with open('receipt.csv', 'w') as f:
        writer = csv.writer(f)
        my_list = [current_user.name, tot, ctime(), productsInCart, quantities]
        writer.writerow(my_list)

#this gives the employee the option to delete a product
def delete_product():
    global quantity, product_roster, attach, mater, pID, pDesc, quant, pri, edit_index, product_list
    product_roster.pop(edit_index)
    product_list.delete(edit_index)

#GUI
window = Tk()
window.config(background='cornsilk')
window.title("KitchenSupply")
window.geometry("650x600")
window.iconbitmap('tree.ico')

bgcolor = 'cornsilk'

total = StringVar()
name = StringVar()
pin = StringVar()
name.set(customer_roster[0])
att = StringVar()
mat = StringVar()
productID = StringVar()
productDesc = StringVar()
quantity = StringVar()
price = StringVar()

menu_bar = Menu(window)
window.config(menu = menu_bar)
file_menu = Menu(menu_bar, tearoff = False)
menu_bar.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label = 'Open')
file_menu.add_command(label = 'Save', command = save_app)
file_menu.add_command(label = 'Exit', command = window.quit)

name_lbl = Label(window, text='Name:', background=bgcolor, justify=LEFT)
name_lbl.grid(row=0, column=2, padx=5, pady=5)
name_cmbx = ttk.Combobox(window, values=customer_roster, textvariable=name, width=27)
name_cmbx.bind("<<ComboboxSelected>>", getName)
name_cmbx.grid(row=0, column=3, columnspan=2)

ok1_button = Button(window, text='OK', command = ok_click)
ok1_button.grid(row=0, column=4, pady=5, sticky=E)

product_list_label = Label(window, text='Product List:', background='cornsilk')
product_list_label.grid(row=1, column=1, columnspan=1)
product_list = Listbox(window, width=50, height = 12)
product_list.bind('<Double-Button-1>', edit_product)
product_list.grid(row=2, column=1, columnspan=3)

for product in product_roster:
   product_list.insert(END, product)

cart_label = Label(window, text='Cart:', background='cornsilk')
cart_label.grid(row=1, column=5, columnspan=1, padx = 5, pady = 5)
cart_list = Listbox(window, width=50)
cart_list.bind('<Double-Button-1>', delete_cart_item)
cart_list.grid(row=2, column=4, columnspan=3)

totalBalance_lbl = Label(window, text=f'Total: $', background='cornsilk', justify=LEFT)
totalBalance_lbl.grid(row=3, column=4, padx=5, pady=5)
total_entry = Entry(window, textvariable=total, width=27)
#major_cmbx.current(0)
total_entry.grid(row=3, column=5, columnspan=2)

attachesTo_lbl = Label(window, text='Attaches To:', background=bgcolor, justify=LEFT)
attachesTo_lbl.grid(row=4, column=4, padx = 5, pady = 5)
attachesTo = Entry(window, textvariable=att, width=27)
#major_cmbx.current(0)
attachesTo.grid(row=4, column=5, columnspan=2)

material_lbl = Label(window, text='Material:', background=bgcolor, justify=LEFT)
material_lbl.grid(row=5, column=4, padx = 5, pady = 5)
material_entry = Entry(window, textvariable=mat, width=27)
#major_cmbx.current(0)
material_entry.grid(row=5, column=5, columnspan=2)

product_id_lbl = Label(window, text='Product ID:', background=bgcolor, justify=LEFT)
product_id_lbl.grid(row=6, column=4, padx = 5, pady = 5)
product_id = Entry(window, textvariable=productID, width=27)
#major_cmbx.current(0)
product_id.grid(row=6, column=5, columnspan=2)

for p in product_roster:
    product_names.append(p.description)

product_name_lbl = Label(window, text='Product Name:', background=bgcolor, justify=LEFT)
product_name_lbl.grid(row=7, column=4, padx = 5, pady = 5)
product_name_cmbx = ttk.Combobox(window, values=product_names, textvariable=productDesc, width=27)
product_name_cmbx.current(0)
product_name_cmbx.grid(row=7, column=5, columnspan=2)

quantity_lbl = Label(window, text='Quantity:', background=bgcolor, justify=LEFT)
quantity_lbl.grid(row=8, column=4, padx=5, pady=5)
quantity_entry = Entry(window, textvariable=quantity, width=27)
quantity_entry.grid(row=8, column=5, columnspan=2)

price_lbl = Label(window, text='Price:', background=bgcolor, justify=LEFT)
price_lbl.grid(row=9, column=4, padx=5, pady=5)
price_cmbx = Entry(window, textvariable=price, width=27)
#major_cmbx.current(0)
price_cmbx.grid(row=9, column=5, columnspan=2)

add_to_button = Button(window, text= "Add item", command = add_item_click)
add_to_button.grid(row=10, column=6, sticky = E)

pin_lbl = Label(window, text='PIN:', background='cornsilk', justify=LEFT)
pin_lbl.grid(row=11, column=2, padx=5, pady=5)
pin_tbx = Entry(window, textvariable=pin, width=30)
pin_tbx.grid(row=11, column=3, columnspan=2)

ok_button = Button(window, text='OK', command = check_pin)
ok_button.grid(row=11, column=4, pady=5, sticky=E)

purchase_button = Button(window, text='Purchase', command = purchaseItems)
purchase_button.grid(row=13, column=3, pady=5, sticky=W)

modify_button = Button(window, text='Edit', command = modifyItems)
modify_button.grid(row=13, column=3, pady=5, sticky=E)

Add_button = Button(window, text='Add', command = addItems)
Add_button.grid(row=13, column=4, pady=5, sticky=W)

delete_product_button = Button(window, text='Delete', command = delete_product)
delete_product_button.grid(row=13, column=4, pady=5, sticky=E)
window.mainloop()



