def read_cookie(file_path):
    f = open(file_path, 'r')
    _cookie = f.read()
    f.close()
    return _cookie
