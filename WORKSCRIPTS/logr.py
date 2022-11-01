from datetime import datetime
import os
import sys
import copy
import shutil
import glob

sys.path.append('/gpfs/home/mep22dku/scratch/AnalysisRobot/WORKSCRIPTS')
sys.path.append('/gpfs/home/mep22dku/scratch/AnalysisRobot/')
import lom as lom

def find_models():
    w = [x[0] for x in os.walk('/gpfs/home/mep22dku/scratch/AnalysisRobot/RobotPlots')]
    mods = []

    for i in range(0,len(w)):
        q = (w[i].find('TOM'))
        if q > -1:
            tm = (w[i][q:q+13])
            if not tm in mods:
                mods.append(tm)

    return mods

def list_models(mods):
    my_file2 = '/gpfs/home/mep22dku/scratch/PlankTOMRobot/index.html'
    my_file1 = '/gpfs/home/mep22dku/scratch/PlankTOMRobot/indexTemplate.html'
    with open(my_file1, 'r') as file:
        lines = file.readlines()
        file.close()

    lines2 = copy.deepcopy(lines)
    print(len(lines2))
    if (len(lines2)) < 100:
        print('not enough lines')
    else:    
        for i in range(0,len(mods)):
            
            try:
                tmod = mods[i]
                desc = lom.mod[tmod]['desc']
            except:
                desc = 'desc not provided'
               
            # print(i)
            # print(len(mods))
            line_to_replace = 92+i
            print(line_to_replace)
    #         print(mods[i])
    #         print(line_to_replace)#the line we want to remplace

            tstring = f'<a href="https://tjarnikova.github.io/PlankTOMRobot/RobotPlots/{mods[i]}/summary.html">{mods[i]}</a> ({desc})<br>'
            # print(tstring)
            # print(line_to_replace)
            # print(len(lines2))
            lines2[line_to_replace] = tstring


        with open(my_file2, 'w') as file:
            file.writelines(lines2)
            file.close()
        print(len(lines2))

def initLog():
    
    LOGDIR = '/gpfs/home/mep22dku/scratch/AnalysisRobot/LOGS/'
    now = datetime.now()
    dt_string = now.isoformat()
    dt_string = (dt_string[0:16])
    dt_string.replace(':','-')
    ts = f'{LOGDIR}AnalysisRobotLog{dt_string}.txt' 
    with open(ts, 'w') as f:
        f.write(f'AnalysisRobot initialized on {dt_string}')
        f.close()
        
    return ts

ts = initLog()        
        
def noteLog(message, lognam = 'RobotLog.txt'):

    with open(lognam, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        file_object.write(message)

def writeLog(tnam, syear, eyear, lognam = 'RobotLog.txt'):

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
        file_object.write("\n")
        file_object.write(f'analysis initiated for {tnam}, {syear}-{eyear}')
        tstamp = f'date and time = {dt_string}'	
        file_object.write(f'___{tstamp}')


        
def setupVarsAndStorageDir(tnam, syear, eyear):
    
    ## make directory in which to store output. 
    resdir = f'/gpfs/home/mep22dku/scratch/AnalysisRobot/RobotPlots/{tnam}'
    resdir2 = f'/gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots/{tnam}'
    try: 
        os.mkdir(resdir);
    except: 
        print(f'results directory ({resdir}) already made') 
    try: 
        os.mkdir(resdir2);
    except: 
        print(f'website directory ({resdir2}) already made') 
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

def make_summarypage(mods):
    for i in range(0, len(mods)):

        ## get plots
        td = (lom.mod[mods[i]]['desc'])
        desc = f'description: {td}'
        tdir = f'/gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots/{mods[i]}/*.jpg'
        jpgs = glob.glob(tdir)
        for q in range(0, len(jpgs)): 
            jpg = (jpgs[q])
            tstr = f'/gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots/{mods[i]}/'
            w = jpg.replace(tstr, '')
            jpgs[q] = w

        #sort alphabetically
        
        jpgs = sorted(jpgs)
        print(jpgs)
        t = '/gpfs/home/mep22dku/scratch/PlankTOMRobot/summary.html'
        dst = f'/gpfs/home/mep22dku/scratch/PlankTOMRobot/RobotPlots/{mods[i]}/summary.html'
        shutil.copyfile(t, dst)
        my_file = f'{dst}'

        with open(my_file, 'r') as file:
            lines = file.readlines()
            file.close()

            lines2 = copy.deepcopy(lines)
            
        tstring = f'<h1>{mods[i]} summary </h1>'
        lines2[42] = tstring
        lines2[50] = desc
        tstring=  f'<title>{mods[i]}</title>'
        lines2[13] = tstring

        for k in range(0,len(jpgs)):
            tj = jpgs[k]

            tstring = f'<img style="width:90%"  src="{tj}"><br>'

            line_to_replace = 53 + k 
            lines2[line_to_replace] = tstring
                
        with open(my_file, 'w') as file:
            file.writelines(lines2)
            file.close()