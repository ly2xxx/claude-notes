def process(data, type):
    if type == 'sum':
        r = 0
        for i in data:
            r = r + i
        return r
    elif type == 'avg':
        r = 0
        for i in data:
            r = r + i
        return r / len(data)
    elif type == 'max':
        r = data[0]
        for i in data:
            if i > r:
                r = i
        return r
    else:
        return None