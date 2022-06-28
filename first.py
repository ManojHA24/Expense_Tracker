import sqlite3 as sql

def input(fo,h,t):
    con = sql.connect('database.db')
    try:
        
        cur = con.cursor()
        cur.execute("INSERT INTO expense(expense_name,expense,day) VALUES (?,?,?)",(fo,h,t) )
        
        con.commit()
        msg = "Record successfully added"
        print(msg) 
    except:
        con.rollback()
        msg = "error in insert operation"
        print(msg)
    
    con.close()
            