from calculate import allin1csv
import matplotlib.pyplot as plt
from datetime import datetime

def draw_hr(data):
    # ti=[]
    # for t in data['Time']:
    #     ti.append(datetime.strftime(t,'%M:%S'))
    # x=ti
    plt.clf()
    x=data['Time']
    plt.xticks(rotation=45)
    plt.plot(x,data['HeartRateBpm'],label='Wear',color='b')
    plt.plot(x,data['PolarHR'],label='Polar',color='r')
    plt.legend(loc='best')
    # plt.title('HR对比折线图')#matplotlib不支持中文
    plt.show()
    pass

if __name__ == '__main__':
    whs_path = 'D:\\chenchen2\\桌面\\力量训练\\2022-08-11T08_25_16.445Z.tcx'
    polar_path = 'D:\\chenchen2\\桌面\\力量训练\\Lct_3_2022-08-11_16-25-11.tcx'
    print(whs_path[0:-28])
    # whs=allin1csv(whs_path, polar_path)
    # draw_hr(whs)
    pass