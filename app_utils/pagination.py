from django.core.paginator import Paginator


def pagination_data(data, page_limit: [int, str], page_number: [int, str]) -> dict:
    """
    pagination data
    :param data: data
    :param page_limit: page limit
    :param page_number: number of page
    :return: object with required data
    """
    paginator = Paginator(data, page_limit)
    result = {
        "per_page": page_limit,
        "data_count": paginator.count,
        "pages": paginator.num_pages,
        "current_page": int(page_number),
        "has_next": False,
        "has_previous": False,
        "data": []
    }
    if int(page_number) <= paginator.num_pages:
        page = paginator.page(page_number)
        result['has_next'] = page.has_next()
        result['has_previous'] = page.has_previous()
        result['data'] = page.object_list
    # ---
    return result
