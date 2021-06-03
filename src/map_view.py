
import numpy as np
import pandas as pd
import plotly.graph_objs as go


class MapPlot:

    plotly_map_style = 'open-street-map'
    """ Other styles are:
    open-street-map
    carto-positron
    carto-darkmatter
    stamen-terrain
    stamen-toner
    stamen-watercolor
    """

    def __init__(self, location_csv: str):

        self._locations = location_csv
        self._loc_df = pd.read_csv(self._locations)
    
    def _calculate_zoom(self, width_to_height=4Author identity unknown.0):
        maxlon, minlon = self._loc_df.Longitude.max(), self._loc_df.Longitude.min()
        maxlat, minlat = self._loc_df.Latitude.max(), self._loc_df.Latitude.min()
        center = {
            "lon": round((maxlon + minlon) / 2, 6),
            "lat": round((maxlat + minlat) / 2, 6),
        }

        # longitudinal range by zoom level (20 to 1)
        # in degress, if centered at equator
        long_zoom_range = np.array([0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096, 0.192, 0.3712, 
                                    0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568, 47.5136, 98.304, 190.0544, 360.0])
        
        margin = 1.2
        height = (maxlon - minlon) * margin
        width = (maxlat - minlat) * margin * width_to_height
        long_zoom = np.interp(height, long_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(width, long_zoom_range, range(20, 0, -1))
        zoom = round(min(long_zoom, lat_zoom), 2)

        return zoom, center
    
    def make_map(self, full_html=False):
        fig = go.Figure(
            # go.Scattermapbox(
            #     mode="markers",
            #     lon=self._loc_df.Longitude,
            #     lat=self._loc_df.Latitude,
            #     marker={'size': 20, 'symbol': ['airport', 'harbor', 'bus']},
            #     text=self._loc_df.Name, textposition='bottom right'
            # )
        )
        hovertemplate = ''
        fig.add_trace(
            go.Scattermapbox(
                mode="markers",
                lon=[self._loc_df.Longitude.iloc[0]],
                lat=[self._loc_df.Latitude.iloc[0]],
                marker=go.scattermapbox.Marker(size=20, color='green'),
                textposition='bottom right',
                name=self._loc_df.Name.iloc[0],
                hovertemplate=f"{self._loc_df.Name.iloc[0]}"
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                mode="markers",
                lon=[self._loc_df.Longitude.iloc[1]],
                lat=[self._loc_df.Latitude.iloc[1]],
                marker={'size': 20,
                # 'symbol': "diamond",
                'color': 'blue'
                # 'opacity': 0.5
                },
                textposition='bottom right',
                name=self._loc_df.Name.iloc[1],
                hovertemplate=f"{self._loc_df.Name.iloc[1]}"
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                mode="markers",
                lon=[self._loc_df.Longitude.iloc[2]],
                lat=[self._loc_df.Latitude.iloc[2]],
                marker={'size': 20,
                # 'symbol':"diamond",
                'color': 'red'
                # 'opacity': 0.2
                },
                textposition='bottom right',
                name=self._loc_df.Name.iloc[2],
                hovertemplate=f"{self._loc_df.Name.iloc[2]}"
            )
        )
        zoom, center = self._calculate_zoom()
        fig.update_layout(
            mapbox={
                'style': MapPlot.plotly_map_style,
                'zoom': zoom,
                'center': center
            },
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            autosize=True,
            showlegend=True,
            hovermode='closest',
            margin={
                'b': 1,
                't': 1,
                'l': 1,
                'r': 1
            }
        )
        
        return fig.to_html(include_plotlyjs=True, full_html=full_html, config={'responsive': True})
    

if __name__ == '__main__':
    input_file_path = r'static/locations.csv'

    map_plot = MapPlot(location_csv=input_file_path)
    html = map_plot.make_map(full_html=False)

    with open(r'map.html', 'w') as outfile:
        outfile.write(html)
        outfile.close()