from flask import Flask, redirect, render_template, url_for, request 
import sqlite3 as sql
import first as f  
  
app = Flask(__name__,template_folder='template')  

@app.route('/')
def first():
   return render_template('first.html')
      
@app.route('/list',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        fo=request.form['exp_name']
        h=request.form['exp']
        t=request.form['dat']
        t=t[:10]
    f.input(fo,h,t)
    
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    
    cur = conn.cursor()
    rows = cur.execute("select * from expense").fetchall()
    conn.close()
        
    return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)