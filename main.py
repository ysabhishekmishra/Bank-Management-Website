from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
conn=mysql.connector.connect(host="localhost",user="root",database="pbl2")
cursor=conn.cursor()


@app.route('/')
def home():
    return render_template("index.html")





@app.route('/Customerlogin')
def Customerlogin():
    return render_template("login.html")




@app.route('/userdashboard')
def userdashboard():
    if 'sr_no' in session:
        return render_template("userdashboard.html",data=session['sr_no'])
    else:
        return redirect('/Customerlogin')
    




@app.route('/Customerlogin_validation',methods=['POST'])
def Customerlogin_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM customerdata Where email Like '{}' and password like '{}'""".format(email,password))
    userdata=cursor.fetchall()
    print(userdata)

    if len(userdata)>0:
        session['sr_no']=userdata
        return redirect('/userdashboard')
    else:
        return redirect('/Customerlogin') 





@app.route('/Employeelogin')
def Employeelogin():
    return render_template("Employeelogin.html")

@app.route('/employeelogin_validation',methods=['POST'])
def employeelogin_validation():
    employeeid=request.form.get('')
    password=request.form.get('epassword')

    cursor.execute("""SELECT * FROM employeedata Where employeeid Like '{}' and password like '{}'""".format(employeeid,password))
    userdata=cursor.fetchall()

    if len(userdata)>0:
        session['sr_no']=userdata[0][0]
        return redirect('/employeedashboard')
    else:
        return redirect('/employeelogin') 


@app.route('/Customersignup')
def Customersignup():
    return render_template("Customersignup.html")

@app.route('/Customersignup_validation',methods=['POST'])  
def Customersignup_validation():
    name=request.form.get('uname')
    accountnumber= request.form.get('uaccountnumber')
    email= request.form.get('uemail')
    contactnumber=request.form.get('ucontactnumber')
    password= request.form.get('upassword')
    cursor.execute("""INSERT INTO customerdata values('NULL','{}','{}','{}','{}','{}')""".format(name,accountnumber,email,contactnumber,password))
    conn.commit()

    cursor.execute("""SELECT * FROM customerdata WHERE email LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['sr_no']=myuser[0][0]
    return redirect('/userdashboard')

@app.route('/logout')
def logout():
    session.pop('sr_no')
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
