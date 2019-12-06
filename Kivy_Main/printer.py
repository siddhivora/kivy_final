import commands 
import webbrowser
from selenium import webdriver

def add_():
	ip_add = commands.getoutput('hostname -I')
	url = 'http://{ip_add}:631/admin'.format(ip_add=ip_add)
	final_url = url.replace(" ","")
	options = webdriver.ChromeOptions()
	options.binary_location = '/usr/lib/chromium-browser/chromium-browser'
	driver = webdriver.Chrome(chrome_options=options)
	chromium.get(final_url)
add_()	
