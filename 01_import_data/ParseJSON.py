import json

def ParseJSON(fileName=None):

   data = []
   if fileName is None: raise ValueError("fileName cannot be None")
   with open(fileName) as fp:
        for line in fp:
            data.append(json.loads(line))


   return(data)

#### pass the data list and the token, get the list of the particular field back
def ProcessID(data,token):

    ID = []

    for item in data:
        if token in item.keys():
            ID.append(item[token])
        else:
            ID.append({})

    return(ID)

