import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
from bokeh.models import DataTable, TableColumn, ColumnDataSource, Select, Div
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.transform import transform
from bokeh.palettes import RdBu7 as colors


def load_data():
    '''Load Boston House price dataset.
    More details: https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html'''
    boston = load_boston()
    data = pd.DataFrame(boston.data, columns=boston.feature_names)
    data['Price'] = boston.target
    return data


def on_feature_change(attr, old, new):
    global source_df, figure_scatter
    source_df.data.update(dict(Feature=df[new]))
    figure_scatter.xaxis.axis_label = new


# Data - Load raw data & define source
df = load_data()
default_feature = df.columns[0]
source_df = ColumnDataSource(df)

# CREATE NEW FEATURES HERE

# Page title
title = Div(text="""<h1>Dive into the Boston House Price Dataset</h1> <br>
<p>This simple dashboard gives an overview of the capabilities of Bokeh
for data visualization. <br> Learn more about this dataset
<a href="https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html">here</a>.</p>""")

# Datatable - Display raw data
table = DataTable(source=source_df,
                  sortable=True)
table.columns = [TableColumn(field=col, title=col)
                 for col in df.columns]

# Data - Compute correlation matrix & define source
df_corr = df.corr()
df_corr.index.name = 'axis1'
df_corr.columns.name = 'axis2'
df_corr = df_corr.stack().rename("value").reset_index()
source_df_corr = ColumnDataSource(df_corr)

# Figure - Features correlation heatmap
figure_heatmap = figure(title="Correlation plot",
                        plot_width=600, plot_height=600,
                        x_range=list(df_corr.axis1.drop_duplicates()),
                        y_range=list(df_corr.axis2.drop_duplicates()))
mapper = LinearColorMapper(palette=colors, low=-1, high=1)
figure_heatmap.rect(x="axis1", y="axis2", width=1, height=1,
                    source=source_df_corr, line_color='black',
                    fill_color=transform('value', mapper))

# Add heatmap colorbar
color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                     ticker=BasicTicker(desired_num_ticks=10))
figure_heatmap.add_layout(color_bar, 'right')
figure_heatmap.xaxis.major_label_orientation = np.pi/4
figure_heatmap.yaxis.major_label_orientation = np.pi/4

# Add heatmap hovertool
hover = HoverTool(tooltips=[("feature1", "@axis1"),
                            ("feature2", "@axis2"),
                            ("correlation", "@value")])
figure_heatmap.add_tools(hover)

# Figure - Scatter plot feature vs price
figure_scatter = figure(title="Influence of feature over house price")
figure_scatter.circle(x='Feature', y='Price',
                      source=source_df,
                      selection_color='red',
                      nonselection_alpha=0.2)
figure_scatter.yaxis.axis_label = 'Price (in k$)'

# Select - Choose among a list of feature
select_feature = Select(title='Feature',
                        options=list(df.columns),
                        width=200)
select_feature.on_change('value', on_feature_change)
select_feature.value = default_feature

# Define layout and add to document
layout = row(column(title, table),
             figure_heatmap,
             column(select_feature, figure_scatter))
curdoc().add_root(layout)
