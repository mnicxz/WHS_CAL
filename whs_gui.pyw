'''
1.5 更新tcx元素定位xpath方法, 解决了GPS LT问题, 解决数据时间不匹配导致的无法计算问题
1.4 解决了绘图bug
1.3 更新whs_cal图标
1.2 增加csv文件导出、心率折线图绘制选项, 设置文件路径输入框长度, 导出csv文件与加载tcx文件在一个目录下py
1.1 增加对比机dis输入框, gps_ape计算, 非输入区域置灰处理
1.0 whs辅助计算初版
'''

import base64, os
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Labelframe
from datetime import datetime

from graph import draw_hr
from calculate import cal,allin1csv,timezone_change
from icon import Icon

def get_whs_path():
    Filepath=filedialog.askopenfilename()
    valueresult.set(Filepath)
    pass

def get_polar_path():
    Filepath=filedialog.askopenfilename()
    valueresult2.set(Filepath)

def get_gps_path():
    # Filepath=filedialog.askopenfilename()
    valueresult3.set('还没做')

def get_result():
    data={'hr_lock_time':0,'hr_ae':0,'hr_ape':0,'gps_lock_time':0,'gps_ae':0,'gps_ape':0,'whs_steps':0,'whs_dis':0}
    whs=allin1csv(valueresult.get(),valueresult2.get())
    data=cal(whs)

    # 是否导出csv, 导出csv文件与加载tcx文件在一个目录下
    if check1.get() == 1:
        filepath=valueresult.get()[0:-28]
        filename=filepath+'WHS_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
        # print(filename)
        whs.to_csv(filename)
        pass

    # 是否绘制心率折线图
    if check2.get() == 1:
        draw_hr(whs)
        pass

    # HR
    hr_lock_time.set(data['hr_lock_time'])
    hr_ae.set(data['hr_ae'])
    hr_ape.set(data['hr_ape'])

    # GPS
    gps_lock_time.set(data['gps_lock_time'])
    # DIS APE
    dis=float(gps_ae.get())
    gps_ape.set('{:.2%}'.format(abs(dis-data['whs_dis'])/dis))


    # STEPS
    sb=int(step_before.get())
    sa=int(step_after.get())
    tmp=abs(sa-sb)
    steps_ape.set('{:.2%}'.format(abs(tmp-data['whs_steps'])/tmp))
    pass

win = Tk()
win.title(string='WHS辅助计算1.5')
# win.geometry('{}x{}+{}+{}'.format(420,200,20,20))


valueresult,valueresult2,valueresult3 = StringVar(),StringVar(),StringVar()
check1,check2 = IntVar(),IntVar()
hr_lock_time,hr_ae,hr_ape=StringVar(),StringVar(),StringVar()
gps_lock_time,gps_ae,gps_ape=StringVar(),StringVar(),StringVar()
step_before,step_after,steps_ape=StringVar(),StringVar(),StringVar()


# paned=PanedWindow(win,orient=VERTICAL,showwinhandle=True,sashrelief=SUNKEN,sashwidth=1)
# paned.pack(fill=BOTH,expand=1)
up_frame=Frame(win)

path_frame=Labelframe(up_frame,text='TCX文件路径',relief=RIDGE)
path_frame.pack(side=LEFT,expand='yes',fill='both')
Label(path_frame,text='WHS PATH:',relief=GROOVE).grid(row=0, column=0, columnspan=1)
Label(path_frame,text='POL PATH: ',relief=GROOVE).grid(row=1, column=0, columnspan=1)
Label(path_frame,text='GPS PATH: ',relief=GROOVE).grid(row=2, column=0, columnspan=1)
Entry(path_frame,text=valueresult,bd=1).grid(row=0, column=1, columnspan=1, ipadx=145)
Entry(path_frame,text=valueresult2,bd=1).grid(row=1, column=1, columnspan=1, ipadx=145)
Entry(path_frame,text=valueresult3,bd=1).grid(row=2, column=1, columnspan=1, ipadx=145)
Button(path_frame, text=' ... ', command=get_whs_path ).grid(row=0, column=2, columnspan=1)
Button(path_frame, text=' ... ', command=get_polar_path ).grid( row=1, column=2, columnspan=1 )
Button(path_frame, text=' ... ', command=get_gps_path ).grid( row=2, column=2, columnspan=1 )

cal_frame=LabelFrame(up_frame,text='计算',relief=RIDGE)
cal_frame.pack(side=RIGHT,expand='yes',fill='both')
# cal_frame=Labelframe(root, text = '计算').pack(side='bottom', expand='yes', fill='both')
Checkbutton(cal_frame,text='是否导出csv ',variable=check1).grid(row=0, column=0, columnspan=1)
Checkbutton(cal_frame,text='是否作心率图',variable=check2).grid(row=1, column=0, columnspan=1)
Button(cal_frame, text=' 计算 ', command=get_result ).grid(row=2, column=0, columnspan=1)
up_frame.pack(side=TOP)

down_frame=Frame(win)

hr_frame=LabelFrame(down_frame,text='心率',relief=RIDGE)
hr_frame.pack(side=LEFT,expand='yes',fill='both')
Label(hr_frame,text='HR LT:  ').grid( row=0 )
Label(hr_frame,text='HR AE:  ').grid( row=1 )
Label(hr_frame,text='HR APE:').grid( row=2 )
Entry(hr_frame, justify='left', textvariable = hr_lock_time, bg='#E0E0E0').grid(row=0,column=1)
Entry(hr_frame, justify='left', textvariable = hr_ae, bg='#E0E0E0').grid(row=1,column=1)
Entry(hr_frame, justify='left', textvariable = hr_ape, bg='#E0E0E0').grid(row=2,column=1)

gps_frame=LabelFrame(down_frame,text='GPS',relief=RIDGE)
gps_frame.pack(side=LEFT,expand='yes',fill='both')
Label(gps_frame,text='GPS LT:  ').grid( row=0 )
Label(gps_frame,text='输入距离:').grid( row=1 )
# Label(gps_frame,text='GPS AE:  ').grid( row=1 )
Label(gps_frame,text='GPS APE:').grid( row=2 )
Entry(gps_frame, justify='left', textvariable = gps_lock_time, bg='#E0E0E0').grid(row=0,column=1)
Entry(gps_frame, justify='left', textvariable = gps_ae).grid(row=1,column=1)
Entry(gps_frame, justify='left', textvariable = gps_ape, bg='#E0E0E0').grid(row=2,column=1)

step_frame=LabelFrame(down_frame,text='Steps',relief=RIDGE)
step_frame.pack(side=RIGHT,expand='yes',fill='both')
Label(step_frame,text='输入测试前步数:').grid( row=0 )
Label(step_frame,text='输入测试后步数:').grid( row=1 )
Label(step_frame,text='计算Steps APE:').grid( row=2 )
Entry(step_frame, justify='left', textvariable = step_before).grid(row=0,column=1)
Entry(step_frame, justify='left', textvariable = step_after).grid(row=1,column=1)
Entry(step_frame, justify='left', textvariable = steps_ape, bg='#E0E0E0').grid(row=2,column=1)

down_frame.pack(side=TOP)

# 使用pyinstaller打包icon，需要将icon提前处理成二进制文件保存在程序中
with open('tmp.ico','wb') as tmp:
    tmp.write(base64.b64decode(Icon().img))
win.iconbitmap('tmp.ico')
os.remove('tmp.ico')
mainloop()
