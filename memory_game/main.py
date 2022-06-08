from machine import Pin, PWM
import random
import time
# uline 715
# digikey 910
# easyeda 440
class SimonSays:
    def __init__(self):
        self.options = ['R','G','B','Y']
        self.pattern = []
        self.user_input = []
        self.playing = False
        # Led pin assignments
        self.led_r = Pin(13, Pin.OUT)
        self.led_g = Pin(12, Pin.OUT)
        self.led_b = Pin(11, Pin.OUT)
        self.led_y = Pin(10, Pin.OUT) 
        # Button pin assignments
        self.btn_r = Pin(9,  Pin.IN)
        self.btn_g = Pin(8,  Pin.IN)
        self.btn_b = Pin(7,  Pin.IN)
        self.btn_y = Pin(6,  Pin.IN)
        # Buzzer pin assignment
        self.buzz = PWM(Pin(15))
        # Led list
        self.leds = [self.led_r, self.led_g, self.led_b, self.led_y]
        # Buzzer frequencies
        self.red_freq = 131
        self.green_freq = 262
        self.blue_freq = 524
        self.yellow_freq = 1047
        # Level variable
        self.level = 0
        # Max level for game
        self.max_level = 10
        # Buzzer volume level
        self.buzz_level = 900
        # Random wait time to change pattern
        #time.sleep(float(random.randint(0, 200)/100))

    def end_game(self):
        '''Once the game ends, the level, pattern and user inputs are reset. 
        The led also do a little song and dance before alerting ready for a
        new game.'''
        # At the end of the game, reset level, pattern and user input
        self.level = 0
        self.pattern = []
        self.user_input = []
        # Turn off all leds
        for led in self.leds:
            led.value(0)
        # Wait one second
        time.sleep(1)
        # Flash leds
        for x in range(9):
            for led in self.leds:
                led.toggle()
            time.sleep(0.3)
        # Create a count down with the leds turning off one led every second
        for led in self.leds[::-1]:
            led.value(0)
            time.sleep(1)
        # Play buzzer noise as an alert for new game
#        for x in range(3):
#            self.buzz.freq(4500)
#            self.buzz.duty_u16(self.buzz_level)
#            time.sleep(0.25)
#            self.buzz.duty_u16(0)
#            time.sleep(0.4)
#        time.sleep(1)
        self.playing = False

    def increase_pattern(self):
        '''Adding new entry to the pattern while the game is played'''
        # If level is zero, change random seed and increase level
        if self.level == 0:
            random.seed(round(time.time() + random.randint(1,1000000)))
            self.pattern.append(random.choice(self.options))
            self.level += 1
            return 0
        # Else, check if level is equal to max level.
        elif self.level > 0 and self.level != self.max_level:
            # If not equal to max, increase level and update pattern
            self.level += 1
            self.pattern.append(random.choice(self.options))
            return 0
        elif self.level == self.max_level:
            self.end_game()

    def add_led(self, sleep_timer, led, letter, frequency):
        '''Sub-functipn that controls adding to user pattern 
        and flashing coorisponding leds'''
        # Set buzzer frequency to red frequency
        self.buzz.freq(frequency)
        # Turn on buzzer
        self.buzz.duty_u16(self.buzz_level)
        # Update user patern
        self.user_input.append(letter)
        # Turn on led
        led.value(1)
        # Wait to allow buzzer play and led to stay on
        time.sleep(sleep_timer)
        # Turn off buzzer
        self.buzz.duty_u16(0)
        # Turn off led
        led.value(0)

    def user_guess(self):
        '''User is allowed to give input guessing the matching pattern'''
        sleep_timer = 0.3
        for color in self.pattern:
            while True:
                if self.btn_r.value():
                    self.add_led(sleep_timer=sleep_timer, led=self.led_r, letter="R", frequency=self.red_freq)
                    break
                if self.btn_g.value():
                    self.add_led(sleep_timer=sleep_timer, led=self.led_g, letter="G", frequency=self.green_freq)
                    break
                if self.btn_b.value():
                    self.add_led(sleep_timer=sleep_timer, led=self.led_b, letter="B", frequency=self.blue_freq)
                    break
                if self.btn_y.value():
                    self.add_led(sleep_timer=sleep_timer, led=self.led_y, letter="Y", frequency=self.yellow_freq)
                    break
        # If user pattern matches saved pattern, clear pattern return True
        if self.user_input == self.pattern:
            self.user_input = []
            return 0
        if self.user_input != self.pattern:     
            self.end_game()

    def show_led(self, led, frequency, show_time, wait_time):
        '''Sub-function that controls displaying leds while showing the
        user the pattern via led and buzzer noises'''
        # Set buzzer frequency
        self.buzz.freq(frequency)
        # Set buzzer volume
        self.buzz.duty_u16(self.buzz_level)
        # Turn on led
        led.value(1)
        time.sleep(show_time)
        # Turn buzzer off
        self.buzz.duty_u16(0)
        # Turn off led
        led.value(0)
        time.sleep(wait_time) 

    def display_pattern(self):
        '''Display pattern to user via leds and buzzer'''
        show_time = 0.25
        wait_time = 0.5
        for entry in self.pattern:
            if entry == 'R':
                self.show_led(self.led_r, self.red_freq, show_time, wait_time)
            if entry == 'G':
                self.show_led(self.led_g, self.green_freq, show_time, wait_time)
            if entry == 'B':
                self.show_led(self.led_b, self.blue_freq, show_time, wait_time)
            if entry == 'Y':
                self.show_led(self.led_y, self.yellow_freq, show_time, wait_time)

if __name__ == '__main__':
    game = SimonSays()
    while True:
        if game.btn_b.value() and game.btn_y.value() and not game.playing:
            time.sleep(0.5)
            game.playing = True
        if game.playing == True:
            time.sleep(1)
            game.increase_pattern()
            game.display_pattern()
            game.user_guess()
            