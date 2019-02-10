import time
import RPi.GPIO as GPIO


class Keypad:
    def __init__(self):
        # Setting up parameters
        self.KEYPAD = [
            [1, 2, 3, 'A'],
            [4, 5, 6, 'B'],
            [7, 8, 9, 'C'],
            ['*', 0, '#', 'D']]

        # Affecting pins
        self.ROW = [21, 22, 23, 24]
        self.COLUMN = [35, 36, 37, 38]

    def get_key(self):
        # Setting columns as outputs
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Setting rows as inputs
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Checking for pressed button
        row_val = -1
        for i in range(len(self.ROW)):
            tmp_read = GPIO.input(self.ROW[i])
            if tmp_read == 0:
                row_val = i
        if row_val < 0 or row_val > 3:
            self.exit()
            return
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.ROW[row_val], GPIO.OUT)
            GPIO.output(self.ROW[row_val], GPIO.HIGH)
            col_val = -1
            for j in range(len(self.COLUMN)):
                tmp_read = GPIO.input(self.COLUMN[j])
                if tmp_read == 1:
                    col_val = j
            if col_val < 0 or col_val > 3:
                self.exit()
                return
            # Return position of pressed button
            self.exit()
            return self.KEYPAD[row_val][col_val]

    def exit(self):
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
