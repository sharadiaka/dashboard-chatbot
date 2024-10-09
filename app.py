import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import os

df = pd.read_csv("data/data.csv")
df.columns = df.columns.str.strip()

media_tempo_conversa = df["tempo_estimado_conversa"].mean()
media_mensagens_por_conversa = df["media_mensagens_por_conversa"].mean()

app = dash.Dash(__name__)

if not os.path.exists("assets"):
    os.makedirs("assets")


wordcloud = WordCloud(width=800, height=400, background_color="#fefefc").generate(
    " ".join(df["palavras_mais_usadas"])
)
wordcloud.to_file("assets/wordcloud.png")

dias_semana = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
horas = [
    "00:00",
    "02:00",
    "04:00",
    "06:00",
    "08:00",
    "10:00",
    "12:00",
    "14:00",
    "16:00",
    "18:00",
    "20:00",
    "22:00",
]
dados_heatmap = np.random.randint(0, 10, size=(12, 7))

heatmap_fig = px.imshow(
    dados_heatmap,
    labels=dict(x="Dia da Semana", y="Hora do Dia", color="Conversas"),
    x=dias_semana,
    y=horas,
    color_continuous_scale="Blues",
    title="Distribuição de Conversas por Hora e Dia",
    aspect="auto",
)

heatmap_fig.update_layout(
    plot_bgcolor="rgba(255, 255, 255, 0.9)",
    paper_bgcolor="rgba(255, 255, 255, 0.9)",
)

feedback_counts = df["feedback"].value_counts().reset_index()
feedback_counts.columns = ["feedback", "count"]

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    children=[
                        html.Img(
                            src="/assets/chart.svg",
                            style={"width": "70%", "display": "flex"},
                        ),
                    ],
                    style={"width": "50px", "gap": "10px"},
                ),
                html.H1("Dashboard"),
                
            ],
            style={
                "background": "#08306b",
                "color": "#FFF",
                "padding": "30px",
                "display": "flex",
            },
        ),
        
        html.Div(
            [
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=df["data"].min(),
                    max_date_allowed=df["data"].max(),
                    start_date=df["data"].min(),
                    end_date=df["data"].max(),
                ),
            ],
            style={"margin": "20px"},
        ),
    
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="respostas-por-dia",
                                    figure=px.line(
                                        df,
                                        x="data",
                                        y="respostas",
                                        title="Número de Respostas por Dia",
                                    ).update_layout(
                                        plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                        paper_bgcolor="rgba(255, 255, 255, 0.9)",
                                    ),
                                    style={
                                        "height": "400px",
                                        "width": "95%",
                                        "margin": "10px auto",
                                        "background-color": "#F8F8FF",
                                        "border-radius": "40px",
                                        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                        "transform": "translateY(-5px)",
                                    },
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="media-conversas-por-dia",
                                    figure=px.line(
                                        df,
                                        x="data",
                                        y="media_conversas_por_dia",
                                        title="Número Médio de Conversas por Dia",
                                    ).update_layout(
                                        plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                        paper_bgcolor="rgba(255, 255, 255, 0.9)",
                                    ),
                                    style={
                                        "height": "400px",
                                        "width": "95%",
                                        "margin": "10px auto",
                                        "background-color": "#F8F8FF",
                                        "border-radius": "40px",
                                        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                        "transform": "translateY(-5px)",
                                    },
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="mapa-origem",
                                    figure=px.choropleth(
                                        df,
                                        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
                                        locations="local",
                                        featureidkey="properties.name",
                                        color="total_interacoes",
                                        hover_name="local",
                                        title="Origem das Conversas por Estado (Brasil)",
                                        color_continuous_scale="Blues",
                                        scope="south america",
                                        center={"lat": -30, "lon": -58.9253},
                                    ).update_layout(
                                        plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                        paper_bgcolor="rgba(255, 255, 255, 0.9)",
                                    ),
                                    style={
                                        "height": "810px",
                                        "width": "95%",
                                        "margin": "10px auto",
                                        "background-color": "#F8F8FF",
                                        "border-radius": "40px",
                                        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                        "transform": "translateY(-5px)",
                                    },
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="tempo-medio-chat",
                                    figure=px.line(
                                        df,
                                        x="data",
                                        y="tempo_medio_chat",
                                        title="Tempo Médio de um Chat",
                                    ).update_layout(
                                        plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                        paper_bgcolor="rgba(255, 255, 255, 0.9)",
                                    ),
                                    style={
                                        "height": "400px",
                                        "width": "95%",
                                        "margin": "10px auto",
                                        "background-color": "#F8F8FF",
                                        "border-radius": "40px",
                                        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                        "transform": "translateY(-5px)",
                                    },
                                    config={"displayModeBar": False},
                                ),
                            ]
                        ),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [
                          html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            ("Tempo Médio de Conversa:"),
                            style={
                                "margin-top": "10px",
                                "margin-left": "10px",
                                "margin-right": "10px",
                                "margin-bottom": "10px",
                                "display": "flex",
                                "align-items": "center",
                                "justify-content": "center",
                                
                                
                            },
                        ),
                        html.Div(
                            f"{media_tempo_conversa:.2f} min",
                            style={"font-weight": "bold", "font-size":"30px"},
                        ),
                    ],
                    style={
                        "height": "192px",
                        "width": "90%",
                        "background-color": "#fefefc",
                        "border-radius": "20px",
                        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                        "transform": "translateY(-5px)",
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "flex-direction": "column",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            (f"Média de Mensagens por Conversa:"),
                            style={
                                "margin-top": "10px",
                                "margin-left": "20px",
                                "margin-right": "10px",
                                "margin-bottom": "10px",
                            },
                        ),
                        html.Div(
                            (f"{media_mensagens_por_conversa:.2f}"),
                            style={"font-weight": "bold", "font-size":"30px"},
                        ),
                    ],
                    style={
                        "height": "192px",
                        "width": "90%",
                        "background-color": "#fefefc",
                        "border-radius": "20px",
                        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                        "transform": "translateY(-5px)",
                        "border-radius": "20px",
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "flex-direction": "column",
                    },
                ),
            ],
            style={
            
                "margin-top": "5px",
                "display": "flex",
                "align-items": "center",
                "flex-direction": "column",
                "gap": "20px",
                "width":"100%"
            },
        ),
                        
                        dcc.Graph(
                            id="total-diario",
                            figure=px.bar(
                                df,
                                x="data",
                                y="respostas",
                                title="Total de Conversas por Dia",
                            ).update_layout(
                                plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                paper_bgcolor="rgba(255, 255, 255, 0.9)",
                            ),
                            style={
                                "height": "400px",
                                "width": "95%",
                                "margin": "10px auto",
                                "background-color": "#F8F8FF",
                                "border-radius": "40px",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                            },
                            config={"displayModeBar": False},
                        ),
                        dcc.Graph(
                            id="heatmap",
                            figure=heatmap_fig,
                            style={
                                "height": "400px",
                                "width": "95%",
                                "margin": "10px auto",
                                "border-radius": "40px",
                                "background-color": "#F8F8FF",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                            },
                            config={"displayModeBar": False},
                        ),
                        dcc.Graph(
                            id="demandas-dia-semana",
                            figure=px.bar(
                                df,
                                x="data",
                                y=["demanda_diaria", "demanda_semanal"],
                                title="Demandas por Dia e Semana",
                            ).update_layout(
                                plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                paper_bgcolor="rgba(255, 255, 255, 0.9)",
                            ),
                            style={
                                "height": "400px",
                                "width": "95%",
                                "margin": "10px auto",
                                "background-color": "#F8F8FF",
                                "border-radius": "40px",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                            },
                            config={"displayModeBar": False},
                        ),
                        html.Div(
                            html.Img(
                                src="/assets/wordcloud.png",
                                style={
                                    "width": "95%",
                                },
                            ),
                            style={
                                "height": "400px",
                                "width": "95%",
                                "background-color": "#fefefc",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                                "margin": "10px auto",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="total-interacoes",
                            figure=px.bar(
                                df,
                                x="data",
                                y="total_interacoes",
                                title="Total de Interações",
                            ).update_layout(
                                plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                paper_bgcolor="rgba(255, 255, 255, 0.9)",
                            ),
                            style={
                                "height": "400px",
                                "width": "31%",
                                "margin": "10px auto",
                                "background-color": "#F8F8FF",
                                "border-radius": "40px",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                            },
                            config={"displayModeBar": False},
                        ),
                        dcc.Graph(
                            id="avaliacao-conversa",
                            figure=px.bar(
                                df,
                                x="data",
                                y="avaliacao_conversa",
                                title="Avaliação da Conversa",
                            ).update_layout(
                                plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                paper_bgcolor="rgba(255, 255, 255, 0.9)",
                            ),
                            style={
                                "height": "400px",
                                "width": "31%",
                                "margin": "10px auto",
                                "background-color": "#F8F8FF",
                                "border-radius": "40px",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                            },
                            config={"displayModeBar": False},
                        ),
                        dcc.Graph(
                            id="feedback",
                            figure=px.bar(
                                feedback_counts,
                                x="feedback",
                                y="count",
                                title="Distribuição de Feedback",
                            ).update_layout(
                                plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                paper_bgcolor="rgba(255, 255, 255, 0.9)",
                            ),
                            style={
                                "height": "400px",
                                "width": "31%",
                                "margin": "10px auto",
                                "background-color": "#F8F8FF",
                                "border-radius": "40px",
                                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.2)",
                                "transform": "translateY(-5px)",
                            },
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={
                        "display": "flex",
                    },
                ),
            ]
        ),
    ]
)

@app.callback(
    [
        Output("respostas-por-dia", "figure"),
        Output("mapa-origem", "figure"),
        Output("media-conversas-por-dia", "figure"),
        Output("total-diario", "figure"),
        Output("tempo-medio-chat", "figure"),
        Output("total-interacoes", "figure"),
        Output("avaliacao-conversa", "figure"),
        Output("feedback", "figure"),
    ],
    [Input("date-picker", "start_date"), Input("date-picker", "end_date")]
)
def update_graphs(start_date, end_date):
    filtered_df = df[(df["data"] >= start_date) & (df["data"] <= end_date)]
    fig_respostas = px.line(
        filtered_df,
        x="data",
        y="respostas",
        title="Número de Respostas por Dia",
        color_discrete_sequence=["#636EFA"]
    )
    fig_respostas.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    fig_mapa = px.choropleth(
        filtered_df,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations="local",
        featureidkey="properties.name",
        color="total_interacoes",
        hover_name="local",
        title="Origem das Conversas por Estado (Brasil)",
        color_continuous_scale="Blues",
        scope="south america",
    )
    fig_mapa.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    fig_media_conversas = px.line(
        filtered_df,
        x="data",
        y="media_conversas_por_dia",
        title="Número Médio de Conversas por Dia",
    )
    fig_media_conversas.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    fig_total_diario = px.bar(
        filtered_df,
        x="data",
        y="respostas",
        title="Total de Conversas por Dia",
    )
    fig_total_diario.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )


    fig_tempo_medio_chat = px.line(
        filtered_df,
        x="data",
        y="tempo_medio_chat",
        title="Tempo Médio de um Chat",
    )
    fig_tempo_medio_chat.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    fig_total_interacoes = px.bar(
        filtered_df,
        x="data",
        y="total_interacoes",
        title="Total de Interações",
    )
    fig_total_interacoes.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    fig_avaliacao_conversa = px.bar(
        filtered_df,
        x="data",
        y="avaliacao_conversa",
        title="Avaliação da Conversa",
    )
    fig_avaliacao_conversa.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    feedback_counts = filtered_df["feedback"].value_counts().reset_index()
    feedback_counts.columns = ["feedback", "count"]

    fig_feedback = px.bar(
        feedback_counts,
        x="feedback",
        y="count",
        title="Distribuição de Feedback",
    )
    fig_feedback.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 0.9)",
        paper_bgcolor="rgba(255, 255, 255, 0.9)",
    )

    return (
        fig_respostas,
        fig_mapa,
        fig_media_conversas,
        fig_total_diario,
        fig_tempo_medio_chat,
        fig_total_interacoes,
        fig_avaliacao_conversa,
        fig_feedback,
    )
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
