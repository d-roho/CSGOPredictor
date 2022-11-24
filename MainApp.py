#  -*- coding: utf-8 -*-
"""
@author: d-roho
"""
import pywintypes
import sys
import time
from gsi_pinger import pingerfunc
from win32gui import GetWindowText, GetForegroundWindow


def current_window():

    # Returns name of current window for listener.py
    window = GetWindowText(GetForegroundWindow())
    return window


def welcome_message():

    # Display Welcome Message unless disabled by "-w" arg
    if "-w" not in sys.argv:
        f = open('welcome.txt', 'r')
        print(''.join([line for line in f]))
        print("CSGOPredictor Launched Successfully!")
        if "-p" in sys.argv:
            print("PAUSE-AND-PLAY = DISABLED")
        else: print("PAUSE-AND-PLAY = ENABLED")
        if "delay" in sys.argv:
            delay_index = sys.argv.index("delay") + 1
            delay_value = float(sys.argv[delay_index])
            print("DELAY VALUE = " + str(delay_value) + " seconds")
        else: print("DELAY VALUE = 0 seconds")
        time.sleep(1.5)


def change_dir():

    """Changes working directory to match location of this python file"""
    import os

    #  Changing working directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(str(dir_path))
    print("current working directory is - " + str(dir_path))
    return dir_path


def import_model():

    """Imports trained Logistic Regression model"""
    import sklearn_json as skljson

    #  Importing Model
    print("Importing Model...")
    model = skljson.from_json("CSGOPredictor")
    print("Model Imported Successfully!")
    return model


def check_for_match_start():

    """Pauses script till useful data is being recorded'
     to generate predictions"""
    test = {}
    print("Waiting for CS:GO to be launched...")
    while len(test.keys()) == 0:
        test = pingerfunc()
    print("CS:GO has been launched!")
    print("Waiting for Match to begin...")

    while test.get("allplayers") is None:
        test = pingerfunc()
    while test.get("map").get("phase") == 'warmup':
        test = pingerfunc()

    print("Match has Begun!")


def match_start_check_postlaunch():

    """Same as check_for_match_start(), but used in cases where
     CS:GO is known to have already been launched"""
    test = {}
    while True:
        try:
            test = pingerfunc()
            if len(test.get("allplayers").keys()) == 0:
                time.sleep(1)
                test = pingerfunc()
            else:
                return False
        except AttributeError:
            time.sleep(1)
            continue

    while True:
        try:
            test = pingerfunc()
            if test.get("map").get("phase") == 'warmup':
                time.sleep(1)
                test = pingerfunc()
            else:
                return False
        except AttributeError:
            time.sleep(1)
            continue


def parse_and_predict():

    """The main loop that parses logs and runs the predictive model.
     Returns probability prediction of round outcome"""
    window = current_window()
    welcome_message()
    change_dir()
    model = import_model()
    check_for_match_start()

    from snapshot_parser import exception_handler, snapshot_formatter, snapshot_arrayfier
    import exceptions
    from listener import pause_detector, pause_screen
    pause_counter = 0
    delay_req = False
    if "delay" in sys.argv:
        delay_req = True
        delay_index = sys.argv.index("delay") + 1
        delay_value = float(sys.argv[delay_index])

    while True:
        try:
            if delay_req is True:
                time.sleep(delay_value)
            # Checking is a Pause request was initiated in previous loop
            if "-p" not in sys.argv:
                from listener import raise_pause_screen  # imports latest value
                if raise_pause_screen is True:  # Checks if pause was requested
                    pause_screen()

            # Pinging for latest snapshot
            snapshot = None
            while snapshot is None:
                snapshot = pingerfunc()

            snapshot = exception_handler(snapshot)

            # formatting snapshot
            snapshot_formatted = snapshot_formatter(snapshot)

            # parsing snapshot to create \attributes lists for predictive model
            predictors = snapshot_arrayfier(snapshot_formatted)

            """Prediction"""

            """Freeze Time - Making Time prediction attribute default to 115 sec
            during freezetime. This makes it so that the low time_left
            during freezetime doesn't skew prediction towards Ts"""
            if snapshot_formatted["phase_countdowns"].get("phase") == "freezetime":
                predictors[4] = 115

            # Running model with predictors
            pred_nested = model.predict_proba([predictors])
            pred = pred_nested[0]  # converts list from nested to unnested
            pred = list(pred)  # converts numpy array to list
            for i in range(2):  # decimal -> %, and round values
                pred[i] = round(pred[i]*100, 2)

            """Default Predictions - These are scenarios in which the winner of
            the round has been decided (or is a virtual certainty) which the
            predictive model is not able to account for when making prediction
            """
            # Round Over
            if snapshot_formatted["round"]["phase"] == "over":
                if snapshot_formatted["round"].get("win_team") == "T":
                    pred = [0, 100]
                if snapshot_formatted["round"].get("win_team") == "CT":
                    pred = [100, 0]

            """Virtual Round Win - Scenarios in which a team cannot lose,
            but the round is still live"""

            # Bomb Timer < 5 seconds
            if snapshot_formatted["phase_countdowns"].get("phase") == "bomb":
                if float(snapshot_formatted["phase_countdowns"].get("phase_ends_in")) < 5.0:
                    pred = [0, 100]

            """Time to Defuse > Time left in Round - cant do this with
            existing info, solution may be possible (more info from GSI?)"""

            # Bomb Planted, All Ts dead - enough time to defuse - same as above

            print(pred)
            with open('predictions.txt', 'a') as fh:  # writes predictions to txt file
                fh.write(str(pred)+'\n')

            # Check for Pause request (every 10 loops unless delay is specified)
            if "-p" not in sys.argv:
                if GetWindowText(GetForegroundWindow()) == window:
                    if delay_req is True:  # when delay, check for pause after each loop
                        pause_detector()
                    elif pause_counter % 10 == 0:
                        pause_detector()
                pause_counter += 1

            # Exceptions
        except exceptions.EmptyServer:

            """Raised by program when no players are found in the server.
            Forces program to wait till at least one player is detected"""
            print("Server is empty. Program will automatically resume once at least one player joins the server.")
            time.sleep(1)
            print("Waiting...")
            match_start_check_postlaunch()
            print("Player(s) Detected!")
            time.sleep(1)
            continue

        except exceptions.MatchNotStarted:

            """Raised by program when player is not spectating a match.
            Usually occurs when user goes into, then exits a match"""
            print("You are not currently spectating a Match. Program will automatically resume when you begin spectating.")
            time.sleep(1)
            print("Waiting...")
            match_start_check_postlaunch()
            print("Match has Begun!")
            time.sleep(1)
            continue

        except exceptions.WarmUp:

            # Raised by program when match being spectated is in warm up mode
            print("Match is in Warm Up Phase. Predictions will begin after Warm Up.")
            time.sleep(1)
            print("Waiting...")
            check_for_match_start()  # For unknown reason, match_start_check_postlaunch() doesnt work here
            time.sleep(1)
            continue

        except KeyError:

            """A catch-all exception which restarts the loop. Should not occur.
            Please report on GitHub if found."""
            print("KeyError. Restarting loop.")
            print("This should not occur. Please raise a Ticket on GitHub!")
            time.sleep(5)
            continue

        except KeyboardInterrupt:

            """Catches Command Terminal keyboard interrupts. Helps exit program smoothly.
            Without this, program raises several errors."""
            print("Exiting Program")
            time.sleep(0.5)
            try:
                sys.exit()
            except:
                sys.exit()

    print("While loop in parse_and_predict somehow broken. This should not occur, please report on GitHub")
    time.sleep(5)
    sys.exit()


if __name__ == '__main__':
    parse_and_predict()
