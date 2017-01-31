# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:22:06 2017
This script was created to read APEX output files and make graphs
for comparison between observed and simulated values.



@author: Qingyu.Feng
"""
from class_parameters import *
from class_readapexoutputs import read_files
import os
import shutil

# Run Cal exe
os.chdir(apextxtinoutfd)
os.system("APEX1501_64R.exe")
os.chdir(r"..")
print(os.getcwd())

read_outputs = read_files()


# Read in APEX sad files
dl_sad, dl_sad_head = read_outputs.read_sad(infn_sad)

dl_dws, dl_dws_head = read_outputs.read_dws(infn_dws)

dl_runfile_sad = []
dl_runfile_dws = []

for yridx in yrlst:
    
    df_start_time = "%i-04-01 00:00:00" %(yridx)
    df_end_time = "%i-10-30 00:00:00" %(yridx)
    
    infn_obs_tileflow_load = 0
    
    infn_obs_flow_load = r"%s/%s/%s_%i.DLY" %(\
                                observationdatafd, site.upper(),\
                                site.upper(),yridx)
    infn_obs_tileflow_load = r"%s/%sT/%sT_%i.DLY" %(\
                                observationdatafd, site.upper(),\
                                site.upper(),yridx)
    
    if not os.path.isfile(infn_obs_tileflow_load):
        print("Observed flow data does not exist.")
        break        
    
    print("Reading input data from obs flow files")
    dl_dly_head, dl_dly_tile_head, dl_dly_flow, dl_dly_tileflow =\
                read_outputs.read_obs(infn_obs_flow_load, infn_obs_tileflow_load)
    print("Finished Reading input data from obs flow files")
        
    print("Combining observed and simulated flow")
    dl_dly_flowsad, dl_dly_tileflowsad = \
        read_outputs.put_obs_sadsim_dataframe(dl_sad, dl_dly_flow, dl_dly_tileflow)
    print("Finished combining observed and simulated flow")

    print("Combining observed and simulated flow")
    dl_dly_flowdws, dl_dly_tileflowdws =\
        read_outputs.put_obs_dwssim_dataframe(dl_dws, dl_dly_flow, dl_dly_tileflow)
    print("Finished combining observed and simulated flow")

    outfd_out_site_dws = "%s/%s_DWS" %(outfd_out_site, site)
    if not os.path.isdir(outfd_out_site_dws):
        os.mkdir(outfd_out_site_dws)

    outfd_out_site_sad = "%s/%s_SAD" %(outfd_out_site, site)
    if not os.path.isdir(outfd_out_site_sad):
        os.mkdir(outfd_out_site_sad)
        
        
    print("Writing files to calcualte statistics")
    read_outputs.write_dwsprn_run_copyexe(yridx,\
                            dl_dly_flowdws,\
                            dl_dly_tileflowdws,\
                            outfd_out_site_dws,\
                            dl_runfile_dws)
    print("Finished writing files to calcualte statistics")

    print("Writing files to calcualte statistics")
    read_outputs.write_sadprn_run_copyexe(yridx,\
                            dl_dly_flowsad,\
                            dl_dly_tileflowsad,\
                            outfd_out_site_sad,\
                            dl_runfile_sad)
    print("Finished writing files to calcualte statistics")
    
    print("Making plots")
    read_outputs.plot_obssim_dws(dl_dly_flowdws,\
                                 dl_dly_tileflowdws,\
                                 outfd_out_site_dws,\
                                 yridx)
    print("Finished making plots")

    print("Making plots")
    read_outputs.plot_obssim_sad(dl_dly_flowsad,\
                                 dl_dly_tileflowsad,\
                                 outfd_out_site_sad,\
                                 yridx)
    print("Finished making plots")
   
    
    
outfid_run_dws = open("%s/RUN.DAT" %(outfd_out_site_dws),"w")
for rlidx in dl_runfile_dws:    
    outfid_run_dws.writelines("%-12s%i\n" %(rlidx[0], rlidx[1]))
outfid_run_dws.close()

outfid_out_site_sad = open("%s/RUN.DAT" %(outfd_out_site_sad),"w")
for rlidx1 in dl_runfile_sad:    
    outfid_out_site_sad.writelines("%-12s%i\n" %(rlidx1[0], rlidx1[1]))
outfid_out_site_sad.close()


shutil.copy2("%s/Cal_EF_R2.exe" %(staticalcaltoolfd),\
                "%s/Cal_EF_R2.exe" %(outfd_out_site_dws))

# Run Cal exe
os.chdir(outfd_out_site_dws)
if os.path.isfile("result.OUT"):
    os.remove("result.OUT")
os.system("Cal_EF_R2.exe")
os.chdir(r"../../..")
print(os.getcwd())


shutil.copy2("%s/Cal_EF_R2.exe" %(staticalcaltoolfd),\
                "%s/Cal_EF_R2.exe" %(outfd_out_site_sad))

# Run Cal exe
os.chdir(outfd_out_site_sad)
if os.path.isfile("result.OUT"):
    os.remove("result.OUT")
os.system("Cal_EF_R2.exe")
os.chdir(r"../../..")
print(os.getcwd())
