def munge(filename):
    for punct in [".","!","$","?",",","(",")"," ","'",'"',"|","#","@","/","\\"]:
        filename = filename.replace(punct,"_").encode('ascii','ignore')
    return filename        