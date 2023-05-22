from dotenv import dotenv_values
from github import Github, UnknownObjectException
from link_proccessing import link_to_issue_data
from markdown_processsing import markdown_to_text
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from dash import Dash, html, dcc, Input, Output, State

import re
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Загрузка .env файла
config = dotenv_values(".env")

# Получение доступа к GitHub API
access_token = config["access_token"]
g = Github(access_token)

# Загрузка модели и создание классификатора
model_path = config["model"]
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Шаблон графика
template_df = pd.DataFrame(data={'label': ['bug', 'documentation', 'enhancement', 'question'],
                                 'score': [0.0, 0.0, 0.0, 0.0]})

fig_template = px.bar(template_df, x="score", y="label", template='plotly_white', title='Предложенные метки',
                      text_auto='.2p')
fig_template.update_layout(yaxis={'categoryorder': 'category descending'},
                           xaxis_range=[0, 1], autosize=True, hovermode=False, yaxis_title=None,
                           xaxis_title='Вероятность', margin=dict(pad=20), title_x=0.5)
fig_template.update_traces(hovertemplate="Метка: %{y} <br>Вероятность:  %{x}")
fig_template.update_xaxes(tickformat=',.2%')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Структура страницы макета
app.layout = html.Div([
    html.Div([
        html.H1("Github Issue теггер", className="py-2 ms-3 text-light"),
        html.Hr()
    ], className="bg-dark"),
    dbc.Row([
        dbc.Col(dbc.Input(id="link_input", type="url", placeholder="Введите ссылку на issue в Github-репозитории",
                          value="", className="ms-2"), md=9),
        dbc.Col(dbc.Button("Проанализировать", id="make_pred_button", className="btn-block", disabled=True, n_clicks=0),
                md=3, className="d-grid gap-2 px-3")
    ], className="g-1 d-flex justify-content-start"),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Markdown(id="markdown", className="text-wrap text-break mx-2 image-fluid"),
                md=8, align="start"),
        dbc.Col(dcc.Graph(id="label_output", figure=fig_template), md=4, align="start")
    ], align="center"),

    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Ошибка")),
        dbc.ModalBody("Данного issue или репозитория не существует")
    ], id="modal_failure", is_open=False)
])


# Функция отображения корректности ссылки
@app.callback(
    Output("link_input", "valid"),
    Output("link_input", "invalid"),
    Input("link_input", "value"),
)
def check_input(link):
    pattern = r'https:\/\/github\.com\/(.+)\/(.+)\/issues\/([0-9]+)'
    if link != "":
        if bool(re.match(pattern, link)):
            return True, False
        else:
            return False, True
    else:
        return False, False


# Функция разблокировки кнопки
@app.callback(
    Output("make_pred_button", "disabled"),
    Input("link_input", "valid")
)
def make_button_available(input_flag):
    if input_flag:
        return False
    else:
        return True


# Функция отображения markdown и графика
@app.callback(
    Output("markdown", "children"),
    Output("label_output", "figure"),
    Output("modal_failure", "is_open"),
    Input("make_pred_button", "n_clicks"),
    State("link_input", "value")
)
def show_markdown_and_plot(btn, link):
    # Считывание issue из репозитория
    pattern = r'https:\/\/github\.com\/(.+)\/(.+)\/issues\/([0-9]+)'
    if bool(re.match(pattern, link)):
        repo_address, issue_number = link_to_issue_data(link)
        # Проверка на существование репозитория
        try:
            repo = g.get_repo(repo_address)
        except UnknownObjectException:
            return "", fig_template, True

        # Проверка на существование issue
        try:
            issue = repo.get_issue(issue_number)
        except UnknownObjectException:
            return "", fig_template, True

        # Генерация markdown-текстов для показа и для анализа
        issue_title_to_show = "# " + issue.title
        markdown_text_show = [issue_title_to_show, issue.body]
        markdown_text_analyse = issue.title + ". " + issue.body + ". "

        comments_list = []
        comments = issue.get_comments()

        if comments.totalCount > 0:
            markdown_text_show.append("\n### Комментарии: \n\n")

        for comment in comments:
            comments_list.append(comment.body)

        for comment in comments_list:
            markdown_text_show.append(comment + "\n *** \n")
            markdown_text_analyse = markdown_text_analyse + comment + ". "

        # Преобразование markdown-текста в обычный
        text_analyse = markdown_to_text(markdown_text_analyse)

        # Получение предсказания
        pred = classifier(text_analyse, top_k=4, padding=True, truncation=True, max_length=512)
        pred_df = pd.DataFrame(pred)

        # Формирование гистограммы
        pred_df['color'] = pred_df['label'].map(
            {"bug": "#d73a4a", "documentation": "#0075ca", "enhancement": "#a2eeef", "question": "#d876e3"})

        fig = px.bar(pred_df, x="score", y="label", template='plotly_white', title='Предложенные метки',
                     text_auto='.2p')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_range=[0, 1], autosize=True,
                          yaxis_title=None, xaxis_title='Вероятность', margin=dict(pad=20), title_x=0.5)
        fig.update_traces(marker_color=pred_df.color, hovertemplate="Метка: %{y} <br>Вероятность:  %{x}")
        fig.update_xaxes(tickformat=',.2%')

        return markdown_text_show, fig, False
    return "", fig_template, False


if __name__ == '__main__':
    app.run_server(debug=True)
