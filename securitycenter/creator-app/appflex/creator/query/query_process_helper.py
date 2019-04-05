def split_values(original_values):
    splited_values = []
    for val in original_values:
        splited_values.extend(val)
    return splited_values


def get_field_by_name(obj, field_name):
    if '.' not in field_name:
        if obj is None:
            return None
        if hasattr(obj, 'get'):
            return obj.get(field_name)
        if hasattr(obj, '__getitem__'):
            return obj[field_name]
        return getattr(obj, field_name)
    spliced = str(field_name).split('.', maxsplit=1)
    return get_field_by_name(get_field_by_name(obj, spliced[0]), spliced[1])


def create_and_or_query_from_values(field_name, field_type, values):
    if not values:
        return ''
    compare_op = ' = ' if field_type == 'SINGLE' else ' : '
    return ' AND ( ' + ' OR '.join(create_compare(field_name, compare_op, values)) + ' ) '


def create_compare(field_name, compare_op, values):
    for val in values:
        yield field_name + compare_op + '"' + val + '"'


def get_element_by_order(elements, element_order):
    for index_ in range(0, len(elements)):
        if elements[index_].get('order') == element_order:
            return elements[index_]
    return None


def build_join(resp, joins, order):
    previous_join = get_element_by_order(joins, order - 1)
    if not previous_join:
        return ''
    join_values = []
    for val in resp:
        field_value = get_field_by_name(val, str(previous_join.get('field')))
        if field_value:
            join_values.append(field_value)
    if 'SINGLE' != previous_join.get('type') and join_values:
        join_values = split_values(join_values)
    next_join = get_element_by_order(joins, order)
    return create_and_or_query_from_values(next_join.get('field'), next_join.get('type'), join_values)
