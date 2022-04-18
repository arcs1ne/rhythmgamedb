from distutils.log import debug 
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from logging import FileHandler,WARNING
import re
from flask_session import Session
from datetime import datetime

countrydict = {"AF":"Afghanistan",
"AX":"Aland Islands",
"AL":"Albania",
"DZ":"Algeria",
"AS":"American Samoa",
"AD":"Andorra",
"AO":"Angola",
"AI":"Anguilla",
"AQ":"Antarctica",
"AG":"Antigua and Barbuda",
"AR":"Argentina",
"AM":"Armenia",
"AW":"Aruba",
"AU":"Australia",
"AT":"Austria",
"AZ":"Azerbaijan",
"BS":"Bahamas",
"BH":"Bahrain",
"BD":"Bangladesh",
"BB":"Barbados",
"BY":"Belarus",
"BE":"Belgium",
"BZ":"Belize",
"BJ":"Benin",
"BM":"Bermuda",
"BT":"Bhutan",
"BO":"Bolivia, Plurinational State of",
"BQ":"Bonaire, Sint Eustatius and Saba",
"BA":"Bosnia and Herzegovina",
"BW":"Botswana",
"BV":"Bouvet Island",
"BR":"Brazil",
"IO":"British Indian Ocean Territory",
"BN":"Brunei Darussalam",
"BG":"Bulgaria",
"BF":"Burkina Faso",
"BI":"Burundi",
"KH":"Cambodia",
"CM":"Cameroon",
"CA":"Canada",
"CV":"Cape Verde",
"KY":"Cayman Islands",
"CF":"Central African Republic",
"TD":"Chad",
"CL":"Chile",
"CN":"China",
"CX":"Christmas Island",
"CC":"Cocos (Keeling) Islands",
"CO":"Colombia",
"KM":"Comoros",
"CG":"Congo",
"CD":"Congo, The Democratic Republic of the",
"CK":"Cook Islands",
"CR":"Costa Rica",
"CI":"Côte d'Ivoire",
"HR":"Croatia",
"CU":"Cuba",
"CW":"Curaçao",
"CY":"Cyprus",
"CZ":"Czech Republic",
"DK":"Denmark",
"DJ":"Djibouti",
"DM":"Dominica",
"DO":"Dominican Republic",
"EC":"Ecuador",
"EG":"Egypt",
"SV":"El Salvador",
"GQ":"Equatorial Guinea",
"ER":"Eritrea",
"EE":"Estonia",
"ET":"Ethiopia",
"FK":"Falkland Islands (Malvinas)",
"FO":"Faroe Islands",
"FJ":"Fiji",
"FI":"Finland",
"FR":"France",
"GF":"French Guiana",
"PF":"French Polynesia",
"TF":"French Southern Territories",
"GA":"Gabon",
"GM":"Gambia",
"GE":"Georgia",
"DE":"Germany",
"GH":"Ghana",
"GI":"Gibraltar",
"GR":"Greece",
"GL":"Greenland",
"GD":"Grenada",
"GP":"Guadeloupe",
"GU":"Guam",
"GT":"Guatemala",
"GG":"Guernsey",
"GN":"Guinea",
"GW":"Guinea-Bissau",
"GY":"Guyana",
"HT":"Haiti",
"HM":"Heard Island and McDonald Islands",
"VA":"Holy See (Vatican City State)",
"HN":"Honduras",
"HK":"Hong Kong",
"HU":"Hungary",
"IS":"Iceland",
"IN":"India",
"ID":"Indonesia",
"IR":"Iran, Islamic Republic of",
"IQ":"Iraq",
"IE":"Ireland",
"IM":"Isle of Man",
"IL":"Israel",
"IT":"Italy",
"JM":"Jamaica",
"JP":"Japan",
"JE":"Jersey",
"JO":"Jordan",
"KZ":"Kazakhstan",
"KE":"Kenya",
"KI":"Kiribati",
"KP":"Korea, Democratic People's Republic of",
"KR":"Korea, Republic of",
"KW":"Kuwait",
"KG":"Kyrgyzstan",
"LA":"Lao People's Democratic Republic",
"LV":"Latvia",
"LB":"Lebanon",
"LS":"Lesotho",
"LR":"Liberia",
"LY":"Libya",
"LI":"Liechtenstein",
"LT":"Lithuania",
"LU":"Luxembourg",
"MO":"Macao",
"MK":"Macedonia, Republic of",
"MG":"Madagascar",
"MW":"Malawi",
"MY":"Malaysia",
"MV":"Maldives",
"ML":"Mali",
"MT":"Malta",
"MH":"Marshall Islands",
"MQ":"Martinique",
"MR":"Mauritania",
"MU":"Mauritius",
"YT":"Mayotte",
"MX":"Mexico",
"FM":"Micronesia, Federated States of",
"MD":"Moldova, Republic of",
"MC":"Monaco",
"MN":"Mongolia",
"ME":"Montenegro",
"MS":"Montserrat",
"MA":"Morocco",
"MZ":"Mozambique",
"MM":"Myanmar",
"NA":"Namibia",
"NR":"Nauru",
"NP":"Nepal",
"NL":"Netherlands",
"NC":"New Caledonia",
"NZ":"New Zealand",
"NI":"Nicaragua",
"NE":"Niger",
"NG":"Nigeria",
"NU":"Niue",
"NF":"Norfolk Island",
"MP":"Northern Mariana Islands",
"NO":"Norway",
"OM":"Oman",
"PK":"Pakistan",
"PW":"Palau",
"PS":"Palestinian Territory, Occupied",
"PA":"Panama",
"PG":"Papua New Guinea",
"PY":"Paraguay",
"PE":"Peru",
"PH":"Philippines",
"PN":"Pitcairn",
"PL":"Poland",
"PT":"Portugal",
"PR":"Puerto Rico",
"QA":"Qatar",
"RE":"Réunion",
"RO":"Romania",
"RU":"Russian Federation",
"RW":"Rwanda",
"BL":"Saint Barthélemy",
"SH":"Saint Helena, Ascension and Tristan da Cunha",
"KN":"Saint Kitts and Nevis",
"LC":"Saint Lucia",
"MF":"Saint Martin (French part)",
"PM":"Saint Pierre and Miquelon",
"VC":"Saint Vincent and the Grenadines",
"WS":"Samoa",
"SM":"San Marino",
"ST":"Sao Tome and Principe",
"SA":"Saudi Arabia",
"SN":"Senegal",
"RS":"Serbia",
"SC":"Seychelles",
"SL":"Sierra Leone",
"SG":"Singapore",
"SX":"Sint Maarten (Dutch part)",
"SK":"Slovakia",
"SI":"Slovenia",
"SB":"Solomon Islands",
"SO":"Somalia",
"ZA":"South Africa",
"GS":"South Georgia and the South Sandwich Islands",
"ES":"Spain",
"LK":"Sri Lanka",
"SD":"Sudan",
"SR":"Suriname",
"SS":"South Sudan",
"SJ":"Svalbard and Jan Mayen",
"SZ":"Swaziland",
"SE":"Sweden",
"CH":"Switzerland",
"SY":"Syrian Arab Republic",
"TW":"Taiwan, Province of China",
"TJ":"Tajikistan",
"TZ":"Tanzania, United Republic of",
"TH":"Thailand",
"TL":"Timor-Leste",
"TG":"Togo",
"TK":"Tokelau",
"TO":"Tonga",
"TT":"Trinidad and Tobago",
"TN":"Tunisia",
"TR":"Turkey",
"TM":"Turkmenistan",
"TC":"Turks and Caicos Islands",
"TV":"Tuvalu",
"UG":"Uganda",
"UA":"Ukraine",
"AE":"United Arab Emirates",
"GB":"United Kingdom",
"US":"United States",
"UM":"United States Minor Outlying Islands",
"UY":"Uruguay",
"UZ":"Uzbekistan",
"VU":"Vanuatu",
"VE":"Venezuela, Bolivarian Republic of",
"VN":"Viet Nam",
"VG":"Virgin Islands, British",
"VI":"Virgin Islands, U.S.",
"WF":"Wallis and Futuna",
"YE":"Yemen",
"ZM":"Zambia",
"ZW":"Zimbabwe"}

app = Flask(__name__)  
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'rhythmgame'

app.secret_key = 'peepeepoopoo'

mysql = MySQL(app)
Session(app)

@app.route("/")
def index():
    if not session.get("username"):
        return redirect("/login")
    return render_template("basic.html", name = session['username'])

@app.route("/tournamentpage/<int:i>", methods = ['GET', 'POST'])
def tournamentpage(i):
    cur = mysql.connection.cursor()
    cur.execute("call tourDetailsPage(%s)",(i,))
    tourdetails = cur.fetchall()
    return render_template("tournamentpage.html", details = tourdetails)

@app.route("/tournament")
def tournament():
    cur = mysql.connection.cursor()
    cur.execute("call listTournaments()")
    tour = cur.fetchall()
    return render_template('tournament.html', tournaments = tour)

@app.route("/delete/<int:i>", methods = ['POST'])
def deletesong(i):
    cur = mysql.connection.cursor()
    cur.execute("call deleteSong(%s)",(i,))
    mysql.connection.commit()
    songs = cur.fetchall()
    return redirect(url_for('song'))

@app.route("/edit/<int:i>", methods = ['POST'])
def editsong(i):
    cur = mysql.connection.cursor()
    cur.execute("call listSongs(%s, %s, %s)", ("", "titlesort", False))
    songs = cur.fetchall()
    return render_template('song.html', songs = songs, searchstr = "", sortby = "titlesort", romanized = False, songtoedit = i, edit = 1)
    
@app.route("/submitedit/<int:i>", methods = ['POST'])
def submitedit(i):  
    cur = mysql.connection.cursor()
    artist = request.form['artistedit']
    title = request.form['titleedit']
    duration = request.form['durationedit']
    bpm = request.form['bpmedit']
    cur.execute("call editSong(%s, %s, %s, %s, %s)", (i,artist,title,duration,bpm))
    mysql.connection.commit()
    songs = cur.fetchall()
    return redirect(url_for('song'))

@app.route("/song", methods = ['GET', 'POST'])
def song():
    sortby = "titlesort"
    searchstr = ""
    romanized = False

    if request.method == "POST":
        print(request.form)
        searchstr = request.form['search']
        sortby = request.form['sortby']
        romanized = 'romanized' in request.form
    cur = mysql.connection.cursor()
    cur.execute("call listSongs(%s, %s, %s)", (searchstr, sortby, romanized))
    songs = cur.fetchall()
    return render_template('song.html', songs = songs, searchstr = searchstr, sortby = sortby, romanized = romanized, songtoedit = -1, edit = 0)

@app.route("/user", methods = ['GET', 'POST'])
def user():
    country = session['country']
    sortby = "usersort"
    countryonly = False
    searchstr = ""

    if request.method == "POST":
        searchstr = request.form['search']
        sortby = request.form['sortby']
        countryonly = 'countryonly' in request.form

    cur = mysql.connection.cursor()
    cur.execute("call listUsers(%s, %s, %s, %s)", (searchstr, sortby, countryonly, country))
    records = cur.fetchall()
    return render_template('user.html', user = records, searchstr = searchstr, sortby = sortby, countryonly = countryonly)

@app.route("/register", methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        username = request.form['name']
        password = request.form['password']
        cfmpassword = request.form['cfmpassword']
        country = request.form['country']
        if password != cfmpassword:
            msg = "The passwords do not match!"
            return render_template('register.html', msg=msg, countries = countrydict, username=username, password=password, cfmpassword=cfmpassword)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        temp = 'INSERT INTO user (username, password, country, globalrank, countryrank, ranklastupdated, mainmode) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = (username, password, country, None, None, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0)
        cursor.execute(temp, val)
        mysql.connection.commit()
        return redirect(url_for('login'))
    return render_template("register.html", countries = countrydict, username = "", password = "", cfmpassword = "")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['name']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cursor.close()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['userid'] = account['userid']
            session['username'] = account['username']
            session['country'] = account['country']
            print(session)
            # Redirect to home page
            return render_template("basic.html", name=session['username'])
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)