def get_id_from_url(url_path):
    """
    get 103102396542 from https://hz.lianjia.com/ershoufang/103102396542.html
    :param url_path: ex:https://hz.lianjia.com/ershoufang/103102396542.html
    :return: id ex:103102396542
    """
    # if not isinstance(url_path, str):
    #     return ''
    if not url_path:
        return ''

    start_index = url_path.rfind('/')
    last_index = url_path.rfind('.')

    if start_index == -1 or last_index == -1 or start_index >= last_index:
        return ''

    return url_path[start_index + 1:last_index]
