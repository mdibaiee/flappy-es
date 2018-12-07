import os
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio

def draw_chart(scatter_x, scatter_y, line_x, line_y):
    marker_opts = dict(
        name = 'Individual Reward',
        x = scatter_x,
        y = scatter_y,
        mode = 'markers',
        marker = {
            'size': 2
        }
    )
    marker_trace = go.Scatter(**marker_opts)
    line_opts = dict(
        name = 'Mean Reward',
        x = line_x,
        y = line_y,
        mode = 'lines'
    )
    line_trace = go.Scatter(**line_opts)

    data = [marker_trace, line_trace]

    fig = go.Figure(data=data)

    log_layout = go.Layout(
        yaxis = {
            'type': 'log',
            'autorange': True
        }
    )
    fig_log = go.Figure(data=data, layout=log_layout)

    pio.orca.config.executable = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules', 'orca', 'bin', 'orca.js')
    pio.write_image(fig, 'fig.svg', width=1600, height=800)
    pio.write_image(fig_log, 'fig-log.svg', width=1600, height=800)
