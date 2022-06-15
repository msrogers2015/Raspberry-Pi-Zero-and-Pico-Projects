from machine import Pin, UART
from time import sleep

rxData = bytes()

a1 = Pin(15, Pin.OUT)
b1 = Pin(14, Pin.OUT)
a2 = Pin(16, Pin.OUT)
b2 = Pin(17, Pin.OUT)

class Motor:
    def __init__(self, forward_lead, reverse_lead):
        self.forward_lead = forward_lead
        self.reverse_lead = reverse_lead

    def forward(self):
        self.forward_lead.high()
        self.reverse_lead.low()

    def reverse(self):
        self.forward_lead.low()
        self.reverse_lead.high()

    def stop(self):
        self.forward_lead.low()
        self.reverse_lead.low()

class Movement:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def stop_drive(self):
        self.left.stop()
        self.right.stop()
        
    def drive_forward(self, time):
        self.left.forward()
        self.right.forward()
        sleep(time)
        self.left.stop()
        self.right.stop()

    def drive_reverse(self, time):
        self.left.reverse()
        self.right.reverse()
        sleep(time)
        self.left.stop()
        self.right.stop()
        
    def turn_left(self, time):
        self.right.forward()
        sleep(time)
        self.right.stop()

    def turn_right(self, time):
        self.left.forward()
        sleep(time)
        self.left.stop()
        
    def hard_left(self, time):
        self.right.forward()
        self.left.reverse()
        sleep(time)
        self.right.stop()
        self.left.stop()
        
    def hard_right(self, time):
        self.left.forward()
        self.right.reverse()
        sleep(5)
        self.left.stop()
        self.right.stop()
        
if __name__ == '__main__':
    left_motor = Motor(a1, b1)
    right_motor = Motor(a2, b2)
    robot = Movement(left_motor, right_motor)
    
    robot.drive_forward(1)
    ''' This is all autonomous driving code
    robot.drive_forward(2)
    sleep(1)
    robot.drive_reverse(2)
    sleep(1)
    robot.turn_left(2)
    sleep(1)
    robot.turn_right(2)
    sleep(1)
    robot.hard_left(2)
    sleep(1)
    robot.hard_right(2)
    sleep(1)
    robot.stop_drive()'''
    
    