# CSGOPredictor

Current Bugs/Tasks

2. UnicodeDecodeError for certain usernames still arises (check for solution)
3. Lighter Program - reducing the amount of space taken by GSI Log
4. Better GSI integration
5. Better Pause and Play functionality (use keystroke detector, not KeyboardInterrupt)

Corrected Bugs:

1.  KeyError in server with <10 players (added a check to see if server is populated to prevent KeyError, and added exception to restart loop if KeyError still occurs)
2.  GSI - Unicode decoding error (fixed by harcoding utf-8 as decoding standard)
3. Virtual Win Scenarios - situations in a round where the winner is acutally or virtually decided, which the model doesn't recognise (hardcoded theses into main script's code)
4. Json.Loads/index Error (patched by restarting loop on IndexError occurance, but occurance of IndexError is not solved)

Known Bugs/Problems that haven't been solved:

1. Index Error - occurs from time to time when the snapshot extracted from the log does not include round data (only timestamp). Possibly occurs due to main script reading latest snapshot before GSI has finished logging it. Possible solution - reduce rate of GSI logging and/or main script prediction. Not code-breaking, but causes frequent break in flow of predictions. Should be fixed. 
2. JSONDecode Error - occurs when 1. has occurred and the snapshot extraction is redone. For an unknown reason, said snapshot is not compatible with json.loads(). Basic manual testing revealed no problems with the second snapshot. Not code-breaking, but good to understand why. Not a priority, look into when free.
3. 175 vs 115 seconds- The Predictive Model was trained on a dataset where the time_left ranged (0-175). Actually, range should be (0,115). Former's range may include freezetime etc. This may lead to the model being less than ideal due to it's faulty usage of time_left in making predictions. Not code-breaking, but good to fix.
4. Imperfect Server Population Detector - the code in place to detect if all 10 players are in server does not work in many scenarios. Not code-breaking, but good to fix. 


Ideas:

1. Java GSI - there seem to be many java programs to interact with CSGO GSI. THey may be more efficient in this usecase.
