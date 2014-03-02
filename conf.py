class Conf:
    def __init__(self):
        pass

    def get_conf(self):
        path = '.\\conf.ini'
        file_object = open(path)
        return [line.split('=')[1] for line in file_object]

if __name__ == "__main__":
    conf = Conf()
    print conf.get_conf()