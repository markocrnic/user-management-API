import ftputil
from ast import literal_eval


def readpathsfromftp():
    try:
        a_host = ftputil.FTPHost('10.0.200.68', 'empiry', '3mp1ry')

        for (dirname, subdirs, files) in a_host.walk("/projects/planthealthcare/api-gateway/"):
            for f in files:
                if f == 'paths.txt':
                    a_host.download(dirname + f, f)
                    with open(f) as txtfile:
                        content = txtfile.read()
                        print(str(content))
        a_host.close()

        return literal_eval(content)

    except Exception as e:
        print(e)
        a_host.close()


def getpath(path):
    path_dict = readpathsfromftp()
    apiname = path.split('/')[0]
    if apiname in path_dict:
        apipath = path_dict[apiname] + path
        print(apipath)
        return apipath
    else:
        print('Path not found: ' + path)
        return '404'