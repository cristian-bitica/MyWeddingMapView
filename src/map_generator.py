import pandas as pd
import numpy as np
from enum import Enum
import plotly.graph_objs as go


class MapStyles(str, Enum):
    OPEN_STREET_MAP = 'open-street-map'
    CARTO_POSITRON = 'carto-positron'
    CARTO_DARKMATTER = 'carto-darkmatter'
    STAMEN_TERRAIN = 'stamen-terrain'
    STAMEN_TONER = 'stamen-toner'
    STAMEN_WATERCOLOR = 'stamen-watercolor'


class MapGenerator:

    map_style = MapStyles.OPEN_STREET_MAP.value
    input_df_cols = ['name', 'latitude', 'longitude']
    # longitudinal range by zoom level (20 to 1)
    # in degress, if centered at equator
    long_zoom_range = np.array([0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096, 0.192, 0.3712, 
                                0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568, 47.5136, 98.304, 190.0544, 360.0])
    margin = 1.2
    zoom_level = 20  # range by zoom level (20 to 1)

    def __init__(self, input_df: pd.DataFrame) -> None:
        if not all([col in input_df.columns for col in ['name', 'latitude', 'longitude']]):
            raise Exception("Provided DF does not contain minimum columns to create map: 'name', 'latitude' and 'longitude'")
        self._df = input_df
    
    def _calculate_zoom(self, width_to_height=4):
        maxlon, minlon = self._df['longitude'].max(), self._df['longitude'].min()
        maxlat, minlat = self._df['latitude'].max(), self._df['latitude'].min()
        center = {
            "lon": round((maxlon + minlon) / 2, 6),
            "lat": round((maxlat + minlat) / 2, 6),
        }

        height = (maxlon - minlon) * self.margin
        width = (maxlat - minlat) * self.margin * width_to_height
        long_zoom = np.interp(height, self.long_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(width, self.long_zoom_range, range(20, 0, -1))
        zoom = round(min(long_zoom, lat_zoom), 2)

        return zoom, center
    
    def make_map(self, full_html=False):
        fig = go.Figure(
        )
        for i in range(len(self._df)):
            fig.add_trace(
                go.Scattermapbox(
                    mode="markers",
                    lon=[self._df['longitude'].iloc[i]],
                    lat=[self._df['latitude'].iloc[i]],
                    marker=dict(
                        size=15,
                        symbol = 'circle',
                        opacity = 1
                        ),
                    # marker=go.scattermapbox.Marker(size=20, color='green'),
                    textposition='bottom right',
                    name=self._df['name'].iloc[i],
                    hovertemplate=f"{self._df['timestamp'].iloc[i]}:"
                )
            )
        
        zoom, center = self._calculate_zoom()
        fig.update_layout(
            mapbox={
                'style': self.map_style,
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
        # fig.update_traces(marker_symbol="square", marker_size=15)
        
        return fig.to_html(include_plotlyjs=True, full_html=full_html, config={'responsive': True})

