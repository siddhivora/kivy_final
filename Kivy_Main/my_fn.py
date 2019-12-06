from datetime import datetime
from datetime import date
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="db1")
mycursor = mydb.cursor()


def fun(p_fname, p_mname, p_lname, p_height, p_weight, p_dob, smoke, gender, age):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    datetime_str = p_dob.text
    datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y').date()
    print(datetime_str)
    print(datetime_object)

    sql = "INSERT INTO jp_mst (p_fname, p_mname, p_lname, p_height, p_weight, p_dob, p_age, p_gender, p_smoke) VALUE( " \
          "%s, %s, %s, %s, %s, %s, %s, %s, %s) "
    val = (p_fname.text, p_mname.text, p_lname.text, p_height.text, p_weight.text, datetime_object, age, gender, smoke)
    mycursor.execute(sql, val)
    mydb.commit()
    print('Submitted')


def count_pid():
    mycursor.execute("SELECT count(p_id) FROM jp_mst ")
    myresult = mycursor.fetchone()
    for x in myresult:
        # p_id = str(x+1)
        return str(x + 1)


# global fetch_info
def fetch_info(self, pa_fname, pa_lname, pa_id=None):
    print(pa_fname, pa_id, pa_lname)
    print(self.ids.p_id.text)
    self.ids.p1_id.text = ''
    self.ids.p1_name.text = ''
    self.ids.p1_gender.text = ''
    self.ids.p2_id.text = ''
    self.ids.p2_name.text = ''
    self.ids.p2_gender.text = ''
    self.ids.p3_id.text = ''
    self.ids.p3_name.text = ''
    self.ids.p3_gender.text = ''

    def print_it(patient_id):
        self.ids.p_id.text = patient_id

    if pa_id != '':

        sql = "select p_id , concat_ws(' ',p_fname,p_mname,p_lname) ,p_gender from jp_mst where p_id = %s and p_fname " \
              "= %s and p_lname = %s "
        val = (pa_id, pa_fname, pa_lname)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            p1_id = str(x[0])
            p1_name = str(x[1])
            p1_gender = str(x[2])
            self.ids.p1_id.text = p1_id
            self.ids.p1_gender.text = p1_gender
            self.ids.p1_name.text = p1_name
            self.ids.p1_name.bind(on_press=lambda v: print_it(p1_id))
            print(self.ids.p_id.text)
    else:

        sql = "select p_id , concat_ws(' ',p_fname,p_mname,p_lname) ,p_gender from jp_mst where p_fname = %s and " \
              "p_lname = %s "
        val = (pa_fname, pa_lname)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        pa_id = []
        pa_name = []
        pa_gender = []
        i = 0

        for x in myresult:
            pa_id.append(str(x[0]))
            pa_name.append(str(x[1]))
            pa_gender.append(str(x[2]))
            i = i + 1

        if i == 0:
            print("error")
        elif i == 1:
            self.ids.p1_id.text = pa_id[0]
            self.ids.p1_name.text = pa_name[0]
            self.ids.p1_gender.text = pa_gender[0]
            self.ids.p1_name.bind(on_press=lambda v: print_it(pa_id[0]))
        elif i <= 2:
            self.ids.p1_id.text = pa_id[0]
            self.ids.p1_name.text = pa_name[0]
            self.ids.p1_gender.text = pa_gender[0]
            self.ids.p2_id.text = pa_id[1]
            self.ids.p2_name.text = pa_name[1]
            self.ids.p2_gender.text = pa_gender[1]
            self.ids.p1_name.bind(on_press=lambda v: print_it(pa_id[0]))
            self.ids.p2_name.bind(on_press=lambda v: print_it(pa_id[1]))
        elif i > 2:
            self.ids.p1_id.text = pa_id[0]
            self.ids.p1_name.text = pa_name[0]
            self.ids.p1_gender.text = pa_gender[0]
            self.ids.p2_id.text = pa_id[1]
            self.ids.p2_name.text = pa_name[1]
            self.ids.p2_gender.text = pa_gender[1]
            self.ids.p3_id.text = pa_id[2]
            self.ids.p3_name.text = pa_name[2]
            self.ids.p3_gender.text = pa_gender[2]
            self.ids.p1_name.bind(on_press=lambda v: print_it(pa_id[0]))
            self.ids.p2_name.bind(on_press=lambda v: print_it(pa_id[1]))
            self.ids.p3_name.bind(on_press=lambda v: print_it(pa_id[2]))


# global pretest_info
def pretest_info():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    sql = "INSERT INTO jp_tx (p_id, p_registration) VALUES (%s, %s)"
    val = ('1', formatted_date)

    mycursor.execute(sql, val)

    mydb.commit()
    print("ok")
    mycursor.execute(sql, val)
    print("nice")
    mydb.commit
    print("well good")
