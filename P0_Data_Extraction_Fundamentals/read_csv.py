def parse_file(datafile):
    data = []
    with open(datafile, "rb") as f:
        header = f.readline().split(',')
        counter = 0
        for line in f:
            if counter == 10:
                break
            
            fields = line.split(',')
            entry = {}
            
            for i, value in enumerate(fields):
                entry[header[i].strip()] = value.strip()
                
            data.append(entry)
            counter += 1
                
    return data
