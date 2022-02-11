def find_child_by_name(object,name):
    try:
        for i in object.children:
            try:
                if i.name == name:
                    return i
                else:
                    if find_child_by_name(i,name) == None:
                        continue
                    else:
                        return find_child_by_name(i,name)
            except:
                if find_child_by_name(i,name) == None:
                    continue
                else:
                    return find_child_by_name(i,name)
    except:
        pass