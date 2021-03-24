#Import modules======================================================
#import matplotlib.pyplot as plt
import numpy as np
#import data_analysis_basic as dab
#import datetime as dt
#import copy
#import scipy.optimize as scpopt
import netCDF4 as nc
import csv

#S5p TROPOMI=========================================================
#Core part-----------------------------------------------------------

def conv_s5p_csv(infile, outfile, optkeys):
    #Load nc file
    nc0  = nc.Dataset(infile, 'r')
    nc0v = nc0['PRODUCT'].variables
    dict0 = {}
    dict0['longitude' ] = nc0v['longitude'][:]
    dict0['latitude' ]  = nc0v['latitude'][:]
    dict0['time_sec']   = nc0v['time'][:] + nc0v['delta_time'][:]*0.001
    dict0['qa_value' ]  = nc0v['qa_value'][:]
    for i in range(len(optkeys)):
        dict0[optkeys[i]] = nc0v[optkeys[i]][:]
    
    nc0.close()
    
    ntime, nsl, ngp = dict0['qa_value'].shape
    time1 = np.zeros(dict0['qa_value'].shape)
    for i in range(ntime):
        for j in range(nsl):
            time1[i,j,:] = dict0['time_sec'][i,j]
    
    mask  = dict0[optkeys[0]].mask
    dict1 = {}
    dict1['longitude' ] = dict0['longitude'][~mask]
    dict1['latitude' ] = dict0['latitude'][~mask]
    dict1['time_sec'] = time1[~mask]
    dict1['qa_value' ] = dict0['qa_value'][~mask]
    for i in range(len(optkeys)):
        dict1[optkeys[i]] = dict0[optkeys[i]][~mask]
    
    nsize = dict1['qa_value'].size
    with open(outfile, 'w') as csv_file:
        #Set Header
        fieldnames = ['time_sec', 'longitude', 'latitude', 'qa_value']
        fieldnames.extend(optkeys)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #Write data
        for i in range(nsize):
            dict_tmp = {}
            dict_tmp['time_sec' ] = dict1['time_sec' ][i]
            dict_tmp['longitude'] = dict1['longitude'][i]
            dict_tmp['latitude' ] = dict1['latitude' ][i]
            dict_tmp['qa_value' ] = dict1['qa_value' ][i]
            for j in range(len(optkeys)):
                dict_tmp[optkeys[j]] = dict1[optkeys[j]][i]
            #
            writer.writerow(dict_tmp)


"""

'time', 'latitude_ccd', 'longitude_ccd', 'latitude_csa', 'longitude_csa', 
'ozone_tropospheric_vertical_column', 'ozone_tropospheric_vertical_column_precision', 
'ozone_tropospheric_mixing_ratio', 
'ozone_tropospheric_mixing_ratio_precision', 'ozone_upper_tropospheric_mixing_ratio', 
'ozone_upper_tropospheric_mixing_ratio_precision', 'ozone_upper_tropospheric_mixing_ratio_flag', 'qa_value']

def conv_s5p_csv_o3_tcl(infile, outfile, optkeys):
    #Load nc file
    nc0  = nc.Dataset(infile, 'r')
    nc0v = nc0['PRODUCT'].variables
    dict0 = {}
    dict0['longitude_ccd' ] = nc0v['longitude_ccd'][:]
    dict0['longitude_csa' ] = nc0v['longitude_csa'][:]
    dict0['latitude_ccd' ] = nc0v['latitude_ccd'][:]
    dict0['latitude_csa' ] = nc0v['latitude_csa'][:]
    dict0['time_utc'] = tconv_str2float(nc0v['time'][:])
    dict0['qa_value' ] = nc0v['qa_value'][:]
    for i in range(len(optkeys)):
        dict0[optkeys[i]] = nc0v[optkeys[i]][:]
    #
    nc0.close()
    #
    ntime, nsl, ngp = dict0['qa_value'].shape
    time1 = np.zeros(dict0['qa_value'].shape)
    for i in range(ntime):
        for j in range(nsl):
            time1[i,j,:] = dict0['time_utc'][i,j]
    #
    mask  = dict0[optkeys[0]].mask
    dict1 = {}
    dict1['longitude' ] = dict0['longitude'][~mask]
    dict1['latitude' ] = dict0['latitude'][~mask]
    dict1['time_utc'] = time1[~mask]
    dict1['qa_value' ] = dict0['qa_value'][~mask]
    for i in range(len(optkeys)):
        dict1[optkeys[i]] = dict0[optkeys[i]][~mask]
    #
    nsize = dict1['qa_value'].size
    with open(outfile, 'w') as csv_file:
        #Set Header
        fieldnames = ['time_utc', 'longitude', 'latitude', 'qa_value']
        fieldnames.extend(optkeys)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #Write data
        for i in range(nsize):
            dict_tmp = {}
            dict_tmp['time_utc' ] = dict1['time_utc' ][i]
            dict_tmp['longitude'] = dict1['longitude'][i]
            dict_tmp['latitude' ] = dict1['latitude' ][i]
            dict_tmp['qa_value' ] = dict1['qa_value' ][i]
            for j in range(len(optkeys)):
                dict_tmp[optkeys[j]] = dict1[optkeys[j]][i]
            #
            writer.writerow(dict_tmp)
"""


"""
#Load file
csv_file = resdir + 'matset0_comparison_w-a_test'+tnum+'.csv'
f0  = np.loadtxt(csv_file, delimiter=',', skiprows=1)
"""

def extract_s5p_csv(flist, outfile, lim_ll):
    #Extraxt Header
    with open(flist[0], 'r') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        f.close()
    #Write csv file
    with open(outfile, 'w') as csv_file:
        #Set Header
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #Load contents
        for infile in flist:
            f0 = np.loadtxt(infile, delimiter=',', skiprows=1)
            if f0.size > 0:
                cd_ll = np.where( (f0[:,1]>lim_ll[0]) & (f0[:,1]<lim_ll[1]) & (f0[:,2]>lim_ll[2]) & (f0[:,2]<lim_ll[3]) )[0]
                if cd_ll.size > 0:
                    fname   = infile.split('/')[-1].split('.nc')[0]
                    print('Extracted '+fname)
                    for i in range(cd_ll.size):
                        dict_tmp = {}
                        for j in range(len(fieldnames)):
                            dict_tmp[fieldnames[j]] = f0[cd_ll[i], j]
                        #
                        writer.writerow(dict_tmp)

#Support part--------------------------------------------------------
"""
def tconv_str2float(inp):
    res = np.zeros(inp.shape)
    for i in range(inp.shape[0]):
        for j in range(inp.shape[1]):
            time_tmp = inp[i,j]
            res[i,j] = float(time_tmp[0:4]+time_tmp[5:7]+time_tmp[8:10]+time_tmp[11:13]+time_tmp[14:16]+time_tmp[17:19])
    #
    return res
"""





