import numpy as np
import pandas as pd
from tensorflow.keras.datasets import fashion_mnist
from bokeh.models import DataTable, TableColumn, ColumnDataSource, Div
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row


def load_data():
    '''Load Fashion MNIST dataset.
    More details: https://research.zalando.com/welcome/mission/research-projects/fashion-mnist/'''
    data = {}
    (data['image'], data['label']), (_, _) = fashion_mnist.load_data()
    data.update(dict(image=[np.flip(x, 0) for x in data['image']],
                     label=list(data['label'])))
    df = pd.DataFrame.from_records(data)
    return df


# Data - Load raw data & define source
df = load_data()
source_df = ColumnDataSource(df.head(500))

# CREATE NEW FEATURES HERE

# Page title
title = Div(text="""<h1>Dive into the Fashion MNIST Dataset</h1> <br>
<p>This simple dashboard gives an overview of the capabilities of Bokeh
for data visualization. <br> Learn more about this dataset
<a href="https://research.zalando.com/welcome/mission/research-projects/fashion-mnist/">here</a>.</p>""")

# Datatable - Display raw data
table = DataTable(source=source_df,
                  sortable=True)
table.columns = [TableColumn(field=col, title=col)
                 for col in ['label']]

# Figure - Visualize sample image
figure_image = figure(plot_height=250, plot_width=250)
figure_image.image(image='image', source=source_df,
                   x=0, y=0, dw=28, dh=28)

# Define layout and add to document
layout = column(title, row(table, figure_image))
curdoc().add_root(layout)
