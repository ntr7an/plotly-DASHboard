import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc

pio.templates.default = "plotly_white"

try:
    df = pd.read_csv('global_alcohol_consumption.csv')
except FileNotFoundError:
    print("Файл 'global_alcohol_consumption.csv' не найден. Пожалуйста, проверьте путь к файлу.")
    exit()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

HEADER_STYLE = {
    'textAlign': 'center',
    'fontFamily': 'Helvetica, Arial, sans-serif',
    'fontSize': '30px',
    'fontWeight': 'bold',
    'marginTop': '20px',
    'marginBottom': '30px',
    'color': '#555'
}

SECTION_TITLE_STYLE = {
    'marginTop': '20px',
    'marginBottom': '15px',
    'color': '#333'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#007bff'
}

app.layout = dbc.Container(fluid=True, style={'backgroundColor': '#f4f4f4', 'padding': '20px'}, children=[
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Цель дашборда:", style=SECTION_TITLE_STYLE),
                html.P("Проанализировать глобальные тенденции потребления алкоголя, выявить ключевые факторы и представить данные в интерактивном формате.", style={'fontSize': '1.1em'}),
                html.H4("Задачи дашборда:", style=SECTION_TITLE_STYLE),
                html.Ul([
                    html.Li("Отобразить общее потребление алкоголя на душу населения по странам и континентам."),
                    html.Li("Сравнить потребление различных типов напитков и их ценовые категории."),
                    html.Li("Проследить динамику потребления алкоголя по годам и выявить тренды."),
                    html.Li("Обеспечить возможность фильтрации данных для детального анализа по континентам, типам напитков, крепости и годам.")
                ], style={'fontSize': '1.1em', 'listStylePosition': 'outside', 'paddingLeft': '20px'})
            ], style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '5px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=12, className="mb-4")
    ]),

    dbc.Row([
        dbc.Col(html.H1("Глобальный Анализ Потребления Алкоголя", style=HEADER_STYLE), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Панель фильтров", className="my-0", style={'fontWeight':'bold'})),
                dbc.CardBody([
                    html.Label("Выберите континент:", style={'fontWeight': 'bold', 'marginTop': '10px'}),
                    dcc.Dropdown(
                        id='continent-dropdown',
                        options=[{'label': i, 'value': i} for i in sorted(df['Continent'].unique())],
                        value=None,
                        placeholder="Все континенты",
                        style={'marginBottom': '15px'}
                    ),
                    html.Label("Выберите типы напитков:", style={'fontWeight': 'bold'}),
                    dcc.Checklist(
                        id='beverage-checklist',
                        options=[{'label': i, 'value': i} for i in sorted(df['Beverage'].unique())],
                        value=sorted(df['Beverage'].unique()),
                        labelStyle={'display': 'block', 'marginBottom': '5px'},
                        style={'marginBottom': '15px', 'paddingLeft': '5px'}
                    ),
                    html.Label("Выберите крепость напитка:", style={'fontWeight': 'bold'}),
                    dcc.RadioItems(
                        id='strength-radioitems',
                        options=[{'label': 'Все крепости', 'value': 'All_Strengths'}] + [{'label': i, 'value': i} for i in sorted(df['Alcohol_Strength'].unique())],
                        value='All_Strengths',
                        labelStyle={'display': 'inline-block', 'marginRight': '10px', 'marginBottom': '5px'},
                        style={'marginBottom': '15px'}
                    ),
                    html.Label("Выберите год:", style={'fontWeight': 'bold'}),
                    dcc.Slider(
                        id='year-slider',
                        min=df['Year'].min(),
                        max=df['Year'].max(),
                        step=1,
                        marks={str(year): {'label': str(year), 'style': {'fontSize': '0.9em'}} for year in df['Year'].unique()},
                        value=df['Year'].min(),
                    )
                ], style={'padding': '20px'})
            ], className="shadow-sm")
        ], md=3, style={'paddingRight': '15px'}),

        dbc.Col([
            html.H5("Панель визуализации", style=SECTION_TITLE_STYLE),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Суммарное потребление (л/чел)", style={'fontWeight':'bold'}),
                    dbc.CardBody(html.H4(id='total-consumption-card', className="card-title", style=CARD_TEXT_STYLE))
                ], className="text-center shadow-sm mb-3"), md=4),
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Средняя цена (за литр)", style={'fontWeight':'bold'}),
                    dbc.CardBody(html.H4(id='avg-price-card', className="card-title", style=CARD_TEXT_STYLE))
                ], className="text-center shadow-sm mb-3"), md=4),
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Уникальных стран в выборке", style={'fontWeight':'bold'}),
                    dbc.CardBody(html.H4(id='unique-countries-card', className="card-title", style=CARD_TEXT_STYLE))
                ], className="text-center shadow-sm mb-3"), md=4)
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id='bar-chart'), className="shadow-sm"), md=6, className="mb-3"),
                dbc.Col(dbc.Card(dcc.Graph(id='pie-chart'), className="shadow-sm"), md=6, className="mb-3")
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id='scatter-plot'), className="shadow-sm"), md=6, className="mb-3"),
                dbc.Col(dbc.Card(dcc.Graph(id='line-chart-dynamic'), className="shadow-sm"), md=6, className="mb-3")
            ])
        ], md=9)
    ], className="mt-4")
])

@app.callback(
    [Output('total-consumption-card', 'children'),
     Output('avg-price-card', 'children'),
     Output('unique-countries-card', 'children'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('line-chart-dynamic', 'figure')],
    [Input('continent-dropdown', 'value'),
     Input('beverage-checklist', 'value'),
     Input('strength-radioitems', 'value'),
     Input('year-slider', 'value')]
)
def update_dashboard(selected_continent, selected_beverages, selected_strength, selected_year):
    filtered_df = df.copy()

    if selected_continent:
        filtered_df = filtered_df[filtered_df['Continent'] == selected_continent]

    if selected_beverages:
        filtered_df = filtered_df[filtered_df['Beverage'].isin(selected_beverages)]
    else:
        filtered_df = pd.DataFrame(columns=df.columns)

    if selected_strength and selected_strength != 'All_Strengths':
        filtered_df = filtered_df[filtered_df['Alcohol_Strength'] == selected_strength]

    filtered_df_for_year_specific_viz = filtered_df[filtered_df['Year'] == selected_year]
    
    empty_fig_layout = {
        'xaxis': {'visible': False},
        'yaxis': {'visible': False},
        'annotations': [{'text': 'Нет данных для выбранных фильтров', 'xref': 'paper', 'yref': 'paper', 'showarrow': False, 'font': {'size': 16, 'color':'#888'}}],
        'paper_bgcolor': 'rgba(255,255,255,0.8)',
        'plot_bgcolor': 'rgba(255,255,255,0.8)'
    }
    empty_fig = {'data': [], 'layout': empty_fig_layout}

    if filtered_df_for_year_specific_viz.empty:
        return "N/A", "N/A", "N/A", empty_fig, empty_fig, empty_fig, empty_fig

    total_consumption = f"{filtered_df_for_year_specific_viz['Consumption_Liters_Per_Capita'].sum():.2f}"
    avg_price = f"{filtered_df_for_year_specific_viz['Avg_Price_Per_Liter'].mean():.2f}" if not filtered_df_for_year_specific_viz['Avg_Price_Per_Liter'].empty else "N/A"
    unique_countries = filtered_df_for_year_specific_viz['Country'].nunique()

    bar_data = filtered_df_for_year_specific_viz.groupby('Beverage', as_index=False)['Consumption_Liters_Per_Capita'].mean()
    if not bar_data.empty:
        bar_fig = px.bar(
            bar_data,
            x='Beverage', y='Consumption_Liters_Per_Capita',
            title=f'Среднее потребление по типу напитка в {selected_year}',
            labels={'Beverage': 'Тип напитка', 'Consumption_Liters_Per_Capita': 'Среднее потребление (л/чел)'},
            color='Beverage',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        bar_fig.update_layout(title_x=0.5, margin=dict(t=60, b=20, l=40, r=20), paper_bgcolor='white', plot_bgcolor='white', legend_title_text='Напиток')
    else:
        bar_fig = {'data':[], 'layout': {**empty_fig_layout, 'title': f'Среднее потребление по типу напитка в {selected_year} (Нет данных)', 'title_x':0.5}}

    pie_data = filtered_df_for_year_specific_viz.groupby('Continent', as_index=False)['Consumption_Liters_Per_Capita'].sum()
    if not pie_data.empty and pie_data['Consumption_Liters_Per_Capita'].sum() > 0:
        pie_fig = px.pie(
            pie_data,
            names='Continent', values='Consumption_Liters_Per_Capita',
            title=f'Распределение потребления по континентам в {selected_year}',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel1
        )
        pie_fig.update_traces(textinfo='percent+label', pull=[0.03] * len(pie_data['Continent'].unique()))
        pie_fig.update_layout(title_x=0.5, margin=dict(t=60, b=20, l=20, r=20), paper_bgcolor='white', plot_bgcolor='white', legend_title_text='Континент')
    else:
        pie_fig = {'data':[], 'layout': {**empty_fig_layout, 'title': f'Распределение потребления по континентам в {selected_year} (Нет данных)', 'title_x':0.5}}
    
    if not filtered_df_for_year_specific_viz.empty:
        scatter_fig = px.scatter(
            filtered_df_for_year_specific_viz,
            x='Avg_Price_Per_Liter', y='Consumption_Liters_Per_Capita',
            color='Beverage',
            size='Consumption_Liters_Per_Capita',
            hover_name='Country',
            title=f'Потребление vs Цена (за литр) в {selected_year}',
            labels={'Avg_Price_Per_Liter': 'Средняя цена (за литр)', 'Consumption_Liters_Per_Capita': 'Потребление (л/чел)', 'Beverage': 'Тип напитка'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        scatter_fig.update_layout(title_x=0.5, margin=dict(t=60, b=20, l=40, r=20), paper_bgcolor='white', plot_bgcolor='white', legend_title_text='Напиток')
    else:
        scatter_fig = {'data':[], 'layout': {**empty_fig_layout, 'title': f'Потребление vs Цена (за литр) в {selected_year} (Нет данных)', 'title_x':0.5}}

    line_df_dynamic = filtered_df.groupby('Year', as_index=False)['Consumption_Liters_Per_Capita'].mean()
    if not line_df_dynamic.empty and len(line_df_dynamic) > 1:
        line_fig_dynamic = px.line(
            line_df_dynamic,
            x='Year', y='Consumption_Liters_Per_Capita',
            title='Динамика среднего потребления по годам',
            markers=True,
            labels={'Year': 'Год', 'Consumption_Liters_Per_Capita': 'Среднее потребление (л/чел)'},
            color_discrete_sequence=["#007bff"]
        )
        line_fig_dynamic.update_layout(title_x=0.5, margin=dict(t=60, b=20, l=40, r=20), paper_bgcolor='white', plot_bgcolor='white')
        line_fig_dynamic.update_xaxes(type='category')
    else:
        line_fig_dynamic = {'data':[], 'layout': {**empty_fig_layout, 'title': 'Динамика среднего потребления по годам (Нет данных или недостаточно данных)', 'title_x':0.5}}
    
    return total_consumption, avg_price, unique_countries, bar_fig, pie_fig, scatter_fig, line_fig_dynamic

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
