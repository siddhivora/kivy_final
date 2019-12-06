import my_fn
from kivy.uix.label import Label
import re
from datetime import date
from kivy.uix.popup import Popup

age = ''


# To Calculate The Age From Date Of Birth
def match(p_dob, p_age):
    global age
    dob_pattern = r'(((0[1-9]|[12][0-9]|3[01])([/])(0[13578]|10|12)([/])(\d{4}))|(([0][1-9]|[12][0-9]|30)([/])(0[469]|11)([/])(\d{4}))|((0[1-9]|1[0-9]|2[0-8])([/])(02)([/])(\d{4}))|((29)(\.|-|\/)(02)([/])([02468][048]00))|((29)([/])(02)([/])([13579][26]00))|((29)([/])(02)([/])([0-9][0-9][0][48]))|((29)([/])(02)([/])([0-9][0-9][2468][048]))|((29)([/])(02)([/])([0-9][0-9][13579][26])))'

    numbers = re.match(dob_pattern, p_dob.text)
    if numbers:
        curr_year = int(date.today().year)
        dob_year = int(p_dob.text[6:10])
        age = str(curr_year - dob_year)
        print(age)
        p_age.text = age + " Years"
    else:
        return True


# To check that weight and height is numeric only
def number_only(value):
    number_pattern = r'^[0-9]*$'
    number = re.match(number_pattern, value.text)
    if number:
        pass
    else:
        return True


# all the popus for all the response
def submit_popup(p_weight, p_height, p_smoke_yes, p_smoke_no, p_dob, p_age, p_fname, p_gender_f, p_gender_m,
                 p_gender_o,
                 p_lname, p_mname):
    # To get the radio button values
    global gender, smoke, age
    if p_smoke_yes.active:
        smoke = "Yes"
        print("smoker=" + smoke)
    else:
        smoke = "No"
        print("smoker=" + smoke)

    # To get the gender button values
    if p_gender_m.active:
        gender = "Male"
        print(gender)
    elif p_gender_f.active:
        gender = "Female"
        print(gender)
    elif p_gender_o.active:
        gender = "Other"
        print(gender)
    # Popups For Submit Button
    pop_sub = Popup(title="Submit", title_align="center", content=Label(text="Information Submitted Successfully"),
                    size=(300, 200),
                    size_hint=(None, None), auto_dismiss=True)

    pop_empty = Popup(title="Error", title_align="center",
                      content=Label(text="Empty Field.\nPlease Fill All Information"),
                      size=(300, 200),
                      size_hint=(None, None), auto_dismiss=True)

    pop_gender = Popup(title="Error", title_align="center",
                       content=Label(text="Please Select A Gender."),
                       size=(300, 200),
                       size_hint=(None, None), auto_dismiss=True)
    pop_number = Popup(title="Error", title_align="center",
                       content=Label(text="Height and Weight Must be numbers."),
                       size=(300, 200),
                       size_hint=(None, None), auto_dismiss=True)
    dob_pop = Popup(title="Error", size=(280, 200), size_hint=(None, None),
                    content=Label(text="Please Enter a valid Date Of Birth. \n(e.g. 01/01/1999)"))

    if p_fname.text == '' or p_height.text == '' or p_weight.text == '' \
            or p_dob.text == '' or p_mname.text == '' or p_lname.text == '':
        pop_empty.open()
    elif number_only(p_weight) or number_only(p_height):
        pop_number.open()
        p_weight.text = ''
        p_height.text = ''
    elif match(p_dob, p_age):
        dob_pop.open()
        p_age.text = ''
    elif p_gender_m.active == False and p_gender_f.active == False and p_gender_o.active == False:
        pop_gender.open()
    else:
        my_fn.fun(p_fname, p_mname, p_lname, p_height, p_weight, p_dob, smoke, gender, age)
        pop_sub.open()
