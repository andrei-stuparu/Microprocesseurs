from grovepi import *
import time
from grove_rgb_lcd import *
import math
#i'll have the fabric heat from 10 to 40 degrees

#set sensors position

rotar = 2 #potentimeter linked to port analog A2
red=6 #red led linked to port D6
green = 5 #blue led linked to digital port D5
button = 3 #button linked to digital port D3
relay = 4 #relay linked to digital port D4
sensor= 7 #temperature sensor is linked to digital port D7
#rgb lcd must be connected to an I2C port
setText("The device is ready to work")
setRGB(0,102,204)

#set sensors status
pinMode(rotar,"INPUT")
pinMode(red, "OUTPUT")
pinMode(green, "OUTPUT")
pinMode(button,"INPUT")
pinMode(relay,"OUTPUT")

#variables
sub_value=0 #inferior value f temperature(-2)
sup_value=0 #superior value of temperature(+2)
full_angle=300 #full angle of the rotary which goes from 0-300 degrees
start=0 #device status
temps=27
w_temp=0.0
digitalWrite(red,1)
while True:
	try:

		[temp,humidity] = dht(sensor,0)
		if math.isnan(temp)==False:
			temps=temp
		if start==0:
			time.sleep(2)
			print("Temperature is:",temps)
			setText("Program status: OFF")
			if digitalRead(button):
				start=1
                                digitalWrite(red,0)
                                digitalWrite(green,1)
                                setText("Program status: ON")
 				print("DEVICE ON")
		if start==1:
			time.sleep(2)
			sensor_value=analogRead(rotar)
			voltage= round((float)(sensor_value) *5/1023,2)
			degrees = round((voltage*full_angle)/5,2)
			w_temp = 10 + int(degrees/full_angle*30)
			setText("Wanted Temperature:"+str(w_temp))
			time.sleep(1)
			setText("Temperature:"+str(temps))
			print("Temperature is: %f Wanted Temperature is: %d" %(temps, w_temp))
			sub_value=w_temp-2
			sup_value=w_temp+2
			if temps<sub_value:
				digitalWrite(relay,1)
			if temps>sup_value:
				digitalWrite(relay,0)
			if digitalRead(button):
				start=0
                                digitalWrite(red,1)
                                digitalWrite(green,0)
                                digitalWrite(relay,0)
                                print("DEVICE OFF") 
	except KeyboardInterrupt:
		print("Interrupted")
		setRGB(0,0,0)
		setText("")
		digitalWrite(green,0)
		digitalWrite(red,0)
		digitalWrite(relay,0)
		time.sleep(0)
		break
	except IOError:
		print("Error")
		setRGB(0,0,0)
		setText("")
