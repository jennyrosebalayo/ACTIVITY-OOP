from tkinter import*
import sqlite3

root=Tk()
root.title('CRUDTRI')
root.geometry ("500x500")

conn=sqlite3.connect ('studentinfo.db')
c=conn.cursor()

def submit():
    conn=sqlite3.connect('C:/Users/STUDENT5/Desktop/jennydatabase.db')
    c.execute("INSERT INTO dataslf VALUES(:f_name,:l_name,:age,:address,:email)",
              {
                  "f_name":f_name.get(),
                  "l_name":l_name.get(),
                  "age":age.get(),
                  "address":address.get(),
                  "email":email.get(),
                  })
    conn.commit()
    conn.close()

    f_name.delete(0,END)
    l_name.delete (0,END)
    age.delete (0,END)
    address.delete (0,END)
    email.delete (0,END)

def query():
        conn=sqlite3.connect('C:/Users/STUDENT5/Desktop/jennydatabase.db')
        c=conn.cursor()
        c.execute("SELECT *,oid FROM dataslf")
        records=c.fetchall()

        print_records=''
        for record in records:
            print_records+=str(record[0])+" "+str(record[1])+" "+str(record[2])+" "+str(record[3])+" "+(record[4])+" "+"\t"+str(record[5])+"\n"
            query_label=Label(root,text=print_records)


        conn.commit()
        conn.close()
                                                   
                                                    
'''
c.execute(""""CREATE TABLE "studentinfo" (
	"f_name"	TEXT,
	"l_name"	TEXT,
	"age"	INTEGER,
	"address"	TEXT,
	"email"	TEXT
)
)
)""")
'''

def delete():
    conn=sqlite3.connect('C:/Users/STUDENT5/Deskto/jennydatabase.db')
    c=conn.cursor()
    c.execute("DELETE from dataslf WHERE oid="+delete_box,get())

    delete_box.delete(0,END)

    conn.commit()
    conn.close()

def edit():
    editor=Tk()
    editor.title('Update Record from database')
    editor.geometry("500x500")

    conn=sqlite3.connect('C:/Users/STUDENT5/Desktop/jennydatabase.db')
    c=conn.cursor

    record_id=delete_box.get()
    c.execute("SELECT * FROM dataslf WHERE oid =" + record_id)
    record=c.fetchall()

    global f_name_editor
    global l_name_editor
    global age_editor
    global address_editor
    global email_editor


def update():
    conn=sqlite.connect('C:/Users/STUDENT5/Desktop/jennydatabase.db')
    c=conn.cursor
    
    record_id=delete_box.get()
    c.execute(""" UPDATE student info SET
        f_name=:first,
        l_name=:last,
        age=:age,
        address=:address,
        email=:email,

        WHERE oid=:oid""",
        {
        'first':f_name_editor.get(),
        'last':l_name_editor.get(),
        'age':age_editor.get(),
        'address':address_editor.get(),
        'eamail':email_editor.get(),
        'oid':record_id


        })

    conn.commit()
    conn.close

f_name=Entry(root,width=30)
f_name.grid(row=0,column=1,padx=20)
l_name=Entry (root,width=30)
l_name.grid(row=1,column=1,padx=20)
age=Entry(root,width=30)
age.grid(row=2,column=1,padx=20)
address=Entry(root,width=30)
address.grid(row=3,column=1,padx=20)
email=Entry(root,width=30)
email.grid (row=4,column=1,padx=20)
delete_box=Entry(root,width=30)
delete_box.grid(row=10,column=1,padx=30)

f_name_label=Label(root,text="First Name")
f_name_label.grid(row=0,column=0)
l_name_label=Label(root,text= "Last Name")
l_name_label.grid(row=1,column=0)
age_label=Label(root,text= "Age")
age_label.grid(row=2,column=0)
address_label=Label(root,text= "Address")
address_label.grid(row=3,column=0)
email_label=Label(root,text= "Email")
email_label.grid(row=4,column=0)

delete_box_label=Label(root,text="Select ID No.")
delete_box_label.grid(row=10,column=0)

submit_btn=Button(root,text= "Add Record to Database",command=submit)
submit_btn.grid(row=6,column=0,columnspan=2, pady=10, padx=10, ipadx=100)

query_btn=Button(root,text= "Show records",command=query)
query_btn.grid (row=7,column=0,columnspan=2, pady=10, padx=10, ipadx=137)

query_btn=Button(root,text="Delete Record",command=delete)
query_btn.grid(row=12,column=0,columnspan=2, pady=10, padx=10, ipadx=136)

update_btn=Button(root,text="Edit Record",command=edit)
update_btn.grid(row=13,column=0,columnspan=2, pady=10, padx=10, ipadx=140)
                  
root.mainloop()
