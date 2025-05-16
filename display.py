from business import GraphBuilder, StatsBuilder
from dash import Dash, Input, Output, State, dcc, html,callback

app = Dash(__name__)

gb = GraphBuilder()

sb = StatsBuilder()


app.layout = html.Div(
    [
        html.H1("Application Demographics"),
        dcc.Dropdown(
            options = ["Nationality", "Age","Education"],
            value = "Nationality",
            id = "demo-plots-dropdown"
        ),
        html.Div(id = "demo-plot-display"),
        html.H1("Experiment"),
        html.H2("Choose your effect"),
        dcc.Slider(min = 0.1, max = 0.8, step = 0.1, value = 0.2, id = "effect-size-slider"),
        html.Div(id = "effect-size-display"),
        html.H2("Choose Experiment Duration"),
        dcc.Slider(min = 150, max = 500, step = 50, value = 150, id = "experiment-days-slider"),
        html.Div(id = "experiment-days-display"),
        html.H1("Results"),
        html.Button("Display Experiment", id= "start-experiment-button",n_clicks= 0),
        html.Div(id = "results-display")
    ]
)


@app.callback(
    Output("demo-plot-display", "children"),
    Input("demo-plots-dropdown","value")
)
def display_demo_graph(graph_name):
    """Serves applicant demograhic visualization.

    Parameters
    ----------
    graph_name : str
        User input given via 'demo-plots-dropdown'. Name of Graph to be returned.
        Options are 'Nationality', 'Age', 'Education'.

    Returns
    -------
    dcc.Graph
        Plot that will be displayed in 'demo-plots-display' Div.
    """
    if graph_name == "Nationality":
        fig = gb.build_nat_choropleth()
    elif graph_name == "Age":
        fig = gb.build_age_hist()
    else:
        fig = gb.build_ed_bar()
    return dcc.Graph(figure = fig)
    


@app.callback(
    Output("effect-size-display", "children"),
    Input("effect-size-slider","value")
)
def display_group_size(effect_size):
    """Serves information about required group size.

    Parameters
    ----------
    effect_size : float
        Size of effect that user wants to detect. Provided via 'effect-size-slider'.

    Returns
    -------
    html.Div
        Text with information about required group size. will be displayed in
        'effect-size-display'.
    """
    n_obs = sb.calculate_n_obs(effect_size)
    text = f"To detect an effect size of {effect_size}, you would need {n_obs} observations"
    return html.Div(text)


@app.callback(
    Output("experiment-days-display", "children"),
    Input("effect-size-slider","value"),
    Input("experiment-days-slider", "value")
)
def display_cdf_pct(effect_size, days):
    """Serves probability of getting desired number of obervations.

    Parameters
    ----------
    effect_size : float
        The effect size that user wants to detect. Provided via 'effect-size-slider'.
    days : int
        Duration of the experiment. Provided via 'experiment-days-slider'.

    Returns
    -------
    html.Div
        Text with information about probabilty. Goes to 'experiment-days-display'.
    """
    # Calculate number of observations
    n_obs = sb.calculate_n_obs(effect_size)
    # Calculate percentage
    pct = sb.calculate_cdf_pct(n_obs, days)
    # Create text
    text = f"The probability of getting this number of observation in {days} days is {pct:.1f}%"
    # Return Div with text
    return html.Div(text)


@app.callback(
    Output("results-display","children"),
    Input("start-experiment-function","n_clicks"),
    State("experiment-days-slider","value")
)
def display_results(n_clicks, days):
    """Serves results from experiment.

    Parameters
    ----------
    n_clicks : int
        Number of times 'start-experiment-button' button has been pressed.
    days : int
        Duration of the experiment. Provided via 'experiment-days-display'.

    Returns
    -------
    html.Div
        Experiment results. Goes to 'results-display'.
    """
    if n_clicks == 0:
       return html.Div()
    else:
        #run experiment
        
        #create side by side bar chart
        
        #run chi square
        
        #return results

        return html.Div()
