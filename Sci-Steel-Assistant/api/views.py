import json
import time
import pandas as pd
import numpy as np
import datetime
# from statsmodels.tsa.holtwinters import ExponentialSmoothing
# from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from sklearn.linear_model import LinearRegression
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from navigate.core import (get_all_selected_documents, get_entity_by_name,
                           get_related_entities_names,
                           get_selected_documents_id,
                           get_session_id,
                           get_all_countries,
                           get_all_orgs,
                           get_all_persons,
                           get_all_mails,
                           get_abstract
                           )
from navigate.models import (
    AIQuery, Folder, MainDoc, NoteItem, Org, DocumentMetaData, ProcessedDocuments
)
from navigate.tools import (
    read_stop_word_list, serialize_int_list_to_string, make_word_cloud,
)
import navigate.cache as navigate_cache

from .serializers import (AIQueryListSerializer, AIQueryUpdateSerializer,
                          MainDocSerializer, OrgSerializer)
from navigate.validators import validate_year
from navigate.workers import search_result_to_folder_worker
from navigate.threads import start_thread, get_threads_count, clean_threads, _shutdown_cleanup_worker
from navigate.search import (
    get_tracking_topic_documents, get_tracking_topic_documents, get_doc_date, unpack_tracking_topic_search_result,
    get_publications_time_series, search_by_note_category
)
from navigate.tools import get_queryset_from_cache


class AIQueryViewSet(viewsets.ModelViewSet):
    """Эндпоинт запросов к диалогам с ИИ-ассистентам."""

    queryset = AIQuery.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AIQueryListSerializer
        elif self.action == 'update' or self.action == 'partitial_update':
            return AIQueryUpdateSerializer
        return AIQueryListSerializer


class MainDocViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт основных документов."""

    queryset = MainDoc.objects.using('navigate').all()
    serializer_class = MainDocSerializer


class OrgViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт организаций."""

    queryset = Org.objects.using('navigate').all()
    serializer_class = OrgSerializer


@require_POST
@csrf_exempt
def api_update_checkbox(request):
    """Помещает или исключает документ в/из папки с отобранными."""
    try:
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        doc_type = data.get('id')[:4]

        if doc_type == 'mdid':
            FolderClass = get_entity_by_name('Folder')
        elif doc_type == 'odid':
            FolderClass = get_entity_by_name('SelectedOrgFolder')
        else:
            return JsonResponse({"error": "Не определен тип выделенного документа."}, status=404)

        document_id = int(data.get('id')[4:])
        is_document_selected = data.get('checked')
        current_session_id = request.session.session_key
        if is_document_selected:
            if current_session_id:
                if FolderClass.objects.filter(session_id=current_session_id, doc_id=document_id).count() == 0:
                    FolderClass.objects.create(session_id=current_session_id, doc_id=document_id)
                else:
                    # документ уже добавлен в рамках сессии
                    pass
            else:
                print('Ошибка: сессия не инициализирована.')
        else:
            try:
                item = FolderClass.objects.get(session_id=current_session_id, doc_id=document_id)
                item.delete()
            except Exception as error:
                print(f'Ошибка при удалении документа из папки: {str(error)}')
        return JsonResponse({"status": "ok"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error JSON - invalid json"}, status=400)


@require_POST
@csrf_exempt
def api_all_to_folder(request):
    """Помещает все найденные документы в отобранные."""
    start_time = time.time()
    try:
        # print('Данные request: ', request.META.get('HTTP_REFERER'))
        HTTP_referer_URL = request.META.get('HTTP_REFERER')
        entity_name = None
        if 'entities' in HTTP_referer_URL:
            entity_name = HTTP_referer_URL[HTTP_referer_URL.find('entities')+9:HTTP_referer_URL.find('?')]

        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        search_string = data.get('search_string')
        search_result_count = int(data.get('search_result_count'))
        category_filter = data.get('search_filter')
        if category_filter == '':
            category_filter_list = None
        else:
            category_filter = category_filter[1:len(category_filter)-1]
            category_filter_list = category_filter.split(', ')

        try:
            search_from = validate_year(int(data.get('search_from', '0')))
        except Exception:
            search_from = 0
        try:
            search_to = validate_year(int(data.get('search_to', '0')))
        except Exception:
            search_to = 0

        current_session_id = request.session.session_key

        print(f'time before search: {str(time.time()-start_time)}')

        start_thread(
            search_result_to_folder_worker,
            args=None,
            kwargs={
                'current_session_id': current_session_id,
                'search_string': search_string,
                'expected_search_result_count': search_result_count,
                'category_filter_list': category_filter_list,
                'entity_name': entity_name,
                'search_from': search_from,
                'search_to': search_to
            })

        print(f'time all view: {str(time.time()-start_time)}')

        return JsonResponse({"status": "ok"})

    except Exception as error:
        return JsonResponse({"error": str(error)}, status=400)


#######################################################################################################################

def parse_edges(edges_list):
    """Возвращает список выбранных ребер для построения графа."""
    result = []
    for pair in edges_list:
        node_from, node_to = pair.split(' - ')
        result.append((settings.GRAPH_NODE_OPTIONS_MAPPING[node_from], settings.GRAPH_NODE_OPTIONS_MAPPING[node_to]))
    return result


@require_POST
@csrf_exempt
def construct_graph_by_settings(request):
    """Построение графа по настройкам, переданным через запрос."""

    session_id = get_session_id(request)
    main_docs_in_folder_ids = get_selected_documents_id(session_id)

    # получаем список стоп-слов
    stop_word_list = read_stop_word_list()

    try:
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        nodes_list = data.get('nodes')
        edges_list = parse_edges(data.get('edges'))

        print(f'ребра графа = связи между сущностями: {edges_list}')

    except Exception as error:
        print(f'Произошла ошибка при построении графа: {error}')
        return JsonResponse({"error": "400"}, status=400)

    nodes_result = []
    edges_result = []

    node_colors = {
        'Person': '#00baff',
        'Org': '#8e8e8e',
        'Country': '#0082b2',
        'Contact': '#c4c4c4',
        'Keyword': '#53cfcb',
        'MainDoc': '#0000ff'
    }
    node_current_index = 0
    did_entity_nids = dict()

    for main_doc_id in main_docs_in_folder_ids:
        did_entity_nids[main_doc_id] = dict()

        # обход сущностей для формирования вершин графа.
        for node_entity in nodes_list:
            did_entity_nids[main_doc_id][node_entity] = []

            # получение экземпляров сущностей (записи в БД СИПАД, например, персоны, организации и т.д.)
            if node_entity == 'MainDoc':
                # выбраны документы.
                entity_instances = MainDoc.objects.using('navigate').filter(pk=main_doc_id)
            else:
                # выбраны иные сущности.
                entity_class = get_entity_by_name(node_entity)
                params_dict = {node_entity.lower()+'ref__doc': main_doc_id}
                entity_instances = entity_class.objects.using('navigate').filter(**params_dict)

            # обход отобранных экземпляров сущностей (документов БД СИПАД, например персоны, объекты и т.д.)
            for entity_instance in entity_instances:

                # Проверки - добавлять ли вершину.
                if str(entity_instance).lower() in stop_word_list:
                    # если сущность в списке стоп-слов, пропускаем ее (важно для ключевых слов)
                    continue

                if str(entity_instance).isdigit():
                    # пропуск сущностей из цифр
                    continue

                # ищем, добавлена ли уже такая вершина
                current_node_name = str(entity_instance) if node_entity != 'MainDoc' else str(f'D{entity_instance.pk}')
                is_added = False
                for node in nodes_result:
                    if node['label'] == current_node_name:
                        is_added = True
                        did_entity_nids[main_doc_id][node_entity].append(node['id'])
                        break

                # добвляем вершину
                if not is_added:
                    nodes_result.append(
                        {
                            'id': node_current_index,
                            'label': current_node_name,
                            'type': node_entity,
                            'color': node_colors[node_entity],
                            'shape': 'dot',
                        }
                    )
                    did_entity_nids[main_doc_id][node_entity].append(node_current_index)
                    node_current_index += 1

    # формирование ребер
    for entity_from, entity_to in edges_list:  # проходим по парам сущностей для связывания
        if entity_from == entity_to:
            pass
    #         # добавление связей между равными сущностями - перебираем пары вершин и связываем одинаковые
    #         for node_1 in nodes_result:
    #             for node_2 in nodes_result:
    #                 if (node_1['type'] == node_2['type'] == entity_from
    #                    and node_1['label'] == node_2['label'] and node_1 != node_2):
    #                     if (node_1['id'], node_2['id']) not in pairs and (node_2['id'], node_1['id']) not in pairs:
    #                         edges_result.append(
    #                             {
    #                                 'from': node_1['id'],
    #                                 'to': node_2['id']
    #                             }
    #                         )
    #                         pairs.add(
    #                             (node_1['id'], node_2['id'])
    #                         )
        else:
            for main_doc_id in main_docs_in_folder_ids:  # проходим по всем документам
                # получаем список документов указанной сущности для данного документа
                entity_from_instances_nid_list = did_entity_nids[int(main_doc_id)][entity_from]
                entity_to_instances_nid_list = did_entity_nids[int(main_doc_id)][entity_to]
                print((f'для документа {main_doc_id} нужно связать ноды'
                       f' {entity_from_instances_nid_list} с нодами {entity_to_instances_nid_list}'))

                for nid_1 in entity_from_instances_nid_list:
                    for nid_2 in entity_to_instances_nid_list:
                        if (nid_1 != nid_2 and {'from': nid_2, 'to': nid_1} not in edges_result
                           and {'from': nid_1, 'to': nid_2} not in edges_result):
                            edges_result.append(
                                {
                                    'from': nid_1,
                                    'to': nid_2
                                }
                            )

    # if main_document_doc_id != entity_instance.pk:
    #     edges_result.append(
    #         {
    #             'from': main_document_doc_id,
    #             'to': entity_instance.pk
    #         }
    #     )
    # print('------------------------ nodes')
    # print(nodes_result)
    # print('------------------------ edges')
    # print(edges_result)
    return JsonResponse(
        {
            "status": "ok",
            "nodes": nodes_result,
            "edges": edges_result,
        }
    )


@require_POST
@csrf_exempt
def api_translate(request):
    """Переводит фрагмент на русский язык."""
    # from navigate.views import get_completion, get_messages
    # from navigate.models import AIQuery
    print('TRANSLATE')
    raw_data = request.body.decode('utf-8')
    json_data = json.loads(raw_data)
    print(json_data)
    fragments = json_data.get('fragments')
    results = [{'id': fragment.get('id'), 'text': f'-{fragment.get("text")}-'} for fragment in fragments]

    ai_query = AIQuery(session_id='system', author=request.user, prompt='translate', temperature=0.1)
    ai_query.save()
    time.sleep(1)
    # get_completion(
    #     ai_query, get_messages('translate', {'$DATA$': data}), deepresearch_id=ai_query.pk, delay=0.5)
    tr_queries = AIQuery.objects.filter(deepresearch_id=ai_query.pk)
    if tr_queries:
        tr_queries.delete()
    ai_query.delete()
    # traslated_data = f"<emt>{truduction}</emt>"
    
    response_data = {'results': results}
    print(response_data)
    return JsonResponse(response_data)

    return JsonResponse({
        'status': 'ok',
        'data': data,
        'translated': traslated_data,
        'uuid': uuid,
    })


@require_POST
@csrf_exempt
def api_folder_action(request):
    """Очищает список отобранных документов."""
    def trunc_stats(x: str) -> str:
        """Выделяет из строкового представления сущность и наименование."""
        entities_map = {
            'countries': 'Country',
            'orgs': 'Org',
            'persons': 'Person',
            'mails': 'Mail',
            'keywords': 'Keyword'
        }
        x = x[6:]
        entity_class, entity_name = entities_map[x[0:x.find('_')]], x[x.find('_') + 1:]
        return entity_class, entity_name

    filters = {
        'Country': [],
        'Org': [],
        'Person': [],
        'Mail': [],
        'Keyword': []
    }

    try:
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        command = data.get('command')
        print('command: ', command)

        # получение отобранных документов
        current_session_id = request.session.session_key
        selected_docs = Folder.objects.filter(session_id=current_session_id)

        if command == 'clear':
            selected_docs.delete()

        elif command in ('filter', 'addnote'):
            # получение фильтров / заметок в блокнот
            selected_entities = list(map(trunc_stats, data.get('data')))
            notes = []
            for filter in selected_entities:
                filters[filter[0]].append(filter[1])
                notes.append(filter[1])

            # формирование множеств по каждой сущности
            for entity in filters.keys():
                filters[entity] = set(filters[entity])

            if command == 'filter':
                # получение отобранных документы
                docs_in_folder = get_all_selected_documents(request=request)

                # фильтрация отобранных документов
                need_to_add = []
                for doc in docs_in_folder:
                    is_doc_mathes_filters = True
                    doc_entities = get_related_entities_names(doc)
                    for entity in filters.keys():
                        is_doc_mathes_filters = ((filters[entity] & doc_entities[entity] == filters[entity])
                                                 and is_doc_mathes_filters)
                    if is_doc_mathes_filters:
                        need_to_add.append(doc.pk)

                # очистка папки
                selected_docs.delete()

                # добавление в папку отфильтрованных документов
                items_to_create = [Folder(session_id=current_session_id, doc_id=document_id)
                                   for document_id in need_to_add]
                Folder.objects.bulk_create(items_to_create)
            elif command == 'addnote':
                print(notes)
                items_to_create = [NoteItem(
                    author=request.user,
                    text=item_text) for item_text in notes]
                NoteItem.objects.bulk_create(items_to_create)

        return JsonResponse({"status": "ok"})

    except Exception as error:
        return JsonResponse({"error": str(error)}, status=400)


@require_POST
@csrf_exempt
def api_action_notes(request):
    """Действия с заметками в блокноте."""
    try:
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        command = data.get('command')

        # получение отобранных документов
        current_session_id = request.session.session_key
        selected_docs = NoteItem.objects.filter(session_id=current_session_id)

        if command == 'clear':
            selected_docs.delete()

        return JsonResponse({"status": "ok"})

    except Exception as error:
        return JsonResponse({"error": str(error)}, status=400)


def api_get_notes(request):
    """Получение списка заметок."""
    print('gettng notes... ')
    # получение заметок
    current_session_id = request.session.session_key
    selected_docs = NoteItem.objects.filter(author=request.user)
    notes_list = [doc.text for doc in selected_docs]
    notes_id = [doc.pk for doc in selected_docs]

    return JsonResponse(
        {
            "notes": notes_list,
            "id": notes_id
        },
        status=200
    )


def get_max_sequence(ts):
    """Возвращает длинну максимальной возрастающей последовательости, точку ее начала и рост относительно среднего."""
    # получаем последовательность дифференциала ряда в каждой точке.
    df = pd.DataFrame({'value': list(np.diff(ts).tolist())})

    # создаем маску для польжительных чисел
    positive_mask = df['value'] > 0

    # создаем группы. Каждое изменение
    groups = positive_mask.ne(positive_mask.shift()).cumsum()

    # фильтруем оставляя только положительные значения и их группы
    positive_groups = df[positive_mask].copy()

    # добавляем столбец для группировки
    positive_groups['group'] = groups[positive_mask]

    # группируем и считаем размер последовательности
    sequence_counts = positive_groups.groupby('group').size().reset_index(name='count')
    if sequence_counts['count'].count() == 0:
        return 0, 0, 0
    longest_sequence_group = sequence_counts.loc[sequence_counts['count'].idxmax(), 'group']  # noqa
    start_index = positive_groups.query(f'group == @longest_sequence_group').index.min()
    growth = ts.iloc[start_index + sequence_counts['count'].max()] * 100 / ts.mean()

    return sequence_counts['count'].max(), start_index, growth


def is_trend_now(positive_sequence_start_date: str, length: int):
    """Возвращает True, если период роста тренда затрагивает текущий месяц (+1)."""
    if '-' not in positive_sequence_start_date:
        return False
    print(positive_sequence_start_date)
    month_component, year_component = positive_sequence_start_date.split('-')
    fin_date = datetime.datetime(
        year=int(year_component),
        month=int(month_component),
        day=1) + datetime.timedelta(days=31 * (length + 1))
    return fin_date > datetime.datetime.now()


def start_fin_analisys(data):
    # Анализ начала и конца ряда
    message = ''
    message += f"Сравнение начала и конца ряда:<br>"
    message += f"   Среднее за первые 3 месяца: {np.mean(data[:3]):.1f}<br>"
    message += f"   Среднее за последние 3 месяца: {np.mean(data[-3:]):.1f}<br>"

    change = ((np.mean(data[-3:]) - np.mean(data[:3])) / np.mean(data[:3])) * 100
    message += f"   Изменение: {change:.1f}%<br>"
    message += "   Интерпретация результатов<br>"
    if change > 10:
        message += "   ЗНАЧИТЕЛЬНЫЙ РОСТ<br>"
    elif change < -10:
        message += "   ЗНАЧИТЕЛЬНОЕ СНИЖЕНИЕ<br>"
    else:
        message += "   СТАБИЛЬНАЯ СИТУАЦИЯ (без резких изменений)<br>"
    return message


def calc_tail_abs_trend(time_series_of_publications: list):
    """Проверяет наличие выброса в конце временного ряда.

    Входные параметры:
    time_series_of_publications: временной ряд публикаций.

    Возвращает:
        - Показатель числа публикаций относительно среднего уровня (без учета нулевых значений)
        в процентах в последний месяц.
    """
    ts_drop_zeros = [item for item in time_series_of_publications if item != 0]
    ts = pd.Series(ts_drop_zeros)
    mean_value = ts.mean()
    return float(ts.iloc[-1] * 100 / mean_value)


def check_tail_trend(time_series_of_publications: list, alpha: float = 0.05, period: int = 3):
    """Проверяет наличие растущего тренда в конце рассматриваемого периода временного ряда.

    Входные параметры:
    time_series_of_publications: временной ряд публикаций.
    alpha: коэффициент экспоненциального сглаживания
    period: рассматриваемый период в конце временного ряда в месяцах.

    Возвращает:
        кортеж (
            процентный рост относительно среднего значения временного ряда,
            признак непрерывного роста в конце периода
        )
    """
    # Преобразуем в pandas.Series
    ts = pd.Series(time_series_of_publications)
    # экспоненциальное сглаживание
    smoothed = ts.ewm(alpha=alpha).mean()
    smoothed_tail = smoothed.tail(period)
    is_growing = (smoothed_tail.diff()[1:] > 0).all()
    growing_slope = smoothed_tail.iloc[-1] * 100 / smoothed.mean()
    return float(growing_slope), is_growing


def get_linear_trend(time_series_of_publications):
    """Вычисляет линейный тренд временного ряда."""
    ts = pd.Series(time_series_of_publications)
    X = np.arange(len(ts)).reshape(-1, 1)
    y = ts.values
    model_lr = LinearRegression(positive=True)
    model_lr.fit(X, y)
    linear_trend = model_lr.predict(X)
    trend_slope = float(model_lr.coef_[0])
    return linear_trend, trend_slope


def get_linear_chart_data(label: str, data: list, color: str):
    """Готовит словарь данных для построения линейного графика."""
    return {
        'label': label,
        'data': data,
        'borderColor': color
    }


def format_label(label: str) -> str:
    """Формирует временную метку для отображения на графике в формате mm-YYYY.

    Исходные данные: текстовая метка формата yymm.
    Пример:
        Вход: 2209,
        Выход: 09-2022.
    """
    return f'{label[2:]}-20{label[0:2]}'


def date_from_label(label: str) -> datetime.datetime:
    """Возвращает дату, указанную в метке временного ряда в формате yymm."""
    year = int(label[0:2])
    month = int(label[2:])
    return datetime.datetime(year=year, month=month, day=1)


def prepare_card_info(trend_slope, one_percent_of_mean, final_period_rate,
                      start_with, seq_length,
                      smoothed_start_with, smoothed_seq_length, smoothed_growth,
                      chart_labels):
    """Подготавливает данные для отображения в карточке на странице мониторинга."""
    if np.abs(trend_slope) < 10 * one_percent_of_mean:
        slow_trend = 'слабый '
    else:
        slow_trend = ''
    if trend_slope > one_percent_of_mean:
        trend_direction = slow_trend + 'восходящий'
    elif trend_slope < -one_percent_of_mean:
        trend_direction = slow_trend + 'нисходящий'
    else:
        trend_direction = 'стабильный'

    if final_period_rate > 100:
        final_period_msg = f'В последний месяц число публикаций превышает среднее на {int(final_period_rate)}%'
    else :
        final_period_msg = ''

    month = list(chart_labels)[start_with]
    label_seq_length = f'{month[2:]}-20{month[0:2]}'
    sequence_analisys = (f'Наиболее продолжительный рост фиксировался в течение {seq_length} '
                        f'мес. начиная с {label_seq_length}')
    month = list(chart_labels)[smoothed_start_with]
    label_smoothed_seq_length = f'{month[2:]}-20{month[0:2]}'
    monitoring_time_phrase = '<b>фиксируется</b>' if is_trend_now(
        label_smoothed_seq_length, int(smoothed_seq_length)) else 'фиксировался'
    smoothed_sequence_analisys = (f'Восходящий тренд {monitoring_time_phrase} в течение '
                                    f'{smoothed_seq_length} мес. начиная с {label_smoothed_seq_length}')
    if smoothed_growth > 200:
        spike = ('<br><b>Дополнительно: наблюдается взрывной рост ("spike"). Рост относительно среднего'
                 f' значения составляет {int(round(smoothed_growth, 0))} %.</b>')
        smoothed_sequence_analisys += spike
    trend_slope_for_display = f'{"+" if trend_slope > 0 else ""}{str(round(trend_slope, 2))}'
    """
        # 'trend_direction': trend_direction,
        # 'trend_slope': trend_slope_for_display,
        # 'sequence_analisys': sequence_analisys,
        # 'smoothed_sequence_analisys': smoothed_sequence_analisys,
        # 'final_period': final_period_msg,
    """
    return (f'Тренд: {trend_direction} ({round(trend_slope, 2)} док. в мес.)<br>'
            f''
            f'{sequence_analisys}<br>'
            f'{smoothed_sequence_analisys}<br>'
            f'{final_period_msg}')


"""
<h6><b>Рассматриваемый период: с {{ note.search_from }} по настоящее время.</b></h6>
    Информационные массивы: {% if preselected_categories %}<span id="preselected-categories-list">{{preselected_categories}}</span>{% else %}все{% endif %}.<br>
    Линейный тренд временного ряда публикаций: <span id="trend_direction">не определен</span>.<br>
    <span data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-html="true" data-bs-title="Среднее значение дифференциала временного ряда. Показывает общую тенденцию ряда за период.">Cредняя скорость изменения тренда</span> составляет: <span id="trend_slope">не определена</span> публикаций в мес.<br>
    <span id="sequence_analisys"></span><br>
    <span data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-html="true" data-bs-title="Рост графика после экспоненциального сглаживания говорит о наличии восходящего временного ряда. Число публикаций систематически увеличивается в этот период и тенденция сохраняется. Может рассматриваться как устойчивый тренд в долгосрочной перспективе." id="smoothed_sequence_analisys"></span><br>
    <span id="final_period"></span><br>
"""


from navigate.html_rendering import BsCard
from navigate.deepsearch_settings import INF_TYPE_CODES_BY_NAME

def api_stats_publications_topic(request: HttpRequest, note_id: int):
    """Возвращает статистические данные по временному ряду, построенному по записям в блокноте с ID note_id."""
    chart_config = {
        'type': 'line',
        'data': {
            'datasets': [],
            'labels': []
        },
        'options': {
            'responsive': True,
            'legend': {
                'display': True
            }
        }
    }
    text_info = {'cards': ''}
    alpha = 0.05


    note = NoteItem.objects.get(id=note_id)
    categories = [int(item) for item in note.tracking_sources.split('-')] if note.tracking_sources else [None,]

    for category in categories:
        card = BsCard(INF_TYPE_CODES_BY_NAME.get(category))
        card.add_to_footer('footer text')
    
        start_time = time.time()
        topic_search_result = search_by_note_category(note, category, search_limit=10000)
        print('[ES search] ', time.time() - start_time)
    
        start_time = time.time()
        publications = get_queryset_from_cache(topic_search_result, MainDoc, list_of_fields=['doc_id', 'doc_name'])
        print('[SQL select] ', time.time() - start_time)

        s_year, s_month, s_day = note.search_from.year, note.search_from.month, note.search_from.day
        ts_initial_date = datetime.datetime(year=s_year, month=s_month, day=s_day)
        statistics_by_month = get_publications_time_series(publications, ts_initial_date=ts_initial_date)

        # print('временной ряд:')
        # print(list(statistics_by_month.values()))
        # print('labels:')
        # print(list(statistics_by_month.keys()))

        time_series_of_publications = list(statistics_by_month.values())
        if len(time_series_of_publications) == 0:
            continue

        # Преобразуем в pandas.Series
        ts = pd.Series(time_series_of_publications)
        seq_length, start_with, growth = get_max_sequence(ts)

        # экспоненциальное сглаживание
        smoothed = ts.ewm(alpha=alpha).mean()

        # анализ наибольших возрастающих последовательностей
        smoothed_seq_length, smoothed_start_with, smoothed_growth = get_max_sequence(smoothed)

        # Вычисление линейного тренда через регрессию
        linear_trend, trend_slope = get_linear_trend(time_series_of_publications)

        one_percent_of_mean = ts.mean() / 100
        final_period_rate = calc_tail_abs_trend(time_series_of_publications)
        chart_labels = [format_label(item) for item in statistics_by_month.keys()]
        print(f'{chart_labels=}')

        # Подготовка описательных данных для передачи на фронтенд
        card_body_text = prepare_card_info(
            trend_slope=trend_slope,
            one_percent_of_mean=one_percent_of_mean,
            final_period_rate=final_period_rate,
            start_with=start_with,
            seq_length=seq_length,
            smoothed_start_with=smoothed_start_with,
            smoothed_seq_length=smoothed_seq_length,
            smoothed_growth=smoothed_growth,
            chart_labels=statistics_by_month.keys())
        card.add_to_body(card_body_text)
        card_html = card.render()

        print(card_html)
        text_info['cards'] += f'{card_html}<br>'

        # формирование данных для построения графиков

        chart_config['data']['labels'] = chart_labels
        chart_config['data']['datasets'].append(get_linear_chart_data(f'{INF_TYPE_CODES_BY_NAME.get(category)} - публикации', ts.tolist(), 'grey'))
        chart_config['data']['datasets'].append(get_linear_chart_data(f'{INF_TYPE_CODES_BY_NAME.get(category)} - эксп. сглаживание', smoothed.tolist(), 'blue'))
        chart_config['data']['datasets'].append(get_linear_chart_data(f'{INF_TYPE_CODES_BY_NAME.get(category)}- тренд', linear_trend.tolist(), 'green'))

        # chart_config['data']['datasets'].append(get_linear_chart_data('линейный рост', linear_trend.tolist(), 'red'))

        # chart_config['data']['datasets'].append(get_linear_chart_data('test', ['null', 2, 2, 2, 2, 1, 2, 2, 5, 6, 2], 'red'))

    result = {
        'text_info': text_info,
        'chart_config': chart_config
    }
    return JsonResponse(data=result)


def api_stats_get_countries(request: HttpRequest):
    """API-view возвращает статистику по странам отобранных документов."""
    queryset_id = serialize_int_list_to_string(get_selected_documents_id(get_session_id(request)))
    if queryset_id in navigate_cache.stat_cache['countries']:
        all_countries_tuple_list = navigate_cache.stat_cache['countries'][queryset_id]
    else:
        maindocument = get_all_selected_documents(request)
        all_countries = get_all_countries(maindocument)
        all_countries_tuple_list = sorted(
            [(country_name, all_countries[country_name]) for country_name in all_countries.keys()],
            key=lambda x: x[1],
            reverse=True
        )
        navigate_cache.stat_cache['countries'][queryset_id] = all_countries_tuple_list

    return JsonResponse(data={
        'labels': [item[0] for item in all_countries_tuple_list],
        'data': [item[1] for item in all_countries_tuple_list]
    })


def api_stats_get_orgs(request: HttpRequest):
    """API-view возвращает статистику по объектам отобранных документов."""
    queryset_id = serialize_int_list_to_string(get_selected_documents_id(get_session_id(request)))
    if queryset_id in navigate_cache.stat_cache['orgs']:
        all_orgs_tuple_list = navigate_cache.stat_cache['orgs'][queryset_id]
    else:
        maindocument = get_all_selected_documents(request)
        all_orgs = get_all_orgs(maindocument)
        all_orgs_tuple_list = sorted(
            [(org_name, all_orgs[org_name]) for org_name in all_orgs.keys()],
            key=lambda x: x[1],
            reverse=True
        )
        navigate_cache.stat_cache['orgs'][queryset_id] = all_orgs_tuple_list

    return JsonResponse(data={
        'labels': [item[0] for item in all_orgs_tuple_list],
        'data': [item[1] for item in all_orgs_tuple_list]
    })


def api_stats_get_persons(request: HttpRequest):
    """API-view возвращает статистику по персонам отобранных документов."""
    maindocument = get_all_selected_documents(request)

    all_persons = get_all_persons(maindocument)

    all_persons_tuple_list = sorted(
        [(person_name, all_persons[person_name]) for person_name in all_persons.keys()],
        key=lambda x: x[1],
        reverse=True
    )

    return JsonResponse(data={
        'labels': [item[0] for item in all_persons_tuple_list],
        'data': [item[1] for item in all_persons_tuple_list]
    })


def api_stats_get_mails(request: HttpRequest):
    """API-view возвращает статистику по email отобранных документов."""
    maindocument = get_all_selected_documents(request)

    all_mails = get_all_mails(maindocument)

    all_mails_tuple_list = sorted(
        [(mail_name, all_mails[mail_name]) for mail_name in all_mails.keys()],
        key=lambda x: x[1],
        reverse=True
    )

    return JsonResponse(data={
        'labels': [item[0] for item in all_mails_tuple_list],
        'data': [item[1] for item in all_mails_tuple_list]
    })


def api_stats_publications_by_years(request: HttpRequest):
    """API-view возвращает статистику по годам публикации отобранных документов."""
    maindocument = get_all_selected_documents(request)

    years = dict()
    for doc in maindocument:
        try:
            year = int(doc.doc_name[0:4])
        except Exception as error:
            print((f'Ошибка при парсинге года в наименовании документа {doc.doc_id} '
                   f'при подсчете статистики публикаций по годам: {error}'))
        else:
            if year in years:
                years[year] += 1
            else:
                years[year] = 1
    sorted_years = list(sorted(years.keys()))
    sorted_values = [years[item] for item in sorted_years]
    return JsonResponse(data={
        'labels': sorted_years,
        'data': sorted_values
    })
    # return JsonResponse(data={
    #     'labels': list(years.keys()),
    #     'data': list(years.values())
    # })


def api_stats_keywords(request: HttpRequest):
    """Подготовка статистики по ключевым словам."""
    maindocument = get_all_selected_documents(request)
    word_frequency = dict()
    all_abstracts = ''
    stop_words_list = set(read_stop_word_list())
    for maindoc in maindocument:
        current_abstract = get_abstract(maindoc)

        if not current_abstract:
            continue

        all_abstracts += ' ' + current_abstract

        abstract_word_list = current_abstract.split(' ')
        for word in abstract_word_list:
            word = word.strip(' ,.()')
            if word.lower() in stop_words_list or len(word) < 2:
                continue
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1

    all_words_tuple_list = sorted(
        [(word, word_frequency[word]) for word in word_frequency.keys()],
        key=lambda x: x[1],
        reverse=True
    )[:30]

    # Возвращаем изображение в формате base64
    return JsonResponse(data={
        'labels': [item[0] for item in all_words_tuple_list],
        'data': [item[1] for item in all_words_tuple_list],
        'image': make_word_cloud(all_abstracts, stop_words_list)
    })


def notifications(request: HttpRequest):
    """Уведомления."""
    print('notification')
    print(int(request.GET.get('folder')))
    if request.GET.get('folder'):
        if get_all_selected_documents(request).count() == int(request.GET.get('folder')):
            return JsonResponse({'status': 'ok'})

        else:
            clean_threads(True)
            if get_threads_count() == 1:
                _shutdown_cleanup_worker()
            return JsonResponse({'reload': '1', 'status': 'stop'})


######################################################################################################################
# Граф - трассировка движения документов\
######################################################################################################################

@csrf_exempt
def get_graph_data(request, dr: int = 0):
    """API endpoint для получения данных графа в формате Vis.js"""
    if request.method == 'GET':
        # Здесь получаем statistic_data и docs_data
        # В реальном приложении это будет из базы данных или кэша
        statistic_data = get_statistic_data(dr)
        docs_data = get_documents_meta_data(dr)

        graph_data = process_graph_data(statistic_data, docs_data)
        return JsonResponse(graph_data)

    return JsonResponse({'error': 'Invalid method'}, status=400)


def process_graph_data(statistic_data, docs_data):
    """Обработка данных для формирования графа"""
    nodes = []
    edges = []
    level_y_positions = {}

    # Определяем позиции по Y для каждого уровня (этапа)
    stages = [stage['stage'] for stage in statistic_data]
    stage_height = 5  # Расстояние между уровнями

    for i, stage in enumerate(stages):
        level_y_positions[stage] = i * stage_height

    # Обрабатываем каждый этап
    for stage_idx, stage_data in enumerate(statistic_data):
        stage_name = stage_data['stage']
        processed_docs = stage_data['processed_documents']

        # Создаем узлы для документов этого этапа
        for doc in processed_docs:
            doc_id = doc['id']

            # Получаем данные документа
            doc_info = docs_data.get(doc_id, {})

            # Определяем цвет узла
            color = 'white'
            if doc_info.get('category') != 'doc':
                color = doc_info.get('color', '#97C2FC')

            # Создаем узел
            node = {
                'id': f"{stage_name}_{doc_id}",
                'label': doc_id,
                'group': stage_name,
                'level': level_y_positions[stage_name],
                'color': color,
                'title': f"ID: {doc_id}<br>Stage: {stage_name}",
                'data': {
                    'original_id': doc_id,
                    'stage': stage_name,
                    'name': doc_info.get('name', ''),
                    'category': doc_info.get('category', ''),
                    'year': doc_info.get('year', ''),
                    'color': doc_info.get('color', ''),
                    'text': doc_info.get('text', '')[:100] if doc_info.get('text') else ''
                }
            }
            nodes.append(node)

            # Создаем ребра к документам-источникам
            for ref_doc_id in doc.get('ref', []):
                if ref_doc_id:  # Пропускаем пустые ссылки
                    # Ищем узел-источник на предыдущих этапах
                    for prev_stage_idx in range(stage_idx):
                        prev_stage = statistic_data[prev_stage_idx]
                        for prev_doc in prev_stage['processed_documents']:
                            if prev_doc['id'] == ref_doc_id:
                                edge = {
                                    'id': f"{ref_doc_id}_{doc_id}",
                                    'from': f"{prev_stage['stage']}_{ref_doc_id}",
                                    'to': f"{stage_name}_{doc_id}",
                                    'arrows': 'to',
                                    'color': {'color': '#848484'}
                                }
                                edges.append(edge)
                                break

    return {
        'nodes': nodes,
        'edges': edges,
        'stages': stages
    }


def get_ai_query_by_dr(dr: int):
    if not dr:
        return None
    ai_query = AIQuery.objects.filter(pk=dr).first()
    if not ai_query:
        return None
    return ai_query


def get_statistic_data(dr: int):
    """Получение статистических данных обработки."""
    ai_query = get_ai_query_by_dr(dr)
    if not ai_query:
        return []

    dr_stages = ai_query.stages.all()
    if not dr_stages:
        return []

    data = []
    for stage in dr_stages:
        processed_docs_queryset = ProcessedDocuments.objects.filter(deepresearch_id_stage=stage)

        processed_docs_unique_id = list(set([doc.doc_id.doc_id for doc in processed_docs_queryset]))
        # print(f'для этапа {stage} нашел записи об обработке документов: {processed_docs_unique_id}')
        refs = dict()
        for tdoc in processed_docs_queryset:
            if tdoc.doc_id.doc_id in refs.keys():
                refs[tdoc.doc_id.doc_id].append(tdoc.ref.doc_id)
            else:
                refs[tdoc.doc_id.doc_id] = [tdoc.ref.doc_id] if tdoc.ref else []

        # print(refs)
        data.append(
            {
                "stage": stage.name,
                "processed_documents": [
                    {'id': doc, 'ref': refs[doc]} for doc in processed_docs_unique_id
                ],
                "processing_time": stage.processing_time
            }
        )

    return data


def get_documents_meta_data(dr: int):
    """Получение метаданных о документах"""
    data = dict()
    ai_query = get_ai_query_by_dr(dr)
    records_queryset = DocumentMetaData.objects.filter(deepresearch_id=ai_query)
    for record in records_queryset:
        data[record.doc_id] = {
            'name': record.name,
            'category': record.category,
            'color': record.color,
            'text': record.text,
            'year': record.year,
        }
    return data


def tracking_topic(request: HttpRequest):
    """Возвращает документы по отслеживаемым тематикам."""
    if not request.GET.getlist('id'):
        return JsonResponse({'error': 'Не заданы id поисковых запросов.'})
    notes_id = [int(item) for item in request.GET.getlist('id')]
    notes = NoteItem.objects.filter(id__in=notes_id)

    return JsonResponse(get_tracking_topic_documents(notes))
