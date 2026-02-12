import numpy as np 
import pandas as pd
from sqlalchemy import create_engine
engine=create_engine("postgresql://postgres.ielqyuxjmixnwxizcffl:HRV8M0C7KGVwPWpK@aws-1-ap-south-1.pooler.supabase.com:6543/postgres")
query1="""SELECT 
    psb."POL_STN_NM" AS police_station,
    psb."AREA" as AREA,
    COALESCE(SUM(c.theft),0)AS total_theft,
    COALESCE(SUM(c.robbery),0)AS total_robbery,
    COALESCE(SUM(c.murder),0)AS total_murder,
    COALESCE(SUM(c.rape),0)AS total_rape,
    COALESCE(SUM(c.gangrape),0)AS total_gangrape,
    COALESCE(SUM(c."sexual harassement"),0)AS total_sexual_harassement,
    COALESCE(SUM(c."assualt murders"),0)AS total_assualt_murders
FROM 
    police_station_boundry psb
LEFT JOIN 
    crime c
ON 
    st_intersects(c.geometry, psb.geometry)
GROUP BY 
    psb."POL_STN_NM",
    psb."AREA";"""
df_crime=pd.read_sql(query1,engine)
ps_area=df_crime['area'].to_numpy()
ps_area=ps_area.astype(float)
crime=df_crime[['total_theft','total_robbery','total_murder','total_rape','total_gangrape','total_sexual_harassement','total_assualt_murders']].to_numpy()
weight1=np.array([[0.01,2,4,5,6,3,4]])
weight1=weight1.reshape(7,1)
answer1=np.matmul(crime,weight1)
answer1=answer1.reshape(180,)/ps_area 
# print(np.shape(answer1))
df_crime=df_crime.insert(9,'f1',answer1)

print(df_crime)
# print(answer1)
query2="""SELECT "DISTRICT" , 
"dist_area",
COUNT(*) FILTER (WHERE "TYPE OF ACCIDENT"='FATAL ACCIDENT') AS FATAL_COUNT,
SUM("# INJURED") FILTER (WHERE "TYPE OF ACCIDENT"='FATAL ACCIDENT' ) AS FATAL_INJURED,
SUM("# KILLED ") FILTER (WHERE "TYPE OF ACCIDENT"='FATAL ACCIDENT') AS FATAL_KILLED,
COUNT(*) FILTER (WHERE "TYPE OF ACCIDENT"='SIMPLE ACCIDENT') AS SIMPLE_COUNT,
SUM("# INJURED") FILTER (WHERE "TYPE OF ACCIDENT"='SIMPLE ACCIDENT') AS SIMPLE_INJURED,
SUM("# KILLED ") FILTER (WHERE "TYPE OF ACCIDENT"='SIMPLE ACCIDENT') AS SIMPLE_KILLED,

COUNT(*) FILTER (WHERE "TYPE OF ACCIDENT"='NON INJURY') AS NON_INJURY_COUNT,
SUM("# INJURED") FILTER (WHERE "TYPE OF ACCIDENT"='NON INJURY') AS NON_INJURY_INJURED,
SUM("# KILLED ") FILTER (WHERE "TYPE OF ACCIDENT"='NON INJURY') AS NON_INJURY_KILLED
FROM delhi_accident_data GROUP BY "DISTRICT","dist_area";
"""
df_accident=pd.read_sql(query2,engine)
df_accident=df_accident.replace(np.nan,0)
dist_area=df_accident['dist_area'].to_numpy()
fatal_count=df_accident['fatal_count'].to_numpy()
fatal_injured=df_accident['fatal_injured'].to_numpy()
fatal_killed=df_accident['fatal_killed'].to_numpy()
simple_count=df_accident['simple_count'].to_numpy()
simple_injured=df_accident['simple_injured'].to_numpy()
non_injury_count=df_accident['non_injury_count'].to_numpy()
answer2=(3*fatal_count*(fatal_injured+fatal_killed)+2*simple_count*(simple_injured)+(non_injury_count))/10**4
answer2=answer2/dist_area
# print(np.shape(answer2))
# print(answer2)
# print(df_accident.tail(2))

def f2(df):
    pass