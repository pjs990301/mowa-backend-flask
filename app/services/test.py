import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-input',
        options=[
            {'label': 'Option 1', 'value': 1},
            {'label': 'Option 2', 'value': 2},
            {'label': 'Option 3', 'value': 3},
        ],
        value=None,
        placeholder="Select an option"
    ),
    html.Div("Or enter a value:"),
    dcc.Input(
        id='integer-input',
        type='number',
        placeholder='Enter a value'
    ),
    html.Div(id='output-div')
])

@app.callback(
    Output('output-div', 'children'),
    [Input('dropdown-input', 'value'),
     Input('integer-input', 'value')]
)
def update_output(dropdown_value, integer_value):
    if dropdown_value is not None:
        return f"You selected: {dropdown_value}"
    elif integer_value is not None and integer_value != "":
        return f"You entered: {integer_value}"
    else:
        return "Please select a value or enter a number."

if __name__ == '__main__':
    app.run_server(debug=True)
