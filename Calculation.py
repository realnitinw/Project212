import numpy as np 
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
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
'''
df_crime=pd.read_sql(query1,engine)
ps_area=df_crime['area'].to_numpy()
ps_area=ps_area.astype(float)
crime=df_crime[['total_theft','total_robbery','total_murder','total_rape','total_gangrape','total_sexual_harassement','total_assualt_murders']].to_numpy()
weight1=np.array([[0.01,2,4,5,6,3,4]])
weight1=weight1.reshape(7,1)
answer1=np.matmul(crime,weight1)
answer1=answer1.reshape(180,)/ps_area 
# print(np.shape(answer1))
df_crime["f1"]=answer1
df_crime.to_sql("police_station_crime",engine)
'''
#print(df_crime)
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
# df_accident=pd.read_sql(query2,engine)
# df_accident=df_accident.replace(np.nan,0)
# dist_area=df_accident['dist_area'].to_numpy()
# fatal_count=df_accident['fatal_count'].to_numpy()
# fatal_injured=df_accident['fatal_injured'].to_numpy()
# fatal_killed=df_accident['fatal_killed'].to_numpy()
# simple_count=df_accident['simple_count'].to_numpy()
# simple_injured=df_accident['simple_injured'].to_numpy()
# non_injury_count=df_accident['non_injury_count'].to_numpy()
# answer2=(3*fatal_count*(fatal_injured+fatal_killed)+2*simple_count*(simple_injured)+(non_injury_count))/10**4
# answer2=answer2/dist_area
# df_accident['f2']=answer2
# print(df_accident)
# df_accident.to_sql('df_accident_f2',engine,if_exists='replace')
# print(np.shape(answer2))
# print(answer2)
# print(df_accident.tail(2))
# df_accident_f2=pd.read_sql('df_accident_f2',engine)
# print(df_accident_f2)
# df_accident=df_accident.replace(np.nan,0)
# dist_area=df_accident_f2['dist_area'].to_numpy()
# fatal_count=df_accident_f2['fatal_count'].to_numpy()
# fatal_injured=df_accident_f2['fatal_injured'].to_numpy()
# fatal_killed=df_accident_f2['fatal_killed'].to_numpy()
# simple_count=df_accident_f2['simple_count'].to_numpy()
# simple_injured=df_accident_f2['simple_injured'].to_numpy()
# non_injury_count=df_accident_f2['non_injury_count'].to_numpy()
# answer2=(3*fatal_count*(fatal_injured+fatal_killed)+2*simple_count*(simple_injured)+(non_injury_count))/10**4
# answer2=answer2/dist_area
# df_accident_f2['f2']=answer2
# df_accident_f2.to_sql('df_accident_f2',engine,if_exists='replace')
# print(df_accident_f2)
def sigmoid(z):
    return 1/(1+np.exp(-z))
points_grid=pd.read_sql_table('points_grid',engine)
f1=points_grid['f1'].to_numpy()
f2=points_grid['f2'].to_numpy()
r=points_grid['ps_dist'].to_numpy()
safety_score=(sigmoid(1/((f1+f2)*r)))**100
plt.hist(safety_score,bins=40)
plt.show()
# points_grid.to_sql('new',engine)
# df=pd.DataFrame()
# df['safety_score']=safety_score
# df.to_sql('safety_score',engine,if_exists='replace')
