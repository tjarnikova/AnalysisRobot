AnalysisRobot is a prototype framework for running a set of automated analyses on PlankTOM models. Here is how it works:

1. modelsToAnalyze.txt specifies a list of models and year spans to run the analysis for. Their specifics are defined in the dictionary lom.py (name, description, colour).

2. All the analysis scripts are in WORKSCRIPS. 

2. The function runAnalysisRobot in WORKSCRIPTS/robotFrame.py:
* reads the models and year spans in modelsToAnalyze.txt 
* initializes a log in LOGS
* creates a directory for each model (the model's name) under the project's website directory PlankTOMRobot:
        /gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots
* runs standardized summary analyses (each analysis is in its own script), saves relevant plots and saves output (in model's RobotPlots directory)
* adds a note about the analyses done to the log

Because relevant plots are saved in the repository https://github.com/tjarnikova/PlankTOMRobot, which is linked to the website, committing and pushing PlankTOMRobot updates the project's website: https://tjarnikova.github.io/PlankTOMRobot/
