from django.urls import include, path
from rest_framework import routers

from .views import (
    MainDocViewSet,
    OrgViewSet,
    AIQueryViewSet,
    api_update_checkbox,
    api_all_to_folder,
    api_folder_action,
    api_stats_get_countries,
    api_stats_get_orgs,
    api_stats_get_persons,
    api_stats_get_mails,
    api_stats_keywords,
    api_stats_publications_by_years,
    api_action_notes,
    api_get_notes,
    construct_graph_by_settings,
    notifications,
    get_graph_data,
    tracking_topic,
    api_stats_publications_topic,
    api_translate,
)
from .agent_views import (
    start_agent_session,
    continue_agent_session,
    get_agent_status,
    get_agent_task_status,
    search_knowledge_graph,
    get_graph_neighborhood,
    import_documents,
    get_import_status,
    generate_analytics_report,
    export_results,
)
from .graph_views import (
    get_viz_data,
    export_gephi,
    get_knowledge_gaps,
    get_comparative_table,
)

router = routers.DefaultRouter()
router.register('maindoc', MainDocViewSet)
router.register('org', OrgViewSet)
router.register('aiquery', AIQueryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('update_checkbox/', api_update_checkbox, name='update_checkbox'),
    path('all_to_folder/', api_all_to_folder, name='all_to_folder'),
    path('notifications/', notifications, name='notifications'),
    path('analysis/clear_folder/', api_folder_action, name='clear_folder'),
    path('analysis/stats_countries/', api_stats_get_countries, name='stats-countries'),
    path('analysis/stats-orgs/', api_stats_get_orgs, name='stats-orgs'),
    path('analysis/stats-persons/', api_stats_get_persons, name='stats-persons'),
    path('analysis/stats-mails/', api_stats_get_mails, name='stats-mails'),
    path('analysis/stats-keywords/', api_stats_keywords, name='stats-keywords'),
    path('analysis/stats-years/', api_stats_publications_by_years, name='stats-years'),
    path('analysis/stats-topic/<int:note_id>', api_stats_publications_topic, name='stats-topic'),
    path('notes/clear_notes', api_action_notes, name='action_notes'),
    path('notes/get_notes', api_get_notes, name='get_notes'),
    path('graph/set_graph_settings/', construct_graph_by_settings, name='set_graph_settings'),
    path('get_graph_data/<int:dr>', get_graph_data, name='get_graph_data'),
    path('tracking/', tracking_topic, name='tracking'),
    path('translate/', api_translate, name='translate'),
    path('agent/start/', start_agent_session, name='agent_start'),
    path('agent/continue/', continue_agent_session, name='agent_continue'),
    path('agent/task_status/<str:task_id>/', get_agent_task_status, name='agent_task_status'),
    path('agent/status/<str:session_id>/', get_agent_status, name='agent_status'),
    path('kg/search/', search_knowledge_graph, name='api_kg_search'),
    path('kg/neighborhood/<str:node_id>/', get_graph_neighborhood, name='kg_neighborhood'),
    path('kg/viz/', get_viz_data, name='kg_viz'),
    path('kg/export/gephi/', export_gephi, name='kg_export_gephi'),
    path('kg/gaps/', get_knowledge_gaps, name='kg_gaps'),
    path('kg/compare/', get_comparative_table, name='kg_compare'),
    path('import/start/', import_documents, name='import_start'),
    path('import/status/<str:task_id>/', get_import_status, name='import_status'),
    path('analytics/report/', generate_analytics_report, name='analytics_report'),
    path('export/<str:format_type>/', export_results, name='export_results'),
]
