import sys
import json
from datetime import datetime


def print_results():
    # читаем оба файла, проверяем наличие.
    try:
        with open('competitors2.json', 'r', encoding='utf-8') as f:
            competitors = json.load(f)
    except:
        sys.exit('competitors2.json не найден')

    try:
        with open('results_RUN.txt', 'r', encoding='utf-8-sig') as f:
            results = f.read().splitlines()
    except:
        sys.exit('results_RUN.txt не найден')

    # Dict comprehansions времени старта и финиша каждого бегуна.
    results_start = {s.split()[0]: s.split(' ', 1)[1:]
                     for s in results if s.split()[1] != 'finish'}
    results_finish = {s.split()[0]: s.split(' ', 1)[1:] for s in results}

    # Вычисление времени бега каждого бегуна.
    results_difference = dict()

    for key in results_start:
        start_time = datetime.strptime(results_start[key][0][-15:],
                                       '%H:%M:%S,%f')
        finish_time = datetime.strptime(results_finish[key][0][-15:],
                                        '%H:%M:%S,%f')
        results_difference[key] = str(finish_time - start_time)

    # Добавляем в словарь спортсменов рассчитанное время бега,
    # подрезаем время до сотых секунды.
    for key in list(competitors):
        if key in list(results_difference):
            competitors[key]['Result'] = results_difference[key][:-4]

    # Сортировка по времени бега.
    # Для сортировки преобразуем словавь в список и сортируем по значениям ключа Result.
    list_by_dict = list(competitors.items())
    list_by_dict.sort(key=lambda x: str(x[1][list(x[1].keys())[-1]]))
    # Составляем список с нагрудными номера спортсменов,
    # в порядке от пришедшего первым.
    sort_dict_key = [i[0] for i in list_by_dict]

    # Печать данных в консоль, согласно задания.
    for i in sort_dict_key:
        index = sort_dict_key.index(i)
        # Проверка наличия результатов забега.
        try:
            print(
                f'{index} {i} {competitors[str(i)]["Name"]}'
                f' {competitors[str(i)]["Surname"]}'
                f' {competitors[str(i)]["Result"]}')
        except:
            print(
                f'{index} {i} {competitors[str(i)]["Name"]}'
                f' {competitors[str(i)]["Surname"]}'
                f' в забеге участия не принимал(а)')


def main():
    print_results()


if __name__ == '__main__':
    main()
