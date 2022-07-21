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
    global keymax
    global valmax
    if request.method == 'POST':
        fo=request.form['exp_name']
        h=request.form['exp']
        h=int(h)
        t=request.form['dat']
        t=t[:10]
    f.input(fo,h,t)
    
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    
    cur = conn.cursor()
    rows = cur.execute("select * from expense").fetchall()
    df = pd.DataFrame(rows, columns =['ExpenseName', 'Expense', 'Day']) 
    df.to_csv(r'C:\Users\Manoj H A\OneDrive\Desktop\my_data.csv', index=False)
    
    
    df.groupby(['ExpenseName']).sum().plot(kind='pie', y='Expense')  #pie chart plot
    plt.savefig('pie.jpeg')
    
    
    high={} #dictionary to store highest expense and expense name
    for i in range(len(df['ExpenseName'])):
        if df.ExpenseName[i] in high:
            high[df.ExpenseName[i]]+=df.Expense[i]
        else:
            high[df.ExpenseName[i]]=df.Expense[i]
    keymax = max(high, key= lambda x: high[x])
    valmax=high[keymax]
    print(keymax, valmax)
    
    expName=list(high.keys()) #using dictionary keys and values for bar graph 
    exp=list(high.values())
    bargraph(expName,exp)
    
    conn.close()
        
    return render_template("list.html",rows = rows) #render_template render the html file and can also pass arguments with it


def bargraph(expName,exp):
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(expName,exp , color ='maroon',width = 0.4)
 
    plt.xlabel("Expense Name")
    plt.ylabel("Expense")
    plt.title("Expense Tracker")
    plt.savefig('bar.jpeg')
    
@app.route('/plot')
def plot():
    im = Image.open("pie.jpeg")
    im1 = Image.open("bar.jpeg")
    data = io.BytesIO()
    data1 = io.BytesIO()
    im.save(data, "JPEG")
    im1.save(data1, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    encoded_img_data1 = base64.b64encode(data1.getvalue())
    return render_template("statistics.html", img_data=encoded_img_data.decode('utf-8'),img_data1=encoded_img_data1.decode('utf-8'),highest_expense_name=keymax,highest_expense=valmax)

if __name__ == '__main__':
   app.run(debug = True)