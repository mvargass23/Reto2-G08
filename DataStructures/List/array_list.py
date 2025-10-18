def new_list():
    new_list = {
        "elements": [],
        "size": 0
    }
    return new_list

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1

def size(my_list):
    return len(my_list['elements'])

def first_element(my_list):
    if size(my_list) == 0:
        return None
    return my_list["elements"][0]

def get_element(my_list, index):
    """
    index: 0-based index
    """
    return my_list["elements"][index]

def is_present(my_list, element, cmp_function):
    size_ = my_list["size"]
    if size_ > 0:
        for keypos in range(0, size_):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                return keypos
    return -1

def is_empty(my_list):
    return my_list['size'] == 0

def remove_first(my_list):
    if my_list['size'] == 0:
        return None
    element = my_list['elements'].pop(0)
    my_list['size'] -= 1
    return element

def remove_last(my_list):
    if my_list['size'] == 0:
        return None
    element = my_list['elements'].pop(my_list['size'] - 1)
    my_list['size'] -= 1
    return element

def insert_element(my_list, element, pos):
    """
    pos: 1-based position like in your original code
    """
    if pos < 1:
        pos = 1
    idx = pos - 1
    my_list['elements'].insert(idx, element)
    my_list['size'] += 1
    return my_list

def delete_element(my_list, pos):
    """
    pos: 1-based
    """
    idx = pos - 1
    if 0 <= idx < my_list['size']:
        my_list['elements'].pop(idx)
        my_list['size'] -= 1
    return my_list

def change_info(my_list, pos, newinfo):
    idx = pos - 1
    my_list['elements'][idx] = newinfo
    return newinfo

def exchange(my_list, pos1, pos2):
    infopos1 = get_element(my_list, pos1-1)
    infopos2 = get_element(my_list, pos2-1)
    change_info(my_list, pos1, infopos2)
    change_info(my_list, pos2, infopos1)
    return my_list

def sub_list(my_list, pos, numelem):
    sub = new_list()
    start = pos
    end = pos + numelem - 1
    # adjust bounds (pos is 0-based if used with this implementation)
    for i in range(start, min(end+1, size(my_list))):
        sub["elements"].append(my_list["elements"][i])
    sub["size"] = len(sub["elements"])
    return sub