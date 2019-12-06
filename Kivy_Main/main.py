import mysql.connector
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.graph import MeshLinePlot
import cnumpy
import spidev
import report
import form
import my_fn
import time
import math
from pre_graph import *
from functools import partial

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

Config.set('kivy', 'keyboard_mode', 'systemanddocked')
from os import listdir
kv_path = './KV/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="db1")
mycursor = mydb.cursor()

age = ''
levels = []
screen_mgr = ScreenManager(id="screen_mgr")
'''
pr_fev1_avg = 0
pr_fvc_avg = 0
pr_fev1_fvc_avg = 0
pr_fet_avg = 0
pr_pef_avg = 0
pr_fef25_avg = 0
pr_fef_50_75_avg = 0
post_fev1_avg = 0
post_fvc_avg = 0
post_fev1_fvc_avg = 0
post_fet_avg = 0
post_pef_avg = 0
post_fef25_avg = 0
post_fef_50_75_avg = 0
'''

class HomeScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class TestScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class PreTestScreen(Screen):
    click = 0
        
    def print__(self):
        print "start" 

    def change_screen(self):
        self.click += 1
        if self.click == 6:
            #self.calculate_average()
            self.manager.current = "PrePostTest_Screen"
            self.click = 0
    def calculate_average(self):
        from pre_graph import pr_fev1_avg, pr_fvc_avg, pr_fev1_fvc_avg, pr_pef_avg, pr_fef25_avg, pr_fef_50_75_avg
        global pr_fev1_avg, pr_fvc_avg, pr_fev1_fvc_avg, pr_fet_avg, pr_pef_avg, pr_fef25_avg, pr_fef_50_75_avg
        pr_fev1_avg = pr_fev1_avg / 6
        pr_fvc_avg = pr_fvc_avg / 6
        pr_fev1_fvc_avg = pr_fev1_fvc_avg / 6
        pr_fet_avg = t
        pr_pef_avg = pr_pef_avg / 6
        pr_fef25_avg = pr_fef25_avg /6
        pr_fef_50_75_avg = pr_fef_50_75_avg / 6
        
        # calculates average of all the pre tests.
        print ('check this2', pr_fev1_avg, pr_fvc_avg)
        print (pr_fev1_fvc_avg, pr_fet_avg, pr_pef_avg)
        print (pr_fef25_avg, pr_fef_50_75_avg) 
        
        '''pr_fvc_avg = ((float(self.ids['p_pr_fvc_t1'].text) + float(self.ids['p_pr_fvc_t2'].text) +
                       float(self.ids['p_pr_fvc_t3'].text) + float(self.ids['p_pr_fvc_t4'].text) +
                       float(self.ids['p_pr_fvc_t5'].text) + float(self.ids['p_pr_fvc_t6'].text)) / 6)

        pr_fev1_fvc_avg = ((int(self.ids.p_pr_fev1_fvc_t1.text) + int(self.ids.p_pr_fev1_fvc_t2.text) +
                            int(self.ids.p_pr_fev1_fvc_t3.text) + int(self.ids.p_pr_fev1_fvc_t4.text) +
                            int(self.ids.p_pr_fev1_fvc_t5.text) + int(self.ids.p_pr_fev1_fvc_t6.text)) / 6)

        pr_fet_avg = ((int(self.ids.p_pr_fet_t1.text) + int(self.ids.p_pr_fet_t2.text) +
                       int(self.ids.p_pr_fet_t3.text) + int(self.ids.p_pr_fet_t4.text) +
                       int(self.ids.p_pr_fet_t5.text) + int(self.ids.p_pr_fet_t6.text)) / 6)

        pr_pef_avg = ((int(self.ids.p_pr_pef_t1.text) + int(self.ids.p_pr_pef_t2.text) +
                       int(self.ids.p_pr_pef_t3.text) + int(self.ids.p_pr_pef_t4.text) +
                       int(self.ids.p_pr_pef_t5.text) + int(self.ids.p_pr_pef_t6.text)) / 6)

        pr_fef25_avg = ((int(self.ids.p_pr_fef25_t1.text) + int(self.ids.p_pr_fef25_t2.text) +
                         int(self.ids.p_pr_fef25_t3.text) + int(self.ids.p_pr_fef25_t4.text) +
                         int(self.ids.p_pr_fef25_t5.text) + int(self.ids.p_pr_fef25_t6.text)) / 6)

        pr_fef_50_75_avg = ((int(self.ids.p_pr_fef50_75_t1.text) + int(self.ids.p_pr_fef50_75_t2.text) +
                             int(self.ids.p_pr_fef50_75_t3.text) + int(self.ids.p_pr_fef50_75_t4.text) +
                             int(self.ids.p_pr_fef50_75_t5.text) + int(self.ids.p_pr_fef50_75_t6.text)) / 6)'''
        
    def __init__(self, **kw):
        super(PreTestScreen, self).__init__(**kw)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot1 = MeshLinePlot(color=[1, 0, 0, 1])        
            
    def start(self):        
        #pre_graph.start(self)
        start(self)

    def VOlume_graph(self):
        volume_graph(self)
        
    def submit(self):
        submit(self)
        

    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class PostTestScreen(Screen):
    clicks = 0

    def change_screen(self):
        self.clicks += 1
        if self.clicks == 6:
            self.manager.current = "Test_Result_Screen"
            pre_result = Pre_Result()
            #pre_result.print_fev1()
            #pre_result.print_fvc()
    def __init__(self, **kw):
        super(PostTestScreen, self).__init__(**kw)
        #self.plot2 = MeshLinePlot(color=[1, 0, 0, 1])
        #self.plot3 = MeshLinePlot(color=[1, 0, 0, 1])
        
        
    def calculate_average(self):
        from pre_graph import post_fev1_avg, post_fvc_avg, post_fev1_fvc_avg, post_pef_avg, post_fef25_avg, post_fef_50_75_avg
        global post_fev1_avg, post_fvc_avg, post_fev1_fvc_avg, post_fet_avg, post_pef_avg, post_fef25_avg \
            , post_fef_50_75_avg
        post_fev1_avg = post_fev1_avg / 6
        post_fvc_avg = post_fvc_avg / 6
        post_fev1_fvc_avg = post_fev1_fvc_avg / 6
        post_fet_avg = t
        post_pef_avg = post_pef_avg / 6
        post_fef25_avg = post_fef25_avg /6
        post_fef_50_75_avg = post_fef_50_75_avg / 6
        
        print ('check this3', post_fev1_avg, post_fvc_avg)
        print (post_fev1_fvc_avg, post_fet_avg, post_pef_avg)
        print (post_fef25_avg, post_fef_50_75_avg)
        
        '''
        # calculates average of all the pre tests.
        post_fev1_avg = ((int(self.ids['p_post_fev1_t1'].text) + int(self.ids['p_post_fev1_t2'].text) +
                          int(self.ids['p_post_fev1_t3'].text) + int(self.ids['p_post_fev1_t4'].text) +
                          int(self.ids['p_post_fev1_t5'].text) + int(self.ids['p_post_fev1_t6'].text)) / 6)

        post_fvc_avg = ((int(self.ids.p_post_fvc_t1.text) + int(self.ids.p_post_fvc_t2.text) +
                         int(self.ids.p_post_fvc_t3.text) + int(self.ids.p_post_fvc_t4.text) +
                         int(self.ids.p_post_fvc_t5.text) + int(self.ids.p_post_fvc_t6.text)) / 6)

        post_fev1_fvc_avg = ((int(self.ids.p_post_fev1_fvc_t1.text) + int(self.ids.p_post_fev1_fvc_t2.text) +
                              int(self.ids.p_post_fev1_fvc_t3.text) + int(self.ids.p_post_fev1_fvc_t4.text) +
                              int(self.ids.p_post_fev1_fvc_t5.text) + int(self.ids.p_post_fev1_fvc_t6.text)) / 6)

        post_fet_avg = ((int(self.ids.p_post_fet_t1.text) + int(self.ids.p_post_fet_t2.text) +
                         int(self.ids.p_post_fet_t3.text) + int(self.ids.p_post_fet_t4.text) +
                         int(self.ids.p_post_fet_t5.text) + int(self.ids.p_post_fet_t6.text)) / 6)

        post_pef_avg = ((int(self.ids.p_post_pef_t1.text) + int(self.ids.p_post_pef_t2.text) +
                         int(self.ids.p_post_pef_t3.text) + int(self.ids.p_post_pef_t4.text) +
                         int(self.ids.p_post_pef_t5.text) + int(self.ids.p_post_pef_t6.text)) / 6)

        post_fef25_avg = ((int(self.ids.p_post_fef25_t1.text) + int(self.ids.p_post_fef25_t2.text) +
                           int(self.ids.p_post_fef25_t3.text) + int(self.ids.p_post_fef25_t4.text) +
                           int(self.ids.p_post_fef25_t5.text) + int(self.ids.p_post_fef25_t6.text)) / 6)

        post_fef_50_75_avg = ((int(self.ids.p_post_fef50_75_t1.text) + int(self.ids.p_post_fef50_75_t2.text) +
                               int(self.ids.p_post_fef50_75_t3.text) + int(self.ids.p_post_fef50_75_t4.text) +
                               int(self.ids.p_post_fef50_75_t5.text) + int(self.ids.p_post_fef50_75_t6.text)) / 6)
        '''
    def start(self):        
        start_post(self)

    def VOlume_graph(self):
        volume_graph_post(self)
        
    def submit(self):
        submit_post(self)
    
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class TestResultScreen(Screen):    
    def __init__(self, **kw):
        super(TestResultScreen, self).__init__(**kw)
        pre_result = Pre_Result()
        self.ids.pre_btn.on_press = partial(pre_result.try_fn)    
        
    def mail_popup(self):
        report.popup()

    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


# Pre Results Screen inside Test Result Screen
class Pre_Result(Screen):
    print 'pre_result running'
    global pr_fev1_avg, pr_fvc_avg, pr_fev1_fvc_avg, pr_fet_avg, pr_pef_avg, pr_fef25_avg, pr_fef_50_75_avg
    #print ('check this22', pr_fev1_avg, pr_fvc_avg)
    #def __init__(self, **kw):
        #super(Pre_Result, self).__init__(**kw)
        #self.ids.tr_pr_fvc.text = self.print_pef()
    
    def try_fn(self): 
        print 'try_fn'
        Builder.load_string('''        
<Pre_Result>:
    name: 'Pre_Result'
    FloatLayout:
        size_hint: (None,None)
        size: (620,280)
        pos: (140,125)
        canvas:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                size: self.size
                pos: self.pos
        Label:
            markup: True
            id:tr_pr_fvc
            #color: (0,0,0)
            text: 'bhagwan'
            size_hint:(None,None)
            pos: (240,250)
            bold:True
            font_size: '15px'

'''
        )
    
    def print_fev1(self):
        global pr_fev1_avg
        print('dekho', pr_fev1_avg)
        #self.ids.tr_pr_fev1.markup = True
        #self.ids.tr_pr_fev1.text = '[color=#0000c8]FVC[/color]'
        #self.ids.tr_pr_fev1.color = (0,0,0,1)
        #self.ids.tr_pr_fev1.font_size = '15px'
        #self.ids.tr_pr_fev1.pos = (240, 280)
        self.ids.tr_pr_fev1.text = 'rt'
        print (self.ids.tr_pr_fev1.text)
        return str(pr_fev1_avg)

    def print_fvc(self):
        global pr_fvc_avg
        print('fvc running')
        #self.ids.tr_pr_fvc.color = (0,0,0,1)
        #self.ids.tr_pr_fvc.text = str('rt')
        return str(pr_fvc_avg)

    def print_fev1_fvc(self):
        global pr_fev1_fvc_avg
        print(pr_fev1_fvc_avg)
        return str(pr_fev1_fvc_avg)

    def print_fet(self):
        global pr_fet_avg
        print(pr_fet_avg)
        return str(pr_fet_avg)

    def print_pef(self):
        global pr_pef_avg
        print(pr_pef_avg)
        return str(pr_pef_avg)

    def print_fef25(self):
        global pr_fef25_avg
        print(pr_fef25_avg)
        return str(pr_fef25_avg)

    def print_fef50_75(self):
        global pr_fef_50_75_avg
        print(pr_fef_50_75_avg)
        return str(pr_fef_50_75_avg)


# Post Results Screen inside Test Result Screen
class Post_Result(Screen):
    def print_fev1(self):
        global post_fev1_avg
        print(post_fev1_avg)
        return str(post_fev1_avg)

    def print_fvc(self):
        global post_fvc_avg
        print(post_fvc_avg)
        return str(post_fvc_avg)

    def print_fev1_fvc(self):
        global pr_fev1_fvc_avg
        print(pr_fev1_fvc_avg)
        return str(post_fev1_fvc_avg)

    def print_fet(self):
        global pr_fet_avg
        print(pr_fet_avg)
        return str(post_fet_avg)

    def print_pef(self):
        global pr_pef_avg
        print(pr_pef_avg)
        return str(post_pef_avg)

    def print_fef25(self):
        global pr_fef25_avg
        print(pr_fef25_avg)
        return str(post_fef25_avg)

    def print_fef50_75(self):
        global pr_fef_50_75_avg
        print(pr_fef_50_75_avg)
        return str(post_fef_50_75_avg)


class FormScreen(Screen):
    yes = ObjectProperty(True)
    no = ObjectProperty(True)

    def submit_popup(self):
        p_weight = self.ids.p_weight
        p_height = self.ids.p_height
        p_smoke_yes = self.ids.p_smoke_yes
        p_smoke_no = self.ids.p_smoke_no
        p_gender_m = self.ids.p_gender_m
        p_gender_f = self.ids.p_gender_f
        p_gender_o = self.ids.p_gender_o
        p_fname = self.ids.p_fname
        p_mname = self.ids.p_mname
        p_lname = self.ids.p_lname
        p_dob = self.ids.p_dob
        p_age = self.ids.p_age
        form.submit_popup(p_weight, p_height, p_smoke_yes, p_smoke_no, p_dob, p_age,
                          p_fname, p_gender_f,
                          p_gender_m,
                          p_gender_o,
                          p_lname, p_mname)

    def __init__(self, **kw):
        super(FormScreen, self).__init__(**kw)
        self.ids["p_id"].color = (0, 0, 1, 1)
        self.ids["p_id"].text = my_fn.count_pid()

    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class RegistrationScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class PrePostTestScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class AlreadyRegisteredScreen(Screen):
    def __init__(self, **kw):
        super(AlreadyRegisteredScreen, self).__init__(**kw)
        '''self.ids.search_btn.on_press = partial(my_fn.fetch_info, self,
                                               self.ids['pa_fname'].text,
                                               self.ids['pa_lname'].text, self.ids['pa_id'].text)'''
        self.ids.search_btn.bind(on_press=lambda x: self.prints())
        self.ids.p_id.color = (0, 0, 0, 1)
        self.ids.p_id.bold = True
        self.ids.p1_name.markup = True
        self.ids.p_id.font = "OpenSans"
        self.ids.p1_id.color = (0, 0, 0, 1)
        self.ids.p1_name.color = (0, 0, 0, 1)
        self.ids.p1_gender.color = (0, 0, 0, 1)
        self.ids.p2_id.color = (0, 0, 0, 1)
        self.ids.p2_name.color = (0, 0, 0, 1)
        self.ids.p2_gender.color = (0, 0, 0, 1)
        self.ids.p3_id.color = (0, 0, 0, 1)
        self.ids.p3_name.color = (0, 0, 0, 1)
        self.ids.p3_gender.color = (0, 0, 0, 1)

    def prints(self):
        my_fn.fetch_info(self, self.ids.pa_fname.text, self.ids.pa_lname.text, self.ids.pa_id.text)

    def exit_prog(self):
        App.get_running_adminapp().stop()
        Window.close()


class CongratsScreen(Screen, Image):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class QuestionScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()

    def edit(self):
        self.ids.cb_dyspnea.disabled = False
        self.ids.cb_sputum.disabled = False
        self.ids.cb_cough.disabled = False
        self.ids.cb_wheezing.disabled = False
        self.ids.cb_yes.disabled = False
        self.ids.cb_no.disabled = False

    def submit(self):
        self.ids.cb_dyspnea.disabled = True
        self.ids.cb_sputum.disabled = True
        self.ids.cb_cough.disabled = True
        self.ids.cb_wheezing.disabled = True
        self.ids.cb_yes.disabled = True
        self.ids.cb_no.disabled = True


class YesNoQuestionScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()

    def submit(self):
        self.ids.cb1_no.disabled = True
        self.ids.cb1_yes.disabled = True
        self.ids.cb2_no.disabled = True
        self.ids.cb2_yes.disabled = True
        self.ids.cb3_no.disabled = True
        self.ids.cb3_yes.disabled = True
        self.ids.cb4_no.disabled = True
        self.ids.cb4_yes.disabled = True
        self.ids.cb5_no.disabled = True
        self.ids.cb5_yes.disabled = True
        self.ids.cb6_no.disabled = True
        self.ids.cb6_yes.disabled = True
        self.ids.cb7_no.disabled = True
        self.ids.cb7_yes.disabled = True

    def edit(self):
        self.ids.cb1_no.disabled = False
        self.ids.cb1_yes.disabled = False
        self.ids.cb2_no.disabled = False
        self.ids.cb2_yes.disabled = False
        self.ids.cb3_no.disabled = False
        self.ids.cb3_yes.disabled = False
        self.ids.cb4_no.disabled = False
        self.ids.cb4_yes.disabled = False
        self.ids.cb5_no.disabled = False
        self.ids.cb5_yes.disabled = False
        self.ids.cb6_no.disabled = False
        self.ids.cb6_yes.disabled = False
        self.ids.cb7_no.disabled = False
        self.ids.cb7_yes.disabled = False


class ContactScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class DiagnosisScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class TreatmentScreen(Screen):
    trt_list = ['oxygen_therapy', 'vaccination', 'bronchodilator', 'pulmonary_rehabilitation', 'smoking_cessation']

    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class COPDScreen(Screen):

    # def show_options(self):
    #   my_fn.trtmnt_name()

    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class SvcScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class Svc1Screen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class SvcInfoScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class SvcInfo2Screen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class VaccinationScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class PulseOximetryScreen(Screen):
    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class AdminMain(Screen):
    def admin_logout(self):
        screen_mgr.current = "AdminLogin_Screen"
    

class AdminLogin(Screen):
    def admin_login(self):
        if self.ids.admin_un.text == 'admin' and self.ids.admin_pw.text == 'admin':
            screen_mgr.current = 'AdminMain_Screen'
            self.ids.admin_un.text = ''
            self.ids.admin_pw.text = ''
            print(self)
        else:
            Popup(title="Invalid Details", title_align="center",
                  content=Label(text="Invalid Username/Password."),
                  size=(300, 200),
                  size_hint=(None, None), auto_dismiss=True).open()
            self.ids.admin_un.text = ''
            self.ids.admin_pw.text = ''


class DrugsName(Screen):
    list = ['abc', 'bcd', 'cde']

    def exit_prog(self):
        App.get_running_app().stop()
        Window.close()


class ThisApp(App):
    def build(self):
        screen_mgr.add_widget(RegistrationScreen(name="Registration_Screen"))
        screen_mgr.add_widget(FormScreen(name="Form_Screen"))
        screen_mgr.add_widget(PrePostTestScreen(name="PrePostTest_Screen"))
        screen_mgr.add_widget(AlreadyRegisteredScreen(name="AlreadyRegistered_Screen"))
        screen_mgr.add_widget(HomeScreen(name="Home_Screen"))
        screen_mgr.add_widget(TestScreen(name="Test_Screen"))
        screen_mgr.add_widget(PreTestScreen(name="Pre_Test_Screen"))
        screen_mgr.add_widget(PostTestScreen(name="Post_Test_Screen"))
        screen_mgr.add_widget(TestResultScreen(name="Test_Result_Screen"))
        screen_mgr.add_widget(CongratsScreen(name="Congrats_Screen"))
        screen_mgr.add_widget(QuestionScreen(name="Question_Screen"))
        screen_mgr.add_widget(YesNoQuestionScreen(name="YesNoQuestion_Screen"))
        screen_mgr.add_widget(ContactScreen(name="Contact_Screen"))
        screen_mgr.add_widget(DiagnosisScreen(name="Diagnosis_Screen"))
        screen_mgr.add_widget(TreatmentScreen(name="Treatment_Screen"))
        screen_mgr.add_widget(COPDScreen(name="COPD_Screen"))
        screen_mgr.add_widget(SvcScreen(name="Svc_Screen"))
        screen_mgr.add_widget(Svc1Screen(name="Svc1_Screen"))
        screen_mgr.add_widget(SvcInfoScreen(name="SvcInfo_Screen"))
        screen_mgr.add_widget(SvcInfo2Screen(name="SvcInfo2_Screen"))
        screen_mgr.add_widget(VaccinationScreen(name="Vaccination_Screen"))
        screen_mgr.add_widget(PulseOximetryScreen(name="PulseOximetry_Screen"))
        screen_mgr.add_widget(AdminLogin(name="AdminLogin_Screen"))
        screen_mgr.add_widget(AdminMain(name="AdminMain_Screen"))
        screen_mgr.add_widget(DrugsName(name="DrugsName_Screen"))
        return screen_mgr


if __name__ == '__main__':
    ThisApp().run()
