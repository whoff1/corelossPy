# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:39:47 2020

@author: Wagner Hoffmann
"""
# import pprint as pp
#import csv
#import os

import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy.optimize import least_squares

#clean variables values like clear all, close all, clc
# from IPython import get_ipython
# get_ipython().magic('reset -sf')

#check NAN and inf values in variable u
#np.isnan(u).any()
#np.isinf(u).any()

# sequece to extract data from txt, tab or csv file
# corelossdata = open(r"C:\Users\...\50x600\BP50Hz.tab")#, "r")
# dataextract = list(csv.reader(corelossdata, delimiter=' ')) #slip two column by space delimiter
# a = np.array(dataextract[1:][1:]) #get B and P values after first line
# corelossdata.close()
# sequece to extract data from txt, tab or csv file

# using numpy to extract data from txt, tab or csv file
#corelossdata = np.genfromtxt(r"C:\Users\...\50x600\BP50Hz.tab", delimiter=" ", skip_header=1)

#Check files inside specific folder path
#------------------------------------------------------------------
# path = 'C:/Users/.../50x600/'
# files = []
# # r=root, d=directories, f = files
# for r, d, f in os.walk(path):
#     for file in f:
#         if '.tab' in file:
#             files.append(os.path.join(r, file))
# for f in files:
#     print(f)
# print(glob.glob('C:/Users/.../50x600/*.tab'))
#------------------------------------------------------------------

#dataname = ("BP" + str(frequency) + "Hz")
#filepath = (r"C:/Users/.../50x600/" + str(dataname) + r".tab")

listfiles = glob.glob('C:/Users/.../50x600/*.tab') #create list with files inside the path

listBP = [] #declaring index variable to recreate list after data extraction
listfreq = [] #declaring index variable to recreate list after data extraction

for freq in range(1,len(listfiles)):  #starting counting positon in the list x=1 - first file
    
    extrdata = listfiles[freq] #extracting each files path name - starting from 1
    corelossdata = np.genfromtxt(extrdata, delimiter=" ", skip_header=1) #extract BP data from file - list file position 'x'    
    
    split_word = 'BP' #get frequencies values after BP in the name of the files    
    datafreqfiles = extrdata.partition(split_word)[2] #get frequencies values after BP in the name of the files
    frequency = datafreqfiles.lstrip().split('Hz.tab')[0]
    
    listBP.append(corelossdata)   
    listfreq.append(frequency)
    
parameters = []

for freq2 in range(1,len(listBP)):

    coredata = listBP[freq2]
    freqdata = listfreq[freq2]
    freqdata = float(freqdata)
    
    def modelbertotti(x, u, freqdata):    
        return (x[1] * freqdata * (u ** x[0])) + (x[2] * (freqdata ** 2) * (u ** 2)) + (x[3] * (freqdata ** 1.5) * (u ** 1.5))
    
    def errorfun(x, u, y, freqdata):
        return modelbertotti(x, u, freqdata) - y
        
    def jac(x, u, y, freqdata):
        J = np.empty((u.size, x.size))
        J[:, 0] = x[0] * x[1] * freqdata * (u ** (x[0] - 1))   #dW/dalpha
        J[:, 1] = freqdata * (u ** x[0])                       #dW/dkh
        J[:, 2] = (freqdata ** 2) * (u ** 2) + x[2]            #dW/dke
        J[:, 3] = (freqdata ** 1.5) * (u ** 1.5) +x[3]         #dW/dka
        return J
    
    x0 =  np.array([2, 1, 1, 1]) #inital values for the fitting variables
    
    u = np.array(coredata[:,0])
    y = np.array(coredata[:,1])
    res = least_squares(errorfun, x0, jac=jac, bounds= ([1.5, 0, 0, 0], [2, 10, 10, 10]), args=(u, y, freqdata), verbose=1)
    
    print(res.x)
    
    u_test = u #np.linspace(0, 1.7)
    y_test = modelbertotti(res.x, u_test,freqdata)
    
    plt.plot(u, y, 'o', markersize=4, label='data')
    plt.title('Losses at Freq. ' + str(int(freqdata)) + 'Hz')
    plt.grid(True)
    plt.plot(u_test, y_test, label='fitted model')
    plt.xlabel('B(T)')
    plt.ylabel(r'Losses (W)')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
    
    parameters.append(res.x)
    
    
    
    
