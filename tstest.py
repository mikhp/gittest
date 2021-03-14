import tushare as ts

pro = ts.pro_api("90560e35833d3f8c1c11275c97fe71d7e1f0557853ecc2e577eb7f1d")

df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')