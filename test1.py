import grovepi
import time
from grove_rgb_lcd import *

#i'll have the fabric heat from 10 to 40 degrees

#set sensors position
rotar = 0 #potentimeter linked to port analog A0
red=5 #red led linked to port D5
green = 6 #blue led linked to digital port D6
button = 3 #button linked to digital port D3
relay = 4 #relay linked to digital port D4
sensor= 1 #temperature sensor is linked to analog port A1
#rgb lcd must be connected to an I2C port
#setText("The device is ready to work")
#setRGB(0,128,64)

#set sensors status
grovepi.pinMode(rotar, "INPUT")
grovepi.pinMode(red, "OUTPUT")
grovepi.pinMode(green, "OUTPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(relay,"OUTPUT")

#variables
sub_value=0#inferior value f temperature(-2)
sup_value=0#superior value of temperature(+2)
full_angle=300 #full angle of the rotary which goes from 0-300 degrees
start=0 #device status
sensor_value=0
temp=0
voltage=0
degrees=0
w_temp=0
digitalWrite(red,0)
while True:
	try:
		#setText("Program status: {}".format(str(status)))
		print("Temperature is:", temp)
		while start==0:
			if grovepi.digitalRead(button):
				start=1;
				digitalWrite(red,0)
				digitalWrite(green,1)
				print("Device OFF")	
				time.sleep(1)

		while start==1:
			print("Device ON")
			temp = grove.temp(sensor,'1.1')
			sensor_value=grove.pi.analogRead(rotar)
			voltage= round((float)(sensor_value) *5/1023,2)
			degrees = round((voltage*full_angle)/5,2)
			w_temp = 10 + int(degrees/full_angle*30)
			#setText(Wanted Temperature:{}".format(str(w_temp)))
			#setText("Temperature:{}".format(str(temp)))
			print("Temperature is: %d Wanted Temperature is: %d" %(temp, w_temp))
			sub_value=w_temp-2
			sup_value=w_temp+2
			if temp<sub_value:
				grovepi.digitalWrite(relay,1)
			if temp<sup_value:
				grovepi.digitalWrite(relay,0) 
			if grovepi.digitalRead(button):
				start=0
				grovepi.digitalWrite(relay,0)
				digitalWrite(red,1)
				digitalWrite(green,0)
		
	except KeyboardInterrupt:
		#setRGB(0,0,0)
		#setText("")
		grovepi.digitalWrite(green,0)
		grovepi.digitalWrite(red,0)
		grovepi.digitalWrite(relay,0)
		break
	except IOError:
		print("Error")
		#setRGB(0,0,0)
		#setText("")
