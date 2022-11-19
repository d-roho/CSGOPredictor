# CSGOPredictor

Current Bugs/Tasks

-> Publish Git Repo 

-> Commit to CSGO-GSI (at end)
_________________________________________________________

Corrected Bugs/Problems:

->  KeyError in server with <10 players (added a check to see if server is populated to prevent KeyError, and added exception to restart loop if KeyError still occurs)

->  GSI - Unicode decoding error (fixed by harcoding utf-8 as decoding standard)

-> Virtual Win Scenarios - situations in a round where the winner is acutally or virtually decided, which the model doesn't recognise (hardcoded theses into main script's code)

-> Json.Loads/index Error (patched by restarting loop on IndexError occurance, but occurance of IndexError is not solved)

-> UnicodeDecodeError, probably for certain usernames (solved by specifying encoding="utf-8" wherever files are read in main script and GSI)

-> Better GSI integration - Created gsi_pinger

-> Bypass manual creation of dictionary with GSI data - solved by gsi_pinger

-> Lighter Program (reducing the amount of space taken by GSI Log) - No more logs with gsi_pinger

-> Make program Server Population agnostic - Done

-> (Fix | High Priority) Imperfect Server Population Detector - Fixed by making program server population agnostic. Ppredictions are made as long as population > 0 - if population = 0, program will wait till at least 1 player joins. 

-> Exceptions Handling - solved using custom exceptions imported from exceptions.py

-> automatic pause-play (during times when a live match is not being spectated) handled using exceptions; Manual pause-play by holding down Esc Key introduced by listener.py module (using Pynput package). Only enabled when the terminal running program is in foreground.

-> Basic GUI - created gui.py

-> Run Linter

-> Add Arguments - added -p, delay X, -w args

-> Modify speed of predictions - added delay argument
_________________________________________________________

Known Bugs/Problems that haven't been solved:

-> (Fix | High Priority) Timeout - Only occurred once. When waiting for usable data to begin flowing, if we wait too long (or ping too many times) we get a timeout error. Exact cause unknown. 

-> (Fix in another Project | Low Priority) 175 vs 115 seconds- The Predictive Model was trained on a dataset where the time_left ranged (0-175). Actually, range should be (0,115). Former's range may include freezetime etc. This may lead to the model being less than ideal due to it's faulty usage of time_left in making predictions. Not code-breaking, but good to fix.

-> (Fix | Low Priority) Miscellaneous minor bugs - A:- All Ts dead and bomb will be defused in time. Prediction should default to win for CT. Probable fix - adding 'bomb' to GSI config to get necessary data for this fix or something similar. 

-> Missing Defuse Kit data - Data on defuse kits held by CT is not transmitted by GSI. Solution unknown

-> (Fix | High Priotity) Exception Handling for Arguments
_________________________________________________________

Ideas:

-> Optimize gsi functionality (alternative to opening/closing server for each ping, increase in speed, elimination of lag spikes)

-> Update Predictors instead of recollecting every time (CSGO GSI may have the functionality, check how they did it)

-> Java GSI - there seem to be many java programs to interact with CSGO GSI. THey may be more efficient in this usecase.

-> HTTP Security (make more robust for deployment)

