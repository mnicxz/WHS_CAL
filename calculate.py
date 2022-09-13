from datetime import datetime
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


def allin1csv(wear_path, polar_path, gps_path, inputcsv):

    whs = pd.DataFrame()
    whs_log = logging.getLogger('log')
    try:
        if len(wear_path) != 0:
            # print(wear_path,'is not null')
            whs_log.info('WHS PATH is not null')
            wear_tp = whs_tcx2csv(wear_path)
            wear = pd.DataFrame(wear_tp)
        else:
            whs_log.info('WHS PATH is null')
        whs = pd.concat([whs, wear], axis=1)
        # if inputcsv:
        #     filepath=wear_path[0:-28]
        # filename=filepath+'Wear_{}.csv'.format(datetime.strftime(timezone_change(wear['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
        # wear.to_csv(filename)
    except:
        whs_log.info('WHS PATH is not available')
        wear_path = ''

    try:
        if len(polar_path) != 0:
            dic['log'].append('POLAR PATH is not null')
            tmphr = {'PolarTime': [], 'PolarHR': []}
            k = 0
            polar_tp = polar_tcx2csv(polar_path)
            polar = pd.DataFrame(polar_tp)

            for i in range(len(whs['Time'])):
                for j in range(k, len(polar['Time'])):
                    if wear['Time'][i] == polar['Time'][j]:
                        tmphr['PolarTime'].append(polar['Time'][j])
                        tmphr['PolarHR'].append(polar['HeartRateBpm'][j])
                        k = j+1
                        break
                    # 若遍历完后无匹配项，则添加空值
                    elif j+1 == len(polar['Time']):
                        tmphr['PolarTime'].append('')
                        tmphr['PolarHR'].append('')
            tmp_hr = pd.DataFrame(tmphr)
            whs = pd.concat([whs, tmp_hr], axis=1)
            # if inputcsv:
            #     filename=filepath+'HR_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
            #     tmp_hr.to_csv(filename)
        else:
            dic['log'].append('POLAR PATH is null')
    except:
        dic['log'].append('POLAR PATH is not available')
        polar_path = ''

    try:
        if len(gps_path) != 0:
            dic['log'].append('GPS PATH is not null')
            if len(gps_path) != 0:
                tmpgps = {'GPSTime': [], 'GPSLat': [], 'GPSLon': []}
                n = 0
                gps_tp = gpx2csv(gps_path)
                gps = pd.DataFrame(gps_tp)

                for i in range(len(whs['Time'])):
                    for m in range(n, len(gps['Time'])):
                        if whs['Time'][i] == gps['Time'][m]:
                            tmpgps['GPSTime'].append(gps['Time'][m])
                            tmpgps['GPSLat'].append(gps['Lat'][m])
                            tmpgps['GPSLon'].append(gps['Lon'][m])
                            n = m+1
                            break
                        # 若遍历完后无匹配项，则添加空值
                        elif m+1 == len(gps['Time']):
                            tmpgps['GPSTime'].append('')
                            tmpgps['GPSLat'].append('')
                            tmpgps['GPSLon'].append('')
                tmp_gps = pd.DataFrame(tmpgps)
                whs = pd.concat([whs, tmp_gps], axis=1)
                # if inputcsv:
                #     filename=filepath+'GPS_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
                #     tmp_gps.to_csv(filename)
        else:
            dic['log'].append('GPS PATH is null')
    except:
        dic['log'].append('GPS PATH is not available')
        gps_path = ''

    if inputcsv:
        # filepath=wear_path[0:-28]
        # filepath='D:\\chenchen2\\桌面\\1\\'
        # filename=filepath+'WHS_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
        filename = 'WHS_{}.csv'.format(datetime.strftime(
            timezone_change(whs['Time'][0]), "%Y-%m-%d_%H-%M-%S"))
        whs.to_csv(filename)
    return whs

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
                    gps_start_time = datetime.strptime(
                        whs['Time'][k], "%Y-%m-%d %H:%M:%S")
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
            if datetime.strptime(whs['Time'][j], "%Y-%m-%d %H:%M:%S") < hr_start_time:
                dic['hr_ae'].append('')
                dic['hr_ape'].append('')
            else:
                # polar hr 为0时异常处理
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
        sumd = 0
        # global gps_start_time
        for l in range(len(whs)-1):
            if datetime.strptime(whs['Time'][l], "%Y-%m-%d %H:%M:%S") < gps_start_time:
                dic['gps_ae'].append('')
            else:
                distance = getDistance(float(whs['GPSLat'][l]), float(whs['GPSLon'][l]), float(whs['GPSLat'][l+1]), float(whs['GPSLon'][l+1]))
                sumd = sumd+distance
                lap=getDistance(float(whs['LatitudeDegrees'][l]), float(whs['LongitudeDegrees'][l]), float(whs['GPSLat'][l]), float(whs['GPSLon'][l]))
                dic['gps_ae'].append(lap)    
        dic['gt_dis'] = sumd
        dic['gps_ape'].append(abs(dut_dis-sumd)/sumd)
        dic['gps_ae'].append(getDistance(float(whs['LatitudeDegrees'][l+1]), float(whs['LongitudeDegrees'][l+1]), float(whs['GPSLat'][l+1]), float(whs['GPSLon'][l+1])))
    
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
