import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# UI program is currently incomplete. Does not function as intended

app = dash.Dash()
colors = {
    'background': '#008fe5',
    'text': '#ffffff'
}

app.layout = html.Div(style={'backgroundColor': colors['background'],
                             'width': '100%',
                             'height': '1000px'
                             },
                      children=[html.H1(children='Injection Detection App',
                                        style={'text-align': 'center',
                                               'color': colors['text'],
                                               }),
                                html.Div(children='Analytics of Detected Injections',
                                         style={'textAlign': 'center',
                                                'color': colors['text']
                                                }),
                                dcc.Store(id='local', storage_type='local'),
                                html.Div(children=[html.Div(children=[html.Span("Sent Request: "),
                                                                      html.Span(id='sql_output')],
                                                            style={'color': colors['text'],
                                                                   'margin': '40px 0 10px 50px',
                                                                   'padding': '10px',
                                                                   'max-width': '700px',
                                                                   'border': '1px solid white'}),
                                                   html.Div(children=[html.Span("Received Data: "),
                                                                      html.Span(id='data_output')],
                                                            style={'color': colors['text'],
                                                                   'margin': '40px 0 10px 50px',
                                                                   'padding': '10px',
                                                                   'max-width': '700px',
                                                                   'border': '1px solid white'}),
                                                   html.P(id='placeholder')],
                                         style={'position': 'relative',
                                                'float': 'left'}
                                         ),
                                html.Div(children=html.Button('Launch Traffic Generator', id='button'),
                                         style={'margin': '40px 50px 100px 0',
                                                'float': 'right'}
                                         ),
                                html.Div(children=dcc.Graph(id='Graph1',
                                                            figure={'data': [
                                                                  {'x': ['Benign', 'Malicious'],
                                                                   'y': [4, 2],
                                                                   'type': 'bar',
                                                                   'name': 'Malicious vs Benign'}],
                                                                  'layout': {'plot_bgcolor': '#d7d7d7',
                                                                             'paper_bgcolor': '#d7d7d7',
                                                                             'font': {'color': '#000000'
                                                                            }
                                                                  }
                                                            }),
                                         style={'width': '100%',
                                                'margin': '20% 0 0 0'
                                                }
                                         )
                                ])


@app.callback(
    Output('data_output', 'children'),
    [Input('button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    while n_clicks == 1:
        return html.Span('{}'.format(str()))
    else:
        pass


if __name__ == '__main__':
    app.run_server(debug=True)
