import numpy as np
from bokeh.models import DataTable, TableColumn, ColumnDataSource, Button
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row


def generate_new_data(new):
    global source
    '''Generate a 2D toy dataset as pandas Dataframe'''
    data = {}
    data['x'] = np.random.randint(-10, 10, 100)
    data['y'] = np.random.randint(-10, 10, 100)
    source.data.update(data)


# Define source data (updated at each call of generate_new_data)
source = ColumnDataSource()
generate_new_data(source)

# Create data table (linked to source)
table = DataTable(source=source, sortable=True)
table.columns = [TableColumn(field=col, title=col)
                 for col in source.data.keys()]

# Create button and callback (update source)
button = Button(label='Generate new data points', button_type='primary')
button.on_click(generate_new_data)

# Create a scatter plot (display source)
p = figure(title='2D toy dataset',
           x_axis_label='X axis',
           y_axis_label='Y axis')
p.circle(x='x', y='y',
         source=source,
         selection_color='red',
         nonselection_alpha=0.2)

# Define layout
column1 = column(table, button)
layout = row(column1, p)

# Add layout to the document
curdoc().add_root(layout)
