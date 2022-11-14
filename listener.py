#Module that enables Pause-and-Play functionality. Hold Esc Key to Pause! 

from pynput.keyboard import Key, Listener
from threading import Timer
import time
import sys
import exceptions

#This variable is imported & used in MainApp's parse_and_predict() loop to detect if a Pause request was initiated 
global raise_pause_screen
raise_pause_screen = False

#Defines the action to be done when Esc Key is held down
def on_press(key):
    if key == Key.esc:
    # Raise pause_screen()
        global raise_pause_screen
        print("pausing...")
        raise_pause_screen = True
        print(raise_pause_screen)
        #raise exceptions.PauseScreen

# Runs the Listener, which looks out for Esc Key press. When Esc detected, runs on_press()
def pause_detector():
    with Listener(
            on_press=on_press) as l:
        Timer(0.01, l.stop).start()
        l.join()


#Temporarily pauses program, allowing users to either resume or exit altogether. Executed when pause request detected by pause_detector            
def pause_screen():
    global raise_pause_screen
    raise_pause_screen = False
    print("Predictions Paused - Hit Enter to resume or type 'quit' to exit program: ")
    while True:
        try:
            response = input()
            if response == 'quit':
                print("quitting...")
                time.sleep(0.5)
                sys.exit()
            elif response == "":
                print("resuming...")
                time.sleep(0.5)
                break
            else:
                print("invalid input. try again")
        except EOFError:
            pass
        except KeyboardInterrupt:
            print("quitting program")
            sys.exit()