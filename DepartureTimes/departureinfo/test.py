from os.path import dirname, realpath, sep, pardir


def test():
    print dirname(realpath(__file__)) + \
        sep + pardir + sep + pardir + sep


if __name__ == "__main__":
    test()
