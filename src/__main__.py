# from common.config import Setting, registered_settings

#Setup logging before importing any further files

import datetime
import logging
with open("qwest.log", "r") as old:
    arch = open("qwest_old.log", "a")
    arch.write(old.read())
    arch.close()
logger = logging.getLogger(__name__)
logging.basicConfig(filename='qwest.log', level=logging.INFO, filemode="w")
logger.info('Started logger at %s' % datetime.datetime.now() )

import test
# from src.graphics.settings import render
from src.level import pap
# def main():
#     render()
def main():
    pap()

if __name__ == '__main__':
    main()

# test()


