from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['page'] = self.page.number
        response.data['total_pages'] = self.page.paginator.num_pages
        return response