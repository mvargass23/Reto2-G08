def new_list():
    newlist = {'first': None,
           'last': None,
           'size': 0,
           }
    return newlist

def size(my_list):
    return my_list["size"]

def first_element(my_list):
    return my_list["first"]

def add_first(my_list, element):
    new_node = {'info': element, 'next': None}
    if my_list['first'] is None:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        new_node['next'] = my_list['first']
        my_list['first'] = new_node

    my_list['size'] += 1

    return my_list

def add_last(my_list, element):
    new_node = {'info': element, 'next': None}
    if my_list['last'] is None:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        my_list['last']['next'] = new_node
        my_list['last'] = new_node
        
    my_list['size'] += 1
    
    return my_list

def get_element(my_list, pos):
    element = None
    if pos==my_list["size"]:
        element = my_list["last"]
    elif pos==1:
        element = my_list["first"]
    elif pos>1 and pos<my_list["size"]:
        i=1
        element = my_list["first"]
        while i<pos:
            element = element["next"]
            i+=1
    else:
        element = "Posición fuera de índice"
        return element
    return element["info"]

def is_present(my_list, pos,cmp_function):
    size = my_list['size']
    if size > 0:
        keyexist = False
        element = my_list["first"]
        i=0
        while i<size:
            if (cmp_function(pos, element["info"]) == 0):
                keyexist = True
                break
            element=element["next"]
            i+=1
        if keyexist:
            return i
    return -1