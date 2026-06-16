from enum import nonmember

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
app = Flask(__name__)

## database connection
app.secret_key="zaker"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raza@123'
app.config['MYSQL_DB'] = 'erp_db'

mysql=MySQL(app)

## Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/admin_dashboard',methods=['POST'])
def admin_dashboard():
    user=request.form['username']
    password=request.form['password']

    if user=='admin' and password=='555':
                session['name']= 'Zaker'  # session variable created

                return render_template('admin_dashboard.html')
    else:
        msg="invalid username or password"
        return render_template("adminlogin.html",msg=msg)


@app.route('/add_employee')
def add_employee():
    return render_template('add_employee.html')

@app.route('/save',methods=['POST'])
def save():
    id=request.form['emp id']
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    dept=request.form['department']
    desig=request.form['designation']
    salary=request.form['salary']

    # database connection
    cur=mysql.connection.cursor()

    # query specification
    cur.execute("insert into registration(id,name,email)"
                "values(%s,%s,%s)",(id,name,email))

    # transaction save
    mysql.connection.commit()

    # connection close
    cur.close()

    return " <h1> employee registration successful <h1>"

@app.route('/view_employee')
def view_employee():
    cur=mysql.connection.cursor()
    cur.execute("select * from registration")
    emp_list=cur.fetchall()
    return render_template('view_employee.html',emp_list=emp_list)

@app.route('/profile')
def profile():
    id=request.args.get('eid')
    cur=mysql.connection.cursor()
    cur.execute("select * from registration where id="+id)
    record_lits=cur.fetchall()
    return render_template('profile.html',emp_list=record_lits)

@app.route("/update_employee",methods=['POST'])
def update_employee():
    id = request.form['emp id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    dept = request.form['department']
    desig = request.form['designation']
    salary = request.form['salary']

    cur=mysql.connection.cursor()
    cur.execute("update registration set salary=%s,name=%s where id=%s" ,(salary,name,id))
    mysql.connection.commit()
    cur.close()
    return render_template('update_employee.html')

@app.route("/delete_employee")
def delete_employee():
    id = request.args.get('eid')
    cur=mysql.connection.cursor()
    cur.execute("delete from registration where id=%s",(id,))
    mysql.connection.commit()
    cur.close()

    return render_template('delete_employee.html')

@app.route("/search_employee")
def search_employee():
    return render_template('search_employee.html')

@app.route("/search_employee_result",methods=['POST'])
def search_employee_result():
    name = request.form['empname']
    cur=mysql.connection.cursor()
    q="select * from registration where name like '%"+name+"%'"
    cur.execute(q)
    emplist=cur.fetchall()
    cur.close()
    return render_template('search_employee_result.html',emplist=emplist)


@app.route("/logout")
def logout():
    session['name']=None
    return render_template('adminlogin.html')



app.run(debug=True)