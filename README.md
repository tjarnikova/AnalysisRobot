AnalysisRobot is a prototype framework for running a set of automated analyses on PlankTOM models. Here is how it works:

modelsToAnalyze.txt specifies a list of models and year spans to run the analysis for. 

The script robotFrame.py:
    - reads the models and year spans in modelsToAnalyze.txt 
    - creates a directory for each model (the model's name) under:
        /gpfs/home/mep22dku/scratch/AnalysisRobot/RobotPlots
    - runs standardized summary analyses based on options specified. Flags:
        CFLX: calculates yearly annual cflx for SO and whole domain, saves as netcdf in model's RobotPlots directory
    - if PLOT flag set to TRUE:
        script plots and saves output (in model's RobotPlots directory) of above analysis flags (with milestone model TOM12_DW_GA01 for reference)
        
The plots produced by robotFrame.py are stored [here](https://github.com/tjarnikova/AnalysisRobot/tree/main/RobotPlots). 
I eventually want to automate putting them on a website but that's a project for future Tereza. 
       
TD: 
    - add year options in cflx plotting script