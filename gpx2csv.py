from scipy.spatial.distance import cdist
import pandas as pd
from math import radians,tan,atan,sin,asin,cos,acos
import gpxpy

def gpx2csv(path):
    trackpoint = {'Time': [],  'Lat': [], 'Lon': []}
    gpx_file=open(path,'r')
    gpx=gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # print(point.time.replace(tzinfo=None))
                trackpoint['Time'].append(point.time.replace(tzinfo=None))
                trackpoint['Lat'].append(point.latitude)
                trackpoint['Lon'].append(point.longitude)
    return trackpoint

def cal_dis(lat1,lon1,lat2,lon2):
    point1=[[lat1,lon1]]
    point2=[[lat2,lon2]]
    # print(point1,point2)
    dis=cdist(point1,point2,metric='euclidean')
    return dis

def getDistance(latA, lonA, latB, lonB):
    # if latA == latB and lonA == lonB:
    #     distance=0
    # else:
    try:
        ra = 6378140 # radius of equator: meter
        rb = 6356755 # radius of polar: meter
        flatten = (ra - rb) / ra # Partial rate of the earth
        # change angle to radians
        radLatA = radians(latA)
        radLonA = radians(lonA)
        radLatB = radians(latB)
        radLonB = radians(lonB)
        
        pA = atan(rb / ra * tan(radLatA))
        pB = atan(rb / ra * tan(radLatB))
        x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
        c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
        c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (x + dr)
    except:
        distance=0
    return distance

if __name__ == '__main__':
    # path = 'D:\\chenchen2\\桌面\\2\\Run\\WHS_2022-09-07_20-03-02.csv'
    sum,suma=0,0
    # trackpoint=gpx2csv(path)
    # gps=pd.DataFrame(trackpoint)
    # # print("tcx数据如下:\n", polar)
    # # polar.to_csv('hr.csv')
    # for i in range(len(gps)-1):
    #     # dis=cal_dis(gps['Lat'][i],gps['Lon'][i],gps['Lat'][i+1],gps['Lon'][i+1])
    #     # sum=sum+dis*100000
    #     distance=getDistance(gps['Lat'][i],gps['Lon'][i],gps['Lat'][i+1],gps['Lon'][i+1])
    #     suma=suma+distance
    #     print('%f' % sum[0][0], suma)
    # print('*'*50)

    whs_path='D:\\chenchen2\\桌面\\2\\Run\\WHS_2022-09-07_20-03-04.csv'
    data=pd.read_csv(whs_path)
    tmp={'Lap':[]}
    # for i in range(len(data['Time'])):
    #     if(data['LatitudeDegrees'][i] == 0):
    #         tmp['Lap'].append('')
    #     else:
    #         print(data['LatitudeDegrees'][i],data['LongitudeDegrees'][i],data['GPSLat'][i],data['GPSLon'][i])
    #         tmp['Lap'].append(getDistance(data['LatitudeDegrees'][i],data['LongitudeDegrees'][i],data['GPSLat'][i],data['GPSLon'][i]))
    # # print(tmp['Lap'])
    # data=pd.concat([data,pd.DataFrame(tmp['Lap'])],axis=1)
    # data.to_csv('bbb.csv')

    for i in range(len(data['Time'])-1):
        if(data['LatitudeDegrees'][i] != 0):
            distance=getDistance(data['GPSLat'][i],data['GPSLon'][i],data['GPSLat'][i+1],data['GPSLon'][i+1])
            suma=suma+distance
            print(suma)
    pass