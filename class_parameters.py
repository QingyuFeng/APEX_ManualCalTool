#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 11:01:17 2016
#
This script was created to read APEX output files and make graphs
for comparison between observed and simulated values.

This class parameter provided the major environmental settings
like the location of the project of the apex model



DWS file have the following variables.
[RFV', 'PRCP', 'ET', 'Q', 'QDR', 'USLE', 'MUSL', 'MUST',
 'RUS2', 'YN', 'QN', 'SSFN', 'PRKN', 'QDRN', 'YP', 'QP', 'DPRK', 'RSSF',
 'QRF', 'QRFN', 'WYLD','QRFP', 'QDRP\n']

#####################################################################
@author: Qingyu.Feng
"""

import os, glob
import numpy as np

yrlst = np.arange(2007, 2012, 1)
apextxtinoutfd = "TxtInOut_AS1_DLY"
site = "AS1"

infn_rch = glob.glob('%s/*.RCH' %(apextxtinoutfd))
infn_sad = glob.glob('%s/*.SAD' %(apextxtinoutfd))
infn_dws = glob.glob('%s/*.DWS' %(apextxtinoutfd))


observationdatafd = r"db09_observed_field"
if not os.path.isdir(observationdatafd):
    print("In folder for observed data does not exist.")

staticalcaltoolfd = "db10_statisticstools"

outfd_out = r"out01_calibrationresults"
if not os.path.isdir(outfd_out):
    os.mkdir(outfd_out)
    print("Output folder for calculation statistics.")

outfd_out_site = r"out01_calibrationresults/%s" %(site)
if not os.path.isdir(outfd_out_site):
    os.mkdir(outfd_out_site)
    print("Output folder for calculation statistics.")

# This is because the flow in the observed file missing a 
# unit converter. I need to time the flow by 60.
# Later on, the file will be updated and this is not needed.
# Change this to 1.0 if not needed.
unit_converter = 60.0


