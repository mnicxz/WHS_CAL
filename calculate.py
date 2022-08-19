
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

    tmp = {'PolarHR':[]}
    k,t = 0,0
    for i in range(len(whs['Time'])):
        for j in range(k,len(polar['Time'])):
            if whs['Time'][i] == polar['Time'][j]:
                tmp['PolarHR'].append(polar['HeartRateBpm'][j])
                t=j
                k = j+1
                break
    
    pt=pd.DataFrame(tmp)
    # print(pt)
    
    csv=pd.concat([whs,pt],axis=1)
    # print(type(csv['PolarHR'][614]))
    return csv

def cal(whs):
    hr_lap=[]
    sum_lap,sum_ape=0,0
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


    return dic


if __name__ == '__main__':

    whs_path = 'D:\\室内跑步\\2022-08-16T02_53_22.373Z.tcx'
    polar_path = 'D:\\室内跑步\\Lct_3_2022-08-16_10-53-05.TCX'

    whs=allin1csv(whs_path, polar_path)
    print(cal(whs))
    pass
