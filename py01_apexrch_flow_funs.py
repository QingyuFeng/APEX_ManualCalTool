# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 15:22:07 2017

To read the output of APEX RCH and compare with observed data
by calculating statistics.

This program was developed to get the output files from the 
.RCH files generated by the APEX model. 
The variables shall follow the settings in the PRNT0806.DAT
in this model. Example can be find in the run file.

Then, the RCH file is processed using AWK program through
cygwin using the sh01_apexrch_extract.sh file. This script
extracts data for the interested stations. 
Then, this python program using the data from each station
and generate figures and statistics for the simulation.


@author: Qingyu.Feng
"""
###########################################################################
## System setup
# For folder check
import os
# For copying files
import shutil
# Making graphs
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np

###########################################################################

# Get a list of files in observation folder
def read_text(textfilename):
    
    fid = open(textfilename, "r")
    lif = fid.readlines()
    fid.close()
    
    return lif


def reformat_obslines(obslines):
    
    del(obslines[0:4])
    
    for oidx in range(len(obslines)):
        obslines[oidx] = obslines[oidx].split(",")
        obslines[oidx][-1] = obslines[oidx][-1][:-1]

        # Prepare for converting this into dictionary
        obslines[oidx] = (obslines[oidx][0],[obslines[oidx][1], 
                                              obslines[oidx][2],
                                              obslines[oidx][3]])
#        print(obslines[oidx])
    obslines = dict(obslines)
    
    return obslines



def reformat_simlines(simlines):

    # APEX uses julian days, I have to generate a
    
    del simlines[0]
    for simcidx in range(len(simlines)):
        simlines[simcidx] = simlines[simcidx].split(" ")
        while "" in simlines[simcidx]:
            simlines[simcidx].remove("")  
    
        simlines[simcidx] = ("%s_%s" %(simlines[simcidx][2], 
                                        simlines[simcidx][3]), 
                                        simlines[simcidx][8])
        
    simlines = dict(simlines)
    
    return simlines


def generate_timeframe(df_start_time,
                        df_end_time,
                        index,
                        column):
  
    df = pd.DataFrame(np.zeros((len(index), len(column))), \
                                columns = column, \
                                index = index)   
    
    
    return df


def filling_df(lif_obs, 
                    df, 
                    station,
                    lif_sim, 
                    column,
                    dateformat):
    
    for dfidx in range(len(df)):
        
        # For sim data I need to get the julian date. 
        # This timetuple is one way to do that.     
#        print(df.index[dfidx].timetuple().tm_yday)
        keysim = "%i_%i" %(df.index[dfidx].year, 
                           df.index[dfidx].timetuple().tm_yday)
        keyobs = df.index[dfidx].strftime(dateformat)
        if lif_obs.has_key(keyobs):
            # Observed data is in the unit of m3/d, need 
            # to be converted to m3/s
            if station == 74: #Fuling
                df[column[1]][dfidx] = float(lif_obs[keyobs][2])
            elif station == 144: #Jianshan
                df[column[1]][dfidx] = float(lif_obs[keyobs][0])
            elif station == 201: #Tuojia
                df[column[1]][dfidx] = float(lif_obs[keyobs][1])
                
        if lif_sim.has_key(keysim):
            df[column[0]][dfidx] = float(lif_sim[keysim])*24*3600
                        
    return df


def write_prn(df, 
              folder, 
              station,
              lst_prnnames, 
              column):

    outfn_prn = "%s/S%s.prn" %(folder, station)

    outfid_prn = open(outfn_prn, "w")
    outfid_prn.writelines("\n")
    for dfidx in range(len(df)):
        lfw = "%.1f\t%.1f\n" %(df[column[0]][dfidx],df[column[1]][dfidx])
        outfid_prn.writelines(lfw)
    
    outfid_prn.close()
            
    lst_prnnames.append(["S%s.prn" %(station), len(df)])
        
    
def write_rundat(folder, runlines):
    
    outfn_run = "%s/RUN.dat" %(folder)
    
    outfid_run = open(outfn_run, "w")
    
    for ridx in runlines:
        lfw = "%-12s%s\n" %(ridx[0], ridx[1])
    
        outfid_run.writelines(lfw)
    
    outfid_run.close()
      
    
    
def copy_cal_run(folder):
    # Copy the executable and do the calculation
    shutil.copy2("calculationprogram/Cal_EF_R2.exe",
                 "%s/Cal_EF_R2.exe" %(folder))
        # Run Cal exe
    os.chdir(folder)
    if os.path.isfile("result.OUT"):
        os.remove("result.OUT")
    os.system("Cal_EF_R2.exe")
    os.chdir("..")
    print(os.getcwd())
    

def draw_plot(df, 
              folder, 
              station,
              column):

    # option 1, specify props dictionaries
    
    
    ax = df.plot(figsize=(12, 6))
    
    
    # option 2, set all colors individually
#    c2 = "purple"
#    box1 = plt.boxplot(data[:,::-2]+1, 
#                       positions=[1.5,2.5,3.5], 
#                       notch=True, 
#                       patch_artist=True)
#    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
#            plt.setp(box1[item], color=c2)
#    plt.setp(box1["boxes"], facecolor=c2)
#    plt.setp(box1["fliers"], markeredgecolor=c2)
#    fig = plot.get_figure()


    # draw temporary red and blue lines and use them to create a legen
    ax.legend()
    ax.set_ylabel('Flow (cms)',size=20)
    ax.set_xlabel('Month',size=20)
    
    plt.savefig("%s/Fig%s.png" %(folder, 
                                     station))
    plt.clf()
#    