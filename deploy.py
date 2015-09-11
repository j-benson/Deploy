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
class Dir(object):
    """Not sure whether I'll use this?"""
    def __init__(self):
        pass;
    def __init__(self, path):
        self.path = path;
        self.files = [];
    def __eq__(self, other):
        if isinstance(other, Dir):
            return self.name() == other.name();
        else:
            return self.name() == str(other);
    def name(self):
        return os.path.basename(self.path);
    def addFile(file):
        self.files.append(file);

class File(object):
    def __init__(self):
        self.path = "";
        self.modified = 0
    def __init__(self, path, modified):
        self.path = path;
        self.modified = modified;
    # Object Comparison
    def __eq__(self, other):
        """As File objects will only be compared within a directory the unique
        identitifier will be the name."""
        if isinstance(other, File):
            return self.name() == other.name();
        else:
            return self.name() == str(other);
    def __lt__(self, other):
        """Determine if the file is older than other using the modified timestamp."""
        return self.modified < other.modified;
    def __gt__(self, other):
        """Determine if the file is newer than other using the modified timestamp."""
        return self.modified > other.modified;
    def __le__(self, other):
        """Determine if the file is older or the same than other using the modified timestamp."""
        return self.modified <= other.modified;
    def __ge__(self, other):
        """Determine if the file is newer or the same than other using the modified timestamp."""
        return self.modified >= other.modified;

    def name(self):
        return os.path.basename(self.path);
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
            if lfile == rfile:
                existsInRemote = True;
                if lfile > rfile:
                    modified.append(lfile);
                else:
                    unmodified.append(lfile);
                break;
        if not existsInRemote:
            new.append(lfile);

    # Check for deleted files
    if checkDeleted:
        for rfile in remoteList:
            existsInLocal = False;
            for lfile in localList:
                if rfile == lfile:
                    existsInLocal = True;
                    break;
            if not existsInLocal:
                deleted.append(rfile);

    return (new, modified, unmodified, deleted);

def compareDirs(localList, remoteList, checkDeleted = True):
    """Compares localList with remoteList gets the tuple containing string
    names of the directories: (new, existing, deleted)
        new: Directories that are in localList but not in remoteList.
        existing: Directories that are in both lists.
        deleted: Directories that are in the remoteList but not in localList.
    localList - list of strings of the directory names in the local location.
    remoteList - list of strings of the directory name in the remote location."""
    new = [];
    existing = [];
    deleted = [];

    for ldir in localList:
        existsInRemote = False;
        for rdir in remoteList:
            if ldir == rdir:
                existsInRemote = True;
                existing.append(ldir)
                break;
        if not existsInRemote:
            new.append(ldir);

    # Check for deleted files
    if checkDeleted:
        for rdir in remoteList:
            existsInLocal = False;
            for ldir in localList:
                if rdir == ldir:
                    existsInLocal = True;
                    break;
            if not existsInLocal:
                deleted.append(rdir);

    return (new, existing, deleted);

def main():
    pass

if __name__ == "__main__":
    main();
