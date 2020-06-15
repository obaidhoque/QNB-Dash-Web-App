########################################################################################################################
########################################################################################################################
########################################### Qatar Stock Market Dashboard ###############################################
########################################################################################################################
########################################################################################################################

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
df = pd.read_csv('/Users/OBAID/Desktop/TradingReports/stock_data.csv')


########################################################## Figure 1 ####################################################
# Create and Initialize figure
scatterFig = go.Figure()

# Add Traces

scatterFig.add_trace(
    go.Scatter(x=list(df.date),
               y=list(df.high_pr),
               name="High",
               line=dict(color="#356130")))

scatterFig.add_trace(
    go.Scatter(x=list(df.date),
               y=[df.high_pr.mean()] * len(df.index),
               name="High Average",
               visible=False,
               line=dict(color="#356130", dash="dash")))

scatterFig.add_trace(
    go.Scatter(x=list(df.date),
               y=list(df.low_pr),
               name="Low",
               line=dict(color="#d134ce")))

scatterFig.add_trace(
    go.Scatter(x=list(df.date),
               y=[df.low_pr.mean()] * len(df.index),
               name="Low Average",
               visible=False,
               line=dict(color="#d134ce", dash="dash")))

# Add Annotations and Buttons
high_annotations = [dict(x="2019-01-03 00:00:00",
                         y=df.high_pr.mean(),
                         xref="x", yref="y",
                         text="High Average:<br> %.3f" % df.high_pr.mean(),
                         ax=0, ay=-40),
                    dict(x=df.high_pr.idxmax(),
                         y=df.high_pr.max(),
                         xref="x", yref="y",
                         text="High Max:<br> %.3f" % df.high_pr.max(),
                         ax=0, ay=-40)]
low_annotations = [dict(x="2019-01-03 00:00:00",
                        y=df.low_pr.mean(),
                        xref="x", yref="y",
                        text="Low Average:<br> %.3f" % df.low_pr.mean(),
                        ax=0, ay=40),
                   dict(x=df.high_pr.idxmin(),
                        y=df.low_pr.min(),
                        xref="x", yref="y",
                        text="Low Min:<br> %.3f" % df.low_pr.min(),
                        ax=0, ay=40)]

scatterFig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="None",
                     method="update",
                     args=[{"visible": [True, False, True, False]},
                           {"title": "Qatar National Bank (in QAR)",
                            "annotations": []}]),
                dict(label="High",
                     method="update",
                     args=[{"visible": [True, True, False, False]},
                           {"title": "Qatar National Bank (in QAR)",
                            "annotations": high_annotations}]),
                dict(label="Low",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {"title": "Qatar National Bank (in QAR)",
                            "annotations": low_annotations}]),
                dict(label="Both",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "Qatar National Bank (in QAR)",
                            "annotations": high_annotations + low_annotations}]),
            ]),
        )
    ])

# Set title
scatterFig.update_layout(title_text="QNB Historical Prices (in QAR)")

########################################################## Figure 2 ####################################################
vol = px.line(df, x='date', y='tr_vol', title='Transaction Volume')

########################################################## Figure 3 ####################################################
vwap = px.line(df, x='date', y='all_day_vwap', title='Volume Weighted Average Price')
vwap.update_xaxes(rangeslider_visible=True)

########################################################## Figure 4 ####################################################
openpr = px.line(df, x='date', y='open_pr', title='Daily Opening Price (drag slider)')
openpr.update_xaxes(rangeslider_visible=True)

########################################################## TABLE ####################################################
tab = go.Figure(data=[go.Table(
    header=dict(values=['Date', 'Transactions', 'Value of Transactions', 'Price Change'],
                fill_color='#2ebed1',
                align='center'),
    cells=dict(values=[df.date, df.no_of_trans, df.tr_val, df.pr_change_percent],
               fill_color='lavender',
               align='center'))
])


########################################################## DASH APP ####################################################
import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__) # to start your dash application
server = app.server # the Flask app
########################################################## APP LAYOUT ####################################################

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("QNBK.jpg"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Qatar National Bank",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Stock Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("QSE", id="learn-more-button"),
                            href="https://www.qe.com.qa/web/guest/company-profile-page?InformationCategory=Company&InformationType=News&CompanyCode=QNBK&FromLocalSite=N&MoreNewsTitle=1",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            "Stock Overview",
                            className="control_label",
                        ),
                        html.P(
                            "Qatar National Bank (QNB Group) (Arabic: بنك قطر الوطني‎) is a Qatari commercial bank headquartered in Doha, Qatar. It was founded in 1964 and currently has subsidiaries and associates in 31 countries spanning three continents. The banks operating income as of 2019 is US$ 6.9 billion and net income is US$ 4.0 billion. The bank has around 29,000 employees with total assets valued at US$ 26.0 billion."
                        ),
                        html.H6(
                            "Board of Directors",
                            className="list_label",
                        ),
                        html.Ol([
                            html.Li("H.E. Mr. Ali Sharif Al Emadi/ Minister Of Finance & Chairman of BOD"),
                            html.Li("H.E. Sheikh Fahad Faisal T Al-Thani / Vice Chairman"),
                            html.Li("H.E. Sheikh Hamad Bin Jabor Bin Jassim Al-Thani / Member"),
                            html.Li("H.E..Sheikh Abdulrahman Bin Saud Bin Fahad Al-Thani / Member"),
                            html.Li("Mr. Ali Hussain Ali Al-Sada / Member"),
                            html.Li("Mr. Bader Abdullah Darwish Fakhroo / Member"),
                            html.Li("Mr. Fahad Mohammed Fahad Buzwair / Member"),
                            html.Li("Mr.Mansoor Ebrahim Al-Mahmoud / Member"),
                            html.Li("Mr. Abdulrahman Mohammed Y Jolo / Member"),
                            html.Li("Mr. Adil Hassan H A Al-Jufairi / Member"),
                        ]),
                    ],
                    className="pretty_container four columns hover_element",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="open_price"), html.P("Open Price")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="volume"), html.P("Volume")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="transaction"), html.P("Transactions")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("27 February, 2020")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(figure=openpr)],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(figure=scatterFig)],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(figure=vol)],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(figure=vwap)],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(figure=tab)],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# todo 1. create app.callback for the small tiles in the dashboard
# todo 2. Update summary for QNB intro tile
# todo 3. Put it in github and host the dash on github pages

if __name__ == '__main__':
    app.run_server(debug=True)


