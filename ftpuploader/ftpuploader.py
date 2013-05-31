import ftplib
import logging
import os
import shutil
import time

def get_dateString(day=0):
	now = time.localtime(time.time() + day * 86400)
	result = time.strftime("%Y.%m.%d", now)
	return result

def get_dateFolder(path):
    return time.strftime("%Y.%m.%d", time.gmtime())

def create_folder(path):
    if os.path.exists(path):
        logging.warning("Path {0} exist! We need to remove it!".format(path))
        shutil.rmtree(path)
    shutil.os.mkdir(path)
    logging.info("mkdir {0}".format(path))

def get_fileName(filePath):
    formatPath = filePath.replace("/", "\\")
    if "\\" not in formatPath:
        return formatPath
    return formatPath[formatPath.rfind("\\")+1:]

def get_relativePath(copath, path, outputPrefix = ""):
    if not path.startswith(copath):
        raise
    relativePath = path[len(copath):]
    if relativePath.startswith("\\") or relativePath.startswith("/"):
        return outputPrefix + relativePath[1:]
    return outputPrefix + relativePath
    
def transfer_dict(targetPath):
    resultDict = {}
    resultDict["."] = []
    list = os.listdir(targetPath)
    if len(list) > 0:
        for item in list:
            sub = os.path.join(targetPath, item)
            if os.path.isfile(sub):
                resultDict["."].append(sub)
            elif os.path.isdir(sub):
                resultDict[item] = transfer_dict(sub)
            else:
                raise
    return resultDict
    
def ftp_action(ftp, fileDict):
    for key in fileDict:
        if key == ".":
            for file in fileDict[key]:
                if not os.path.isfile(file):
                    logging.error("The file {0} does not exist anymore!".format(file))
                    continue
                with open(file, "rb") as f:
                    ftp.storbinary("STOR {0}".format(get_fileName(file)), f)
        else:
            try:
                ftp.mkd(key)
                logging.info("make directory {0}".format(key))
                ftp.cwd(key)
                logging.info("cwd to {0}".format(key))
                ftp_action(ftp, fileDict[key])
                ftp.cwd("..")
            except:
                logging.error("ftp exception! folder is {0}".format(key))
                return
            
    
def upload_directory(targetPath, ftpSubpath, host, user, password):
    ftp = ftplib.FTP(host)
    with ftplib.FTP(host) as ftp:
        ftp.login(user, password, 1000)
        subList = [path for path in ftpSubpath.split("\\") if path != ""]
        for sub in subList:
            ftp.cwd(sub)
        fileDict = transfer_dict(targetPath)
        if fileDict == {}:
            logging.error("target path is wrong!")
            return
        ftp_action(ftp, fileDict)
    logging.info("ftp copy done.")
    
def upload_daily(pairs, host, user, password, fun_getDateString):
    '''
    :Args:
         - pairs: each pair has three elements: source path, ftp server path, root path of ftp server
    '''
    for pair in pairs:
        if not os.path.isdir(pair[0]):
            logging.error("Wrong path! Path {0} does not exist! ".format(pair[0]))
        else:
            #deal with paths, add date string
            sourcePath = os.path.join(pair[0], fun_getDateString(pair[0]))
            #check whether the path exists
            if not os.path.isdir(sourcePath):
                logging.error("Not ready! Path {0} does not exist".format(sourcePath))
                continue
            
            #create path on ftp server
            pathOnFtpServer = os.path.join(pair[1], fun_getDateString(pair[1]))
            ftpSubpath = get_relativePath(pair[2], pathOnFtpServer)
            create_folder(pathOnFtpServer)
            
            #ftp copy files in target path
            logging.info("uploading {0}".format(pair[0]))
            upload_directory(sourcePath, ftpSubpath, host, user, password)
            logging.info("upload complete.")
            
    
if __name__ == "__main__":
    HOST = "testhost"
    USER = r"domain\username"
    PASSWORD = "password"
    PAIR_LIST = [
    (r"\\sourceserver\source\path", r"\\targetserver\target\path", r"\\sourceserver\source")
    ]
    logging.basicConfig(format='%(asctime)s %(message)s', filename='logkey-{0}.log'.format(get_dateString()),
        level=logging.DEBUG)
    upload_daily(PAIR_LIST, HOST, USER, PASSWORD, get_dateFolder)