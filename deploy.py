"""
    Script to deploy a website to the server by ftp.

        - Compares local directory with remote directory
        - Updates modified files
        - Adds new files
        - Optionally, removes deleted files from remote

    Requires: python 3.3+
              Due to use of ftplib.mlsd()

    The MIT License (MIT)
    Copyright (c) 2015 James Benson
"""

"""
    TODO: FTP response codes to look out for:
        - 502 unknown command
        - 550 empty directory
        - 451 can't remove directory

    Good ones:
        - 226 transfer complete
"""
asciiExt = ['coffee', 'css', 'erb', 'haml', 'handlebars', 'hb', 'htm', 'html',
    'js', 'less', 'markdown', 'md', 'ms', 'mustache', 'php', 'rb', 'sass', 'scss',
    'slim', 'txt', 'xhtml', 'xml'];
deleteIgnoreFiles = ["/.ftpquota"];
deleteIgnoreDirs = ["/cgi-bin"];
remoteSep = "/";
dLogName = "debug.txt";
STOR_AUTO = 0;
STOR_BINARY = 1;
STOR_ASCII = 2;
UPLOAD_OVERWRITE = 0;
UPLOAD_MODIFIED = 1;
######################### SETUP ##########################
remoteHost = "127.0.0.1";
remoteUser = "Benson";
remotePassword = "benson";
localPath = "D:\\test\\ftp";
remotePath = "/";

### OPTIONS ###
verbose = True;
remoteTLS = False; # SSL/TLS doesn't work invalid certificate error
remoteDelete = True;
remoteIgnoreHidden = False; # TODO: Implement hidden.
storMode = STOR_BINARY; # only binary currently works
uploadMode = UPLOAD_MODIFIED;
debug = True;
##########################################################
import os;
from datetime import datetime, timedelta;
from ftplib import FTP, FTP_TLS, error_reply, error_temp, error_perm, error_proto, all_errors;
if remoteTLS:
    import ssl;

ftp = None;
dLog = None;
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

def stor(dirpath, file):
    """Store the file obj to the dirpath of server."""
    ext = (os.path.splitext(file.name())[1]).lstrip('.');
    storpath = remoteJoin(dirpath, file.name());
    try:
        if (storMode == STOR_ASCII) or (storMode == STOR_AUTO and ext in asciiExt):
            # Store in ASCII mode
            if verbose: print("[asc] ", end="");
            ftp.storlines("STOR %s" % storpath, open(file.path));
        else:
            # Store in binary mode
            if verbose: print("[bin] ", end="");
            ftp.storbinary("STOR %s" % storpath, open(file.path, "rb"));
        setModified(dirpath, file);
        if verbose: print("Uploaded: %s -> %s" % (file.path, storpath));
    except OSError as oserror:
        print("Failed Upload: %s\n  %s" % (file.path, oserror));
def setModified(dirpath, file):
    """Attempts to set the modified time with MFMT."""
    ftp.voidcmd("MFMT %s %s" % (file.getModified(), remoteJoin(dirpath, file.name())));
def rm(dirpath, file):
    """Delete the file at the path from the server."""
    p = remoteJoin(dirpath, file.name());
    _rm(p);
    if verbose: print("Deleted: %s" % p);
def _rm(filepath):
    ftp.delete(filepath);

def mkDir(dirpath, name):
    dirname = remoteJoin(dirpath, name);
    ftp.mkd(dirname);
    if verbose: print("Created: %s" % dirname);

def rmDir(dirpath, name, recursive = False):
    dirname = remoteJoin(dirpath, name);
    if recursive:
        _rmDirR(dirname);
        _rmDir(dirname);
    else:
        _rmDir(dirname);
    if verbose: print("Deleted: %s" % remoteJoin(dirname, "*"));
def _rmDir(dirpath):
    """Delete directory with name from the current working directory.
    Only deletes empty directories."""
    ftp.rmd(dirpath); # TODO: What if fails to delete?
def _rmDirR(dirpath):
    """Remove the directory at dirpath and its contents (recursive)."""
    try:
        dirs, files = listRemote(dirpath);
        for f in files:
            _rm(f.path);
        for d in dirs:
            _rmDirR(d.path);
            _rmDir(d.path);
    except:
        raise error_temp("451 Can't remove directory");
# === End FTP Functions ===

# === Traversal Functions ===
def traverse(localPath, remotePath = remoteSep):
    dprint("TRAVERSING: local %s | remote %s"%(localPath, remotePath));
    localDirs, localFiles = listLocal(localPath);
    remoteDirs, remoteFiles = listRemote(remotePath);
    newF, modifiedF, unmodifiedF, deletedF = compareFiles(localFiles, remoteFiles, remoteDelete);
    newD, existingD, deletedD = compareDirs(localDirs, remoteDirs, remoteDelete);
    for f in newF + modifiedF:
        stor(remotePath, f);
    for d in newD:
        mkDir(remotePath, d);
    for d in newD + existingD:
        dname = d.name();
        traverse(os.path.join(localPath, dname), remoteJoin(remotePath, dname));
    if remoteDelete:
        for d in deletedD:
            rmDir(remotePath, d, True);
        for f in deletedF:
            rm(remotePath, f);

def listLocal(path):
    dirs = [];
    files = [];
    names = os.listdir(path);
    for n in names:
        fullp = os.path.join(path, n);
        if os.path.isdir(fullp):
            dirs.append(Directory(fullp));
        if os.path.isfile(fullp):
            f = File(fullp);
            f.setModifiedTimestamp(os.stat(fullp).st_mtime);
            files.append(f);
    return (dirs, files);

def listRemote(path = ""):
    dirs = [];
    files = [];
    response = ftp.mlsd(path);
    for name, fact in response:
        if fact["type"] == "dir":
            dirs.append(Directory(remoteJoin(path, name)));
        if fact["type"] == "file":
            f = File(remoteJoin(path, name));
            f.setModifiedUTCStr(fact["modify"]);
            files.append(f);
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
    def __init__(self, path):
        self.path = str(path);
        self.datetimeFormat = "%Y%m%d%H%M%S";
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
    def setModifiedUTCStr(self, modified):
        # Should be a string of the utc time.
        self.modified = datetime.strptime(modified, self.datetimeFormat);
    def setModifiedTimestamp(self, modified):
        # Timestamp (in windows at least) gives extra microseconds (us) that ftp doesn't have
        usModified = datetime.utcfromtimestamp(modified)
        usExtra = timedelta(microseconds=usModified.microsecond);
        self.modified = usModified - usExtra;
    def getModified(self):
        return datetime.strftime(self.modified, self.datetimeFormat);

class Directory(object):
    def __init__(self, path):
        self.path = path;
    def __str__(self):
        return self.name();
    def __eq__(self, other):
        if isinstance(other, Directory):
            return self.name() == other.name();
        else:
            return self.name() == str(other);
    # def __len__(self):
    #     len()
    def name(self):
        if isinstance(self.path, Directory):
            raise Exception("Expected str found Directory");
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

    dprint("COMPARE FILES");
    for lfile in localList:
        dprint("LOCAL: %s - %s" % (lfile.path, lfile.modified));
        existsInRemote = False;
        for rfile in remoteList:
            if lfile == rfile:
                dprint("REMOTE: %s - %s" % (rfile.path, rfile.modified));
                existsInRemote = True;
                if uploadMode == UPLOAD_OVERWRITE or lfile > rfile:
                    dprint("Upload Mode: %s | Modified: lfile > rfile" % uploadMode);
                    modified.append(lfile);
                else:
                    dprint("Not Modified: lfile <= rfile");
                    unmodified.append(lfile);
                break;
        if not existsInRemote:
            dprint("New local file");
            new.append(lfile);
        dprint("--------------------------------------");

    # Check for deleted files
    if checkDeleted:
        dprint("CHECK FOR DELETED FILES");
        for rfile in remoteList:
            existsInLocal = False;
            for lfile in localList:
                if rfile == lfile:
                    existsInLocal = True;
                    break;
            if not existsInLocal and not rfile.path in deleteIgnoreFiles:
                dprint("DELETED: %s" % rfile.path);
                deleted.append(rfile);
        dprint("--------------------------------------");

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

    dprint("COMPARE DIRECTORIES");
    for ldir in localList:
        dprint("LOCAL DIR: %s"%ldir.path);
        existsInRemote = False;
        for rdir in remoteList:
            if ldir == rdir:
                dprint("REMOTE DIR: %s"%rdir.path);
                dprint("Exists On Local and Remote");
                existsInRemote = True;
                existing.append(ldir)
                break;
        if not existsInRemote:
            dprint("New Local Directory");
            new.append(ldir);

    # Check for deleted directories
    if checkDeleted:
        dprint("CHECK FOR DELETED DIRECTORIES");
        for rdir in remoteList:
            existsInLocal = False;
            for ldir in localList:
                if rdir == ldir:
                    existsInLocal = True;
                    break;
            if not existsInLocal and not rdir.path in deleteIgnoreDirs:
                dprint("DELETED: %s" % rdir.path);
                deleted.append(rdir);
        dprint("--------------------------------------");

    return (new, existing, deleted);

def dprint(line, end="\n"):
    global dLog;
    if debug:
        if dLog == None:
            if os.path.exists(dLogName):
                os.remove(dLogName);
            dLog = open(dLogName, "w")
        dLog.write(line + end);

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
        # printing like this won't work I doubt, but I'm doing it anyway.
        print(a);
    finally:
        if not ftp == None:
            try:
                ftp.quit();
            except: pass;
            ftp.close();
        if not dLog == None and not dLog.closed:
            dLog.flush();
            dLog.close();

if __name__ == "__main__":
    main();
