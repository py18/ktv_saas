from django.core.paginator import Paginator


def get_page(data,size,pg):
    '''
    :param data: get方法传出的list信息
    :param size: 每页容量
    :param pg: 页数
    :return: 处理完整的data信息
    '''
    p = Paginator(data, size)
    next_page = None
    previous_page = None
    page1 = p.page(pg)
    if page1.has_next():
        next_page = page1.next_page_number()
    if page1.has_previous():
        previous_page = page1.previous_page_number()
    data = {"count": p.count, "num_pages": p.num_pages, "next_page": next_page,
            "previous_page": previous_page,
            "ret": page1.object_list}
    return data