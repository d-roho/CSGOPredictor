# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:08:20 2022

@author: NewAdmin
"""
import os
import sys
import time
"""changing working directory
"""
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(str(dir_path))
print("current directory is - " + str(dir_path))


dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(str(dir_path))
        
from pypmml import Model
import glob
from file_read_backwards import FileReadBackwards
from snapshot_formatter import string_formatter
from snapshot_parser import snapshot_dictifyer, snapshot_arrayfier
from json.decoder import JSONDecodeError


"""Importing Model
"""

model = Model.load("CSGOPredictor.pmml")
print("model imported successfully")

list_of_files = glob.glob(str( str(dir_path) + '/CSGO-GSI/logs/*'))
latest_log = max(list_of_files, key=os.path.getctime)
print("The latest CSGO GSI Log is - " + str(latest_log))

"""waiting till useful data is being recorded to generate predictions"""

print("Waiting for CS:GO to be launched")
    
characters = 0
while characters < 50:
    characters = len(open(latest_log).read())

print("CS:GO has been launched")
print("Waiting for Match to begin")

ammo_presence = ""
while "ammo" not in ammo_presence:
    ammo_presence = open(latest_log).read()[-200:-1]
print("Match has Begun!")    
#print("Predictions will begin in 15 seconds")

#time.sleep(15)
#print("starting predictions")
    
while True:
    
    try:
        
        """Reading Data Log
        """
        
        with FileReadBackwards(latest_log) as file:
            snapshot = list()
            for line in file:
                if not line.startswith('snapshot'):
                    snapshot.append(line)
                else:
                    break
        snapshot.reverse()
        del snapshot[0]
        while True:
            try:
                snapshot = str(snapshot[0])
                break
            except IndexError:
                print("index error")
                time.sleep(5)
                with FileReadBackwards(latest_log) as file:
                    snapshot = list()
                    for line in file:
                        if not line.startswith('snapshot'):
                            snapshot.append(line)
                        else:
                            break
                snapshot.reverse()
                del snapshot[0]
                snapshot = str(snapshot[0])
        
            
        
        """formatting snapshot string 
        """
        
        snapshotformatted = string_formatter(snapshot)
      
        
        """parsing formatted snapshot and creating list of attributes for predictive model 
        """
        snapshotdictionary = snapshot_dictifyer(snapshotformatted)
        predictors = snapshot_arrayfier(snapshotdictionary)
      
        """Prediction
        """

        """running model with predictors"""

        pred = model.predict([predictors])


        """Default Predictions - These are scenarios in which the winner of the round has been decided (or is a virtual certainty)
        which the predictive model is not able to take into account when making its prediction
        """

        #Round Over

        if snapshotdictionary["round"]["phase"] == "over":
            if snapshotdictionary["round"]["win_team"] == "T":
                pred = [[0,1]]
            elif snapshotdictionary["round"]["win_team"] == "CT":
                pred = [[1,0]]

        #Virtual Round Win - Scenarios in which a team cannot lose, but the round is still live

        #Bomb Timer < 5 seconds
        if snapshotdictionary["phase_countdowns"].get("phase") == "bomb":
            if float(snapshotdictionary["phase_countdowns"].get("phase_ends_in")) < 5.0:
                pred = [[0,1]]
        #Time to Defuse > Time left in Round - cant do this with existing info, solution may be possible (more info from GSI?)
        #Bomb Planted - All Ts dead - enough time to defuse - same as above

        """Freeze Time - Making Time prediction attribute default to 115 seconds during freezetime. 
        This makes it so that the low time_left during freezetime doesn't skew prediction towards Ts"""

        if snapshotdictionary["phase_countdowns"].get("phase") == "freezetime":
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
    except JSONDecodeError as jsonde:
        continue

sys.exit()
    