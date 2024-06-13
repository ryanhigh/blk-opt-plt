from flask import Blueprint, render_template
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from flask.json import jsonify
import pyecharts
print('pyecharts version in app4 :',pyecharts.__version__)

# 使用flask中的蓝图，每个.py文件对应一个html页面。分多个.py文件容易修改和扩展
dp = Blueprint('tx_conflict_rate', __name__)

@dp.route("/changanlian_metric_2")
def changanlian_metric_2():
    return render_template('changanlian_metric_2.html')

# 返回dataframe的下一行的第m、n列数据
def next_xy(df,i,m,n):
    x = df.iloc[i+1,m]
    y = df.iloc[i+1,n]
    i = i+1
    return i,x,y
    
# 根据all_df的第0列和第n列的前2行数据，初始化一条line，
def line_base(df,line_name,n):
    # print('rows data:',df.iloc[:,0])
    line = (
        Line()
        .add_xaxis(xaxis_data=df.iloc[:2,0][-5:].tolist())#第0列是时间
        .add_yaxis(series_name=line_name,
                   y_axis=df.iloc[:2,n].tolist(),
                   is_smooth=True, 
                #    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                   )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%"),
                         xaxis_opts=(opts.AxisOpts(type_="time",name='时间戳',name_location='center',min_='dataMin',name_gap=25)),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return line


all_df = pd.read_csv('files/res0.csv') #包含微观指标的文件

# ################################# tx_conflict_rate的曲线 18############################
@dp.route("/tx_conflict_rate")
def tx_conflict_rate():
    l = line_base(all_df,'块内交易冲突率',18)
    return l.dump_options_with_quotes()

tx_conflict_rate_idx = 3
@dp.route("/tx_conflict_rate_dynamicdata")
def tx_conflict_rate_dynamicdata():
    global tx_conflict_rate_idx
    print('tx_conflict_rate_idx:',tx_conflict_rate_idx)
    if tx_conflict_rate_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        tx_conflict_rate_idx,x,y = next_xy(all_df,tx_conflict_rate_idx,0,18)
        return jsonify({"x_data": x, "y_data": y})

