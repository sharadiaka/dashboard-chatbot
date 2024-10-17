import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import numpy as np
import os

df = pd.read_csv("data/data.csv")
df.columns = df.columns.str.strip()

media_tempo_conversa = df["tempo_estimado_conversa"].mean()

minutos = int(media_tempo_conversa)
segundos = int((media_tempo_conversa - minutos) * 60)

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
                "background": "#f1f2f1",
                "color": "#000",
                "padding": "30px",
                "display": "flex",
            },
        ),

        html.Div(
            [
                html.H4("Filtros:"),
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=df["data"].min(),
                    max_date_allowed=df["data"].max(),
                    start_date=df["data"].min(),
                    end_date=df["data"].max(),
                    display_format='DD/MM/YYYY',
                    style={"heigth":"30px"}
                ),
        
                dcc.Dropdown(
                    id='local-dropdown',
                    options=[
                        {'label': local, 'value': local} for local in df['local'].unique()
                    ],
                    placeholder="Filtrar por estado",                   
                    multi=True,
                    style={ "min-width":"240px", "max-width":"400px","min-height":"49px"},
                ),
                
                dcc.Dropdown(
                    id='feedback-dropdown',
                    options=[
                        {'label': 'Neutro', 'value': 'neutro'},
                        {'label': 'Positivo', 'value': 'positivo'},
                        {'label': 'Negativo', 'value': 'negativo'},
                    ],
                    
                    placeholder="Filtrar por feedback",  
                    multi=True,
                    style={ "min-width":"240px", "max-width":"400px","min-height":"49px"},
                ),
            ],
            style={"margin": "20px", "gap":"10px", "display":"flex", "justify-content": "center", "align-items":"center"},
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
                            id="title_tempo_conversa",
                        ),
                        html.Div(
                            f"{minutos}:{segundos} min",
                            id="tempo_conversa",
                            style={"font-weight": "bold", "font-size":"30px"},
                        ),
                    ],
                     className="metrics_in_text",
                ),
                html.Div(
                    [
                        html.Div(
                            (f"Média de Mensagens por Conversa:"),
                            id ="title_media_msg_conversa",
                        ),
                        html.Div(
                            (f"{media_mensagens_por_conversa:.2f}"),
                            id ="media_msg_conversa",
                            style={"font-weight": "bold", "font-size":"30px"},
                        ),
                    ],
                    className="metrics_in_text",
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
                                y="numero_total_conversas",
                                title="Total de Conversas por Dia",
                            ).update_layout(
                                plot_bgcolor="rgba(255, 255, 255, 0.9)",
                                paper_bgcolor="rgba(255, 255, 255, 0.9)",
                            ),
                            config={"displayModeBar": False},
                        ),
                        dcc.Graph(
                            id="heatmap",
                            figure=heatmap_fig,
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
                            config={"displayModeBar": False},
                        ),
                        html.Div(
                            html.Img(
                                src="/assets/wordcloud.png",
                                style={
                                    "width": "95%",
                                },
                            ),
                            id = "word_cloud",
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
        Output("tempo_conversa", "children"),
        Output("media_msg_conversa", "children") 
    ],
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("local-dropdown", "value"),
        Input("feedback-dropdown", "value"),
    ]
)
def update_graphs(start_date, end_date, selected_local, feedback_value):
    filtered_df = df[(df["data"] >= start_date) & (df["data"] <= end_date)]
    
    if selected_local:
        filtered_df = filtered_df[filtered_df["local"].isin(selected_local)]
        
    if feedback_value:
         filtered_df = filtered_df[filtered_df["feedback"].isin(feedback_value)]

    media_tempo_conversa = filtered_df["tempo_estimado_conversa"].mean()
    minutos = int(media_tempo_conversa)
    segundos = int((media_tempo_conversa - minutos) * 60)
    media_mensagens_por_conversa = filtered_df["media_mensagens_por_conversa"].mean()

    # Agrupando os dados por data e local
    grouped_df = filtered_df.groupby("data").agg(
        respostas=('respostas', 'sum'),
        media_conversas_por_dia=('media_conversas_por_dia', 'mean'),
        tempo_medio_chat=('tempo_medio_chat', 'mean'),
        total_interacoes=('total_interacoes', 'sum'),
        avaliacao_conversa=('avaliacao_conversa', 'mean'),
        numero_total_conversas=('numero_total_conversas', 'sum'),
    ).reset_index()

    # Criando as figuras
    fig_respostas = px.line(
        grouped_df,
        x="data",
        y="respostas",
        title="Número de Respostas por Dia",
        color_discrete_sequence=["#636EFA"]
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

    fig_media_conversas = px.line(
        grouped_df,
        x="data",
        y="media_conversas_por_dia",
        title="Número Médio de Conversas por Dia",
    )

    fig_total_diario = px.bar(
        grouped_df,
        x="data",
        y="numero_total_conversas",
        title="Total de Conversas por Dia",
    )

    fig_tempo_medio_chat = px.line(
        grouped_df,
        x="data",
        y="tempo_medio_chat",
        title="Tempo Médio de um Chat",
    )

    fig_total_interacoes = px.bar(
        grouped_df,
        x="data",
        y="total_interacoes",
        title="Total de Interações",
    )

    fig_avaliacao_conversa = px.bar(
        grouped_df,
        x="data",
        y="avaliacao_conversa",
        title="Avaliação da Conversa",
    )

    feedback_counts = filtered_df["feedback"].value_counts().reset_index()
    feedback_counts.columns = ["feedback", "count"]

    fig_feedback = px.bar(
        feedback_counts,
        x="feedback",
        y="count",
        title="Distribuição de Feedback",
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
        f"{minutos}:{segundos} min",
        f"{media_mensagens_por_conversa:.2f}"
    )

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
