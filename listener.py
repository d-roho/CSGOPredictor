"""Module that enables Pause-and-Play functionality. Hold Esc Key to Pause!"""

from pynput.keyboard import Key, Listener
from threading import Timer
import time
import sys

"""This variable is imported & used in MainApp's parse_and_predict() loop
to detect if a Pause request was initiated"""
global raise_pause_screen
raise_pause_screen = False


def on_press(key):

    # Defines the action to be done when Esc Key is held down
    if key == Key.esc:
        global raise_pause_screen
        print("pausing...")
        raise_pause_screen = True


def pause_detector():

    """Runs the Listener, which looks out for Esc Key press.
    When Esc detected, runs on_press()"""
    with Listener(
            on_press=on_press) as l:
        Timer(0.01, l.stop).start()
        l.join()


def pause_screen():

    """Temporarily pauses program, allowing users to either resume or exit altogether.
Executed when pause request detected by pause_detector"""
    global raise_pause_screen
    raise_pause_screen = False
    print("Predictions Paused - Hit Enter to resume or enter 'q' to exit program: ")
    while True:
        try:
            response = input()
            if response == 'q':
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
