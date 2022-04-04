files = {}

def splitFile(bytesFile,name,servers,key):
    chunks = {}

    if(servers<2):
        print("Only 1 Node!!!!!")
        files["code"]=-1
        fname=f'{name}_{key}'
        chunks[fname]=bytesFile
        return chunks
    
    resourceName = name
    originalSize = bytesFile
    f_size = len(bytesFile) / servers
    if isinstance(f_size, float):
        f_size = int(f_size) + 1
    min_limit = 0
    max_limit = f_size
    f_names = []
    counter = 0
    name_cons = f'{name}_{key}'

    for i in range(servers):
        if counter == 1:
            name = name_cons +'_'+'1'
        else:
            name = name_cons +'_'+str(counter)
        
        f_names.append(name)
        #file = open(name, 'wb')
        #file.write(bytesFile[min_limit:max_limit])
        chunks[name]=bytesFile[min_limit:max_limit]
        #file.close()
        min_limit = max_limit
        max_limit += f_size
        counter += 1
        files["files"] = f_names
    files["code"]=1
    return chunks

def combine(f_format,f_name):
    filenames = files["files"]
    with open(f'{f_name}.{f_format}', "wb") as new_file:
        for name in filenames:
            with open(name,"rb") as f:
                for line in f:
                    new_file.write(line)

def convertToBytes(src):
    with open(src, 'rb') as f:
        contents = f.read()
        return contents

'''
def main():
    bytes_f=convertToBytes('./hilda.jpg')
    splitFile(bytes_f,"diego",2)
    if(files["code"]!=-1):
        combine('jpg','hildaSplitted')

if __name__ == '__main__':
    main()
'''