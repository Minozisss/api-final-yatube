from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetIfRequestedPagination(LimitOffsetPagination):
    """Включаю пагинацию только когда её явно попросили в query params"""

    default_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        """Если limit и offset не передали, то отдаю обычный список"""
        if (
            'limit' not in request.query_params
            and 'offset' not in request.query_params
        ):
            return None
        return super().paginate_queryset(queryset, request, view)
