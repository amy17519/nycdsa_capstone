def ProcessID(data,token):

    ID = []

    for item in data:
        if token in item.keys():
            ID.append(item[token])
        else:
            ID.append({})

    return(ID)