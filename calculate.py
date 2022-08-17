
from datetime import datetime
from whs_tcx2csv import whs_tcx2csv
from polar_tcx2csv import polar_tcx2csv

import pandas as pd

dic={'hr_lock_time':0,'hr_ae':0,'hr_ape':0,'gps_lock_time':0,'gps_ae':0,'gps_ape':0,'whs_steps':0,'whs_dis':0}

def timezone_change(time):
    local_time = datetime.now()
    utc_time = datetime.utcnow()
    tmp = local_time-utc_time

    start_time=tmp+time
    return start_time

def allin1csv(whs_path, polar_path):
    whs_tp = whs_tcx2csv(whs_path)
    polar_tp = polar_tcx2csv(polar_path)

    whs = pd.DataFrame(whs_tp)
    polar = pd.DataFrame(polar_tp)

    # print(whs['Time'][1])k
    tmp = []
    k = 0
    for i in range(len(whs['Time'])):
        # print("whs['Time']:",whs['Time'][i])
        # tmp.append('NaN')
        for j in range(len(polar['Time'])-k):
            j=j+k
            # print("polar['Time']:",polar['Time'][j])
            if whs['Time'][i] == polar['Time'][j]:
                # tmp[i] = polar['HeartRateBpm'][j]
                tmp.append(polar['HeartRateBpm'][j])
                k = j+1
                break
    # print(len(tmp))
    whs.insert(8, 'PolarHR', tmp)
    # print(whs)

    # filename='WHS_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
    # # print(whs)
    # whs.to_csv(filename)
    return whs
    pass

def cal(whs):
    hr_lap=[]
    sum_lap,sum_ape=0,0
    # HR Lock Time
    for i in range(len(whs)):
        if whs['HeartRateBpm'][i] != 0:
            # print('HR Lock Time:', i)
            # hr.append(i)
            dic['hr_lock_time']=i
            break

    # HR AE & APE
    for j in range(len(whs)-i):
        # polar hr 为0时异常处理
        if whs['PolarHR'][j+i] != 0:    
        # if whs['HeartRateBpm'][j+i] !='NaN' | whs['HeartRateBpm'][j+i] !='NaN':
            hr_ae=abs(int(whs['HeartRateBpm'][j+i])-int(whs['PolarHR'][j+i]))
            hr_lap.append(hr_ae)
            sum_lap=sum_lap+hr_ae
            hr_ape=hr_ae/whs['PolarHR'][j+i]
            sum_ape=sum_ape+hr_ape
        pass
    # print("HR AE:", sum_lap/len(hr_lap))
    # print("HR APE:{:.2%}".format(sum_ape/len(hr_lap)))
    dic['hr_ae']='{:.2}'.format(sum_lap/len(hr_lap))
    dic['hr_ape']='{:.2%}'.format(sum_ape/len(hr_lap))
    # hr.append(sum_lap/len(hr_lap))
    # hr.append('{:.2%}'.format(sum_ape/len(hr_lap)))

    # GPS Lock Time
    for i in range(len(whs)):
        if whs['LongitudeDegrees'][i] != 0:
            # print('HR Lock Time:', i)
            # hr.append(i)
            dic['gps_lock_time']=i
            break

    # WHS STEPS
    dic['whs_steps']=int(whs['Steps'][len(whs['Steps'])-1])

    # WHS DISTANCES
    dic['whs_dis']=float(whs['DistanceMeters'][len(whs['DistanceMeters'])-1])


    return dic


if __name__ == '__main__':

    whs_path = 'D:\\chenchen2\\桌面\\力量训练\\2022-08-11T08_25_16.445Z.tcx'
    polar_path = 'D:\\chenchen2\\桌面\\力量训练\\Lct_3_2022-08-11_16-25-11.tcx'

    whs=allin1csv(whs_path, polar_path)
    print(cal(whs))
    # whs.to_csv('site.csv')
    pass
