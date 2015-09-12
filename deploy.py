"""
    Script to deploy a website to the server by ftp.

    - Compare local directory with remote directory
    - Update modified files
    - Add new files
    - Optional, remove deleted files from remote

    Author: James Benson
    Version: 0.8.0
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
remoteASCII = ['coffee', 'css', 'erb', 'haml', 'handlebars', 'hb', 'htm', 'html',
    'js', 'less', 'markdown', 'md', 'ms', 'mustache', 'php', 'rb', 'sass', 'scss',
    'slim', 'txt', 'xhtml', 'xml']
##########################################################
import os;
from ftplib import FTP, FTP_TLS;
if remoteTLS:
    import ssl;

ftp = None;
# === FTP Functions ===
def connect():
    if remoteTLS:
        context = ssl.create_default_context();
        ftp = FTP_TLS(remoteHost, remoteUser, remotePassword, acct="", keyfile=None, certfile=None, context=context, timeout=20);
        ftp.prot_p();
    else:
        ftp = FTP(remoteHost, remoteUser, remotePassword, 20);
    print(ftp.getwelcome());

def setCwd(path):
    response = ftp.cwd(path);
def send(file):
    """Send the file obj to the cwd of ftp server."""
    pass;
def rm(file):
    """Delete the file obj from the cwd of the fpt server."""
    response = ftp.delete(str(file));
def mkDir(name):
    response = ftp.mkd(name);
def rmDir(name):
    """Delete directory with name from the current working directory."""
    response = ftp.rmd(name);
# === End FTP Functions ===

# === Traversal Functions ===
def traverse(localPath, remotePath):
    setCwk(remotePath);
    newF, modifiedF, unmodifiedF, deletedF = compareFiles(listLocalFiles(localPath),
                                                        listRemoteFiles(remotePath),
                                                        remoteDelete);
    newD, existingD, deletedD = compareDirs(listLocalDirs(localPath),
                                listRemoteDirs(remotePath),
                                remoteDelete);
    for f in newF + modifiedF:
        send(f);
    if remoteDelete:
        for f in deletedF:
            rm(f);
    for d in newD:
        mkdir(d);
    for d in newD + existingD:
        traverse(os.path.join(localPath, d), remotePath + "/" + d);
    if remoteDelete:
        for d in deletedD:
            rmDir(d);

def listLocalDirs(path):
    dirs = [];
    names = os.listdir(path);
    for n in names:
        if os.path.isdir(os.path.join(path, n)):
            dirs.append(n);
    return dirs;
def listRemoteDirs(path):
    return [];

def listLocalFiles(path):
    files = [];
    names = os.listdir(path);
    for n in names:
        fpath = os.path.join(path, n);
        if os.path.isfile(fpath):
            files.append(File(fpath, 0)); # TODO: get date modified
    return files;
def listRemoteFiles(path):
    return [];
# === End Traversal Functions ===

# === Structures ===
class File(object):
    def __init__(self):
        self.path = "";
        self.modified = 0
    def __init__(self, path, modified):
        self.path = path;
        self.modified = modified;
    def __str__(self):
        return self.name();
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
