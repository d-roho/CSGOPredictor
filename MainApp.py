# -*- coding: utf-8 -*-
"""
@author: d-roho
"""

def change_dir():
    #Changes working directory to match location of this python file
    import os
    import sys
    import time
    
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
    import time
    #Pauses script till useful data is being recorded to generate predictions
    test = {}
    while len(test.keys()) == 0:
        print("Waiting for CS:GO to be launched")
        from gsi_pinger import pingerfunc
        test = pingerfunc()
    print("CS:GO has been launched")
    print("Waiting for Match to begin")
    
    while test.get("allplayers") is None:
        test = pingerfunc()
    print("Match has Begun!")
    print("Waiting for server to be fully populated")

    while len(test.get("allplayers").keys()) != 10:
        test = pingerfunc()
    print("Server is Populated! Beginning Predictions")
    time.sleep(2)


def parse_and_predict():
    #The main loop that parses logs and runs the predictive model. Returns probability prediction of round outcome
    dir_path   = change_dir()
    model      = import_model()
    check_for_match_start()

    import time
    import sys
    from snapshot_parser import snapshot_formatter, snapshot_arrayfier

        
    while True:
        
        try:
            #Pinging for latest snapshot

            from gsi_pinger import pingerfunc
            snapshot = None
            while snapshot is None:
                snapshot = pingerfunc()

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
                if snapshot_formatted["round"]["win_team"] == "T":
                    pred = [[0,1]]
                elif snapshot_formatted["round"]["win_team"] == "CT":
                    pred = [[1,0]]

            #Virtual Round Win - Scenarios in which a team cannot lose, but the round is still live

            #Bomb Timer < 5 seconds
            if snapshot_formatted["phase_countdowns"].get("phase") == "bomb":
                if float(snapshot_formatted["phase_countdowns"].get("phase_ends_in")) < 5.0:
                    pred = [[0,1]]
            #Time to Defuse > Time left in Round - cant do this with existing info, solution may be possible (more info from GSI?)
            #Bomb Planted - All Ts dead - enough time to defuse - same as above

            """Freeze Time - Making Time prediction attribute default to 115 seconds during freezetime. 
            This makes it so that the low time_left during freezetime doesn't skew prediction towards Ts"""

            if snapshot_formatted["phase_countdowns"].get("phase") == "freezetime":
                predictors[4] = 115
                pred = model.predict([predictors])
       

            """ Outputting Prediction
            """

            print(pred)
            with open('predictions.txt', 'a') as fh:
                fh.write(str(pred)+'\n')
                
        except KeyboardInterrupt:
            print("Predictions Paused - Hit Enter to resume or type quit exit program: ")      
            try:
                response = input()
                if response == 'quit':
                    break
            except KeyboardInterrupt:
                print('Resuming...')
                continue
            """
            Following restarts from top of While. Used to handle cases when the log entry 
            is not properly extracted from the log and extraction needs to redone. The log entry extracted from
            second attempt raises a JSONDecodeError in the snapshot_dictifyer function of the snapshot_parser module. When the rest of
            the loop is skipped, the error does not recur. Does not fix the underlying problem (which I have not yet figured out), but 
            this fix results in no major loss of functionality (predictions resume after 1-2 seconds). 
            """ 
        except KeyError:
            print("KeyError")
            time.sleep(5)
            continue
        except IndexError:
            print("index error. restarting")
            time.sleep(0.5)
            continue

    sys.exit()
 
if __name__ == '__main__':
    parse_and_predict()
