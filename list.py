from flask import Flask, redirect, render_template, url_for, request 
import sqlite3 as sql
import first as f  
import pandas as pd  
import matplotlib.pyplot as plt
from PIL import Image
import base64
import io
  
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
    df = pd.DataFrame(rows, columns =['Expense Name', 'Expense', 'Day']) 
    df.to_csv(r'C:\Users\Manoj H A\OneDrive\Desktop\my_data.csv', index=False)
    df.groupby(['Expense Name']).sum().plot(kind='pie', y='Expense')
    
    plt.savefig('pie.jpeg')
    conn.close()
        
    return render_template("list.html",rows = rows)

@app.route('/plot')
def plot():
    im = Image.open("pie.jpeg")
    data = io.BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("statistics.html", img_data=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
   app.run(debug = True)