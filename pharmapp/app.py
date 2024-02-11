from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory
from flask_mysqldb import MySQL
from openpyxl import Workbook
import MySQLdb.cursors
import flask_excel as excel
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

#конфигурация подключения к базе данных 
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_PORT'] = config.MYSQL_PORT
app.config['MYSQL_CURSORCLASS'] = config.MYSQL_CURSORCLASS
#инициализация mysql и excel для формирования отчетов
mysql = MySQL(app)
excel.init_excel(app)

#Запсись типа пользователя в сессию
def userTypeSetup(userType):
    if userType == config.userTypeMainAdmin:
        session['userType'] = 'admin'
    if userType == config.userTypeModerator:
        session['userType'] = 'moderator'
    if userType == config.userTypeDoctor:
        session['userType'] = 'doctor'
    if userType == config.userTypePatient:
        session['userType'] = 'patient'
    return session['userType']
#Редирект на страницу авторизации
@app.route('/', methods=['GET', 'POST'])
def default():
    return redirect('/login')
#Вывод списка пациентов
@app.route('/patients', methods =['GET', 'POST'])
def showUsers():
    if session['userType'] == 'admin' or session['userType'] == 'moderator' or session['userType'] == 'doctor':
        lastName = request.form.get('searchByLastName')
        selectForSearch = "SELECT * FROM patient where last_name = "+'"'+str(lastName)+'"'
        selectWithoutSearch = 'SELECT * FROM patient'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if lastName == None:
            cursor.execute(selectWithoutSearch)
        else:
            cursor.execute(selectForSearch)
            lastName = None
        patientData = cursor.fetchall()
        cursor.close()
        return render_template('/patients/user.html', patientData = patientData)
    else:
        return redirect('/service')
#При нажатии на кнопку "Подробнее" на странице с пациентами выводится информация о человеке
@app.route('/patients/patientInfo', methods =['GET', 'POST'])
def showInfoAboutUser():
    userID = request.args.get('userID')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select record_id, date_of_creation, caption, doctor.first_name, doctor.last_name, doctor.speciality, service.service_name, service.price, service_status.service_status from records"
                   " join doctor on records.doctor_doctor_id = doctor.doctor_id"
                   " join service on service.service_id = records.service_service_id"
                   " join service_status on service_status.id_service_status = records.service_status_id_service_status"
                   " where patient_patient_id = "+str(userID))
    recordsData = cursor.fetchall()
    cursor.execute("select * from patient where patient_id = " + str(userID))
    patientData = cursor.fetchall()
    cursor.close()
    return render_template('/patients/patientInfo.html', recordsData = recordsData, patientData = patientData)
#Обработчик формы для изменения данных о пациенте
@app.route('/patients/patientUpdate', methods =['GET', 'POST'])
def userUpdate():
    ID = request.form.get('patientID')
    firstName = request.form.get('first_name')
    lastName = request.form.get('last_name')
    userName = request.form.get('username')
    password = request.form.get('password')
    age = request.form.get('age')
    phone = request.form.get('phone')
    passport = request.form.get('passport')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE patient SET first_name = %s, last_name = %s, username = %s, password = %s, age = %s, phone = %s, passport = %s WHERE patient_id = %s', 
                   (firstName, lastName, userName, password, age, phone, passport, ID))
    mysql.connection.commit()
    cursor.close()
    return showUsers()
#Обработчик формы для изменения данных о пациенте
@app.route('/patients/changePatientInfo', methods =['GET', 'POST'])
def changeUserData():
    userID = request.args.get('userID')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from patient where patient_id = " + str(userID))
    userData = cursor.fetchall()
    cursor.close()
    return render_template('/patients/changeuserdata.html', userData = userData)
#Обработчик формы для добавления нового пациента
@app.route('/patients/addPatient', methods =['GET', 'POST'])
def addPatient():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        userName = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        phone = request.form.get('phone')
        passport = request.form.get('passport')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into patient SET first_name = %s, last_name = %s, username = %s, password = %s, age = %s, phone = %s, passport = %s, user_type_id_user_type = %s', 
                   (firstName, lastName, userName, password, age, phone, passport, config.userTypePatient))
        mysql.connection.commit()
        cursor.close()
        return showUsers()
    else:
        return render_template('/patients/addPatient.html')
#Вывод данных на страницу с записями приемов пациентов
@app.route('/records', methods =['GET', 'POST'])
def showRecords():
    if session['userType'] != 'patient':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT record_id, caption, date_of_creation, patient.first_name, patient.last_name, doctor.last_name as doctor_last_name, doctor.speciality, service.service_name, service.price,"
                    "service_status.service_status from records LEFT JOIN patient ON patient_patient_id = patient.patient_id LEFT JOIN doctor ON doctor.doctor_id = doctor_doctor_id"
                    " LEFT JOIN service ON service.service_id = service_service_id LEFT JOIN service_status ON service_status.id_service_status = service_status_id_service_status")
        recordsData = cursor.fetchall()
        cursor.close()

        return render_template('/records/records.html', recordsData = recordsData)
    else:
        return redirect('/service')
#Добавление новой записи при нажатии на кнопку "Записать на прием" в дополнительной информации о пациенте
@app.route('/patients/addRecord', methods =['GET', 'POST'])
def addRecord():
    patient_id = request.args.get('userID')
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select doctor_id, first_name, last_name, speciality from doctor where user_type_id_user_type = 1 or user_type_id_user_type = 3')
        doctorData = cursor.fetchall()
        cursor.execute('select * from service')
        serviceData = cursor.fetchall()
        cursor.close()
        return render_template('/records/addRecord.html', doctorData=doctorData, serviceData=serviceData)
    
    if request.method == 'POST':
        doctor = request.form.get('doctor')
        service = request.form.get('service')
        datetimeSet = request.form.get('datetime')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into records SET date_of_creation = %s, patient_patient_id = %s, doctor_doctor_id = %s, service_service_id = %s, service_status_id_service_status = 2',
                    (datetimeSet, patient_id, doctor, service))
        mysql.connection.commit()
        cursor.close()
        return showUsers()
#Обработчик формы для изменения записи
@app.route('/records/changeRecord', methods =['GET', 'POST'])
def changeRecord():
    recordID = request.args.get('recordID')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT record_id, caption, date_of_creation, patient.first_name, patient.last_name, doctor.last_name as doctor_last_name, doctor.speciality, service.service_name, service.price,"
                   "service_status.service_status from records LEFT JOIN patient ON patient_patient_id = patient.patient_id LEFT JOIN doctor ON doctor.doctor_id = doctor_doctor_id"
                   " LEFT JOIN service ON service.service_id = service_service_id LEFT JOIN service_status ON service_status.id_service_status = service_status_id_service_status"
                   " where records.record_id = "+str(recordID))
    recordData = cursor.fetchall()
    cursor.close()
    return render_template('/records/changeRecord.html', recordData = recordData)
#Обработчик формы для изменения записи
@app.route('/records/updateRecord', methods =['GET', 'POST'])
def updateRecord():
    record_id = request.args.get('record_id')
    caption = request.form.get('caption')
    status = request.form.get('status')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE records SET caption = %s, service_status_id_service_status = %s where record_id = %s', 
                   (caption, status, record_id))
    mysql.connection.commit()
    cursor.close()
    return showRecords()
#Вывод страницы о сотрудниках
@app.route('/users/showEmployee', methods =['GET', 'POST'])
def showEmployee():
    if session['userType'] == 'admin' or session['userType'] == 'moderator':
        lastName = request.form.get('searchByLastName')
        selectForSearch = "SELECT * FROM doctor where last_name = "+'"'+str(lastName)+'"'
        selectWithoutSearch = 'SELECT * FROM doctor'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if lastName == None:
            cursor.execute(selectWithoutSearch)
        else:
            cursor.execute(selectForSearch)
            lastName = None
        doctorData = cursor.fetchall()
        cursor.close()
        return render_template('/employees/showEmployee.html', doctorData = doctorData)
    else:
        return redirect('/service')
#Добавление нового сотрудника
@app.route('/users/addEmployee', methods =['GET', 'POST'])
def addEmployee():
    if request.method == 'GET':
        return render_template('/employees/addEmployee.html')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        speciality = request.form.get('speciality')
        usertype = request.form.get('usertype')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into doctor SET username = %s, password = %s, first_name = %s, last_name = %s,  age = %s, phone = %s, email = %s, speciality = %s, user_type_id_user_type = %s', 
                   (username, password, firstName, lastName, age, phone, email, speciality, usertype))
        mysql.connection.commit()
        cursor.close()
        return showEmployee()
#Изменение данных о сотруднике
@app.route('/users/changeEmployee', methods =['GET', 'POST'])
def changeEmployee():
    employeeID = request.args.get('employeeID')
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from doctor where doctor_id = %s', (employeeID))
        employeeData = cursor.fetchall()
        cursor.close()
        return render_template('/employees/changeEmployee.html', employeeData=employeeData)
    if request.method == 'POST':
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        speciality = request.form.get('speciality')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update doctor SET username = %s, password = %s, first_name = %s, last_name = %s,  age = %s, phone = %s, email = %s, speciality = %s where doctor_id = %s', 
                   (username, password, firstName, lastName, age, phone, email, speciality, employeeID))
        mysql.connection.commit()
        cursor.close()
        return showEmployee()
#Вывод страницы процедур
@app.route('/service', methods =['GET', 'POST'])
def showService():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from service')
    serviceData = cursor.fetchall()
    cursor.close()
    return render_template('/services/service.html', serviceData=serviceData)
#Добавление нового процедуры
@app.route('/service/addService', methods =['GET', 'POST'])
def addService():
    if request.method == 'GET':
        return render_template('/services/addService.html')
    if request.method == 'POST':
        service = request.form.get('serviceName')
        price = request.form.get('price')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into service set service_name = %s, price = %s', 
                   (service, price))
        mysql.connection.commit()
        cursor.close()
        return showService()
#Удаление процедуры 
@app.route('/service/serviceDelete', methods =['GET'])
def serviceDelete():
    service_id = request.args.get('service_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from service where service_id = %s', 
            (service_id))
    mysql.connection.commit()
    cursor.close()
    return showService()
#Удаление пациентов
@app.route('/patients/patientDelete', methods =['GET'])
def patientDelete():
    patient_id = request.args.get('userID')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from patient where patient_id = %s', 
            (patient_id))
    mysql.connection.commit()
    cursor.close()
    return showUsers()
#Удаление сотрудников
@app.route('/employees/employeeDelete', methods =['GET'])
def employeeDelete():
    employee_id = request.args.get('employee_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from doctor where doctor_id = %s', 
            (employee_id))
    mysql.connection.commit()
    cursor.close()
    return showEmployee()
#Удаление записей
@app.route('/records/recordDelete', methods =['GET'])
def recordDelete():
    recordID = request.args.get('recordID')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from records where record_id = %s', 
            (recordID))
    mysql.connection.commit()
    cursor.close()
    return showRecords()
#Формирование отчета о записях
@app.route('/reports', methods =['GET', 'POST'])
def formAndSendRecordsReport():
    if session['userType'] == 'admin' or session['userType'] == 'moderator':
        if request.method == 'GET':
            return render_template('reports.html')
        if request.method == 'POST':
            dateFrom = request.form.get('datefrom')
            dateTo = request.form.get('dateto')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT record_id as 'id',patient.first_name as 'Пациент.Имя', patient.last_name as 'Пациент.Фамилия', caption as 'Комментарий врача', date_of_creation as 'Дата', "
                        "doctor.last_name as 'Фамилия доктора', doctor.speciality as 'Специализация врача', service.service_name as 'Процедура', service.price as 'Стоимость услуги',"
                            "service_status.service_status as 'Статус приема' from records LEFT JOIN patient ON patient_patient_id = patient.patient_id LEFT JOIN doctor ON doctor.doctor_id = doctor_doctor_id"
                            " LEFT JOIN service ON service.service_id = service_service_id LEFT JOIN service_status ON service_status.id_service_status = service_status_id_service_status"
                            " where date_of_creation between %s and %s", (dateFrom, dateTo))
            report = cursor.fetchall()
            cursor.close()

        wb = Workbook()
        ws = wb.active
        fieldnames = ['id', 'Пациент.Имя', 'Пациент.Фамилия', 'Комментарий врача', 'Дата', 'Фамилия доктора', 'Специализация врача', 'Процедура', 'Стоимость услуги', 'Статус приема']
        ws.append(fieldnames)
        for record in report:
            values = (record[k] for k in fieldnames)
            ws.append(values)
        wb.save('static/reports/Отчет по записям.xlsx')
        return send_from_directory('static/reports/', 'Отчет по записям.xlsx')
    else: 
        return showService()
#Формирование отчета о сотрудниках
@app.route('/reports/employeereport', methods =['GET', 'POST'])
def formAndSendEmployeeReport():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select doctor_id as "id", username as "Логин", password as "Пароль", first_name as "Сотрудник.Имя", last_name as "Сотрудник.Фамилия", age as "Возраст", phone as "Телефон", email as "Почта", speciality as "Специальность", hours_worked as "Отработанные часы" from doctor')
        employeeData = cursor.fetchall()
        cursor.close()
        wb = Workbook()
        ws = wb.active
        fieldnames = ['id', 'Логин', 'Пароль', 'Сотрудник.Имя', 'Сотрудник.Фамилия', 'Возраст', 'Телефон', 'Почта', 'Специальность', 'Отработанные часы']
        ws.append(fieldnames)
        for record in employeeData:
            values = (record[k] for k in fieldnames)
            ws.append(values)
        wb.save('static/reports/Отчет по сотрудникам.xlsx')
        return send_from_directory('static/reports/', 'Отчет по сотрудникам.xlsx')

#Обработчик формы входа
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM (SELECT username, password, user_type_id_user_type FROM doctor UNION SELECT username, password, user_type_id_user_type FROM patient) as users WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['loggedin'] = True
            session['username'] = user['username']
            session['password'] = user['password']
            userTypeSetup(user['user_type_id_user_type'])
            print(session['userType'])
            mesage = 'Logged in successfully !'
            return showService()
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)
#Обработчик формы выхода
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    session.pop('userType', None)
    return redirect(url_for('login'))
#Инициализация приложения
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)