@app.route("/")
def ():
    l = line_base(all_df,'',)
    return l.dump_options_with_quotes()

_idx = 3
@app.route("/_dynamicdata")
def _dynamicdata():
    global _idx
    print('_idx:',_idx)
    if _idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        _idx,x,y = next_xy(all_df,_idx,0,)
        return jsonify({"x_data": x, "y_data": y})

