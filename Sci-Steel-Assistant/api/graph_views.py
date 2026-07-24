import json
import logging

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_viz_data(request):
    query = request.GET.get('query', '') or (request.data.get('query', '') if hasattr(request, 'data') else '')
    node_types = request.GET.get('types', '')
    try:
        limit = int(request.GET.get('limit', 50))
    except (ValueError, TypeError):
        limit = 50
    limit = max(5, min(limit, 500))

    from navigate.neo4j_client import search_graph
    from navigate.graph_export import graph_to_visjs_data

    filters = {'limit': limit}
    if node_types:
        filters['types'] = node_types.split(',')

    try:
        results = search_graph(query, filters)
        logger.info(f'get_viz_data: query={query!r}, limit={limit}, results={len(results)}')

        nodes_map = {}
        edges = []
        seen_edges = set()

        def extract_node_id(node_data):
            if not node_data:
                return None
            return node_data.get('id', node_data.get('_id', node_data.get('element_id', '')))

        def add_node(node_data):
            if not node_data:
                return None
            nid = extract_node_id(node_data)
            if not nid:
                logger.warning(f'Node without id: {node_data}')
                return None

            nid_str = str(nid)
            if nid_str not in nodes_map:
                nlabels = node_data.get('_labels', ['Unknown'])
                ntype = nlabels[0] if nlabels else 'Unknown'
                nlabel = node_data.get('name', node_data.get('title', nid_str))
                nodes_map[nid_str] = {
                    'id': nid_str,
                    'label': nlabel,
                    'name': nlabel,
                    'type': ntype,
                }
            return nid_str

        for item in results:
            n_data = item.get('n') or {}
            neighbor_data = item.get('neighbor') or {}
            rel_type = item.get('rel_type')

            n_id = add_node(n_data)
            neighbor_id = add_node(neighbor_data)

            if rel_type and n_id and neighbor_id and n_id != neighbor_id:
                edge_key = (n_id, neighbor_id, rel_type)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        'from': n_id,
                        'to': neighbor_id,
                        'type': rel_type,
                    })

        nodes = list(nodes_map.values())
        logger.info(f'get_viz_data: nodes={len(nodes)}, edges={len(edges)}')

        vis_data = graph_to_visjs_data(nodes, edges)
        return JsonResponse(vis_data)
    except Exception as e:
        logger.exception(f'Viz error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_gephi(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'Query is required'}, status=400)

    from navigate.neo4j_client import search_graph
    from navigate.graph_export import export_to_gephi

    try:
        results = search_graph(query, {})
        nodes = []
        edges = []

        for item in results:
            node = item.get('n', {})
            if node:
                nodes.append({
                    'id': node.get('id', ''),
                    'name': node.get('name', ''),
                    'type': list(node.get('labels', []))[0] if hasattr(node, 'labels') else '',
                })
            if item.get('rel_type') and item.get('m'):
                edges.append({
                    'from': node.get('id', ''),
                    'to': item['m'].get('id', ''),
                    'type': item['rel_type'],
                })

        return export_to_gephi(nodes, edges)
    except Exception as e:
        logger.error(f'Gephi export error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_knowledge_gaps(request):
    from navigate.graph_export import find_knowledge_gaps

    try:
        gaps = find_knowledge_gaps()
        return JsonResponse({'gaps': gaps})
    except Exception as e:
        logger.error(f'Knowledge gaps error: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_comparative_table(request):
    material = request.data.get('material', '')
    criteria = request.data.get('criteria', [])

    if not material:
        return JsonResponse({'error': 'Material is required'}, status=400)

    from navigate.graph_export import get_comparative_data

    try:
        result = get_comparative_data(material, criteria)
        return JsonResponse(result)
    except Exception as e:
        logger.error(f'Compare error: {e}')
        return JsonResponse({'error': str(e)}, status=500)
