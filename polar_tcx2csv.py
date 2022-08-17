from datetime import datetime
from lxml import etree
# from whs_tcx2csv import timezone_change
import pandas as pd

trackpoint = {'Time': [],  'HeartRateBpm': []}


def polar_tcx2csv(path):
    trackpoint = {'Time': [],  'HeartRateBpm': []}

    polar=etree.parse(path)
    root=polar.getroot()
    # for node in root.getchildren():
    #     print(node)
    for tp in root[0][0][1][7]:
        # tmp_time = datetime.strptime(tp[0].text[0:-5], "%Y-%m-%dT%H:%M:%S")
        trackpoint['Time'].append(datetime.strptime(tp[0].text[0:-5], "%Y-%m-%dT%H:%M:%S"))
        trackpoint['HeartRateBpm'].append(int(tp[1][0].text))
        # print(tp[0].text)
        # print(tp)
    return trackpoint
    pass


if __name__ == '__main__':
    path = 'D:\\chenchen2\\桌面\\力量训练\\Lct_3_2022-08-11_16-25-11.tcx'
    trackpoint=polar_tcx2csv(path)
    polar=pd.DataFrame(trackpoint)
    print("tcx数据如下:\n", polar)
    # polar.to_csv('hr.csv')
    pass
