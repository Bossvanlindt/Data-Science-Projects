import pandas as pd
import math

from bokeh.plotting import figure, curdoc
from bokeh.models import Select, ColumnDataSource
from bokeh.layouts import column

params = curdoc().session_context.request.arguments
try:
  username = params.get('username')[0].decode('UTF-8')
except:
  username = "false"
try:
  password = params.get('password')[0].decode('UTF-8')
except:
  password = "false"

if username == 'nyc' and password == 'iheartnyc':

    # Constant lists
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    zip_codes = ['00083', '10000', '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10009', '10010', '10011', '10012', '10013', '10014', '10016', '10017', '10018', '10019', '10020', '10021', '10022', '10023', '10024', '10025', '10026', '10027', '10028', '10029', '10030', '10031', '10032', '10033', '10034', '10035', '10036', '10037', '10038', '10039', '10040', '10041', '10044', '10045', '10048', '10055', '10065', '10069', '10075', '10103', '10105', '10106', '10107', '10110', '10111', '10112', '10115', '10118', '10119', '10120', '10121', '10122', '10123', '10128', '10151', '10152', '10153', '10154', '10155', '10158', '10162', '10165', '10166', '10167', '10168', '10169', '10170', '10171', '10172', '10173', '10174', '10175', '10176', '10177', '10178', '10179', '10271', '10278', '10279', '10280', '10281', '10282', '10301', '10302', '10303', '10304', '10305', '10306', '10307', '10308', '10309', '10310', '10312', '10314', '10451', '10452', '10453', '10454', '10455', '10456', '10457', '10458', '10459', '10460', '10461', '10462', '10463', '10464', '10465', '10466', '10467', '10468', '10469', '10470', '10471', '10472', '10473', '10474', '10475', '11001', '11004', '11005', '11040', '11101', '11102', '11103', '11104', '11105', '11106', '11109', '11201', '11203', '11204', '11205', '11206', '11207', '11208', '11209', '11210', '11211', '11212', '11213', '11214', '11215', '11216', '11217', '11218', '11219', '11220', '11221', '11222', '11223', '11224', '11225', '11226', '11228', '11229', '11230', '11231', '11232', '11233', '11234', '11235', '11236', '11237', '11238', '11239', '11241', '11242', '11249', '11251', '11354', '11355', '11356', '11357', '11358', '11359', '11360', '11361', '11362', '11363', '11364', '11365', '11366', '11367', '11368', '11369', '11370', '11371', '11372', '11373', '11374', '11375', '11377', '11378', '11379', '11385', '11411', '11412', '11413', '11414', '11415', '11416', '11417', '11418', '11419', '11420', '11421', '11422', '11423', '11426', '11427', '11428', '11429', '11430', '11432', '11433', '11434', '11435', '11436', '11691', '11692', '11693', '11694', '11695', '11697', '12345']

    # Read data into dataframes
    df = pd.read_csv('data/all.csv')

    # Create the graph
    graph = figure(title = 'NYC Incidence Response Times by ZIP Code')
    graph.xaxis.axis_label = 'Month (2020)'
    graph.yaxis.axis_label = 'Create-to-Closed Lengths, Monthly Average (in Hours)'

    # Plot All 2020 Data graph
    times = df['Create-to-Closed Time'].map(lambda x : 0 if math.isnan(x) else x).tolist()
    graph.line(
            x=months,
            y=times,
            line_color = 'blue',
            line_dash = 'solid',
            legend_label = 'All 2020 Data'
         )

    # Plot the graphs for the 2 selected zip codes, initially empty
    zip1_source = ColumnDataSource({'Month': [1,2,3,4,5,6,7,8,9,10,11,12],
                                    'Create-to-Closed Time': [0,0,0,1.1994444444444443,0.26541666666666663,1.181388888888889,0,0,0,0,0,0]})
    zip2_source = ColumnDataSource({'Month': [1,2,3,4,5,6,7,8,9,10,11,12],
                                    'Create-to-Closed Time': [0,0,0,1.1994444444444443,0.26541666666666663,1.181388888888889,0,0,0,0,0,0]})
    graph.line(
        x='Month',
        y='Create-to-Closed Time',
        source = zip1_source,
        line_color = 'red',
        line_dash = 'solid',
        name = 'zip1',
        legend_label = 'Zipcode 1 Data'
    )
    graph.line(
        x='Month',
        y='Create-to-Closed Time',
        source = zip2_source,
        line_color = 'green',
        line_dash = 'solid',
        name = 'zip2',
        legend_label = 'Zipcode 2 Data'
    )

    # 2 dropdowns for zip codes, updating graph with two zip code graphs when changed
    d1 = Select(title='Zipcode 1', value='00083', options=zip_codes)
    d2 = Select(title='Zipcode 2', value='00083', options=zip_codes)
    def d1_graph(attr, old, new):
        df1 = pd.read_csv(f'data/{d1.value}.csv')
        d1_times = df1['Create-to-Closed Time'].map(lambda x : 0 if math.isnan(x) else x).tolist()
        zip1_source.data['Create-to-Closed Time'] = d1_times
    def d2_graph(attr, old, new):
        df2 = pd.read_csv(f'data/{d2.value}.csv')
        d2_times = df2['Create-to-Closed Time'].map(lambda x : 0 if math.isnan(x) else x).tolist()
        zip2_source.data['Create-to-Closed Time'] = d2_times
    d1.on_change('value', d1_graph)
    d2.on_change('value', d2_graph)

    # Plot the graph
    curdoc().add_root(column(d1, d2, graph))