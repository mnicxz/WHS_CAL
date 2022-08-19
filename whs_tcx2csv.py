from datetime import datetime
# from sqlite3 import Time
from lxml import etree
import pandas as pd



# xml=''

# WHS为Zulu time，与对比数据比较需要切换时区
# 时区有时不为整数，导致计算出错
def timezone_change(time):
    local_time = datetime.now()
    utc_time = datetime.utcnow()
    tmp = local_time-utc_time
    # print(type(tmp))
    # freq='1min'
    # tmp=
    # print(tmp)
    

    tmp_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    start_time = tmp_time+tmp
    # print(time,type(time))
    # local_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_time
    pass


# 获取WHS运动开始时间
def whs_start_time(path):
    tcx = etree.parse(path)
    root = tcx.getroot()

    # 运动开始时间 root[0][0][0]
    start_time = datetime.strptime(root[0][0][0].text[0:-5], "%Y-%m-%dT%H:%M:%S")
    
    return start_time

def whs_tcx2csv(path):

    trackpoint = {'Time': [], 'LatitudeDegrees': [], 'LongitudeDegrees': [], 'AltitudeMeters': [
], 'DistanceMeters': [], 'HeartRateBpm': [], 'Steps': [], 'ElevationGainMeters': []}

    tcx = etree.parse(path)
    root = tcx.getroot()

    # 运动开始时间 root[0][0][0]
    start_time = datetime.strptime(root[0][0][0].text[0:-5], "%Y-%m-%dT%H:%M:%S")
    # local_time = timezone_change(start_time)
    # print(start_time)

    # 运动trackpoint
    for tp in root[0][0][1][0]:
        # # print('+++++++++++++WHS Trackpoint++++++++++++')
        # # Time tp[0]
        # # LatitudeDegrees tp[1][0]
        # # LongitudeDegrees tp[1][1]
        # # AltitudeMeters tp[2]
        # # DistanceMeters tp[3]
        # # HeartRateBpm tp[4][0]
        # hr = tp[4][0].text
        # bpm=int(hr[0:-2])
        # print('心率值：',bpm)
        # # Steps tp[5]
        # # ElevationGainMeters tp[6]
        tp_time = datetime.strptime(tp[0].text[0:-1], "%Y-%m-%dT%H:%M:%S")
        if tp_time >= start_time:
            trackpoint['Time'].append(tp_time)
            trackpoint['LatitudeDegrees'].append(float(tp[1][0].text))
            trackpoint['LongitudeDegrees'].append(float(tp[1][1].text))
            trackpoint['AltitudeMeters'].append(tp[2].text)
            trackpoint['DistanceMeters'].append(tp[3].text)
            trackpoint['HeartRateBpm'].append(int(float(tp[4][0].text)))
            trackpoint['Steps'].append(tp[5].text)
            trackpoint['ElevationGainMeters'].append(tp[6].text)
        pass
    # print(trackpoint['HeartRateBpm'])
    return trackpoint


if __name__ == '__main__':
    path = 'D:\\桌面\\Running\\2022-08-15T13_31_47.276Z.tcx'
    print("开始时间：", whs_start_time(path))
    trackpoint = whs_tcx2csv(path)
    whs = pd.DataFrame(trackpoint)
    print("tcx数据如下:\n", whs)
    # whs.to_csv('site.csv')
