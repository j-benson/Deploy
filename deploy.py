"""
    Script to deploy a website to the server by ftp.

    - Compare local directory with remote directory
    - Update modified files
    - Add new files
    - Optional, remove deleted files from remote
    - Traverse directories, remote and local.


    ----------
    input:
        Website directory on local filesystem
        FTP server address
        FTP username and password
        Website directory on FTP server
    process:
        traverse local file tree
        traverse remote file tree
        At each stage in the traversal
            compare local dirs and files with remote -> to find new and modified dirs and files
            compare remote dirs and files with local -> to find deleted dirs and files.
"""
######################### SETUP ##########################
remoteHost = "127.0.0.1";
remoteUser = "Benson";
remotePassword = "benson";
localPath = "D:\\test\\remote";
remotePath = "/";

### OPTIONS ###
remoteTLS = False;
remoteDelete = False;

##########################################################
import os;
from ftplib import FTP, FTP_TLS;
if remoteTLS:
    import ssl;

ftp = None;

def connect():
    if remoteTLS:
        context = ssl.create_default_context();
        ftp = FTP_TLS(remoteHost, remoteUser, remotePassword, acct="", keyfile=None, certfile=None, context=context);
        ftp.prot_p();
    else:
        ftp = FTP(remoteHost, remoteUser, remotePassword);
    print(ftp.getwelcome());

# === Traversal Functions ===
def traverse():
    # traverse local first

    # local files
    localFiles = listFiles(localPath);

def _traverse(path):
    pass

def listDirs(path, rpath = ""):
    pass
def _local_listDirs(path, rpath):
    pass
def _remote_listDirs(path, rpath):
    pass

def listFiles(path, rpath = ""):
    """ Get a list of files within a directory relative to the home path. """
    pass
def _local_listFiles(path, rpath):
    pass
def _remote_listFiles(path, rpath):
    pass


# === End Traversal Functions ===

# === Structures ===
class File(object):
    def __init__(self):
        self.path = "";
        self.rpath = "";
        self.name = "";
        self.modified = "";
    def __init__(self, path, rpath, name, modified):
        self.path = path;
        self.rpath = rpath;
        self.name = name;
        self.modified = modified;
# === End Structures ===

def compareFiles(localList, remoteList, checkDeleted = True):
    """Compares localList with remoteList gets the tuple containing File objects:
    (new, modified, unmodified, deleted)
        new: Files that are in localList but not in remoteList.
        modified: Files that are newer in localList than remoteList.
        unmodified: Files that are the same in both lists.
        deleted: Files that are in the remoteList but not in localList.
    *newer is defined by the file's date modified attribute.
    New, Modified and Unmodified will contain local files objects that need to
    be uploaded to the remote location.
    Deleted will contain remote file objects that need to be deleted from
    the remote location."""
    new = [];
    modified = [];
    unmodified = [];
    deleted = [];

    for lfile in localList:
        existsInRemote = False;
        for rfile in remoteList:
            if lfile.name == rfile.name:
                existsInRemote = True;
                if lfile.modified > rfile.modified:
                    modified.add(lfile);
                else:
                    unmodified.add(lfile);
                break;
        if not existsInRemote:
            new.add(lfile);

    # Check for deleted files
    if checkDeleted:
        for rfile in remoteList:
            existsInLocal = False;
            for lfile in localList:
                if rfile.name == lfile.name:
                    existsInLocal = True;
                    break;
            if not existsInLocal:
                deleted.add(rfile);

    return (new, modified, unmodified, deleted);

def main():
    pass


if __name__ == "__main__":
    main();
