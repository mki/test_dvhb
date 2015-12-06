import json
import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import View
from .utils import pagination_vars
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from django.utils import timezone


class PaginatedListViewMixin(View):
    template_name = ''
    page_query_param = 'p'
    template_items_var = ''

    def get(self, request):
        if self.template_items_var == '' or self.template_name == '':
            raise NotImplementedError()

        cur_page = int(request.GET.get(self.page_query_param, 1))

        context = pagination_vars(cur_page, 20, self._items(), self._url)
        context[self.template_items_var] = context['paginated_items']
        del context['paginated_items']

        return render(request, self.template_name, context)

    def _items(self):
        raise NotImplementedError()

    def _url(self, page):
        raise NotImplementedError()


class BlogListView(PaginatedListViewMixin):
    template_name = 'blog/blogs.html'
    template_items_var = 'blogs'

    def _items(self):
        return '1', '2'

    def _url(self, page):
        return '/blog/view/{0}/'.format(page)
