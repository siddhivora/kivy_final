import time
import numpy as np
import math
import scipy
from scipy import integrate
import spidev
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot
import cnumpy

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

global levels
levels = []
global plot
plot = MeshLinePlot(color=[0, 0, 1, 1])
global plot1
plot1 = MeshLinePlot(color=[1, 0, 1, 1])

global t
t = 6     # exhalation time
vsource = 3.3   # supply voltage
global t_time
t_time = []
global t_volt
t_volt = []
global t_pressure
t_pressure = []
global t_flow
t_flow = []
global t_volume
t_volume = []
global flow_best
flow_best = []
global volume_best
volume_best = []
global t_p_volume
t_p_volume = []
global rt_volume
rt_volume = []
# Define sensor channels
adc_channel = 0 
# Define delay between readings
samples=5000
delay = (t/float(samples))

global pr_fev1_avg
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

def ReadChannel(channel):	
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
        
def ConvertVolts(data,places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts,places)
	return volts
	
def get_level(dt): 
	global levels
	global t 
	global t_time
	global t_volt
	global t_pressure
	global t_flow 
	global rt_volume
	#t_flow = []	
	data = ReadChannel(7)            
	mx = ConvertVolts(data, 5) 
	t_volt.append(mx)
	mx = (((750 *mx)/vsource)-150)		
	if mx < 0:      # mx is complex so we need to define mx as real or imaginary
		mx = 0  
	t_pressure.append(mx)
	mx = math.sqrt(mx) * 0.533      # cmath gives complex sqrt
	if mx < 0:      # mx is complex so we need to define mx as real or imaginary
		mx = 0      
	t_flow.append(mx)
	t_time = np.linspace(0,t,len(t_flow))
	single_volume = np.trapz(t_flow, t_time)
	rt_volume.append(single_volume)
	if len(levels) >= 100:
		levels = []
		Clock.unschedule(get_level)
	levels.append(mx)
	print (len(t_time), len(t_flow), len(t_volt))	
	
def start(self):
	global plot
	global plot1	
	global t
	global levels
	global t_flow
	global t_volt
	global t_end
	t_end = time.time() + t
	levels = []	 
	t_flow = []
	t_volt = []
	print ('check', levels)
	#plot = MeshLinePlot(color=[1, 0, 0, 1])
	self.ids.pre_start.add_plot(plot)
	self.ids.pre_svg.add_plot(plot1)
	Clock.schedule_interval(get_value, 0.1)
	Clock.schedule_interval(stop, 0.1)


def stop(dt):
	global t_end
	if time.time() >= t_end:
		Clock.unschedule(get_value)

def get_value(dt):
	global plot	      
	global levels
	Clock.schedule_once(get_level)	
	plot.points = [(i, j) for i, j in enumerate(levels)]

def volume_graph(self):
	global t_time        
	global t_flow
	global t_volume
	global t_p_volume
	global FEV1
	global plot1 
	#print t_flow
	graph_volume = []       
	dy = []
	dy0 = []
	dy1=0
	lim=np.size(t_flow)
	j = 0
	t_volume= []
	t_p_volume = []
	#print (len(t_flow), len(t_time))
	for i in range(lim):
	  dy1=0
	  global FVC
	  dy1=scipy.integrate.trapz(t_flow[i:i+2],t_time[i:i+2])
	  j = j+dy1
	  if i == 12:
		  FEV1 = j
		  FEV1 = round(FEV1, 3)
	  FVC = j
	  FVC = round(FVC, 3)
	  dy.append(j) 
	  dy0.append(dy1)       
	t_volume = dy
	#print t_volume
	graph_volume = t_volume
	t_p_volume = dy0
	t_time = np.linspace(0,t,len(t_flow))
	
	plot1.points = [(t_time[i], graph_volume[i]) for i in range(len(graph_volume))]
	graph_volume = []
	''' 
	with open('volume_trial.csv', 'wb') as csvFile:
			fieldnames = ['dy', 'dy0', 't_volume', 't_p_volume']
			writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(np.size(dy)):
					writer.wrifgfgterow({'dy':dy[i], 'dy0':dy0[i], 't_volume':t_volume[i], 't_p_volume':t_p_volume[i]})
	'''
	dy = []
	dy0 = []
	dy1=0	

global submit_time
submit_time = 0

global PEF
PEF = 0
global FET
FET = 6
global FEF25
FEF25 = 0
global FEF50
FEF50 = 0
global FVC
FVC = 0

global PEF_t
PEF_t = 0
global FVC_t
FVC_t = 0
global FEV1_t
FEV1_t = 0
global FEV1FVC_t
FEV1FVC_t = 0
global FEF25_t
FEF25_t = 0
global FEF50_t
FEF50_t = 0

def submit(self):
	global submit_time
	global flow_best
	global volume_best
	global t_time
	global t_pressure
	global t_flow
	global t_volume
	global PEF
	global FVC
	global FEV1
	global FEV1FVC
	global FEF25
	global FEF50
	
	global PEF_t
	global FVC_t
	global FEV1_t
	global FEV1FVC_t
	global FEF25_t
	global FEF50_t
	
	global fev11
	fev11 = 0
	global fev12
	fev12 = 0
	global fev13
	fev13 = 0
	
	global pr_fev1_avg, pr_fvc_avg, pr_fev1_fvc_avg, pr_fet_avg, pr_pef_avg, pr_fef25_avg, pr_fef_50_75_avg
	
	submit_time = submit_time + 1        
	PEF = max(t_flow)
	PEF = round(PEF, 3)
	FEV1FVC = FEV1 / FVC
	FEV1FVC = round(FEV1FVC, 3) 
	for i in range (60):
		if i == 15:
			FEF25 = t_flow[i]
			FEF25 = round(FEF25, 3)
		if i == 30:
			FEF50 = t_flow[i]
			FEF50 = round(FEF50, 3)
	if submit_time == 1:
		global fev11
		flow_best = t_flow            
		volume_best = t_volume
		print (len(flow_best),len(volume_best))
		self.ids.p_pr_fvc_t1.text = str(FVC)
		
		pr_fvc_avg = pr_fvc_avg + FVC
		self.ids.p_pr_fev1_t1.text = str(FEV1)
		fev11 = FEV1
		pr_fev1_avg = pr_fev1_avg + FEV1		
		self.ids.p_pr_pef_t1.text = str(PEF)
		pr_pef_avg = pr_pef_avg + PEF
		
		self.ids.p_pr_fet_t1.text = str(FET)
		self.ids.p_pr_fev1_fvc_t1.text = str(FEV1FVC)
		pr_fev1_fvc_avg = pr_fev1_fvc_avg + FEV1FVC
		
		self.ids.p_pr_fef50_75_t1.text = str(FEF50)
		pr_fef_50_75_avg = pr_fef_50_75_avg + FEF50         
		self.ids.p_pr_fef25_t1.text = str(FEF25)
		pr_fef25_avg = pr_fef25_avg + FEF25
	if submit_time == 2:
		global fev11
		global fev12
		self.ids.p_pr_fvc_t2.text = str(FVC)
		pr_fvc_avg = pr_fvc_avg + FVC		            
		self.ids.p_pr_fev1_t2.text = str(FEV1)
		fev12 = FEV1
		pr_fev1_avg = pr_fev1_avg + FEV1		
		if fev11 < fev12:
			flow_best = t_flow
			volume_best = t_volume
		self.ids.p_pr_pef_t2.text = str(PEF)
		pr_pef_avg = pr_pef_avg + PEF		
		self.ids.p_pr_fet_t2.text = str(FET)
		self.ids.p_pr_fev1_fvc_t2.text = str(FEV1FVC)
		pr_fev1_fvc_avg = pr_fev1_fvc_avg + FEV1FVC		
		self.ids.p_pr_fef50_75_t2.text = str(FEF50)	
		pr_fef_50_75_avg = pr_fef_50_75_avg + FEF50 	            
		self.ids.p_pr_fef25_t2.text = str(FEF25)
		pr_fef25_avg = pr_fef25_avg + FEF25		
	if submit_time == 3:
		global fev11
		global fev12
		global fev13
		self.ids.p_pr_fvc_t3.text = str(FVC)
		pr_fvc_avg = pr_fvc_avg + FVC		
		self.ids.p_pr_fev1_t3.text = str(FEV1)		
		fev13 = FEV1
		pr_fev1_avg = pr_fev1_avg + FEV1
		if fev11 < fev13 and fev12 < fev13:
			flow_best = t_flow
			volume_best = t_volume
		self.ids.p_pr_pef_t3.text = str(PEF)
		pr_pef_avg = pr_pef_avg + PEF		
		self.ids.p_pr_fet_t3.text = str(FET)
		self.ids.p_pr_fev1_fvc_t3.text = str(FEV1FVC)
		pr_fev1_fvc_avg = pr_fev1_fvc_avg + FEV1FVC		
		self.ids.p_pr_fef50_75_t3.text = str(FEF50)
		pr_fef_50_75_avg = pr_fef_50_75_avg + FEF50 		              
		self.ids.p_pr_fef25_t3.text = str(FEF25)
		pr_fef25_avg = pr_fef25_avg + FEF25		
	if submit_time == 4:
		global fev11
		#flow_best = t_flow            
		#volume_best = t_volume
		#print (len(flow_best),len(volume_best))
		self.ids.p_pr_fvc_t4.text = str(FVC)
		pr_fvc_avg = pr_fvc_avg + FVC		
		self.ids.p_pr_fev1_t4.text = str(FEV1)
		fev11 = FEV1
		pr_fev1_avg = pr_fev1_avg + FEV1		
		self.ids.p_pr_pef_t4.text = str(PEF)
		pr_pef_avg = pr_pef_avg + PEF		
		self.ids.p_pr_fet_t4.text = str(FET)
		self.ids.p_pr_fev1_fvc_t4.text = str(FEV1FVC)
		pr_fev1_fvc_avg = pr_fev1_fvc_avg + FEV1FVC		
		self.ids.p_pr_fef50_75_t4.text = str(FEF50)
		pr_fef_50_75_avg = pr_fef_50_75_avg + FEF50 		         
		self.ids.p_pr_fef25_t4.text = str(FEF25)
		pr_fef25_avg = pr_fef25_avg + FEF25
		
	if submit_time == 5:
		global fev11
		#flow_best = t_flow            
		#volume_best = t_volume
		#print (len(flow_best),len(volume_best))
		self.ids.p_pr_fvc_t5.text = str(FVC)
		pr_fvc_avg = pr_fvc_avg + FVC		
		self.ids.p_pr_fev1_t5.text = str(FEV1)
		fev11 = FEV1
		pr_fev1_avg = pr_fev1_avg + FEV1		
		self.ids.p_pr_pef_t5.text = str(PEF)
		pr_pef_avg = pr_pef_avg + PEF		
		self.ids.p_pr_fet_t5.text = str(FET)
		self.ids.p_pr_fev1_fvc_t5.text = str(FEV1FVC)
		pr_fev1_fvc_avg = pr_fev1_fvc_avg + FEV1FVC		
		self.ids.p_pr_fef50_75_t5.text = str(FEF50)
		pr_fef_50_75_avg = pr_fef_50_75_avg + FEF50 		          
		self.ids.p_pr_fef25_t5.text = str(FEF25)
		pr_fef25_avg = pr_fef25_avg + FEF25
		
	if submit_time == 6:
		global fev11
		#flow_best = t_flow            
		#volume_best = t_volume
		#print (len(flow_best),len(volume_best))
		submit_time = 0
		self.ids.p_pr_fvc_t6.text = str(FVC)
		pr_fvc_avg = pr_fvc_avg + FVC		
		self.ids.p_pr_fev1_t6.text = str(FEV1)
		fev11 = FEV1
		pr_fev1_avg = pr_fev1_avg + FEV1		
		self.ids.p_pr_pef_t6.text = str(PEF)
		pr_pef_avg = pr_pef_avg + PEF		
		self.ids.p_pr_fet_t6.text = str(FET)
		self.ids.p_pr_fev1_fvc_t6.text = str(FEV1FVC)
		pr_fev1_fvc_avg = pr_fev1_fvc_avg + FEV1FVC		
		self.ids.p_pr_fef50_75_t6.text = str(FEF50)
		pr_fef_50_75_avg = pr_fef_50_75_avg + FEF50 		         
		self.ids.p_pr_fef25_t6.text = str(FEF25)
		pr_fef25_avg = pr_fef25_avg + FEF25
		self.calculate_average()		

global t_time_post
t_time_post = []
global t_volt_post
t_volt_post = []
global t_pressure_post
t_pressure_post = []
global t_flow_post
t_flow_post = []
global t_volume_post
t_volume_post = []
global flow_best_post
flow_best_post = []
global volume_best_post
volume_best_post = []
global t_p_volume_post
t_p_volume_post = []
global rt_volume_post
rt_volume_post = []

global levels_post
levels_post = []
global plot2
plot2 = MeshLinePlot(color=[1, 0, 0, 1], bold = True)
global plot3
plot3 = MeshLinePlot(color=[1, 0, 0, 1])

def start_post(self):
	global plot2
	global plot3	
	global t
	global t_end_post	
	t_end_post = time.time() + t
	global levels_post
	global t_flow_post
	global t_volt_post
	levels_post = []
	t_flow_post = []
	t_volt_post = []	 
	#plot = MeshLinePlot(color=[1, 0, 0, 1])
	self.ids.post_start.add_plot(plot2)
	self.ids.post_svg.add_plot(plot3)
	Clock.schedule_interval(get_value_post, 0.1)
	Clock.schedule_interval(stop_post, 0.1)

def get_level_post(dt): 
	global levels_post
	global t 
	global t_time_post
	global t_volt_post
	global t_pressure_post
	global t_flow_post
	global rt_volume_post
	#t_flow = []	
	data_post = ReadChannel(7)            
	mx_post = ConvertVolts(data_post, 5) 
	t_volt_post.append(mx_post)
	mx_post = (((750 *mx_post)/vsource)-150)		
	if mx_post < 0:      # mx is complex so we need to define mx as real or imaginary
		mx_post = 0  
	t_pressure_post.append(mx_post)
	mx_post = math.sqrt(mx_post) * 0.533      # cmath gives complex sqrt
	if mx_post < 0:      # mx is complex so we need to define mx as real or imaginary
		mx_post = 0      
	t_flow_post.append(mx_post)
	t_time_post = np.linspace(0,t,len(t_flow_post))
	single_volume_post = np.trapz(t_flow_post, t_time_post)
	rt_volume_post.append(single_volume_post)
	if len(levels_post) >= 100:
		levels_post = []
		Clock.unschedule(get_level_post)
	levels_post.append(mx_post)
	print (len(t_time_post), len(t_flow_post), len(t_volt_post))

def stop_post(dt):
	global t_end_post
	if time.time() >= t_end_post:
		Clock.unschedule(get_value_post)

def get_value_post(dt):
	global plot2	      
	global levels_post
	Clock.schedule_once(get_level_post)	
	plot2.points = [(i, j) for i, j in enumerate(levels_post)]

def volume_graph_post(self):
	print 'abs'
	global t_time_post       
	global t_flow_post
	global t_volume_post
	global t_p_volume_post
	global FEV1_post
	global plot3 
	#print t_flow
	graph_volume_post = []       
	dy_post = []
	dy0_post = []
	dy1_post=0
	lim_post=np.size(t_flow_post)
	j_post = 0
	t_volume_post= []
	t_p_volume_post = []
	
	for i in range(lim_post):
	  dy1_post=0
	  global FVC_post
	  dy1_post=scipy.integrate.trapz(t_flow_post[i:i+2],t_time_post[i:i+2])
	  j_post = j_post+dy1_post
	  if i == 12:
		  FEV1_post = j_post
		  FEV1_post = round(FEV1_post, 3)
	  FVC_post = j_post
	  FVC_post = round(FVC_post, 3)
	  dy_post.append(j_post) 	  
	  dy0_post.append(dy1_post)
	print dy_post       
	t_volume_post = dy_post
	#print t_volume
	graph_volume_post = t_volume_post
	t_p_volume_post = dy0_post
	t_time_post = np.linspace(0,t,len(t_flow_post))	
	print (len(graph_volume_post), len(t_time_post))
	#if len(graph_volume_post) != len(t_time_post):
	#	c = len(graph_volume_post) - len(t_time_post)
	#	del graph_volume_post[-1]
	plot3.points = [(t_time_post[i], graph_volume_post[i]) for i in range(len(graph_volume_post))]
	graph_volume_post = []	
	dy_post = []
	dy0_post = []
	dy1_post=0

global post_submit_time
post_submit_time = 0

global PEF_post
PEF_post = 0
global FET_post
FET_post = 6
global FEF25_post
FEF25_post = 0
global FEF50_post
FEF50_post = 0
global FVC_post
FVC_post = 0

global PEF_post_t
PEF_post_t = 0
global FVC_post_t
FVC_post_t = 0
global FEV1_post_t
FEV1_post_t = 0
global FEV1FVC_post_t
FEV1FVC_post_t = 0
global FEF25_post_t
FEF25_post_t = 0
global FEF50_post_t
FEF50_post_t = 0

def submit_post(self):
	global post_submit_time
	global flow_best
	global volume_best
	global t_time
	global t_pressure
	global t_flow
	global t_volume
	global PEF_post
	global FVC_post
	global FEV1_post
	global FEV1FVC_post
	global FEF25_post
	global FEF50_post
	
	global post_fev1_avg, post_fvc_avg, post_fev1_fvc_avg, post_fet_avg, post_pef_avg, post_fef25_avg \
            , post_fef_50_75_avg
	
	global fev11_post
	fev11_post = 0
	global fev12_post
	fev12_post = 0
	global fev13_post
	fev13_post = 0
	
	post_submit_time = post_submit_time + 1        
	PEF_post = max(t_flow_post)
	PEF_post = round(PEF_post, 3)
	print FEV1_post, FVC_post
	FEV1FVC_post = FEV1_post / FVC_post
	FEV1FVC_post = round(FEV1FVC_post, 3) 
	for i in range (60):
		if i == 15:
			FEF25_post = t_flow_post[i]
			FEF25_post = round(FEF25_post, 3)
		if i == 30:
			FEF50_post = t_flow_post[i]
			FEF50_post = round(FEF50_post, 3)
	
	
	if post_submit_time == 1:
		global fev11_post
		flow_best_post = t_flow_post            
		volume_best_post = t_volume_post
		print (len(flow_best_post),len(volume_best_post))
		self.ids.p_post_fvc_t1.text = str(FVC_post)
		post_fvc_avg = post_fvc_avg + FVC_post		
		self.ids.p_post_fev1_t1.text = str(FEV1_post)
		fev11_post = FEV1_post
		post_fev1_avg = post_fev1_avg + FEV1_post
		self.ids.p_post_pef_t1.text = str(PEF_post)
		post_pef_avg = post_pef_avg + PEF_post
		self.ids.p_post_fet_t1.text = str(FET_post)
		self.ids.p_post_fev1_fvc_t1.text = str(FEV1FVC_post)
		post_fev1_fvc_avg = post_fev1_fvc_avg + FEV1FVC_post
		self.ids.p_post_fef50_75_t1.text = str(FEF50_post)
		post_fef_50_75_avg = post_fef_50_75_avg + FEF50_post           
		self.ids.p_post_fef25_t1.text = str(FEF25_post)
		post_fef25_avg = post_fef25_avg + FEF25_post
	
	if post_submit_time == 2:
		global fev11_post
		self.ids.p_post_fvc_t2.text = str(FVC_post)
		post_fvc_avg = post_fvc_avg + FVC_post
		self.ids.p_post_fev1_t2.text = str(FEV1_post)
		fev11_post = FEV1_post
		post_fev1_avg = post_fev1_avg + FEV1_post
		self.ids.p_post_pef_t2.text = str(PEF_post)
		post_pef_avg = post_pef_avg + PEF_post
		self.ids.p_post_fet_t2.text = str(FET_post)
		self.ids.p_post_fev1_fvc_t2.text = str(FEV1FVC_post)
		post_fev1_fvc_avg = post_fev1_fvc_avg + FEV1FVC_post
		self.ids.p_post_fef50_75_t2.text = str(FEF50_post)
		post_fef_50_75_avg = post_fef_50_75_avg + FEF50_post
		self.ids.p_post_fef25_t2.text = str(FEF25_post)
		post_fef25_avg = post_fef25_avg + FEF25_post 
		
	if post_submit_time == 3:
		global fev11_post
		self.ids.p_post_fvc_t3.text = str(FVC_post)
		post_fvc_avg = post_fvc_avg + FVC_post
		self.ids.p_post_fev1_t3.text = str(FEV1_post)
		fev11_post = FEV1_post
		post_fev1_avg = post_fev1_avg + FEV1_post
		self.ids.p_post_pef_t3.text = str(PEF_post)
		post_pef_avg = post_pef_avg + PEF_post
		self.ids.p_post_fet_t3.text = str(FET_post)
		self.ids.p_post_fev1_fvc_t3.text = str(FEV1FVC_post)
		post_fev1_fvc_avg = post_fev1_fvc_avg + FEV1FVC_post
		self.ids.p_post_fef50_75_t3.text = str(FEF50_post)
		post_fef_50_75_avg = post_fef_50_75_avg + FEF50_post 
		self.ids.p_post_fef25_t3.text = str(FEF25_post)
		post_fef25_avg = post_fef25_avg + FEF25_post
	if post_submit_time == 4:
		global fev11_post
		self.ids.p_post_fvc_t4.text = str(FVC_post)
		post_fvc_avg = post_fvc_avg + FVC_post
		self.ids.p_post_fev1_t4.text = str(FEV1_post)
		fev11_post = FEV1_post
		post_fev1_avg = post_fev1_avg + FEV1_post
		self.ids.p_post_pef_t4.text = str(PEF_post)
		post_pef_avg = post_pef_avg + PEF_post
		self.ids.p_post_fet_t4.text = str(FET_post)
		self.ids.p_post_fev1_fvc_t4.text = str(FEV1FVC_post)
		post_fev1_fvc_avg = post_fev1_fvc_avg + FEV1FVC_post
		self.ids.p_post_fef50_75_t4.text = str(FEF50_post)
		post_fef_50_75_avg = post_fef_50_75_avg + FEF50_post 
		self.ids.p_post_fef25_t4.text = str(FEF25_post)
		post_fef25_avg = post_fef25_avg + FEF25_post
	if post_submit_time == 5:
		global fev11_post
		self.ids.p_post_fvc_t5.text = str(FVC_post)
		post_fvc_avg = post_fvc_avg + FVC_post
		self.ids.p_post_fev1_t5.text = str(FEV1_post)
		fev11_post = FEV1_post
		post_fev1_avg = post_fev1_avg + FEV1_post
		self.ids.p_post_pef_t5.text = str(PEF_post)
		post_pef_avg = post_pef_avg + PEF_post
		self.ids.p_post_fet_t5.text = str(FET_post)
		self.ids.p_post_fev1_fvc_t5.text = str(FEV1FVC_post)
		post_fev1_fvc_avg = post_fev1_fvc_avg + FEV1FVC_post
		self.ids.p_post_fef50_75_t5.text = str(FEF50_post)
		post_fef_50_75_avg = post_fef_50_75_avg + FEF50_post 
		self.ids.p_post_fef25_t5.text = str(FEF25_post)
		post_fef25_avg = post_fef25_avg + FEF25_post
	if post_submit_time == 6:
		global fev11_post
		post_submit_time = 0
		self.ids.p_post_fvc_t6.text = str(FVC_post)
		post_fvc_avg = post_fvc_avg + FVC_post
		self.ids.p_post_fev1_t6.text = str(FEV1_post)
		fev11_post = FEV1_post
		post_fev1_avg = post_fev1_avg + FEV1_post
		self.ids.p_post_pef_t6.text = str(PEF_post)
		post_pef_avg = post_pef_avg + PEF_post
		self.ids.p_post_fet_t6.text = str(FET_post)
		self.ids.p_post_fev1_fvc_t6.text = str(FEV1FVC_post)
		post_fev1_fvc_avg = post_fev1_fvc_avg + FEV1FVC_post
		self.ids.p_post_fef50_75_t6.text = str(FEF50_post)
		post_fef_50_75_avg = post_fef_50_75_avg + FEF50_post
		self.ids.p_post_fef25_t6.text = str(FEF25_post)
		post_fef25_avg = post_fef25_avg + FEF25_post
		self.calculate_average()
	
