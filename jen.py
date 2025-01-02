import sqlite3
from tkinter import *
from tkinter import ttk

# Create or connect to the database
conn = sqlite3.connect('hardware_company.db')
c = conn.cursor()

# Create tables if not exist
c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
""")
conn.commit()

# Root window
root = Tk()
root.title("Hardware Company Management System")
root.geometry("800x600")

# Predefined categories for combobox
categories = ["Electronics", "Plumbing", "Tools", "Furniture", "Gardening", "Paint"]

# Function to create a new product
def add_product():
    name = name_entry.get()
    category = category_combobox.get()
    price = price_entry.get()
    stock = stock_entry.get()
    
    if name and category and price and stock:
        c.execute("INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                  (name, category, float(price), int(stock)))
        conn.commit()
        clear_entries()
        display_products()
    else:
        status_label.config(text="All fields are required.", fg="red")

# Function to display products in Treeview
def display_products():
    for row in treeview.get_children():
        treeview.delete(row)

    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    
    for row in rows:
        product_id = row[0]
        name = row[1]
        category = row[2]
        price = row[3]
        stock = row[4]
        total_value = price * stock  # Calculate total value (stock * price)
        
        # Insert row in the Treeview with total_value
        treeview.insert('', 'end', values=(product_id, name, category, f"${price:.2f}", stock, f"${total_value:.2f}"))

# Function to update product details
def update_product():
    selected_item = treeview.selection()
    
    if selected_item:
        selected_product = treeview.item(selected_item[0])['values']
        product_id = selected_product[0]
        
        name = name_entry.get()
        category = category_combobox.get()
        price = price_entry.get()
        stock = stock_entry.get()
        
        if name and category and price and stock:
            c.execute("""UPDATE products SET name = ?, category = ?, price = ?, stock = ? WHERE id = ?""",
                      (name, category, float(price), int(stock), product_id))
            conn.commit()
            clear_entries()
            display_products()
        else:
            status_label.config(text="All fields are required.", fg="red")
    else:
        status_label.config(text="No product selected to update.", fg="red")

# Function to delete a product
def delete_product():
    selected_item = treeview.selection()
    
    if selected_item:
        selected_product = treeview.item(selected_item[0])['values']
        product_id = selected_product[0]
        
        c.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        display_products()
    else:
        status_label.config(text="No product selected to delete.", fg="red")

# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, END)
    category_combobox.set('')  # Reset combobox
    price_entry.delete(0, END)
    stock_entry.delete(0, END)

# Frame for the form
form_frame = Frame(root)
form_frame.pack(pady=20)

# Name field
name_label = Label(form_frame, text="Product Name:", font=("Helvetica", 12))
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = Entry(form_frame, font=("Helvetica", 12))
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Category field (Combobox)
category_label = Label(form_frame, text="Category:", font=("Helvetica", 12))
category_label.grid(row=1, column=0, padx=10, pady=10)
category_combobox = ttk.Combobox(form_frame, values=categories, font=("Helvetica", 12), state="normal")
category_combobox.grid(row=1, column=1, padx=10, pady=10)

# Price field
price_label = Label(form_frame, text="Price:", font=("Helvetica", 12))
price_label.grid(row=2, column=0, padx=10, pady=10)
price_entry = Entry(form_frame, font=("Helvetica", 12))
price_entry.grid(row=2, column=1, padx=10, pady=10)

# Stock field
stock_label = Label(form_frame, text="Stock:", font=("Helvetica", 12))
stock_label.grid(row=3, column=0, padx=10, pady=10)
stock_entry = Entry(form_frame, font=("Helvetica", 12))
stock_entry.grid(row=3, column=1, padx=10, pady=10)

# Buttons for actions
button_frame = Frame(root)
button_frame.pack(pady=10)

add_button = Button(button_frame, text="Add Product", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_product)
add_button.grid(row=0, column=0, padx=10, pady=10)

update_button = Button(button_frame, text="Update Product", font=("Helvetica", 12), bg="#2196F3", fg="white", command=update_product)
update_button.grid(row=0, column=1, padx=10, pady=10)

delete_button = Button(button_frame, text="Delete Product", font=("Helvetica", 12), bg="#F44336", fg="white", command=delete_product)
delete_button.grid(row=0, column=2, padx=10, pady=10)

# Status label for messages
status_label = Label(root, text="", font=("Helvetica", 12), fg="green")
status_label.pack(pady=10)

# Treeview to display products
treeview_frame = Frame(root)
treeview_frame.pack(pady=20)

treeview = ttk.Treeview(treeview_frame, columns=("ID", "Name", "Category", "Price", "Stock", "Total Value"), show="headings")
treeview.pack()

# Define columns
treeview.heading("ID", text="ID")
treeview.heading("Name", text="Name")
treeview.heading("Category", text="Category")
treeview.heading("Price", text="Price")
treeview.heading("Stock", text="Stock")
treeview.heading("Total Value", text="Total Value")

# Set column widths
treeview.column("ID", width=50, anchor="center")
treeview.column("Name", width=200, anchor="center")
treeview.column("Category", width=150, anchor="center")
treeview.column("Price", width=100, anchor="center")
treeview.column("Stock", width=100, anchor="center")
treeview.column("Total Value", width=120, anchor="center")

# Add the data to the treeview
display_products()

# Start the Tkinter main loop
root.mainloop()

# Close the database connection on exit
conn.close()
