from flask import Flask, render_template, request, make_response
import json
import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid, Pie, Tab
from flask.json import jsonify
from random import randrange
from pyecharts.commons.utils import JsCode
import pyecharts
print('pyecharts version in app1 :',pyecharts.__version__)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

import app2 as a2
import app3 as a3
import app4 as a4
app = Flask(__name__, template_folder="templates",static_folder="resource")
app.register_blueprint(a2.bp)
app.register_blueprint(a3.cp)
app.register_blueprint(a4.dp)



@app.route("/")
def index():
  return render_template("main_content.html")


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
        .add_xaxis(xaxis_data=df.iloc[:2,0].tolist())#第0列是时间
        .add_yaxis(series_name=line_name,   
                   y_axis=df.iloc[:2,n].tolist(),
                   is_smooth=True, 
                   
                #    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                   )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%",
                                                     textstyle_opts=opts.TextStyleOpts(font_family="微软雅黑",font_size="18")),
                         xaxis_opts=(opts.AxisOpts(type_="time",name='时间戳',name_location='center',min_='dataMin',name_gap=25,
                                                   name_textstyle_opts=opts.TextStyleOpts(font_family="微软雅黑",font_size="12"))),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return line


all_df = pd.read_csv('files/res0.csv') #包含微观指标的文件


# ################################# cpu_use_rate的曲线 ############################
@app.route("/cpu_use_rate")
def cpu_use_rate():
    cpu_l = line_base(all_df,'CPU利用率',1) #第1列是CPU利用率的值
    return cpu_l.dump_options_with_quotes()

cpu_use_rate_idx=3
@app.route('/cpu_use_rate_dynamicdata')
def cpu_use_rate_dynamicdata():
    global cpu_use_rate_idx
    if cpu_use_rate_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        cpu_use_rate_idx,x,y = next_xy(all_df,cpu_use_rate_idx,0,1) #第0列是时间，第1列是CPU利用率的值
        # x=all_df.iloc[cpu_use_rate_idx+1,0]
        # y=all_df.iloc[cpu_use_rate_idx+1,1]
        # cpu_use_rate_idx = cpu_use_rate_idx + 1
        # print("cpu_use_rate:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})




# ################################# memory_use_rate的曲线 ############################
@app.route("/memory_use_rate")
def memory_use_rate():
    l = line_base(all_df,'内存利用率',2)#第2列是CPU利用率的值
    return l.dump_options_with_quotes()

memory_use_rate_idx=3
@app.route("/memory_use_rate_dynamicdata")
def memory_use_rate_dynamicdata():
    global memory_use_rate_idx
    print('memory_use_rate_idx:',memory_use_rate_idx)
    if memory_use_rate_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        memory_use_rate_idx,x,y = next_xy(all_df,memory_use_rate_idx,0,2) #第0列是时间，第2列是 memory 利用率的值
        # print("memory_use_rate_idx,x,y:",memory_use_rate_idx,x,y)
        return jsonify({"x_data": x, "y_data": y})
    

# ################################# tx_pool_input的曲线 ############################
@app.route("/txpool_input")
def tx_pool_input():
    l = line_base(all_df,'交易池输入通量',3)#第3列是交易池输入通量的值
    return l.dump_options_with_quotes()

txpool_input_idx = 3
@app.route("/txpool_input_dynamicdata")
def tx_pool_input_dynamicdata():
    global txpool_input_idx
    print('tx_pool_input_idx:',txpool_input_idx)
    if txpool_input_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        txpool_input_idx,x,y = next_xy(all_df,txpool_input_idx,0,3)
        return jsonify({"x_data": x, "y_data": y})


# ################################# p2p_avg_transDelay的曲线 ############################
@app.route("/p2p_delay")
def p2p_avg_delay():
    l = line_base(all_df,'P2P网络平均传输时延',4)#第4列是...的值
    return l.dump_options_with_quotes()

p2p_delay_idx = 3
@app.route("/p2p_delay_dynamicdata")
def p2p_avg_delay_dynamicdata():
    global p2p_delay_idx
    print('p2p_delay_idx:',p2p_delay_idx)
    if p2p_delay_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        p2p_delay_idx,x,y = next_xy(all_df,p2p_delay_idx,0,4)
        return jsonify({"x_data": x, "y_data": y})


# ################################# node_info_forwardNum的曲线 ############################
@app.route("/node_forwardNum")
def node_forwardNum():
    l = line_base(all_df,'节点接发消息总量',5)#第5列是...的值
    return l.dump_options_with_quotes()

node_forwardNum_idx = 3
@app.route("/node_forwardNum_dynamicdata")
def node_forwardNum_dynamicdata():
    global node_forwardNum_idx
    print('node_forwardNum_idxNumpyEncoder:',node_forwardNum_idx)
    if node_forwardNum_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        node_forwardNum_idx,x,y = next_xy(all_df,node_forwardNum_idx,0,5)
        ############### TypeError: int64 cannot be json serialized ################
        # 创建数据字典
        data = {"x_data": x, "y_data": y}

        # 使用自定义的NumpyEncoder进行JSON序列化
        json_data = json.dumps(data, cls=NumpyEncoder)
        
        # 创建响应并设置内容类型为application/json
        response = make_response(json_data)
        response.headers['Content-Type'] = 'application/json'
        
        return response
        # return jsonify({"x_data": x, "y_data": y})

# ################################# db_write_v的曲线 ############################
@app.route("/db_write")
def db_write_v():
    l = line_base(all_df,'数据库状态写入速率',6)
    return l.dump_options_with_quotes()

db_write_idx = 3
@app.route("/db_write_dynamicdata")
def db_write_dynamicdata():
    global db_write_idx
    print('db_write_idx:',db_write_idx)
    if db_write_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        db_write_idx,x,y = next_xy(all_df,db_write_idx,0,6)
        return jsonify({"x_data": x, "y_data": y})

# ################################# db_read_v的曲线 ############################
@app.route("/db_read")
def db_read_v():
    l = line_base(all_df,'数据库状态读取速率',7)
    return l.dump_options_with_quotes()

db_read_idx = 3
@app.route("/db_read_dynamicdata")
def db_read_dynamicdata():
    global db_read_idx
    print('db_read_idx:',db_read_idx)
    if db_read_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        db_read_idx,x,y = next_xy(all_df,db_read_idx,0,7)
        return jsonify({"x_data": x, "y_data": y})
    
# ################################# tx_queue_delay的曲线 ############################
@app.route("/tx_queue_delay")
def tx_queue_delay():
    l = line_base(all_df,'交易排队时延',8)
    return l.dump_options_with_quotes()

tx_queue_delay_idx = 3
@app.route("/tx_queue_delay_dynamicdata")
def tx_queue_delay_dynamicdata():
    global tx_queue_delay_idx
    print('tx_queue_delay_idx:',tx_queue_delay_idx)
    if tx_queue_delay_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        tx_queue_delay_idx,x,y = next_xy(all_df,tx_queue_delay_idx,0,8)
        return jsonify({"x_data": x, "y_data": y})


# ################################# block_delay的曲线 9############################
@app.route("/block_delay")
def block_delay():
    l = line_base(all_df,'出块时延',9)
    return l.dump_options_with_quotes()

block_delay_idx = 3
@app.route("/block_delay_dynamicdata")
def block_delay_dynamicdata():
    global block_delay_idx
    print('block_delay_idx:',block_delay_idx)
    if block_delay_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        block_delay_idx,x,y = next_xy(all_df,block_delay_idx,0,9)
        return jsonify({"x_data": x, "y_data": y})


# ################################# tps_in_blk的曲线 10############################
@app.route("/tps_in_blk")
def tps_in_blk():
    l = line_base(all_df,'块内交易吞吐量',10)
    return l.dump_options_with_quotes()

tps_in_blk_idx = 3
@app.route("/tps_in_blk_dynamicdata")
def tps_in_blk_dynamicdata():
    global tps_in_blk_idx
    print('tps_in_blk_idx:',tps_in_blk_idx)
    if tps_in_blk_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        tps_in_blk_idx,x,y = next_xy(all_df,tps_in_blk_idx,0,10)
        return jsonify({"x_data": x, "y_data": y})
# ################################# blk_val_efficiency的曲线 11############################
@app.route("/blk_val_efficiency")
def blk_val_efficiency():
    l = line_base(all_df,'区块验证效率',11)
    return l.dump_options_with_quotes()

blk_val_efficiency_idx = 3
@app.route("/blk_val_efficiency_dynamicdata")
def blk_val_efficiency_dynamicdata():
    global blk_val_efficiency_idx
    print('blk_val_efficiency_idx:',blk_val_efficiency_idx)
    if blk_val_efficiency_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        blk_val_efficiency_idx,x,y = next_xy(all_df,blk_val_efficiency_idx,0,11)
        return jsonify({"x_data": x, "y_data": y})
# ################################# tx_delay的曲线 12############################
@app.route("/tx_delay")
def tx_delay():
    l = line_base(all_df,'交易时延',12)
    return l.dump_options_with_quotes()

tx_delay_idx = 3
@app.route("/tx_delay_dynamicdata")
def tx_delay_dynamicdata():
    global tx_delay_idx
    print('tx_delay_idx:',tx_delay_idx)
    if tx_delay_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        tx_delay_idx,x,y = next_xy(all_df,tx_delay_idx,0,12)
        return jsonify({"x_data": x, "y_data": y})
# ################################# consensus_cost的曲线 13############################
@app.route("/consensus_cost")
def consensus_cost():
    l = line_base(all_df,'平均每轮共识耗时',13)
    return l.dump_options_with_quotes()

consensus_cost_idx = 3
@app.route("/consensus_cost_dynamicdata")
def consensus_cost_dynamicdata():
    global consensus_cost_idx
    print('consensus_cost_idx:',consensus_cost_idx)
    if consensus_cost_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        consensus_cost_idx,x,y = next_xy(all_df,consensus_cost_idx,0,13)
        return jsonify({"x_data": x, "y_data": y})
# ################################# proposal的曲线 14############################
@app.route("/proposal")
def proposal():
    l = line_base(all_df,'proposal',14)
    return l.dump_options_with_quotes()

proposal_idx = 3
@app.route("/proposal_dynamicdata")
def proposal_dynamicdata():
    global proposal_idx
    print('proposal_idx:',proposal_idx)
    if proposal_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        proposal_idx,x,y = next_xy(all_df,proposal_idx,0,14)
        return jsonify({"x_data": x, "y_data": y})
# ################################# prevote的曲线 15############################
@app.route("/prevote")
def prevote():
    l = line_base(all_df,'prevote',15)
    return l.dump_options_with_quotes()

prevote_idx = 3
@app.route("/prevote_dynamicdata")
def prevote_dynamicdata():
    global prevote_idx
    print('prevote_idx:',prevote_idx)
    if prevote_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        prevote_idx,x,y = next_xy(all_df,prevote_idx,0,15)
        return jsonify({"x_data": x, "y_data": y})
# ################################# precommit的曲线 16############################
@app.route("/precommit")
def precommit():
    l = line_base(all_df,'precommit',16)
    return l.dump_options_with_quotes()

precommit_idx = 3
@app.route("/precommit_dynamicdata")
def precommit_dynamicdata():
    global precommit_idx
    print('precommit_idx:',precommit_idx)
    if precommit_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        precommit_idx,x,y = next_xy(all_df,precommit_idx,0,16)
        return jsonify({"x_data": x, "y_data": y})
<<<<<<< HEAD
=======
# # ################################# commit的曲线 17############################
# @app.route("/commit")
# def commit():
#     l = line_base(all_df,'commit',17)
#     return l.dump_options_with_quotes()

# commit_idx = 3
# @app.route("/commit_dynamicdata")
# def commit_dynamicdata():
#     global commit_idx
#     print('commit_idx:',commit_idx)
#     if commit_idx == all_df.shape[0]-1:
#         return jsonify({"x_data": '', "y_data": ''})
#     else:
#         commit_idx,x,y = next_xy(all_df,commit_idx,0,17)
#         return jsonify({"x_data": x, "y_data": y})
# # ################################# tx_conflict_rate的曲线 18############################
# @app.route("/tx_conflict_rate")
# def tx_conflict_rate():
#     l = line_base(all_df,'块内交易冲突率',18)
#     return l.dump_options_with_quotes()

# tx_conflict_rate_idx = 3
# @app.route("/tx_conflict_rate_dynamicdata")
# def tx_conflict_rate_dynamicdata():
#     global tx_conflict_rate_idx
#     print('tx_conflict_rate_idx:',tx_conflict_rate_idx)
#     if tx_conflict_rate_idx == all_df.shape[0]-1:
#         return jsonify({"x_data": '', "y_data": ''})
#     else:
#         tx_conflict_rate_idx,x,y = next_xy(all_df,tx_conflict_rate_idx,0,18)
#         return jsonify({"x_data": x, "y_data": y})
>>>>>>> 78edd86 ('commit' & 'tx_conflict_rate' update in Page2)


if __name__=='__main__':
    app.run(debug=True)