# -*- coding: utf-8 -*-
import time

d = 0.02
n = 5
centerxy = '27.788464,105.423782'
olat = float(centerxy.split(',')[0])
olng = float(centerxy.split(',')[1])
s = str(time.strftime('%Y%m%d%H%M'))
file_ = open('lat_lng_amap' + str(s) + '.txt', 'w')
file_.write('dx,dy,distance,time\n')

def getdestination():
    i = 0
    while i < n:
        j = 0
        while j < n:
            dx = olat - (n - 1) / 2 * d + i * d
            dy = olng - (n - 1) / 2 * d + j * d
            data = str(dx) + ',' + str(dy)
            file_.write(data)
            file_.write('\n')
            j += 1
        i += 1


if __name__ == '__main__':
    getdestination()
    print 'welldone'
