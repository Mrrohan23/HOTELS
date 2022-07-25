from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flaskext.mysql import MySQL
import pymysql


 
app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"
  
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'hotel'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/')
def home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM register WHERE id = %s', [session['email']])
        account = cursor.fetchone()
   
        # User is loggedin show them the home page
        return render_template('home.html',account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('home2'))


# @app.route('/')
# def home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
   
#         # User is loggedin show them the home page
#         return render_template('home.html', username=session['username'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/reg')
def reg():
    return render_template('register.html')
@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('home2'))
#User register

@app.route('/register', methods=['POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        salution= request.form['salution']
        first_name= request.form['first_name']
        last_name= request.form['last_name']
        gender= request.form['gender']
        email= request.form['email']
        phone= request.form['phone']
        country= request.form['country']
        password= request.form['password']
       
        cursor.execute('INSERT INTO register(salution,first_name,last_name,gender,email,phone,country,password) '
                       'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                       (salution,first_name,last_name,gender,email,phone,country,password))
       
        conn.commit()
        return redirect(url_for('home'))
    return render_template('register.html')



####################

@app.route('/signin', methods=['POST'])
def signin():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM register WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
             
            session['first_name'] = account['first_name']
            # Redirect to home page
            # return 'Logged in successfully!'
            return render_template('home.html',account=account)
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM admin_login WHERE email=%s AND password=%s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'



    return render_template('signin.html', msg=msg)


#Booking

@app.route('/booking', methods=['POST'])
def booking(): 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        arrival= request.form['arrival']
        deprature= request.form['deprature']
        room= request.form['room']
        adults= request.form['adults']
        children= request.form['children']
        cursor.execute('INSERT INTO booking(arrival,deprature,room,adults,children) '
                       'VALUES (%s,%s,%s,%s,%s)',
                       (arrival,deprature,room,adults,children))       
        conn.commit()
        return redirect(url_for('home'))
    return render_template('booking.html')



@app.route('/tables')
def tables():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM booking JOIN register USING (id);")
    BOOKING = cursor.fetchall()
    return render_template('tables.html',booking=BOOKING)













app.run()
