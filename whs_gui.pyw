'''
2.0 添加step path, actigraphy steps数据整合,移除结果层
1.8 添加gtx path, gps数据整合
1.6 解决了polar心率无数据时的异常
1.5 更新tcx元素定位xpath方法, 解决了GPS LT问题, 解决数据时间不匹配导致的无法计算问题
1.4 解决了绘图bug
1.3 更新whs_cal图标
1.2 增加csv文件导出、心率折线图绘制选项, 设置文件路径输入框长度, 导出csv文件与加载tcx文件在一个目录下py
1.1 增加对比机dis输入框, gps_ape计算, 非输入区域置灰处理
1.0 whs辅助计算初版
'''

import base64
import os
import logging
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Labelframe, Combobox
from datetime import datetime

from timezone_change import timezone_change
from graph import draw_hr, draw_gps
from calculate import cal1, cal2
from whs_tcx2csv import whs_tcx2csv
from polar_tcx2csv import polar_tcx2csv
from gpx2csv import gpx2csv, getDistance
from testlog import TextboxHander
from icon import Icon


class whs:
    def __init__(self, wear_path, gps_path, polar_path, step_path):
        self.wear_path = wear_path
        self.gps_path = gps_path
        self.polar_path = polar_path
        self.step_path = step_path

    def get_wear_path():
        Filepath = filedialog.askopenfilename()
        show_wear_path.set(Filepath)

    def get_gps_path():
        Filepath = filedialog.askopenfilename()
        show_gps_path.set(Filepath)

    def get_polar_path():
        Filepath = filedialog.askopenfilename()
        show_polar_path.set(Filepath)

    def get_step_path():
        Filepath = filedialog.askopenfilename()
        show_step_path.set(Filepath)

    def get_dic_path():
        Filepath = filedialog.askdirectory()
        show_dic_path.set(Filepath)

    def allin1csv(wear_path, gps_path, polar_path, step_path, inputcsv=False):
        whs = pd.DataFrame()
        whs_log = logging.getLogger('log')
        whs_log.info('***START***')
        try:
            if len(wear_path) != 0:
                whs_log.info('WHS PATH: {}'.format(wear_path))
                wear_tp = whs_tcx2csv(wear_path)
                wear = pd.DataFrame(wear_tp)
            else:
                whs_log.info('WHS PATH is null')
            whs = pd.concat([whs, wear], axis=1)
        except:
            whs_log.info('{} is not available'.format(wear_path))
            wear_path = ''

        try:
            if len(gps_path) != 0:
                whs_log.info('GPS PATH: {}'.format(gps_path))
                # if len(gps_path) != 0:
                tmpgps = {'GPSTime': [], 'GPSLat': [], 'GPSLon': []}
                n = 0
                gps_tp = gpx2csv(gps_path)
                gps = pd.DataFrame(gps_tp)

                for i in range(len(whs['Time'])):
                    for m in range(n, len(gps['Time'])):
                        if whs['Time'][i] == gps['Time'][m]:
                            tmpgps['GPSTime'].append(gps['Time'][m])
                            tmpgps['GPSLat'].append(gps['Lat'][m])
                            tmpgps['GPSLon'].append(gps['Lon'][m])
                            n = m+1
                            break
                        # 若遍历完后无匹配项，则添加空值
                        elif m+1 == len(gps['Time']):
                            tmpgps['GPSTime'].append('')
                            tmpgps['GPSLat'].append('')
                            tmpgps['GPSLon'].append('')
                tmp_gps = pd.DataFrame(tmpgps)
                whs = pd.concat([whs, tmp_gps], axis=1)
                # if inputcsv:
                #     filename=filepath+'GPS_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
                #     tmp_gps.to_csv(filename)
            else:
                whs_log.info('GPS PATH is null')
        except:
            whs_log.info('{} is not available'.format(gps_path))
            gps_path = ''

        try:
            if len(polar_path) != 0:
                whs_log.info('POLAR PATH: {}'.format(polar_path))
                tmphr = {'PolarTime': [], 'PolarHR': []}
                k = 0
                polar_tp = polar_tcx2csv(polar_path)
                polar = pd.DataFrame(polar_tp)

                for i in range(len(whs['Time'])):
                    for j in range(k, len(polar['Time'])):
                        if wear['Time'][i] == polar['Time'][j]:
                            tmphr['PolarTime'].append(polar['Time'][j])
                            tmphr['PolarHR'].append(polar['HeartRateBpm'][j])
                            k = j+1
                            break
                        # 若遍历完后无匹配项，则添加空值
                        elif j+1 == len(polar['Time']):
                            tmphr['PolarTime'].append('')
                            tmphr['PolarHR'].append('')
                tmp_hr = pd.DataFrame(tmphr)
                whs = pd.concat([whs, tmp_hr], axis=1)
                # if inputcsv:
                #     filename=filepath+'HR_{}.csv'.format(datetime.strftime(timezone_change(whs['Time'][0]),"%Y-%m-%d_%H-%M-%S"))
                #     tmp_hr.to_csv(filename)5
            else:
                whs_log.info('POLAR PATH is null')
        except:
            whs_log.info('{} is not available'.format(polar_path))
            polar_path = ''

        try:
            if len(step_path) != 0:
                whs_log.info('STEP PATH: {}'.format(step_path))
                tmp = pd.read_csv(step_path, header=10)
                rawstep, tmpstep = {'ActiTime': [], 'ActiSteps': []}, {
                    'ActiTime': [], 'ActiSteps': []}
                t = 0
                try:
                    rawstep['ActiTime'] = tmp['Date']+' '+tmp['Epoch']
                except:
                    rawstep['ActiTime'] = tmp['Date']+' '+tmp[' Time']
                rawstep['ActiSteps'] = tmp['Steps']
                # raw_step=pd.DataFrame(rawstep)
                # 切换成格林威治时间
                local_time = datetime.now()
                utc_time = datetime.utcnow()
                tmp = local_time-utc_time
                for i in range(len(whs['Time'])):
                    for s in range(t, len(rawstep['ActiTime'])):
                        tmptime = datetime.strptime(
                            rawstep['ActiTime'][s], "%Y/%m/%d %H:%M:%S")-tmp
                        print(tmptime, type(tmptime),
                              wear['Time'][i], type(wear['Time'][i]))
                        if wear['Time'][i] == tmptime:
                            tmpstep['ActiTime'].append(tmptime)
                            # try: tmpstep['ActiSteps'].append(rawstep['ActiSteps'][i-1]+rawstep['ActiSteps'][s])
                            # except: tmpstep['ActiSteps'].append(rawstep['ActiSteps'][s])
                            tmpstep['ActiSteps'].append(
                                rawstep['ActiSteps'][s])
                            t = s+1
                            break
                        # 若遍历完后无匹配项，则添加空值
                        elif s+1 == len(rawstep['ActiTime']):
                            tmpstep['ActiTime'].append('')
                            tmpstep['ActiSteps'].append('')
                tmp_step = pd.DataFrame(tmpstep)
                whs = pd.concat([whs, tmp_step], axis=1)
            else:
                whs_log.info('STEP PATH is null')
            # whs = pd.concat([whs, wear], axis=1)
        except:
            whs_log.info('{} is not available'.format(step_path))

        if inputcsv:
            filename = 'WHS_{}.csv'.format(datetime.strftime(
                timezone_change(whs['Time'][0]), "%Y-%m-%d_%H-%M-%S"))
            whs.to_csv(filename)
            whs_log.info('CSV pulled, path: {}\n\n'.format(
                os.path.dirname(__file__)))
        return whs

    def run1():
        data = {'hr_lock_time': 0, 'hr_ae': 0, 'hr_ape': 0, 'gps_lock_time': 0,
                'gps_ae': 0, 'gps_ape': 0, 'whs_steps': 0, 'whs_dis': 0}
        csv = whs.allin1csv(show_wear_path.get(), show_gps_path.get(
        ), show_polar_path.get(), show_step_path.get(), check1.get())
        # data=cal1(csv)

        # 是否绘制心率折线图
        if check2.get() == 1:
            draw_hr(csv)
            pass

        # 是否绘制GPS路线图
        if check3.get() == 1:
            draw_gps(csv)
            pass
        # print(data)
        # # HR
        # hr_lock_time.set(data['hr_lock_time'])
        # hr_ae.set(data['hr_ae'])
        # hr_ape.set(data['hr_ape'])

        # # GPS
        # gps_lock_time.set(data['gps_lock_time'])
        # # DIS APE
        # dis = float(gps_ae.get())
        # gps_ape.set('{:.2%}'.format(abs(dis-data['whs_dis'])/dis))

        # # STEPS
        # sb = int(step_before.get())
        # sa = int(step_after.get())
        # tmp = abs(sa-sb)
        # steps_ape.set('{:.2%}'.format(abs(tmp-data['whs_steps'])/tmp))
        pass

    def all2onecsv():
        pass

    def run2():
        whs_log.info('***START***\n')
        whs = pd.DataFrame()
        i = 0
        data = {'start_time': 0, 'end_time': 0, 'hr_start_time': 0, 'hr_lock_time': [], 'hr_ae': [], 'hr_ape': [
        ], 'gps_start_time': 0, 'gps_lock_time': [], 'gps_ae': [], 'gps_ape': [], 'dut_steps': 0, 'steps_ape': [], 'dut_dis': 0, 'gt_dis': 0, 'gt_steps': 0}

        dicpath = show_dic_path.get()
        filenames = os.listdir(dicpath)
        for filename in filenames:
            filepath = dicpath+'/'+filename
            whs_log.info('{}. {} added.'.format(i+1, filename))
            csv = pd.read_csv(filepath, index_col=0)

            # 获取各项数据
            data = cal2(csv)
            # 直接显示心率相关数据: HR Lock Time
            whs_log.info('HR lock time: {}'.format(data['hr_lock_time'][i]))
            # 直接显示GPS相关数据: GPS Lock Time、DUT distance、GT distance、Distance APE
            if 'GPSLat' in csv.columns:
                whs_log.info('GPS lock time: {}\nDUT distance: {}\nGT distance: {}\nDistance APE: {:.2%}'.format(
                    data['gps_lock_time'][i], round(data['dut_dis'], 2), round(data['gt_dis'], 2), data['gps_ape'][0]))
            # 直接显示STEP相关数据: DUT steps、GT steps、Steps APE
            if 'ActiTime' in csv.columns:
                whs_log.info('DUT steps: {}\nGT steps: {}\nSTEP APE: {:.2%}'.format(
                    data['dut_steps'], data['gt_steps'], data['steps_ape']))
                pass

            whs = pd.concat([whs, csv])
            i = i+1
            pass

        whs.insert(len(whs.columns), 'Track Accuracy AE', data['gps_ae'])
        whs.insert(len(whs.columns), 'HR AE', data['hr_ae'])
        whs.insert(len(whs.columns), 'HR APE', data['hr_ape'])
        whs_log.info('\n***{} file added***\n\n'.format(len(filenames)))

        # TODO:90%percentile
        # print(np.percentile(array(data['gps_ae']),0.9))
        # print(whs['Track Accuracy AE'].quantile(0.9))

        protocol_csv_name=protocol_combobox.get()
        whs.to_csv('{}.csv'.format(protocol_csv_name))
        whs_log.info('\n***{}\{}.csv***\n\n'.format(os.path.dirname(__file__),protocol_csv_name))

        pass


if __name__ == '__main__':
    win = Tk()
    win.title(string='WHS辅助计算2.0')

    show_wear_path, show_gps_path, show_polar_path, show_step_path, show_dic_path = StringVar(
    ), StringVar(), StringVar(), StringVar(), StringVar()
    check1, check2, check3 = IntVar(), IntVar(), IntVar()
    hr_lock_time, hr_ae, hr_ape = StringVar(), StringVar(), StringVar()
    gps_lock_time, gps_ae, gps_ape = StringVar(), StringVar(), StringVar()
    step_before, step_after, steps_ape = StringVar(), StringVar(), StringVar()
    whs_log = StringVar()

    # 上层源文件路径
    up_frame = Frame(win)
    path_frame = Labelframe(up_frame, text='TCX文件路径', relief=RIDGE)
    path_frame.pack(side=LEFT, expand='yes', fill='both')
    # valueresult.set('   必选项')
    Label(path_frame, text='WEAR PATH:', relief=GROOVE).grid(
        row=0, column=0, columnspan=1)
    Label(path_frame, text=' GPS PATH:  ', relief=GROOVE).grid(
        row=1, column=0, columnspan=1)
    Label(path_frame, text=' HR  PATH:  ', relief=GROOVE).grid(
        row=2, column=0, columnspan=1)
    Label(path_frame, text='STEP PATH:  ', relief=GROOVE).grid(
        row=3, column=0, columnspan=1)
    Entry(path_frame, text=show_wear_path, bd=1).grid(
        row=0, column=1, columnspan=1, ipadx=145)
    Entry(path_frame, text=show_gps_path, bd=1).grid(
        row=1, column=1, columnspan=1, ipadx=145)
    Entry(path_frame, text=show_polar_path, bd=1).grid(
        row=2, column=1, columnspan=1, ipadx=145)
    Entry(path_frame, text=show_step_path, bd=1).grid(
        row=3, column=1, columnspan=1, ipadx=145)
    Button(path_frame, text=' ... ', command=whs.get_wear_path).grid(
        row=0, column=2, columnspan=1)
    Button(path_frame, text=' ... ', command=whs.get_gps_path).grid(
        row=1, column=2, columnspan=1)
    Button(path_frame, text=' ... ', command=whs.get_polar_path).grid(
        row=2, column=2, columnspan=1)
    Button(path_frame, text=' ... ', command=whs.get_step_path).grid(
        row=3, column=2, columnspan=1)

    run_frame = LabelFrame(up_frame, text='运行', relief=RIDGE)
    run_frame.pack(side=RIGHT, expand='yes', fill='both')
    Checkbutton(run_frame, text='是否导出csv ', variable=check1).grid(
        row=0, column=0, columnspan=1)
    Checkbutton(run_frame, text='是否作心率图', variable=check2).grid(
        row=1, column=0, columnspan=1)
    Checkbutton(run_frame, text='是否作路线图', variable=check3).grid(
        row=2, column=0, columnspan=1)
    Button(run_frame, text=' RUN ', command=whs.run1).grid(
        row=3, column=0, columnspan=1)
    up_frame.pack(side=TOP)

    # 中层协议文件
    mid_frame = Frame(win)
    protocol_frame = LabelFrame(mid_frame, text='协议路径', relief=RIDGE)
    protocol_frame.pack(side=LEFT, expand='yes', fill='both')
    protocol_choose = StringVar()
    protocol_combobox = Combobox(
        protocol_frame, textvariable=protocol_choose, state='readonly')
    protocol_combobox['values'] = (
        'Sedentary', 'Calibration', 'Daily Activities', 'Biking', 'Running', 'Strength Training')
    protocol_combobox.grid(row=0, column=0, columnspan=1, ipadx=0)
    Label(protocol_frame, text='PATH:').grid(row=0, column=1, columnspan=1)
    Entry(protocol_frame, text=show_dic_path, bd=1).grid(
        row=0, column=2, columnspan=1, ipadx=120)
    Button(protocol_frame, text='...', command=whs.get_dic_path).grid(
        row=0, column=3, columnspan=1)
    Button(protocol_frame, text='RUN', command=whs.run2).grid(
        row=0, column=4, columnspan=1)
    mid_frame.pack(side=TOP)

    # 下层结果层
    # down_frame = Frame(win)
    # hr_frame = LabelFrame(down_frame, text='心率', relief=RIDGE)
    # hr_frame.pack(side=LEFT, expand='yes', fill='both')
    # Label(hr_frame, text='HR LT:  ').grid(row=0)
    # Label(hr_frame, text='HR AE:  ').grid(row=1)
    # Label(hr_frame, text='HR APE:').grid(row=2)
    # Entry(hr_frame, justify='left', textvariable=hr_lock_time,
    #       bg='#E0E0E0').grid(row=0, column=1)
    # Entry(hr_frame, justify='left', textvariable=hr_ae,
    #       bg='#E0E0E0').grid(row=1, column=1)
    # Entry(hr_frame, justify='left', textvariable=hr_ape,
    #       bg='#E0E0E0').grid(row=2, column=1)

    # gps_frame = LabelFrame(down_frame, text='GPS', relief=RIDGE)
    # gps_frame.pack(side=LEFT, expand='yes', fill='both')
    # Label(gps_frame, text='GPS LT:  ').grid(row=0)
    # Label(gps_frame, text='GPS AE: ').grid(row=1)
    # Label(gps_frame, text='GPS APE:').grid(row=2)
    # Entry(gps_frame, justify='left', textvariable=gps_lock_time,
    #       bg='#E0E0E0').grid(row=0, column=1)
    # Entry(gps_frame, justify='left', textvariable=gps_ae).grid(row=1, column=1)
    # Entry(gps_frame, justify='left', textvariable=gps_ape,
    #       bg='#E0E0E0').grid(row=2, column=1)

    # step_frame = LabelFrame(down_frame, text='Steps', relief=RIDGE)
    # step_frame.pack(side=RIGHT, expand='yes', fill='both')
    # Label(step_frame, text='输入测试前步数:').grid(row=0)
    # Label(step_frame, text='输入测试后步数:').grid(row=1)
    # Label(step_frame, text='计算Steps APE:').grid(row=2)
    # Entry(step_frame, justify='left',
    #       textvariable=step_before).grid(row=0, column=1)
    # Entry(step_frame, justify='left',
    #       textvariable=step_after).grid(row=1, column=1)
    # Entry(step_frame, justify='left', textvariable=steps_ape,
    #       bg='#E0E0E0').grid(row=2, column=1)
    # down_frame.pack(side=TOP)

    # 底层LOG层
    bottom_frame = Frame(win)
    log_frame = LabelFrame(bottom_frame, text='Log', relief=RIDGE)
    log_frame.pack(side=RIGHT, expand='yes', fill='both')
    normalTextBox = Text(log_frame)
    normalTextBox.grid(ipadx=20, ipady=16, row=0)
    whs_log = logging.getLogger('log')
    whs_log.setLevel(logging.INFO)
    handler = TextboxHander(normalTextBox)
    whs_log.addHandler(handler)

    def clear():
        normalTextBox.delete(0.0, END)  # 清楚text中的内容，0.0为删除全部
        normalTextBox.grid(ipadx=20, ipady=16, row=0)

    Button(bottom_frame, text='Clear', command=clear).pack(side='right')
    bottom_frame.pack(side=TOP)

    # 使用pyinstaller打包icon，需要将icon提前处理成二进制文件保存在程序中
    with open('tmp.ico', 'wb') as tmp:
        tmp.write(base64.b64decode(Icon().img))
    win.iconbitmap('tmp.ico')
    os.remove('tmp.ico')
    mainloop()
