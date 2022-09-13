from datetime import datetime
from lxml import etree
import pandas as pd

NSMAP={"tcd":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}


def polar_tcx2csv(path):
    trackpoint = {'Time': [],  'HeartRateBpm': []}

    polar=etree.parse(path)
    root=polar.getroot()

    # trackpoint
    for tp in root.xpath('.//tcd:Trackpoint',namespaces=NSMAP):
        # Time
        for ti in tp.xpath('.//tcd:Time',namespaces=NSMAP):
            trackpoint['Time'].append(datetime.strptime(ti.text[0:-5], "%Y-%m-%dT%H:%M:%S"))
        # HeartRateBpm, Polar心率消失时赋0处理
        if len(tp.xpath('.//tcd:Value',namespaces=NSMAP)) == 0:
            trackpoint['HeartRateBpm'].append(0)
        else:
            for hr in tp.xpath('.//tcd:Value',namespaces=NSMAP):
                trackpoint['HeartRateBpm'].append(int(hr.text))
            pass
    
    return trackpoint


if __name__ == '__main__':
    path = 'D:\\chenchen2\\桌面\\Tester10-zj-female-Fitzpatrick Type II-BMI Normal\\户外快跑\\Lct_3_2022-08-15_20-02-34.TCX'
    trackpoint=polar_tcx2csv(path)
    polar=pd.DataFrame(trackpoint)
    # print("tcx数据如下:\n", polar)
    # polar.to_csv('hr.csv')
    pass
