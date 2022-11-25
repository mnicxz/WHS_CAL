from cmath import isnan
from datetime import datetime
from math import dist
from whs_tcx2csv import whs_tcx2csv
from polar_tcx2csv import polar_tcx2csv
from gpx2csv import gpx2csv, getDistance

import pandas as pd
import logging

dic = {'start_time': 0, 'end_time': 0, 'hr_start_time': 0, 'hr_lock_time': [], 'hr_ae': [], 'hr_ape': [],
       'gps_start_time': 0, 'gps_lock_time': [], 'gps_ae': [], 'gps_ape': [], 'dut_steps': 0, 'steps_ape': [], 'dut_dis': 0, 'gt_dis': 0, 'gt_steps': 0}


def timezone_change(time):
    local_time = datetime.now()
    utc_time = datetime.utcnow()
    tmp = local_time-utc_time

    start_time = tmp+time
    return start_time

def cal1(whs):
    hr_lap=[]
    sum_lap,sum_ape,sumd,suml=0,0,0,0
    # HR Lock Time
    for i in range(len(whs)):
        if whs['HeartRateBpm'][i] != 0:
            dic['hr_lock_time']=whs['Time'][i]-whs["Time"][0]
            break

    # HR AE & APE
    for j in range(i,len(whs)):
        # 在whs和polar都有数据时取值计算
        if not pd.isna(whs['HeartRateBpm'][j]) and not pd.isna(whs['PolarHR'][j]):
            # polar hr 为0时异常处理
            if int(whs['PolarHR'][j]) != 0:    
                hr_ae=abs(int(whs['HeartRateBpm'][j])-int(whs['PolarHR'][j]))
                hr_lap.append(hr_ae)
                sum_lap=sum_lap+hr_ae
                hr_ape=hr_ae/whs['PolarHR'][j]
                sum_ape=sum_ape+hr_ape
            pass
    # print("HR AE:", sum_lap/len(hr_lap))
    # print("HR APE:{:.2%}".format(sum_ape/len(hr_lap)))
    dic['hr_ae']=round(sum_lap/len(hr_lap),2)
    dic['hr_ape']='{:.2%}'.format(sum_ape/len(hr_lap))

    # GPS Lock Time
    for k in range(len(whs)):
        if whs['LatitudeDegrees'][k] != 0:
            dic['gps_lock_time']=whs['Time'][k]-whs["Time"][0]
            break

    # WHS STEPS
    dic['whs_steps']=int(whs['Steps'][len(whs['Steps'])-1])

    # WHS DISTANCES
    dic['whs_dis']=float(whs['DistanceMeters'][len(whs['DistanceMeters'])-1])
    for l in range(k,len(whs)-1):
        distance = getDistance(float(whs['GPSLat'][l]), float(whs['GPSLon'][l]), float(whs['GPSLat'][l+1]), float(whs['GPSLon'][l+1]))
        sumd = sumd+distance
        lap=getDistance(float(whs['LatitudeDegrees'][l]), float(whs['LongitudeDegrees'][l]), float(whs['GPSLat'][l]), float(whs['GPSLon'][l]))
        # dic['gps_ae'].append(lap)    
    dic['gt_dis'] = sumd
    dic['gps_ape'] = abs(dic['whs_dis']-sumd)/sumd
    # dic['gps_ae']=getDistance(float(whs['LatitudeDegrees'][l+1]), float(whs['LongitudeDegrees'][l+1]), float(whs['GPSLat'][l+1]), float(whs['GPSLon'][l+1]))


    return dic

def cal2(whs):

    if 'Time' in whs.columns:
        # WEAR START TIME
        start_time = datetime.strptime(whs['Time'][0], "%Y-%m-%d %H:%M:%S")
        dic['start_time'] = start_time

        # WEAR END TIME
        end_time = datetime.strptime(
            whs['Time'][len(whs['Time'])-1], "%Y-%m-%d %H:%M:%S")
        dic['end_time'] = end_time

        # WHS HR Lock Time
        for i in range(len(whs)):
            if whs['HeartRateBpm'][i] != 0:
                hr_start_time = datetime.strptime(
                    whs['Time'][i], "%Y-%m-%d %H:%M:%S")
                dic['hr_start_time'] = hr_start_time
                dic['hr_lock_time'].append(hr_start_time-start_time)
                break

        # WHS GPS Lock Time
        for k in range(len(whs)):
            if whs['LatitudeDegrees'][k] != 0:
                gps_start_time = datetime.strptime(whs['Time'][k], "%Y-%m-%d %H:%M:%S")
                dic['gps_start_time'] = gps_start_time
                print(dic['gps_start_time'],type(dic['gps_start_time']))
                print(gps_start_time,type(gps_start_time))
                dic['gps_lock_time'].append(gps_start_time-start_time)
                break

        # WHS STEPS
        dut_steps = int(whs['Steps'][len(whs['Steps'])-1])
        dic['dut_steps'] = dut_steps

        # WHS DISTANCES
        dut_dis = float(whs['DistanceMeters'][len(whs['DistanceMeters'])-1])
        dic['dut_dis'] = dut_dis

    # HR AE & APE
    # print(len(polar_path))
    if 'PolarHR' in whs.columns:
        for j in range(len(whs)):
            # dut和polar都有数据且不为0时取值计算,即在dut获取到心率后开始取值计算
            if datetime.strptime(whs['Time'][j], "%Y-%m-%d %H:%M:%S") < hr_start_time or pd.isna(whs['HeartRateBpm'][j]) or pd.isna(whs['PolarHR'][j]):
                dic['hr_ae'].append('')
                dic['hr_ape'].append('')
            else:
                # polar hr 为0时异常处理、polar hr无数据
                if int(whs['PolarHR'][j]) != 0:
                    hr_ae = abs(int(whs['HeartRateBpm'][j]) - int(whs['PolarHR'][j]))
                    dic['hr_ae'].append(hr_ae)
                    dic['hr_ape'].append(hr_ae/int(whs['PolarHR'][j]))
                    # sum_lap = sum_lap+hr_ae
                    # hr_ape = hr_ae/whs['PolarHR'][j]
                    # sum_ape = sum_ape+hr_ape
                else:
                    dic['hr_ae'].append('')
                    dic['hr_ape'].append('')
                # pass
        # print("HR AE:", sum_lap/len(hr_lap))
        # print("HR APE:{:.2%}".format(sum_ape/len(hr_lap)))
        # dic['hr_ae'] = round(sum_lap/len(hr_lap), 2)
        # dic['hr_ape'] = '{:.2%}'.format(sum_ape/len(hr_lap))

    # GPS distance APE、Track Accuracy AE
    if 'GPSLat' in whs.columns:        
        for m in range(len(whs)):
            if datetime.strptime(whs['Time'][m], "%Y-%m-%d %H:%M:%S") < gps_start_time:
                dic['gps_ae'].append('')
            else:
                lap=getDistance(float(whs['LatitudeDegrees'][m]), float(whs['LongitudeDegrees'][m]), float(whs['GPSLat'][m]), float(whs['GPSLon'][m]))
                dic['gps_ae'].append(lap)    
    
    # Steps
    if 'ActiTime' in whs.columns:
        dic['gt_steps']=whs['ActiSteps'].sum()
        dic['steps_ape']=abs(dic['gt_steps']-dic['dut_steps'])/dic['gt_steps']

    return dic

if __name__ == '__main__':
    gps_path = 'D:\\chenchen2\\桌面\\test\\WHS_2022-09-09_11-10-45.csv'

    # whs = allin1csv(wear_path, polar_path, gps_path, True)
    whs=pd.read_csv(gps_path)
    print(cal2(whs))
    # whs.to_csv('test.csv')
    pass
