"""
    Script to deploy a website to the server by ftp.

        - Compares local directory with remote directory
        - Updates modified files
        - Adds new files
        - Optionally, removes deleted files from remote

    Author: James Benson
    Version:
    Requires: python 3.3+
              Due to use of ftplib.mlsd()
"""
"""
    MLSD - means machine listing of directory
    TODO: FTP response codes to look out for:
        - 502 unknown command
        - 550 empty directory

    Good ones:
        - 226 transfer complete
"""
asciiExt = ['coffee', 'css', 'erb', 'haml', 'handlebars', 'hb', 'htm', 'html',
    'js', 'less', 'markdown', 'md', 'ms', 'mustache', 'php', 'rb', 'sass', 'scss',
    'slim', 'txt', 'xhtml', 'xml']
remoteSep = "/";
STOR_AUTO = 0;
STOR_BINARY = 1;
STOR_ASCII = 2;
######################### SETUP ##########################
remoteHost = "127.0.0.1";
remoteUser = "Benson";
remotePassword = "benson";
localPath = "D:\\test\\ftp";
remotePath = "/";

### OPTIONS ###
verbose = True;
remoteTLS = False;
remoteDelete = False;
storMode = STOR_BINARY;
##########################################################
import os;
from ftplib import FTP, FTP_TLS, error_reply, error_temp, error_perm, error_proto, all_errors;
if remoteTLS:
    import ssl;

ftp = None;
cwd = None;
# === FTP Functions ===
def connect():
    global ftp;
    if remoteTLS:
        context = ssl.create_default_context();
        ftp = FTP_TLS(remoteHost, remoteUser, remotePassword, acct="", keyfile=None, certfile=None, context=context, timeout=20);
        ftp.prot_p();
    else:
        ftp = FTP(remoteHost, remoteUser, remotePassword, 20);
    print(ftp.getwelcome());

def setCwd(path):
    ftp.cwd(path);
    global cwd;
    cwd = path;
    if verbose: print("Cwd: %s" % path);
def stor(file):
    """stor the file obj to the cwd of ftp server."""
    ext = os.path.splitext(file.name())[1];
    try:
        if (storMode == STOR_ASCII) or (storMode == STOR_AUTO and ext.lstrip('.') in asciiExt):
            # Store in ASCII mode
            if verbose: print("[asc] ", end="");
            #with open(file.path, "rt") as fo:
            ftp.storlines("STOR %s" % file.name(), open(file.path));
        else:
            # Store in binary mode
            if verbose: print("[bin] ", end="");
            ftp.storbinary("STOR %s" % file.name(), open(file.path, "rb"));
        # TODO: Add modified stamp to remote file.
        setModified(file);
        if verbose: print("Uploaded: %s -> %s" % (file.path, remoteJoin(cwd, file.name())));
    except OSError as oserror:
        print("Failed: %s\n  %s" % (file.path, oserror));

def rm(file):
    """Delete the file obj from the cwd of the fpt server."""
    ftp.delete(str(file));
    if verbose: print("Deleted: %s" % file.path);
def mkDir(name):
    ftp.mkd(name);
    if verbose: print("Created: %s" % remoteJoin(cwd, name));
def rmDir(name):
    """Delete directory with name from the current working directory."""
    ftp.rmd(name);
    if verbose: print("Deleted: %s" % remoteJoin(cwd, name));
def setModified(file):
    pass;
# === End FTP Functions ===

# === Traversal Functions ===
def traverse(localPath, remotePath = remoteSep):
    setCwd(remotePath);
    localDirs, localFiles = listLocal(localPath);
    remoteDirs, remoteFiles = listRemote(remotePath);
    newF, modifiedF, unmodifiedF, deletedF = compareFiles(localFiles, remoteFiles, remoteDelete);
    newD, existingD, deletedD = compareDirs(localDirs, remoteDirs, remoteDelete);
    for f in newF + modifiedF:
        stor(f);
    for d in newD:
        mkDir(d);
    for d in newD + existingD:
        traverse(os.path.join(localPath, d), remoteJoin(remotePath, d));
    if remoteDelete:
        for d in deletedD:
            rmDir(d);
        for f in deletedF:
            rm(f);

def listLocal(path):
    dirs = [];
    files = [];
    names = os.listdir(path);
    for n in names:
        fullp = os.path.join(path, n);
        if os.path.isdir(fullp):
            dirs.append(n);
        if os.path.isfile(fullp):
            #stat = os.stat(fullp);
            files.append(File(fullp, os.stat(fullp).st_mtime));
    return (dirs, files);

def listRemote(path):
    dirs = [];
    files = [];
    response = ftp.mlsd();
    for name, fact in response:
        if fact["type"] == "dir":
            dirs.append(name);
        if fact["type"] == "file":
            files.append(File(remoteJoin(path, name), fact["modify"]));
    return (dirs, files);

# === End Traversal Functions ===

def remoteJoin(pathA, pathB):
    if not pathA.endswith(remoteSep) and not pathB.startswith(remoteSep):
        pathA += remoteSep;
    elif pathA.endswith(remoteSep) and pathB.startswith(remoteSep):
        pathA = pathA.rstrip(remoteSep);
    return pathA + pathB;

# === Structures ===
class File(object):
    def __init__(self):
        self.path = "";
        self.modified = 0
    def __init__(self, path, modified):
        self.path = str(path);
        self.modified = int(modified);
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
    # End Object Comparison
    def name(self):
        return os.path.basename(self.path);
    def path(self):
        return self.path;
    def modified(self):
        return self.modified;
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
    if not os.path.isdir(localPath):
        print("Path Not Found: %s" % localPath);
        return -1;
    try:
        connect();
        traverse(localPath, remotePath);
    except error_reply as r:
        print(r);
    except error_temp as t:
        print(t);
    except error_perm as p:
        print(p);
    except error_proto as pr:
        print(pr);
    except all_errors as a:
        # REVIEW: all_errors is a tuple of (Error, OSError, EOFError)
        # printing like this won't work I doubt, not sure.
        print(a);
    finally:
        if not ftp == None:
            try:
                ftp.quit();
            except: pass;
            ftp.close();

if __name__ == "__main__":
    main();
