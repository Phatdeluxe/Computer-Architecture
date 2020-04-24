import keyboard
import time
release_counter = 0

def print_word(x):
    print(release_counter)
    release_counter += 1

while not keyboard.is_pressed('space'):
    print('not yet')
    time.sleep(2)
    keyboard.on_release(print_word, suppress=False)
    

print('space pressed')