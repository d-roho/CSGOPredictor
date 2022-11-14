# CSGOPredictor

Current Bugs/Tasks

-> Better GSI integration

-> Lighter Program - reducing the amount of space taken by GSI Log

-> Better Pause and Play functionality (use keystroke detector, not KeyboardInterrupt)

-> Add args to disable certain features (pause/play, gui...)

-> Commit to CSGO-GSI (at end)

Corrected Bugs:

->  KeyError in server with <10 players (added a check to see if server is populated to prevent KeyError, and added exception to restart loop if KeyError still occurs)

->  GSI - Unicode decoding error (fixed by harcoding utf-8 as decoding standard)

-> Virtual Win Scenarios - situations in a round where the winner is acutally or virtually decided, which the model doesn't recognise (hardcoded theses into main script's code)

-> Json.Loads/index Error (patched by restarting loop on IndexError occurance, but occurance of IndexError is not solved)

-> UnicodeDecodeError, probably for certain usernames (solved by specifying encoding="utf-8" wherever files are read in main script and GSI)

Known Bugs/Problems that haven't been solved:

-> (Fix | High Priority) Imperfect Server Population Detector - the code in place to detect if all 10 players are in server does not work in many scenarios. Not code-breaking, but good to fix. 

-> (Fix | Low Priority) Index Error - occurs from time to time when the snapshot extracted from the log does not include round data (only timestamp). Possibly occurs due to main script reading latest snapshot before GSI has finished logging it. Possible solution - reduce rate of GSI logging and/or main script prediction. Not code-breaking, but causes frequent break in flow of predictions. 

-> (Understand| Low Priority) JSONDecode Error - occurs when 1. has occurred and the snapshot extraction is redone. For an unknown reason, said snapshot is not compatible with json.loads(). Basic manual testing revealed no problems with the second snapshot. Not code-breaking, but good to understand why. Not a priority, look into when free.

-> (Fix in another Project | Low Priority) 175 vs 115 seconds- The Predictive Model was trained on a dataset where the time_left ranged (0-175). Actually, range should be (0,115). Former's range may include freezetime etc. This may lead to the model being less than ideal due to it's faulty usage of time_left in making predictions. Not code-breaking, but good to fix.


Ideas:
-> Update Predictors instead of recollecting every time (CSGO GSI may have the functionality, check how they did it)
-> Bypass creation of dictionary (CSGO GSI may already do this for us)
-> Java GSI - there seem to be many java programs to interact with CSGO GSI. THey may be more efficient in this usecase.
-> HTTP Security (make more robust for deployment)
-> Make program Team Size agnostic (currently requires 10 players in server to function). Would improve compatibility, just need to replace hardcoding.
