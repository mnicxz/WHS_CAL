from datetime import datetime
from lxml import etree
import pandas as pd

NSMAP={"tcd":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}


def polar_tcx2csv(path):
    trackpoint = {'Time': [],  'HeartRateBpm': []}
    i=2

    polar=etree.parse(path)
    root=polar.getroot()

    # Time
    for ti in root.xpath('.//tcd:Time',namespaces=NSMAP):
        trackpoint['Time'].append(datetime.strptime(ti.text[0:-5], "%Y-%m-%dT%H:%M:%S"))
    # 前两个Value值为平均心率及最大心率，需要去除
    for hr in root.xpath('.//tcd:Value',namespaces=NSMAP):
        if i ==0:
            trackpoint['HeartRateBpm'].append(int(hr.text))
        else:
            i=i-1
        # print(hr.text)
    return trackpoint
    pass


if __name__ == '__main__':
    path = 'D:\\桌面\\20 xyw\\running\\Lct_1_2022-08-17_16-28-11.TCX'
    trackpoint=polar_tcx2csv(path)
    polar=pd.DataFrame(trackpoint)
    # print("tcx数据如下:\n", polar)
    # polar.to_csv('hr.csv')
    pass
