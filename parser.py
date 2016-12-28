mport sys
import csv
import os

import urllib.request
from bs4 import BeautifulSoup  # Библиотека для парсинга.
# import re #  Импортируем библиотеку работы с регулярными выражениями

url_addr = 'https://www.weblancer.net/jobs/?page=165'


def get_html(url):
    # Функция для получения html по url.
    response = urllib.request.urlopen(url)
    return response.read()


def get_page_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find('ul', class_='pagination')
    return int(pagination.find_all('a')[-3].text)


def parse(html):
    '''Функция парсинга.'''
    soup = BeautifulSoup(html, "html.parser")
    # Обьект Soup'а, интерфейс к странице.
    table = soup.find('div', class_='container-fluid cols_table show_visited')
    '''Создаем объект table. Это метод файнд из супа
    с параметрами: тег контейнера и его имя.'''

    projects = []
    for row in table.find_all('div', class_='row'):
        #  В table методом find_all
        #  с параметрами по аналогии из выше ищем строки.
        cols = row.find_all('div')
        #  Создаем список словарей для объектов.
        projects.append({
            #  по ключу title записываем текст из тега а из cols[0]
            'title': cols[0].a.text,
            'category': cols[-1].a.text,
            'url': url_addr[:-10] + cols[0].find('a').get('href'),
            'price': cols[1].text.strip(),
            'application': cols[2].text.strip(),
            'added': cols[-1].find_all('span')[-2].text,
            })
    #     # print(cols)
    # for project in projects:
    #     print(project)
    return projects


def save(projects, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow((
            'Проект', 'Категории', 'Цена',
            'Заявки', 'Добавлен', 'Ссылка'
            ))

        for project in projects:
            writer.writerow((
                project['title'], project['category'],
                project['price'], project['application'],
                project['added'], project['url']
                ))


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=60):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def main():
    page_count = get_page_count(get_html(url_addr))

    print('Всего найдено страниц %d' % page_count)

    projects = []

    for page in range(1, page_count + 1):
        # print('Парсинг %d%%' % (page / page_count * 100))
        print_progress(page, page_count, 'Парсинг')
        projects.extend(parse(get_html(url_addr + '?page=%d' % page)))

    # for project in projects:
    #     print(project)
    path = os.getcwd()
    print('Результаты парсинга сохранены в %s\parsing.csv' % path)
    save(projects, 'parsing.csv')

if __name__ == '__main__':
    main()
