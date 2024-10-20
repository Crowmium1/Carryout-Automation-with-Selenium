# Carryout-Automation-with-Selenium
I used selenium and pandas mainly to login and loop through the forms on the Synergy inventory management system. Eliminates manual data entry of web form information with a loop and creates an errors excel to highlight revisions to be made by the user.


Don't have the excel open while the executable is running.
If you quit out or the program crashed, you can just restart it and the program will resume from the recent 50 row mark.
If you want to begin processing from row 0 again, just go to the Checkpoint folder and delete the checkpoint.txt.
Move the excel out of the folder once the script is complete. This may be done with a Microsoft task event instead of changing the script.
Rename variables in the config.ini file to set place, supplier, time etc for the script to run on.
Name your script here to align with the config.ini variables so that they may be moved to their correct folder by another script.

Run this command when you want to reset, alternatively: python your_script.py --reset
