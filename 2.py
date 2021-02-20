import pandas as pd 
from sqlalchemy import create_engine

# 创建廉洁数据库的引擎
engine = create_engine("mysql+pymysql://root:@localhost:3306/hpdb")

# 读取文件不同的sheet页内容数据DataFrame
df = pd.read_excel("000.xlsx",sheet_name="钉钉9172")
df1 = pd.read_excel("000.xlsx",sheet_name="科信9312")
df2 = pd.read_excel("000.xlsx",sheet_name="智慧政工6949")
df3 = pd.read_excel("000.xlsx",sheet_name="咚咚9057")

#通过数据引擎自动创建表，并导入mysql数据库，replace---drop表重建，appand---表存在，数据添加在后面
df.to_sql(name="dingding",con=engine,index=False,if_exists="replace")
df1.to_sql(name="kexin",con=engine,index=False,if_exists="replace")
df2.to_sql(name="zhihuizhenggong",con=engine,index=False,if_exists="replace")
df3.to_sql(name="dongdong",con=engine,index=False,if_exists="replace")