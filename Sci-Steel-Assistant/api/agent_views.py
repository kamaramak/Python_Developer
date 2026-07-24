import json
import logging
import time
from typing import Any, Dict, List, Optional

from celery.result import AsyncResult
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_agent_session(request):
    from navigate.tasks import agent_query_task

    query = request.data.get('query', '')
    session_id = request.data.get('session_id', f'session_{int(time.time())}')
    answer_mode = request.data.get('answer_mode', 'detailed')

    if not query:
        return JsonResponse({'error': 'Query is required'}, status=400)

    logger.info(f'[AGENT] start request: session={session_id}, mode={answer_mode}, query={query[:80]!r}')
    task = agent_query_task.delay(query, session_id, answer_mode)
    return JsonResponse({'task_id': task.id, 'session_id': session_id, 'status': 'started'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def continue_agent_session(request):
    from navigate.tasks import agent_continue_task

    session_id = request.data.get('session_id', '')
    follow_up = request.data.get('follow_up', '')

    if not session_id or not follow_up:
        return JsonResponse({'error': 'session_id and follow_up are required'}, status=400)

    logger.info(f'[AGENT] continue request: session={session_id}')
    task = agent_continue_task.delay(session_id, follow_up)
    return JsonResponse({'task_id': task.id, 'session_id': session_id, 'status': 'started'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agent_task_status(request, task_id):
    result = AsyncResult(task_id)
    response = {
        'task_id': task_id,
        'state': result.state,
    }
    if result.state == 'PROGRESS':
        response['progress'] = result.info
    elif result.state == 'SUCCESS':
        response['result'] = result.result
    elif result.state == 'FAILURE':
        response['error'] = str(result.result)
    return JsonResponse(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agent_status(request, session_id):
    from navigate.agent_controller import get_session_status
    status = get_session_status(session_id)
    return JsonResponse(status)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def search_knowledge_graph(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        filters_str = request.GET.get('filters', '{}')
        try:
            filters = json.loads(filters_str) if filters_str else {}
        except:
            filters = {}
    else:
        query = request.data.get('query', '')
        filters = request.data.get('filters', {})

    from navigate.neo4j_client import search_graph

    try:
        results = search_graph(query, filters)
        return JsonResponse({'results': results})
    except Exception as e:
        logger.error(f'Graph search error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_graph_neighborhood(request, node_id):
    node_label = request.GET.get('label', 'Material')
    depth = int(request.GET.get('depth', 2))

    from navigate.neo4j_client import get_neighborhood
    try:
        result = get_neighborhood(node_id, node_label, depth)
        return JsonResponse(result)
    except Exception as e:
        logger.error(f'Neighborhood error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_documents(request):
    directory_path = request.data.get('directory_path', '')
    if not directory_path:
        return JsonResponse({'error': 'directory_path is required'}, status=400)

    from navigate.tasks import import_documents_from_directory
    task = import_documents_from_directory.delay(directory_path, request.user.id)
    return JsonResponse({
        'task_id': task.id,
        'status': 'started',
        'message': f'Импорт из {directory_path} запущен'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_import_status(request, task_id):
    result = AsyncResult(task_id)
    response = {
        'task_id': task_id,
        'status': result.status,
    }
    if result.status == 'PROGRESS':
        response['progress'] = result.info
    elif result.status == 'SUCCESS':
        response['result'] = result.result
    elif result.status == 'FAILURE':
        response['error'] = str(result.result)
    return JsonResponse(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_analytics_report(request):
    query = request.data.get('query', '')
    report_type = request.data.get('report_type', 'literature_review')
    filters = request.data.get('filters', {})

    if not query:
        return JsonResponse({'error': 'Query is required'}, status=400)

    from navigate.analytics import generate_report
    try:
        result = generate_report(query, report_type, filters)
        return JsonResponse(result)
    except Exception as e:
        logger.error(f'Analytics error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_results(request, format_type):
    query = request.GET.get('query', '')
    session_id = request.GET.get('session_id', '')

    from navigate.analytics import export_data
    try:
        if format_type == 'json-ld':
            content_type = 'application/ld+json'
        elif format_type == 'markdown':
            content_type = 'text/markdown'
        else:
            content_type = 'application/pdf'

        data = export_data(query, session_id, format_type)

        if format_type == 'pdf':
            from django.http import HttpResponse
            response = HttpResponse(data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
        else:
            return JsonResponse({'data': data, 'format': format_type})
    except Exception as e:
        logger.error(f'Export error: {e}')
        return JsonResponse({'error': str(e)}, status=500)
