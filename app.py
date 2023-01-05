from flask import Flask, render_template
import geoviews as gv
import holoviews as hv
import geoviews.tile_sources as gvts
import pandas as pd
from bokeh.models import HoverTool
from geoviews import dim, opts
import numpy as np
from bokeh.embed import components
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/")
def index():
     # Load the data and create the GeoViews points
    college_data = pd.read_csv('/Users/caden/Adv Computing/College Map Project/updated_locations.csv')
    college_gv_points = gv.Points(college_data, ['longitude', 'latitude'], ['university', 'num_students_attended'])

    # Create the hover tool
    tooltips = [('Unviversity', '@university'),
                ('Attendees', '@num_students_attended'),]
    hover = HoverTool(tooltips=tooltips)

    # Create the light and dark plots
    light_plot = (gvts.CartoLight * college_gv_points).opts(
        opts.Points(alpha=0.3,
                    hover_line_color='black',
                    color = 'blue', line_color='black', xaxis=None, yaxis=None,
                    tools=[hover],size=np.sqrt(dim('num_students_attended'))*2,
                    hover_fill_color='blue', hover_fill_alpha=0.2))

    dark_plot = (gvts.CartoDark.options(alpha=0.8) * college_gv_points).opts(
    opts.Points(
        alpha=0.6,hover_line_color='black', color = 'orange', line_color=None, 
        xaxis=None, yaxis=None,
        tools=[hover],
        size=np.sqrt(dim('num_students_attended'))*2,
        hover_fill_color='orange', hover_fill_alpha=0.4))

    # Render the map using Holoviews
    hv_points = hv.render(dark_plot)
    hv_points.sizing_mode = 'stretch_both'  # Set the sizing_mode property
    script, div = components(hv_points)
    return render_template('index.html', script=script, div=div)


if __name__ == '__main__':
    app.run()
