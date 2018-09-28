import pandas as pd
import requests
r =requests.get("https://restapi.amap.com/v3/config/district?keywords=山东&subdistrict=0&key=你的密钥&extensions=all")
s=r.json()
poly=s["districts"][0]["polyline"]
p=poly.split("|")
x=[]
for i in range(len(p)):
    a=p[i].split(";")
    for j in range(len(a)):
        x.append([a[j].split(",")[0],a[j].split(",")[1],i])
c = pd.DataFrame(x)
c.to_csv('xzqh.csv')
