import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine


df=pd.read_csv("Delhi Accident Data.csv")
#gdf=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.long,df.lat))
engine=create_engine("postgresql://postgres.ielqyuxjmixnwxizcffl:HRV8M0C7KGVwPWpK@aws-1-ap-south-1.pooler.supabase.com:6543/postgres")
#gdf.set_crs(epsg=4326,allow_override=True)
df.to_sql("delhi_accident_data",engine,index=False,if_exists="replace")
