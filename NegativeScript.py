import numpy as np
import pandas as pd
import os
import math
import sys


def min_result(list1, n):
    temp = list1
    result = list1
    window = 1
    for iter in range(n):
        temp = np.fmin(temp[0:(np.size(temp)-window)], temp[window:])
        result = np.concatenate((result, temp))
        window = window * 2
    return result


def max_result(list1, n):
    temp = list1
    result = list1
    window = 1
    for iter in range(n):
        temp = np.fmax(temp[0:(np.size(temp)-window)], temp[window:])
        result = np.concatenate((result, temp))
        window = window * 2
    return result

# list1, list2 are the average of the first and second moments of the datapoints
def avg_sd_result(list1, list2, list3, n):
    temp1 = list1
    temp2 = list2
    temp3 = list3
    result1 = temp1
    result2 = temp2
    window = 1
    for iter in range(n):
        temp1 = temp1 * temp3
        temp2 = temp2 * temp3
        temp1 = np.nansum(np.array([temp1[0:(np.size(temp1)-window)], temp1[window:]]), axis = 0)
        temp2 = np.nansum(np.array([temp2[0:(np.size(temp2)-window)], temp2[window:]]), axis = 0)
        temp3 = np.nansum(np.array([temp3[0:(np.size(temp3)-window)], temp3[window:]]), axis = 0)
        temp4 = np.fmax(temp3, 1)
        temp1 = temp1/temp4
        temp2 = temp2/temp4
        result1 = np.concatenate((result1, temp1))
        result2 = np.concatenate((result2, temp2))
        window = window * 2
    result2 = np.sqrt(result2 - np.square(result1))
    return np.concatenate((result1, result2))


def min_max_avg_sd(stats, n):
    result_min = min_result(stats[:, 0], n)
    result_max = max_result(stats[:, 1], n)
    # result_avg_sd = avg_sd_result(stats[:, 2], np.square(stats[:, 2]) + np.square(stats[:, 3]), n)
    result_avg_sd = avg_sd_result(stats[:, 2], np.square(stats[:, 2]) + np.square(stats[:, 3]) * (1-1/np.fmax(1, stats[:, 4])), stats[:, 4], n)
    return np.concatenate((result_min, result_max, result_avg_sd))



def col_ref_matrix(n):
    window = 1
    result1 = range(n)
    result2 = range(n)
    size = n
    for iter in range(math.floor(math.log(n, 2))):
        size = size - window
        result1 = np.concatenate((result1, range(0, size)))
        result2 = np.concatenate((result2, range(n-size, n)))
        window = window * 2
    return np.vstack((result1, result2))




def ParseNegatives(directory,filename):

    dfOrig2 = pd.read_csv(directory+filename,
                     parse_dates=[['Date','Time']], delimiter='\t')
    dfOrig2['Date_Time'] = pd.to_datetime(dfOrig2['Date_Time'], format='%d.%m.%Y %H:%M:%S', coerce=True)
    dfOrig2 = dfOrig2.dropna(subset=['Date_Time'])

    #Only select the columns we care about
    dfSubset = dfOrig2[['Date_Time', 'Operating_status:_Error_Locking', 'Operating_status:_Error_Blocking',
                   'Actual_Power', 'Number_of_burner_starts', 'Operating_status:_Central_heating_active',
                  'Operating_status:_Hot_water_active', 'Operating_status:_Flame', 'Relay_status:_Gasvalve',
                  'Relay_status:_Fan', 'Relay_status:_Ignition', 'Relay_status:_internal_3-way-valve',
                  'Relay_status:_HW_circulation_pump', 'Supply_temperature_(primary_flow_temperature)',
                  'Maximum_supply_(primary_flow)_temperature', 'Hot_water_temperature_setpoint', 
                  'Hot_water_outlet_temperature', 'Actual_flow_rate_turbine', 'Fan_speed']]
    
    #Fill in missing entries
    df = dfSubset.fillna(method = 'ffill')
    
    print "Successfully loaded:", directory + filename

                
    #Find number of samples
    numLines = int( os.popen('wc -l ' + directory + filename).read().split()[0])

    #1,000,000 / 2,242,549,616
    numSamples = max(np.random.binomial(numLines, 0.00044592101457433261088659),1)




    sensorList = ['Actual_Power', 'Number_of_burner_starts', 'Operating_status:_Central_heating_active',
                  'Operating_status:_Hot_water_active', 'Operating_status:_Flame', 'Relay_status:_Gasvalve',
                  'Relay_status:_Fan', 'Relay_status:_Ignition', 'Relay_status:_internal_3-way-valve',
                  'Relay_status:_HW_circulation_pump', 'Supply_temperature_(primary_flow_temperature)',
                  'Maximum_supply_(primary_flow)_temperature', 'Hot_water_temperature_setpoint', 
                  'Hot_water_outlet_temperature', 'Actual_flow_rate_turbine', 'Fan_speed'] 


    Negative_result = np.zeros((numSamples, 4388 * len(sensorList))) 
    outer_iter = 0
    
    startDataTime = df.ix[1]['Date_Time'] #Since ix is one-based...
    for i in range(numSamples):

        #Pick a random row
        rowNum = np.random.randint(1, numLines)
        row  = df.ix[rowNum+1]

        #Keep re-picking random rows until conditions are met
        while (True):

            eventTime = row['Date_Time']
            startTime = eventTime - pd.Timedelta('7 days')
            dfPos = df[(df['Date_Time'] >= startTime) & (df['Date_Time'] <= eventTime)]

            sumErrLock = dfPos['Operating_status:_Error_Locking'].sum()

            if ((startTime > startDataTime) and sumErrLock <= 0):
                break

            else:
                rowNum = np.random.randint(1, numLines)
                row  = df.ix[rowNum]

        #For each Negative example...
        eventTime = row['Date_Time']
        startTime = eventTime - pd.Timedelta('7 days')
        dfPos = df[(df['Date_Time'] >= startTime) & (df['Date_Time'] < eventTime)]
        
        d = {}
        for sensor in sensorList:
            d["rawData_"+sensor] = np.zeros((168,5))
        
        for j in range(168):

            lastTime = startTime + j*pd.Timedelta('1 hour')
            currTime = startTime + (j+1)*pd.Timedelta('1 hour')

            dfHourly = dfPos[(dfPos['Date_Time'] >= lastTime) & (dfPos['Date_Time'] < currTime)]

            for sensor in sensorList:
                
                description = dfHourly[sensor].describe()
                d["rawData_"+sensor][j,0] = description['min']
                d["rawData_"+sensor][j,1] = description['max']
                d["rawData_"+sensor][j,2] = description['mean']
                d["rawData_"+sensor][j,3] = description['std']
                d["rawData_"+sensor][j,4] = description['count']

        inner_iter = 0
        for sensor in sensorList:
            Negative_result[outer_iter, (inner_iter * 4388):(inner_iter+1)*4388] = min_max_avg_sd(d["rawData_"+sensor], 7)    
            inner_iter = inner_iter + 1
            
        outer_iter = outer_iter + 1

        
    with open('NegativeData/NegativeExamples_'+file+'.txt','a') as f_handle:
        np.savetxt(f_handle,Negative_result, fmt='%1.3e')


def main(argv):

    np.random.seed(0)
    print "Starting", argv[0]
    for filename in os.listdir(argv[0]):
        parseFile = argv[0] + filename
        if (os.stat(parseFile).st_size > 0):
            ParseNegatives(argv[0],filename)

    # ParseNegatives('/dfs/scratch0/bosch/BG-Data_Part11/', '2029718103746674690.csv')



if __name__ == "__main__":
    main(sys.argv[1:])
