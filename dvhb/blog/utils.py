from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string, TemplateDoesNotExist


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


def render_multipart(template, context):
    text = u''
    try:
        html = render_to_string('%s.html' % template, context)
    except TemplateDoesNotExist:
        html = u''
    return text, html


def _send_email(email, post_id):
    subject = 'Добавилась запись'
    from_email = 'Test <info@test.ru>'
    template = "mail/post/new"
    context = {
        'post_id': post_id,
    }

    text, html = render_multipart(template, context=context)
    msg = EmailMultiAlternatives(subject, text, from_email, [email])
    msg.attach_alternative(html, "text/html")
    msg.send()
