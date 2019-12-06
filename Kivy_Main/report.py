import smtplib
import webbrowser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class widgets(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lbl = self.lbl = Label(text="Enter Your Email Id", pos=(330, 280), size=(150, 100), size_hint=(None, None),
                               halign='justify')
        btn1 = self.btn1 = Button(text="Send", pos=(320, 220), size=(80, 30), size_hint=(None, None))
        btn = self.btn = Button(text="Cancel", pos=(410, 220), size=(80, 30), size_hint=(None, None))
        ti = self.ti = TextInput(multiline=False, use_bubble=True, hint_text='example@gmail.com', pos=(310, 270),
                                 size=(200, 30),
                                 size_hint=(None, None))
        self.add_widget(lbl)
        self.add_widget(btn)
        self.add_widget(btn1)
        self.add_widget(ti)


def popup():
    widg = widgets()
    greet = Popup(title="Send Report To Email", content=widg, size=(290, 200), size_hint=(None, None),
                  auto_dismiss=False)
    greet.open()
    widg.btn.bind(on_press=lambda x: greet.dismiss())
    widg.btn1.bind(on_press=lambda b: send_email(mail, widg.ti.text))


def send_email(mail, mail_id):
    sender = "jamesshah@gecg28.ac.in"
    passwd = "vcygwfmsnzargutb"
    reciever = mail_id
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.ehlo()
    server.login(sender, passwd)
    server.sendmail(sender, reciever, mail)
    print("Mail Sent Successfully!")


mail = 'Subject: "Quote Of The Day"\n\n Hello There.'.format()


class ThisApp(App):

    def build(self):
        return popup()
