"""
It is commonly used for cleanning daily build files
"""

import logging
import os
import shutil
import datetime

DAYFROM = 9
DAYTO = 14
PATHLIST = [
r"D:\installers\version1001\product",
r"D:\installers\version1002\product"
]

def get_dateList(startDayCount, endDayCount):
    '''
    Get date list from today
    '''
    today = datetime.date.today()
    return [(today - datetime.timedelta(dayCount)) for dayCount in range(startDayCount, endDayCount)]

def get_subfolderList(path, startDayCount, endDayCount):
    '''
    Get subfolder list depend on date period
    '''
    allSubPaths = [os.path.join(path, pathName) for pathName in os.listdir(path)]
    dateList = get_dateList(startDayCount, endDayCount)
    return list(filter(lambda x: is_validDatePath(x, dateList), allSubPaths))
    
def is_validDatePath(path, dates):
    postfix1s = [date.strftime("AnnualLicense(%m.%d)") for date in dates]
    postfix2s = [date.strftime("%m.%d.%Y") for date in dates]
    postfix3s = [date.strftime("%Y.%m.%d") for date in dates]
    postfixs = []
    postfixs.extend(postfix1s)
    postfixs.extend(postfix2s)
    postfixs.extend(postfix3s)
    if any(map(path.endswith, postfixs)):
        return True
    else:
        return False

def clean_path(path):
    if os.path.isfile(path):
        try:
            os.remove(path)
            logging.info("file {0} is removed".format(path))
        except:
            logging.error("remove file {0} fail!".format(path))
    elif os.path.isdir(path):
        try:
            shutil.rmtree(path)
            logging.info("all files in {0} is removed".format(path))
        except:
            logging.error("remove directory {0} fail!".format(path))
    else:
        logging.error("invalid path! {0}".format(path))

def run(pathList, dayFrom, dayTo):
    for path in pathList:
        #get subpath list
        cleanList = get_subFolderList(path, dayFrom, dayTo)
        #clean
        for targetPath in cleanList:
            clean_path(targetPath)
            
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', filename='logkey-{0}.log'.format(get_dateString()),
        level=logging.DEBUG)
    run(PATHLIST, DAYFROM, DAYTO)
