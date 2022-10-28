from datetime import datetime
import os
import sys
sys.path.append('/gpfs/home/mep22dku/scratch/AnalysisRobot/WORKSCRIPTS')
sys.path.append('/gpfs/home/mep22dku/scratch/AnalysisRobot/')
import lom as lom

def write_log(tnam, syear, eyear, PLOT, CFLX, lognam = 'RobotLog.txt'):

    with open(lognam, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")

        #append
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        tstamp = f'date and time = {dt_string}'	
        file_object.write(f'analysis initiated for {tnam}, {syear}-{eyear}')
        file_object.write("\n")
        file_object.write(f'___{tstamp}')
        file_object.write("\n")
        file_object.write(f'___options: PLOT {PLOT}, CFLX {CFLX}')
        file_object.write("\n")
        file_object.write(f'_______________________')
        file_object.close()
        
def setupVarsAndStorageDir(tnam, syear, eyear):
    
    ## make directory in which to store output. 
    resdir = f'/gpfs/home/mep22dku/scratch/AnalysisRobot/RobotPlots/{tnam}'
    try: 
        os.mkdir(resdir);
    except: 
        print(f'results directory ({resdir}) already made') 

    ### for plotting, set up a list of things to plot, including the milestone model
    tms = ['TOM12_DW_GA01']
    yst = [1950]
    yen = [2015]
    ls = [':']
    


    tms.append(tnam)
    yst.append(syear)
    yen.append(eyear)
    ls.append('-')
    
    cols = []
    for tm in tms:
        try:
            cols.append(lom.mod[tm]['color'])
        except:
            tcol = 'red'
            cols.append(tcol)
            
    return tms, yst, yen, ls, cols, resdir
