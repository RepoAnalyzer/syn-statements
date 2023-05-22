import re


def link_to_issue_data(link):
    """
    Функция преобразования ссылки
    :param link: Ссылка на issue в GitHub
    :return: Адрес репозитория и номер issue
    """

    pattern = r'https:\/\/github\.com\/(.+)\/(.+)\/issues\/([0-9]+)'

    split_link = re.split(pattern, link)
    split_link = list(filter(lambda x: x != '', split_link))
    repo_path = split_link[0] + "/" + split_link[1]
    issue_number = int(split_link[2])

    return repo_path, issue_number
