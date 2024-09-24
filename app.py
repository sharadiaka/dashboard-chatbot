import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()

app = dash.Dash(__name__)

if not os.path.exists('assets'):
    os.makedirs('assets')

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['palavras_mais_usadas']))
wordcloud.to_file('assets/wordcloud.png')

app.layout = html.Div(children=[
    html.H1('Dashboard do Chatbot'),
    
    dcc.Graph(id='respostas-por-dia', figure=px.line(df, x='data', y='respostas', title='Número de Respostas por Dia')),
    
    dcc.Graph(id='media-conversas-por-dia', figure=px.line(df, x='data', y='media_conversas_por_dia', title='Número Médio de Conversas por Dia')),

    dcc.Graph(id='mapa-origem', figure=px.bar(df, x='local', y='total_interacoes', title='Origem das Conversas')),
    
    dcc.Graph(id='total-diario', figure=px.bar(df, x='data', y='respostas', title='Total de Conversas por Dia')),
    
    dcc.Graph(id='feedback', figure=px.pie(df, names='feedback', title='Distribuição de Feedback')),

    html.Img(src='/assets/wordcloud.png', style={'height': '400px'}),

    dcc.Graph(id='demandas-dia-semana', figure=px.bar(df, x='data', y=['demanda_diaria', 'demanda_semanal'], title='Demandas por Dia e Semana')),

    dcc.Graph(id='avaliacao-conversa', figure=px.bar(df, x='data', y='avaliacao_conversa', title='Avaliação da Conversa')),

    html.H3(f"Total de Conversas: {df['numero_total_conversas'].sum()}"),

    dcc.Graph(id='media-mensagens-por-conversa', figure=px.bar(df, x='data', y='media_mensagens_por_conversa', title='Média de Mensagens por Conversa')),

    dcc.Graph(id='tempo-estimado-conversa', figure=px.line(df, x='data', y='tempo_estimado_conversa', title='Tempo Estimado de Conversa')),

    dcc.Graph(id='tempo-medio-chat', figure=px.line(df, x='data', y='tempo_medio_chat', title='Tempo Médio de um Chat')),
    
    dcc.Graph(id='total-interacoes', figure=px.bar(df, x='data', y='total_interacoes', title='Total de Interações')),

    dcc.Graph(id='acuracia-respostas', figure=px.bar(df, x='data', y='acuracia_respostas', title='Acurácia das Respostas')),
])

if __name__ == '__main__':
    app.run_server(debug=True)
