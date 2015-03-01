from dsb_import import dsb_import
from time import sleep

import_timeout_minutes = 5

def run():
    import_all()

def import_all():
    while True:
        try:
            dsb_import()
        except Exception as ex:
            print "Something went wrong in the import: %r" % ex
            print "Next import commences in %r minutes" % import_timeout_minutes

        # Wait 5 minutes before importing again
        sleep(60 * import_timeout_minutes)


if __name__ == "__main__":
    run()
