### WHS_CAL
* 提取TCX文件数据并转化成CSV格式
* 解决GOOGLE WHS raw数据与POLAR运动心率数据
* 计算HR Lock Time、AE(Absolute Error)、APE(Absolute Percent Error)
* 计算GPS Lock Time、(TODO: Track Accuracy AE)、Distance APE
* 计算Steps APE

### RELEASENOTE
* 2.0 添加step path, actigraphy steps数据整合,移除结果层
* 1.8 添加gtx path, gps数据整合
* 1.6 解决了polar心率无数据时的异常
* 1.5 更新tcx元素定位xpath方法, 解决了GPS LT问题, 解决数据时间不匹配导致的无法计算问题
* 1.4 解决了绘图bug
* 1.3 更新whs_cal图标
* 1.2 增加csv文件导出、心率折线图绘制选项, 设置文件路径输入框长度, 导出csv文件与加载tcx文件在一个目录下py
* 1.1 增加对比机dis输入框, gps_ape计算, 非输入区域置灰处理
* 1.0 whs辅助计算初版