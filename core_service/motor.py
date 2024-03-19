import time

import Jetson.GPIO as GPIO

# import RPi.GPIO as GPIO

class Motor:
    def __init__(self, stop_pin = 29, sensor_pin=21, pwm_pin=33, dir_pin=37):
        self.sensor_pin = 21
        self.stop_pin = 29
        self.pwm_pin = 33
        self.is_running = True
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BOARD)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(pwm_pin, self.GPIO.OUT, initial=self.GPIO.LOW)
        self.GPIO.setup(dir_pin, self.GPIO.OUT, initial=self.GPIO.HIGH)
        self.GPIO.setup(sensor_pin, self.GPIO.IN)
        self.GPIO.setup(stop_pin, self.GPIO.IN)     ###############
        # self.motor1 = GPIO.PWM(pwm_pin, 200)  # set pwm for M1
        self.sensor_status = GPIO.HIGH
        self.stop_status = GPIO.HIGH     ##########################
        self.detection_complete = False

    def main(self):
        while True:
            self.sensor_status = GPIO.input(self.sensor_pin)
            self.stop_status = GPIO.input(self.stop_pin)   #########
            if self.sensor_status == GPIO.LOW and self.detection_complete is False:
                self.is_running = False
                
                while self.detection_complete is False:
                    self.GPIO.output(self.pwm_pin, GPIO.LOW)
                
                self.is_running = True
                #time.sleep(2)
                while self.stop_status is GPIO.HIGH:
                    self.GPIO.output(self.pwm_pin, GPIO.HIGH)
                    time.sleep(0.00004)
                    self.GPIO.output(self.pwm_pin, GPIO.LOW)
                    time.sleep(0.00004)
                    self.stop_status = GPIO.input(self.stop_pin)
                while self.stop_status == GPIO.LOW:
                    self.stop_status = GPIO.input(self.sensor_pin)
                    self.GPIO.output(self.pwm_pin, GPIO.LOW)
            elif self.sensor_status == GPIO.HIGH and self.stop_status == GPIO.HIGH:
                
                self.is_running = True
                self.GPIO.output(self.pwm_pin, GPIO.HIGH)
                time.sleep(0.00004)
                self.GPIO.output(self.pwm_pin, GPIO.LOW)
                time.sleep(0.00004)


                #self.is_running = False
                #self.GPIO.output(self.pwm_pin, GPIO.)


#            if self.sensor_status == GPIO.LOW and self.detection_complete is False:
#                self.is_running = False
#                self.motor1.start(0)
#            elif self.sensor_status == GPIO.HIGH or self.detection_complete is True:
#                self.detection_complete = False
#                self.is_running = True
#                self.motor1.start(50)
#                #değiştirilmesi gerek baaklm
#                time.sleep(2)

    def cleanup(self):
        self.GPIO.cleanup()
