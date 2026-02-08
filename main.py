import geopandas as gpd
from sqlalchemy import create_engine


gdf=gpd.read_parquet("points_grid.parquet")
engine=create_engine("postgresql://postgres.ielqyuxjmixnwxizcffl:HRV8M0C7KGVwPWpK@aws-1-ap-south-1.pooler.supabase.com:6543/postgres")
gdf.set_crs(epsg=4326,allow_override=True)
gdf.to_postgis("points_grid",engine,index=True,if_exists="replace")
