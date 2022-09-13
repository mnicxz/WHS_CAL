import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import shapely.geometry as sgeom
import pandas as pd

def draw_hr(data):
    plt.clf()
    x=data['Time']
    plt.xticks(rotation=45)
    plt.plot(x,data['HeartRateBpm'],label='Wear',color='b')
    plt.plot(x,data['PolarHR'],label='Polar',color='r')
    plt.legend(loc='best')
    # plt.title('HR对比折线图')#matplotlib不支持中文
    plt.show()
    pass

def draw_gps(data):
    min_lon,max_lon,min_lat,max_lat=180.0,0.0,90.0,0.0
    for i in range(len(data['Time'])-1):
        if(data['LatitudeDegrees'][i] != 0):
            if min_lon > data['LongitudeDegrees'][i]: min_lon=data['LongitudeDegrees'][i]
            if max_lon < data['LongitudeDegrees'][i]: max_lon=data['LongitudeDegrees'][i]
            if min_lat > data['LatitudeDegrees'][i]: min_lat=data['LatitudeDegrees'][i]
            if max_lat < data['LatitudeDegrees'][i]: max_lat=data['LatitudeDegrees'][i]
    # print(min_lon,max_lon,min_lat,max_lat)
    min_lon=round(min_lon-0.001,3)
    max_lon=round(max_lon+0.001,3)
    min_lat=round(min_lat-0.001,3)
    max_lat=round(max_lat+0.001,3)
    # print(min_lon,max_lon,min_lat,max_lat)
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([min_lon,max_lon,min_lat,max_lat], crs=ccrs.PlateCarree())

    # ax.add_feature(cfeature.LAND)
    # ax.add_feature(cfeature.OCEAN)
    # ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.RIVERS)
    # ax.add_feature(cfeature.LAKES, alpha=0.5)
 
    for i in range(len(data['Time'])-1):
        if(data['LatitudeDegrees'][i] != 0):
            point_1=data['LongitudeDegrees'][i],data['LatitudeDegrees'][i]
            point_2=data['LongitudeDegrees'][i+1],data['LatitudeDegrees'][i+1]
            ax.add_geometries([sgeom.LineString([point_1,point_2])],crs=ccrs.PlateCarree(),edgecolor='red')
            if 'GPSLat' in data.columns:
                point_3=data['GPSLon'][i],data['GPSLat'][i]
                point_4=data['GPSLon'][i+1],data['GPSLat'][i+1]
                ax.add_geometries([sgeom.LineString([point_3,point_4])],crs=ccrs.PlateCarree(),edgecolor='blue')
    plt.title('Wear-Red, Bad Elf-Blue')
    plt.show()
    pass

if __name__ == '__main__':
    # whs_path = 'D:\\桌面\\力量训练\\2022-08-11T08_16.445Z.tcx'
    # polar_path = 'D:\\桌面\\力量训练\\Lct_3_2022-08-125_1_16-25-11.tcx'
    whs_path='D:\\chenchen2\\桌面\\2\\Run\\WHS_2022-09-07_20-03-04.csv'
    data=pd.read_csv(whs_path)
    # print(type(data['LatitudeDegrees'][1])
    draw_gps(data)

    pass