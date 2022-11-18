# -*- coding: utf-8 -*-
"""
@author: d-roho
"""

import sys
import time
from gsi_pinger import pingerfunc

def change_dir():
  
    #Changes working directory to match location of this python file
    import os  
    #changing working directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(str(dir_path))
    print("current directory is - " + str(dir_path))
    return dir_path
        
def import_model():
   
    #Imports trained Logistic Regression model 
    from pypmml import Model

    #Importing Model
    model = Model.load("CSGOPredictor.pmml")
    print("model imported successfully")
    return model


def check_for_match_start():

    #Pauses script till useful data is being recorded to generate predictions

    test = {}
    print("Waiting for CS:GO to be launched")
    while len(test.keys()) == 0:
        test = pingerfunc()
    print("CS:GO has been launched")
    print("Waiting for Match to begin")
    
    while test.get("allplayers") is None:
        test = pingerfunc()
    while test.get("map").get("phase") == 'warmup':
        test = pingerfunc()

    print("Match has Begun!")

def match_start_check_postlaunch():
    
    #Same as check_for_match_start(), but used in cases where CS:GO is known to have already been launched
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
    #The main loop that parses logs and runs the predictive model. Returns probability prediction of round outcome
    dir_path   = change_dir()
    model      = import_model()
    check_for_match_start()

    from snapshot_parser import exception_handler, snapshot_formatter, snapshot_arrayfier
    import exceptions
    from listener import pause_detector, pause_screen, raise_pause_screen
    pause_counter = 0
    
    while True:   
        try:

            #Checking is a Pause request was initiated in previous loop 
            if raise_pause_screen == True:
                pause_screen()

            #Pinging for latest snapshot
            snapshot = None
            while snapshot is None:
                snapshot = pingerfunc()

            snapshot = exception_handler(snapshot)

            """formatting snapshot dictionary 
            """

            snapshot_formatted = snapshot_formatter(snapshot)
          
            
            """parsing formatted snapshot and creating list of attributes for predictive model 
            """
            predictors = snapshot_arrayfier(snapshot_formatted)
          
            """Prediction
            """

            """running model with predictors"""

            pred = model.predict([predictors])


            """Default Predictions - These are scenarios in which the winner of the round has been decided (or is a virtual certainty)
            which the predictive model is not able to take into account when making its prediction
            """

            #Round Over

            if snapshot_formatted["round"]["phase"] == "over":
                if snapshot_formatted["round"].get("win_team") == "T":
                    pred = [0,1]
                if snapshot_formatted["round"].get("win_team") == "CT":
                    pred = [1,0]

            #Virtual Round Win - Scenarios in which a team cannot lose, but the round is still live

            #Bomb Timer < 5 seconds
            if snapshot_formatted["phase_countdowns"].get("phase") == "bomb":
                if float(snapshot_formatted["phase_countdowns"].get("phase_ends_in")) < 5.0:
                    pred = [0,1]
            #Time to Defuse > Time left in Round - cant do this with existing info, solution may be possible (more info from GSI?)
            #Bomb Planted - All Ts dead - enough time to defuse - same as above

            """Freeze Time - Making Time prediction attribute default to 115 seconds during freezetime. 
            This makes it so that the low time_left during freezetime doesn't skew prediction towards Ts"""

            if snapshot_formatted["phase_countdowns"].get("phase") == "freezetime":
                predictors[4] = 115
                
       

            """ Outputting Prediction
            """

            pred_nested = model.predict([predictors]) #returns list of list with 1 entry, a nested list with the predictions
            pred = pred_nested[0] #converts list from nested to unnested

            print(pred)
            with open('predictions.txt', 'a') as fh:
                fh.write(str(pred)+'\n')

            if pause_counter % 10 == 0: 
                pause_detector()
            pause_counter += 1
                
            """
            Following restarts from top of While. Used to handle cases when the log entry 
            is not properly extracted from the log and extraction needs to redone. The log entry extracted from
            second attempt raises a JSONDecodeError in the snapshot_dictifyer function of the snapshot_parser module. When the rest of
            the loop is skipped, the error does not recur. Does not fix the underlying problem (which I have not yet figured out), but 
            this fix results in no major loss of functionality (predictions resume after 1-2 seconds). 
            """ 
        except exceptions.EmptyServer:
            #Manually Raised when no players are found in the server. Forces program to wait till at least one player is detected 
            print("Server is empty. Program will automatically resume once at least one player joins the server.")
            time.sleep(1)
            print("Waiting...")
            match_start_check_postlaunch()
            print("Player(s) Detected!")
            time.sleep(1)
            continue
        except exceptions.MatchNotStarted:
            #
            print("You are not currently spectating a Match. Program will automatically resume when you begin spectating.")
            time.sleep(1)
            print("Waiting...")
            match_start_check_postlaunch()
            print("Match has Begun!")
            time.sleep(1)
            continue
        except exceptions.WarmUp:
            print("Match is in Warm Up Phase. Predictions will begin after Warm Up.")
            time.sleep(1)
            print("Waiting...")
            check_for_match_start() #For unkown reason, match_start_check_postlaunch() doesnt work here
            time.sleep(1)
            continue
        except KeyError:
            #Should not occur. Please report on GitHub if found.
            print("KeyError. Restarting loop.")
            print("This should not occur. Please raise a Ticket on GitHub!")
            time.sleep(5)
            continue
        except KeyboardInterrupt:
            print("Exiting Program")
            time.sleep(0.5)
            sys.exit()

    sys.exit()
 
if __name__ == '__main__':
    parse_and_predict()
