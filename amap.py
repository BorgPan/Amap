# -*- coding: utf-8 -*-
"""
# Import ArcPy site-package and os modules
Created on Wed Aug 16 17:38:09 2017
@author: BorgPan
"""
import requests
import time
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

s = str(time.strftime('%Y%m%d%H%M%S'))


def drivedata(centerxy, key, d, n):
    file_ = open('amap_timeget.txt', 'a')
    file_.write('ox, oy, dx, dy, distance, time\n')
    ox = float(centerxy.split(',')[0])
    oy = float(centerxy.split(',')[1])
    i = 0
    while i < n:
        j = 0
        while j < n:
            dx = ox - (n - 1) / 2 * d + i * d
            dy = oy - (n - 1) / 2 * d + j * d
            url = "https://restapi.amap.com/v3/direction/driving"
            destination = str(dx) + ',' + str(dy)
            parameters = {
                "origin": centerxy,
                "destination": destination,
                "output": "json",
                "key": key
            }
            r = requests.get(url, parameters)
            res = r.json()

            if res['status'] == '1':
                destination = res['route']['destination']
                distance = res['route']['paths'][0]['distance']
                time = res['route']['paths'][0]['duration']
                data = str(centerxy) + ',' + str(destination) + ',' + str(distance) + ',' + str(time)
                file_.write(data)
                file_.write('\n')
            else:
                pass
            j += 1
        i += 1


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def writetxt():
    f = open("amap_timeget.txt", 'r')
    f_new = open('wgs84' + str(s) + '.txt', 'w')
    f_new.write('lng,lat,distance,time\n')   #坐标转换
    line = f.readlines()
    i = 1
    while i < len(line):
        xy = line[i].split(",")
        lng = float(xy[2])
        lat = float(xy[3])
        if lng < lat:
            lng,lat=lat,lng
        else:
            pass
        distance =xy[4]
        time =xy[5]
        result = gcj02_to_wgs84(lng, lat)
        data= str(result[0])+','+str(result[1])+','+str(distance)+','+str(time)
        f_new.write(data)
        i+=1


if __name__ == '__main__':
    drivedata('105.427217,27.789296','e1d04227c29d3a0c88368b7fe8e06fe6',0.02,50)
    #drivedata(centerxy,key,d,n)
    #高德限制一天一千，n<30
    # key地址http://lbs.amap.com/dev/analysis/quota?
# key=95e46e572483054e7c339c8f4cc0041b
    writetxt()


print("Well Done")
