from flask import Flask,render_template, request, redirect, url_for, session

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=flg36832;PWD=inj6N0FQbZdukmqv",'','')
app = Flask(__name__)


@app.route("/")
def Log():
    return render_template('LoginRegister.html')

@app.route("/")
def Regs():
    return render_template('LoginRegister.html')

print('Database connected Successfully')

@app.route('/Register', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':

        name = request.form['username']
        email = request.form['Emailaddress']
        password = request.form['password']
        sql = "SELECT * FROM Register WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('LoginRegister.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO Register VALUES (?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)

        return render_template('LoginRegister.html', msg="Data saved successfuly..Please login using your details")

@app.route('/Login', methods=['POST'])
def Login():
    email = request.form['username']
    password = request.form['password']

    sql = "SELECT * FROM Register WHERE Emailaddress =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
        return render_template('dashboard.html')
    else:
        return render_template('LoginRegister.html', msg="Login unsuccessful. Incorrect username / password !")

    print('Database connected')
