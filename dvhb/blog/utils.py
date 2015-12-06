from django.core.paginator import Paginator


def pagination_vars(page, page_size, items, url_func):
    paginator = Paginator(items, page_size)
    paginated_items = paginator.page(page).object_list
    total_pages = paginator.num_pages

    return {
        'paginated_items': paginated_items,
        'cur_page': page,
        'total_pages': total_pages,
        'prev_page_link': url_func(page-1) if page != 1 else None,
        'next_page_link': url_func(page+1) if page != total_pages else None,
    }
