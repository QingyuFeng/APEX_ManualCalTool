#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 11:01:17 2016
# By Qingyu Feng
#
# This script is created to analyze the output files form daily simulation
make the graph and calculate the statistics.

DWS file have the following variables.
[RFV', 'PRCP', 'ET', 'Q', 'QDR', 'USLE', 'MUSL', 'MUST',
 'RUS2', 'YN', 'QN', 'SSFN', 'PRKN', 'QDRN', 'YP', 'QP', 'DPRK', 'RSSF',
 'QRF', 'QRFN', 'WYLD','QRFP', 'QDRP\n']

#####################################################################
@author: Qingyu.Feng
"""

import os
import pandas as pd
import numpy as np
from class_parameters import *


class read_files:
    
    def __init__(self):
        self.data = 0
    
    
    def read_sad(self, infn_sad):
    
        infid_sad = 0
        dl_sad = 0
        
        infid_sad = open(infn_sad[0], "r")
        dl_sad = infid_sad.readlines()
        infid_sad.close()
        
        del dl_sad[:9]
        
        dl_sad_head = dl_sad[0].split(" ")
    
        while "" in dl_sad_head:
            dl_sad_head.remove("")
        
        dl_sad_head = dl_sad_head[1:25]
        
        del dl_sad[0]
    
        for dlidx in xrange(len(dl_sad)):
            dl_sad[dlidx] = dl_sad[dlidx].split(" ")
           
            while "" in dl_sad[dlidx]:
                dl_sad[dlidx].remove("")
    
            dl_sad[dlidx][0] = pd.to_datetime("%i %i %i" %(int(dl_sad[dlidx][2]),
                                                      int(dl_sad[dlidx][3]),
                                                    int(dl_sad[dlidx][4]))) 
    
            dl_sad[dlidx][-1] = dl_sad[dlidx][-1][:-1]
            dl_sad[dlidx] = (dl_sad[dlidx][0], dl_sad[dlidx][1:25])
    
        dl_sad = dict(dl_sad)
    
        return dl_sad, dl_sad_head
    
    
    def read_dws(self, infn_dws):
        
        infid_dws = 0
        dl_dws = 0
        
        infid_dws = open(infn_dws[0], "r")
        dl_dws = infid_dws.readlines()
        infid_dws.close()
        
        dl_dws_head = dl_dws[8].split(" ")[3:]
        while "" in dl_dws_head:
            dl_dws_head.remove("")
        dl_dws_head[-1] = dl_dws_head[-1][0:-1]
        
        del dl_dws[:9]
        
        for dlidx in xrange(len(dl_dws)):
            
            dl_dws[dlidx] = dl_dws[dlidx].split(" ")
            while "" in dl_dws[dlidx]:
                dl_dws[dlidx].remove("")
                
            dl_dws[dlidx][0] = pd.to_datetime(dl_dws[dlidx][0]\
                                    + " " + dl_dws[dlidx][1]\
                                    + " " + dl_dws[dlidx][2]) 
    
            dl_dws[dlidx][-1] = dl_dws[dlidx][-1][:-1]
            dl_dws[dlidx] = (dl_dws[dlidx][0], dl_dws[dlidx][0:])
    
        dl_dws = dict(dl_dws)
    
        return dl_dws, dl_dws_head
    
    
    

    def read_obs(self, infn_obs_flow_load, infn_obs_tileflow_load):
        
        infid_obs_dly_flow = 0
        dl_dly_flowdws = 0    
        infid_obs_dly_tileflow = 0
        dl_dly_tileflow = 0 
        
        infid_obs_dly_flow = open(infn_obs_flow_load, "r")
        dl_dly_flow = infid_obs_dly_flow.readlines()
        infid_obs_dly_flow.close()
        
        infid_obs_dly_tileflow = open(infn_obs_tileflow_load, "r")
        dl_dly_tileflow = infid_obs_dly_tileflow.readlines()
        infid_obs_dly_tileflow.close()    
        
        dl_dly_head = dl_dly_flow[0]
        dl_dly_tile_head = dl_dly_tileflow[0]
    
        dl_dly_head = dl_dly_head.split("\t")
        for thidx in xrange(len(dl_dly_head)):
            dl_dly_head[thidx] = "OBS" + dl_dly_head[thidx]
        
        dl_dly_tile_head = dl_dly_tile_head.split("\t")
        for thidx in xrange(len(dl_dly_tile_head)):
            dl_dly_tile_head[thidx] = "OBSTile" + dl_dly_tile_head[thidx]
    
        dl_dly_head[-1] = dl_dly_head[-1][0:-1]        
        dl_dly_tile_head[-1] = dl_dly_tile_head[-1][0:-1]        
    
        del dl_dly_flow[0]
        del dl_dly_tileflow[0]
        
        for dldlyidx in xrange(len(dl_dly_flow)):
            # Flow
            dl_dly_flow[dldlyidx] = dl_dly_flow[dldlyidx].split("\t")
            dl_dly_flow[dldlyidx][0] = pd.to_datetime(dl_dly_flow[dldlyidx][0])
            dl_dly_flow[dldlyidx][-1] = dl_dly_flow[dldlyidx][-1][:-1]
            # in RCH, flow unit is cms, but in obs is cmd, need to devide 24*3600        
            dl_dly_flow[dldlyidx][2] = float(dl_dly_flow[dldlyidx][2])/24/3600
            dl_dly_flow[dldlyidx] = (dl_dly_flow[dldlyidx][0],\
                                        dl_dly_flow[dldlyidx][1:])
            # Tile flow
            dl_dly_tileflow[dldlyidx] = dl_dly_tileflow[dldlyidx].split("\t")
            dl_dly_tileflow[dldlyidx][0] = pd.to_datetime(dl_dly_tileflow[dldlyidx][0])
            dl_dly_tileflow[dldlyidx][-1] = dl_dly_tileflow[dldlyidx][-1][:-1]
    
            dl_dly_tileflow[dldlyidx] = (dl_dly_tileflow[dldlyidx][0],\
                                        dl_dly_tileflow[dldlyidx][1:])
        
    
        dl_dly_flow = pd.DataFrame.from_dict(dict(dl_dly_flow),\
                                            orient='index',\
                                            dtype=float)
        dl_dly_flow.columns = dl_dly_head[1:]                                   
        dl_dly_tileflow = pd.DataFrame.from_dict(dict(dl_dly_tileflow),\
                                            orient='index',\
                                            dtype=float)
        dl_dly_tileflow.columns = dl_dly_tile_head[1:]                                   
    
        return dl_dly_head, dl_dly_tile_head, dl_dly_flow, dl_dly_tileflow 
    
        
        
    def put_obs_sadsim_dataframe(self, dl_sad, dl_dly_flow, dl_dly_tileflow):
        
        dl_dly_flowsad = dl_dly_flow.copy(deep = True)
        dl_dly_tileflowsad = dl_dly_tileflow.copy(deep = True)
        
        
        dl_dly_flowsad['OBSYN'] = dl_dly_flowsad["OBSTNkgpd "]\
                                - dl_dly_flowsad["OBSAMMOkgpd "]\
                                - dl_dly_flowsad["OBSNOLkgpd "]\
                                - dl_dly_flowsad["OBSTKNkgpd "]
        dl_dly_flowsad['OBSYP'] = dl_dly_flowsad["OBSTPkgpd "]\
                                -dl_dly_flowsad["OBSOPkgpd "] 
                                
        dl_dly_tileflowsad['OBSTileYN'] = dl_dly_tileflowsad["OBSTileTNkgpd "]\
                                -dl_dly_tileflowsad["OBSTileTKNkgpd "]\
                                -dl_dly_tileflowsad["OBSTileNOLkgpd "]\
                                -dl_dly_tileflowsad["OBSTileAMMOkgpd "]
        dl_dly_tileflowsad['OBSTileYP'] = dl_dly_tileflowsad["OBSTileTPkgpd "]\
                                -dl_dly_tileflowsad["OBSTileOPkgpd "]    
            
        dl_dly_flowsad['SIMWYLD'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)
        dl_dly_flowsad['SIMYN'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)
        dl_dly_flowsad['SIMQN'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index) 
        dl_dly_flowsad['SIMYP'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)        
        dl_dly_flowsad['SIMQP'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)          
        dl_dly_flowsad['SIMUSLE'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)            
        dl_dly_flowsad['SIMRUS2'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)          
        dl_dly_flowsad['SIMMUSL'] = pd.Series(\
            np.zeros(len(dl_dly_flowsad["OBSFlowcmd "])),\
            index=dl_dly_flowsad.index)
    
        dl_dly_tileflowsad['SIMQDR'] = pd.Series(\
            np.zeros(len(dl_dly_tileflowsad["OBSTileFlowcmd "])),\
            index=dl_dly_tileflowsad.index)      
        dl_dly_tileflowsad['SIMQDRN'] = pd.Series(\
            np.zeros(len(dl_dly_tileflowsad["OBSTileFlowcmd "])),\
            index=dl_dly_tileflowsad.index)          
        dl_dly_tileflowsad['SIMQDRP'] = pd.Series(\
            np.zeros(len(dl_dly_tileflowsad["OBSTileFlowcmd "])),\
            index=dl_dly_tileflowsad.index)         
            
            
        for dfidx in range(len(dl_dly_flowsad)):
            if pd.Timestamp(dl_dly_flowsad.index[dfidx]) in dl_sad:
                dl_dly_flowsad["SIMWYLD"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][5])
                dl_dly_flowsad["SIMQN"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][12])
    #                               + float(dl_sad[pd.Timestamp\
    #                                (dl_dly_flow.index[dfidx])][20]) \
    #                               + float(dl_sad[pd.Timestamp\
    #                                (dl_dly_flow.index[dfidx])][22])
                dl_dly_flowsad["SIMYN"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][11])  
                dl_dly_flowsad["SIMQP"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][17])  
                dl_dly_flowsad["SIMYP"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][16])  
                dl_dly_flowsad["SIMUSLE"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][7])  
                dl_dly_flowsad["SIMMUSL"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][8])  
                dl_dly_flowsad["SIMRUS2"][dfidx] = float(dl_sad[pd.Timestamp\
                                    (dl_dly_flowsad.index[dfidx])][10])  
    
        for dftileidx in range(len(dl_dly_tileflowsad)):
            if pd.Timestamp(dl_dly_tileflowsad.index[dftileidx]) in dl_sad:
                dl_dly_tileflowsad["SIMQDR"][dftileidx] = \
                    float(dl_sad[pd.Timestamp(\
                    dl_dly_tileflowsad.index[dftileidx])][6])           
                dl_dly_tileflowsad["SIMQDRN"][dftileidx] = \
                    float(dl_sad[pd.Timestamp(\
                    dl_dly_tileflowsad.index[dftileidx])][15])
                dl_dly_tileflowsad["SIMQDRP"][dftileidx] = \
                    float(dl_sad[pd.Timestamp(\
                    dl_dly_tileflowsad.index[dftileidx])][23])
               
        return dl_dly_flowsad, dl_dly_tileflowsad    
    
    

    def put_obs_dwssim_dataframe(self, dl_dws, dl_dly_flow, dl_dly_tileflow):
        
        dl_dly_flowdws = dl_dly_flow.copy(deep = True)
        dl_dly_tileflowdws = dl_dly_tileflow.copy(deep = True)
        
        
        dl_dly_flowdws['OBSYN'] = dl_dly_flowdws["OBSTNkgpd "]\
                                - dl_dly_flowdws["OBSAMMOkgpd "]\
                                - dl_dly_flowdws["OBSNOLkgpd "]\
                                - dl_dly_flowdws["OBSTKNkgpd "]
        dl_dly_flowdws['OBSYP'] = dl_dly_flowdws["OBSTPkgpd "]\
                                -dl_dly_flowdws["OBSOPkgpd "] 
                                
        dl_dly_tileflowdws['OBSTileYN'] = dl_dly_tileflowdws["OBSTileTNkgpd "]\
                                -dl_dly_tileflowdws["OBSTileTKNkgpd "]\
                                -dl_dly_tileflowdws["OBSTileNOLkgpd "]\
                                -dl_dly_tileflowdws["OBSTileAMMOkgpd "]
        dl_dly_tileflowdws['OBSTileYP'] = dl_dly_tileflowdws["OBSTileTPkgpd "]\
                                -dl_dly_tileflowdws["OBSTileOPkgpd "]    
            
        dl_dly_flowdws['SIMWYLD'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)
        dl_dly_flowdws['SIMYN'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)
        dl_dly_flowdws['SIMQN'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index) 
        dl_dly_flowdws['SIMYP'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)        
        dl_dly_flowdws['SIMQP'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)          
        dl_dly_flowdws['SIMUSLE'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)            
        dl_dly_flowdws['SIMRUS2'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)          
        dl_dly_flowdws['SIMMUSL'] = pd.Series(\
            np.zeros(len(dl_dly_flowdws["OBSFlowcmd "])),\
            index=dl_dly_flowdws.index)
    
        dl_dly_tileflowdws['SIMQDR'] = pd.Series(\
            np.zeros(len(dl_dly_tileflowdws["OBSTileFlowcmd "])),\
            index=dl_dly_tileflowdws.index)      
        dl_dly_tileflowdws['SIMQDRN'] = pd.Series(\
            np.zeros(len(dl_dly_tileflowdws["OBSTileFlowcmd "])),\
            index=dl_dly_tileflowdws.index)          
        dl_dly_tileflowdws['SIMQDRP'] = pd.Series(\
            np.zeros(len(dl_dly_tileflowdws["OBSTileFlowcmd "])),\
            index=dl_dly_tileflowdws.index)         
            
            
        for dfidx in range(len(dl_dly_flowdws)):
            if pd.Timestamp(dl_dly_flowdws.index[dfidx]) in dl_dws:
                dl_dly_flowdws["SIMWYLD"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][21])
                dl_dly_flowdws["SIMQN"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][12])          
                dl_dly_flowdws["SIMYN"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][11])  
                dl_dly_flowdws["SIMQP"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][17])  
                dl_dly_flowdws["SIMYP"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][16])  
                dl_dly_flowdws["SIMUSLE"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][7])  
                dl_dly_flowdws["SIMMUSL"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][8])  
                dl_dly_flowdws["SIMRUS2"][dfidx] = float(dl_dws[pd.Timestamp\
                                    (dl_dly_flowdws.index[dfidx])][10])  
    
        for dftileidx in range(len(dl_dly_tileflowdws)):
            if pd.Timestamp(dl_dly_tileflowdws.index[dftileidx]) in dl_dws:
                dl_dly_tileflowdws["SIMQDR"][dftileidx] = \
                    float(dl_dws[pd.Timestamp(\
                    dl_dly_tileflowdws.index[dftileidx])][6])           
                dl_dly_tileflowdws["SIMQDRN"][dftileidx] = \
                    float(dl_dws[pd.Timestamp(\
                    dl_dly_tileflowdws.index[dftileidx])][15])
                dl_dly_tileflowdws["SIMQDRP"][dftileidx] = \
                    float(dl_dws[pd.Timestamp(\
                    dl_dly_tileflowdws.index[dftileidx])][23])
               
        return dl_dly_flowdws, dl_dly_tileflowdws    
    
    


    def write_dwsprn_run_copyexe(self, yridx,\
                                dl_dly_flowdws,\
                                dl_dly_tileflowdws,\
                                outfd_out_site_dws,\
                                dl_runfile_dws):
        

            
        dl_dly_flowdws = dl_dly_flowdws[dl_dly_flowdws.index.month >= 4]    
        dl_dly_flowdws = dl_dly_flowdws[dl_dly_flowdws.index.month <= 10]  
        
        dl_dly_flowdws = dl_dly_flowdws.sort_index()    
        
        outfn_obssim_q = r"%s/sq%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_qn = r"%s/qn%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_yn = r"%s/yn%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_qp = r"%s/qp%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_yp = r"%s/yp%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_yusle = r"%s/yu%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_ymusl = r"%s/ym%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_yrus2 = r"%s/yr%i.prn" %(outfd_out_site_dws, yridx)
        
        outfn_obssim_tq = r"%s/tq%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_tqn = r"%s/tqn%i.prn" %(outfd_out_site_dws, yridx)
        outfn_obssim_tqp = r"%s/tqp%i.prn" %(outfd_out_site_dws, yridx)
    
        outfid_obssim_q = open(outfn_obssim_q, "w")
        outfid_obssim_qn = open(outfn_obssim_qn, "w")
        outfid_obssim_yn = open(outfn_obssim_yn, "w")
        outfid_obssim_qp = open(outfn_obssim_qp, "w")
        outfid_obssim_yp = open(outfn_obssim_yp, "w")
        outfid_obssim_yusle = open(outfn_obssim_yusle, "w")
        outfid_obssim_ymusl = open(outfn_obssim_ymusl, "w")
        outfid_obssim_yrus2 = open(outfn_obssim_yrus2, "w")
        
        outfid_obssim_q.writelines("\n")
        outfid_obssim_qn.writelines("\n")
        outfid_obssim_yn.writelines("\n")
        outfid_obssim_qp.writelines("\n")
        outfid_obssim_yp.writelines("\n")
        outfid_obssim_yusle.writelines("\n")
        outfid_obssim_ymusl.writelines("\n")
        outfid_obssim_yrus2.writelines("\n")
    

        for dfwidx in dl_dly_flowdws.index:
            
            # Only calculate statistics between April 1 to Oct 31
            outfid_obssim_q.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSFlowmm "][dfwidx]),\
                    float(dl_dly_flowdws["SIMWYLD"][dfwidx])\
                    ))    
            outfid_obssim_qn.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSAMMOkgpd "][dfwidx])\
                    +float(dl_dly_flowdws["OBSNOLkgpd "][dfwidx])\
                    +float(dl_dly_flowdws["OBSTKNkgpd "][dfwidx]),\
                    float(dl_dly_flowdws["SIMQN"][dfwidx])\
                    ))
            outfid_obssim_yn.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSYN"][dfwidx]),\
                    float(dl_dly_flowdws["SIMYN"][dfwidx])\
                    )) 
            outfid_obssim_qp.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSOPkgpd "][dfwidx]),\
                    float(dl_dly_flowdws["SIMQP"][dfwidx])\
                    ))   
            outfid_obssim_yp.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSYP"][dfwidx]),\
                    float(dl_dly_flowdws["SIMYP"][dfwidx])\
                    )) 
            outfid_obssim_yusle.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSSEDkgpd "][dfwidx]),\
                    float(dl_dly_flowdws["SIMUSLE"][dfwidx])\
                    ))   
            outfid_obssim_ymusl.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSSEDkgpd "][dfwidx]),\
                    float(dl_dly_flowdws["SIMMUSL"][dfwidx])\
                    ))  
            outfid_obssim_yrus2.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowdws["OBSSEDkgpd "][dfwidx]),\
                    float(dl_dly_flowdws["SIMRUS2"][dfwidx])\
                    ))                               
        outfid_obssim_q.close()
        outfid_obssim_qn.close()
        outfid_obssim_yn.close()
        outfid_obssim_qp.close()
        outfid_obssim_yp.close()
        outfid_obssim_yusle.close()
        outfid_obssim_ymusl.close()
        outfid_obssim_yrus2.close()
    
        
        outfid_obssim_tq = open(outfn_obssim_tq, "w")
        outfid_obssim_tqn = open(outfn_obssim_tqn, "w")
        outfid_obssim_tqp = open(outfn_obssim_tqp, "w")
        
        outfid_obssim_tq.writelines("\n")
        outfid_obssim_tqn.writelines("\n")
        outfid_obssim_tqp.writelines("\n")
        
        dl_dly_tileflowdws = dl_dly_tileflowdws[dl_dly_tileflowdws.index.month > 3]        
        dl_dly_tileflowdws = dl_dly_tileflowdws[dl_dly_tileflowdws.index.month < 11]  
    
        dl_dly_tileflowdws = dl_dly_tileflowdws.sort_index()       
#        print(dl_dly_tileflowdws)
        for df1wtdidx in dl_dly_tileflowdws.index:
            outfid_obssim_tq.writelines("%10.6f\t%10.6f\n" %(\
                float(dl_dly_tileflowdws["OBSTileFlowmm "][df1wtdidx]),\
                float(dl_dly_tileflowdws["SIMQDR"][df1wtdidx])\
                                    ))
            
            outfid_obssim_tqn.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_tileflowdws["OBSTileAMMOkgpd "][df1wtdidx])\
                    +float(dl_dly_tileflowdws["OBSTileNOLkgpd "][df1wtdidx])\
                    +float(dl_dly_tileflowdws["OBSTileTKNkgpd "][df1wtdidx]),\
                float(dl_dly_tileflowdws["SIMQDRN"][df1wtdidx])\
                                    ))   
            outfid_obssim_tqp.writelines("%10.6f\t%10.6f\n" %(\
                float(dl_dly_tileflowdws["OBSTileOPkgpd "][df1wtdidx]),\
                float(dl_dly_tileflowdws["SIMQDRP"][df1wtdidx])\
                                    )) 
        outfid_obssim_tq.close()
        outfid_obssim_tqn.close()
        outfid_obssim_tqp.close()
        
        dl_runfile_dws.append([os.path.split(outfn_obssim_q)[-1], len(dl_dly_flowdws.index)])
        dl_runfile_dws.append([os.path.split(outfn_obssim_qn)[-1], len(dl_dly_flowdws.index)])
        dl_runfile_dws.append([os.path.split(outfn_obssim_yn)[-1], len(dl_dly_flowdws.index)])
        dl_runfile_dws.append([os.path.split(outfn_obssim_qp)[-1], len(dl_dly_flowdws.index)])
        dl_runfile_dws.append([os.path.split(outfn_obssim_yp)[-1], len(dl_dly_flowdws.index)])
    #    dl_runfile_dws.append([os.path.split(outfn_obssim_yusle)[-1], len(dl_dly_flowdws.index)])
    #    dl_runfile_dws.append([os.path.split(outfn_obssim_ymusl)[-1], len(dl_dly_flowdws.index)])
    #    dl_runfile_dws.append([os.path.split(outfn_obssim_yrus2)[-1], len(dl_dly_flow.index)])
        
        dl_runfile_dws.append([os.path.split(outfn_obssim_tq)[-1], len(dl_dly_tileflowdws.index)])
    #    dl_runfile_dws.append([os.path.split(outfn_obssim_tqn)[-1], len(dl_dly_tileflowdws.index)])
        dl_runfile_dws.append([os.path.split(outfn_obssim_tqp)[-1], len(dl_dly_tileflowdws.index)])
    
    
            
        
    def write_sadprn_run_copyexe(self, yridx,\
                                dl_dly_flowsad,\
                                dl_dly_tileflowsad,\
                                outfd_out_site_sad,\
                                dl_runfile_sad):
     

        dl_dly_flowsad = dl_dly_flowsad[dl_dly_flowsad.index.month >= 4]    
        dl_dly_flowsad = dl_dly_flowsad[dl_dly_flowsad.index.month <= 10]  
        
        outfn_obssim_q = r"%s/sq%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_qn = r"%s/qn%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_yn = r"%s/yn%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_qp = r"%s/qp%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_yp = r"%s/yp%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_yusle = r"%s/yu%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_ymusl = r"%s/ym%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_yrus2 = r"%s/yr%i.prn" %(outfd_out_site_sad, yridx)
        
        outfn_obssim_tq = r"%s/tq%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_tqn = r"%s/tqn%i.prn" %(outfd_out_site_sad, yridx)
        outfn_obssim_tqp = r"%s/tqp%i.prn" %(outfd_out_site_sad, yridx)
    
        outfid_obssim_q = open(outfn_obssim_q, "w")
        outfid_obssim_qn = open(outfn_obssim_qn, "w")
        outfid_obssim_yn = open(outfn_obssim_yn, "w")
        outfid_obssim_qp = open(outfn_obssim_qp, "w")
        outfid_obssim_yp = open(outfn_obssim_yp, "w")
        outfid_obssim_yusle = open(outfn_obssim_yusle, "w")
        outfid_obssim_ymusl = open(outfn_obssim_ymusl, "w")
        outfid_obssim_yrus2 = open(outfn_obssim_yrus2, "w")
        
        outfid_obssim_q.writelines("\n")
        outfid_obssim_qn.writelines("\n")
        outfid_obssim_yn.writelines("\n")
        outfid_obssim_qp.writelines("\n")
        outfid_obssim_yp.writelines("\n")
        outfid_obssim_yusle.writelines("\n")
        outfid_obssim_ymusl.writelines("\n")
        outfid_obssim_yrus2.writelines("\n")
    
        dl_dly_flowsad = dl_dly_flowsad.sort_index()    
        
        for dfwidx in dl_dly_flowsad.index:
            
            # Only calculate statistics between April 1 to Oct 31
            
            outfid_obssim_q.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSFlowmm "][dfwidx]),\
                    float(dl_dly_flowsad["SIMWYLD"][dfwidx])\
                    ))    
            outfid_obssim_qn.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSAMMOkgpd "][dfwidx])\
                    +float(dl_dly_flowsad["OBSNOLkgpd "][dfwidx])\
                    +float(dl_dly_flowsad["OBSTKNkgpd "][dfwidx]),\
                    float(dl_dly_flowsad["SIMQN"][dfwidx])\
                    ))                         
            outfid_obssim_yn.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSYN"][dfwidx]),\
                    float(dl_dly_flowsad["SIMYN"][dfwidx])\
                    ))                                              
            outfid_obssim_qp.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSOPkgpd "][dfwidx]),\
                    float(dl_dly_flowsad["SIMQP"][dfwidx])\
                    ))                                     
            outfid_obssim_yp.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSYP"][dfwidx]),\
                    float(dl_dly_flowsad["SIMYP"][dfwidx])\
                    )) 
                                                 
            outfid_obssim_yusle.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSSEDkgpd "][dfwidx]),\
                    float(dl_dly_flowsad["SIMUSLE"][dfwidx])\
                    ))                                              
            outfid_obssim_ymusl.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSSEDkgpd "][dfwidx]),\
                    float(dl_dly_flowsad["SIMMUSL"][dfwidx])\
                    ))                                     
            outfid_obssim_yrus2.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_flowsad["OBSSEDkgpd "][dfwidx]),\
                    float(dl_dly_flowsad["SIMRUS2"][dfwidx])\
                    ))                               
                                
        outfid_obssim_q.close()
        outfid_obssim_qn.close()
        outfid_obssim_yn.close()
        outfid_obssim_qp.close()
        outfid_obssim_yp.close()
        outfid_obssim_yusle.close()
        outfid_obssim_ymusl.close()
        outfid_obssim_yrus2.close()
    
        
        outfid_obssim_tq = open(outfn_obssim_tq, "w")
        outfid_obssim_tqn = open(outfn_obssim_tqn, "w")
        outfid_obssim_tqp = open(outfn_obssim_tqp, "w")
        
        outfid_obssim_tq.writelines("\n")
        outfid_obssim_tqn.writelines("\n")
        outfid_obssim_tqp.writelines("\n")
        
        dl_dly_tileflowsad = dl_dly_tileflowsad[dl_dly_tileflowsad.index.month >= 4]        
        dl_dly_tileflowsad = dl_dly_tileflowsad[dl_dly_tileflowsad.index.month <= 10]  
    
        dl_dly_tileflowsad = dl_dly_tileflowsad.sort_index()       
        
        for df1wtdidx in dl_dly_tileflowsad.index:
            outfid_obssim_tq.writelines("%10.6f\t%10.6f\n" %(\
                float(dl_dly_tileflowsad["OBSTileFlowmm "][df1wtdidx]),\
                float(dl_dly_tileflowsad["SIMQDR"][df1wtdidx])\
                                    ))
            outfid_obssim_tqn.writelines("%10.6f\t%10.6f\n" %(\
                    float(dl_dly_tileflowsad["OBSTileAMMOkgpd "][dfwidx])\
                    +float(dl_dly_tileflowsad["OBSTileNOLkgpd "][dfwidx])\
                    +float(dl_dly_tileflowsad["OBSTileTKNkgpd "][dfwidx]),\
                float(dl_dly_tileflowsad["SIMQDRN"][df1wtdidx])\
                                    ))   
    
            outfid_obssim_tqp.writelines("%10.6f\t%10.6f\n" %(\
                float(dl_dly_tileflowsad["OBSTileOPkgpd "][df1wtdidx]),\
                float(dl_dly_tileflowsad["SIMQDRP"][df1wtdidx])\
                                    )) 
        outfid_obssim_tq.close()
        outfid_obssim_tqn.close()
        outfid_obssim_tqp.close()
        
        dl_runfile_sad.append([os.path.split(outfn_obssim_q)[-1], len(dl_dly_flowsad.index)])
        dl_runfile_sad.append([os.path.split(outfn_obssim_qn)[-1], len(dl_dly_flowsad.index)])
        dl_runfile_sad.append([os.path.split(outfn_obssim_yn)[-1], len(dl_dly_flowsad.index)])
        dl_runfile_sad.append([os.path.split(outfn_obssim_qp)[-1], len(dl_dly_flowsad.index)])
        dl_runfile_sad.append([os.path.split(outfn_obssim_yp)[-1], len(dl_dly_flowsad.index)])
    #    dl_runfile_sad.append([os.path.split(outfn_obssim_yusle)[-1], len(dl_dly_flowsad.index)])
    #    dl_runfile_sad.append([os.path.split(outfn_obssim_ymusl)[-1], len(dl_dly_flowsad.index)])
    #    dl_runfile_sad.append([os.path.split(outfn_obssim_yrus2)[-1], len(dl_dly_flowsad.index)])
        
        dl_runfile_sad.append([os.path.split(outfn_obssim_tq)[-1], len(dl_dly_tileflowsad.index)])
    #    dl_runfile_sad.append([os.path.split(outfn_obssim_tqn)[-1], len(dl_dly_tileflowsad.index)])
        dl_runfile_sad.append([os.path.split(outfn_obssim_tqp)[-1], len(dl_dly_tileflowsad.index)])
    
        
            
    def plot_obssim_sad(self,\
                        dl_dly_flowsad,\
                        dl_dly_tileflowsad,\
                        outfd_out_site_sad,\
                        yridx):
        
        dl_dly_flowsad = dl_dly_flowsad[dl_dly_flowsad.index.month >= 4]    
        dl_dly_flowsad = dl_dly_flowsad[dl_dly_flowsad.index.month <= 10]  
        
    
        plotting_sq = dl_dly_flowsad.plot(y=["OBSFlowmm ","SIMWYLD"],\
                                title="%s_%i" %(site.upper(), yridx),\
                                fontsize=20,\
                                figsize = (6,4))
        outfn_fig_sq = plotting_sq.get_figure()
        outfn_fig_sq.savefig("%s/%s_sq.png" %(outfd_out_site_sad, yridx))
    #
    #    plotting_qn = dl_dly_flow.plot(y=["OBSFlowmm ","SIMWYLD"],\
    #                            title="%s_%i" %(site.upper(), yridx),\
    #                            fontsize=20,\
    #                            figsize = (6,4))
    #    plotting_qn = plotting_sq.get_figure()
    #    plotting_qn.savefig("%s/%s_sq.png" %(outfd_out_site, yridx))
    #    
    
    
    
        
        dl_dly_tileflowsad = dl_dly_tileflowsad[dl_dly_tileflowsad.index.month >= 4]        
        dl_dly_tileflowsad = dl_dly_tileflowsad[dl_dly_tileflowsad.index.month <= 10]  
    
        plotting_qdr = dl_dly_tileflowsad.plot(y=["OBSTileFlowmm ","SIMQDR"],\
                                title="%s_%i" %(site.upper(), yridx),\
                                fontsize=20,\
                                figsize = (6,4))
        outfn_fig_qdr = plotting_qdr.get_figure()
        outfn_fig_qdr.savefig("%s/%s_qdr.png" %(outfd_out_site_sad, yridx))



    def plot_obssim_dws(self,\
                        dl_dly_flowdws,\
                        dl_dly_tileflowdws,\
                        outfd_out_site_dws,\
                        yridx):
        
        dl_dly_flowdws = dl_dly_flowdws[dl_dly_flowdws.index.month >= 4]    
        dl_dly_flowdws = dl_dly_flowdws[dl_dly_flowdws.index.month <= 10]  
        
    
        plotting_sq = dl_dly_flowdws.plot(y=["OBSFlowmm ","SIMWYLD"],\
                                title="%s_%i" %(site.upper(), yridx),\
                                fontsize=20,\
                                figsize = (6,4))
        outfn_fig_sq = plotting_sq.get_figure()
        outfn_fig_sq.savefig("%s/%s_sq.png" %(outfd_out_site_dws, yridx))
    #
    #    plotting_qn = dl_dly_flow.plot(y=["OBSFlowmm ","SIMWYLD"],\
    #                            title="%s_%i" %(site.upper(), yridx),\
    #                            fontsize=20,\
    #                            figsize = (6,4))
    #    plotting_qn = plotting_sq.get_figure()
    #    plotting_qn.savefig("%s/%s_sq.png" %(outfd_out_site, yridx))
    #    
    
    
    
        
        dl_dly_tileflowdws = dl_dly_tileflowdws[dl_dly_tileflowdws.index.month >= 4]        
        dl_dly_tileflowdws = dl_dly_tileflowdws[dl_dly_tileflowdws.index.month <= 10]  
    
        plotting_qdr = dl_dly_tileflowdws.plot(y=["OBSTileFlowmm ","SIMQDR"],\
                                title="%s_%i" %(site.upper(), yridx),\
                                fontsize=20,\
                                figsize = (6,4))
        outfn_fig_qdr = plotting_qdr.get_figure()
        outfn_fig_qdr.savefig("%s/%s_qdr.png" %(outfd_out_site_dws, yridx))
