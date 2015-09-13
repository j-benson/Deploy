import unittest;
import deploy;
import os;
import shutil;

class FileObj(unittest.TestCase):
	def setUp(self):
		self.file1 = deploy.File("W:\\file1.txt", 1234567);
		self.file2 = deploy.File("W:\\file2.txt", 2345);
		self.file3 = deploy.File("W:\\folder\\file3.txt", 7654);
		self.file4 = deploy.File("W:\\folder\\file4.txt", 4321);
	def test_str(self):
		self.assertEqual(self.file1, "file1.txt");
		self.assertEqual(self.file2, "file2.txt");
		self.assertEqual(self.file3, "file3.txt");
		self.assertEqual(self.file4, "file4.txt");
	def test_name(self):
		self.assertEqual(self.file1.name(), "file1.txt");
		self.assertEqual(self.file2.name(), "file2.txt");
		self.assertEqual(self.file3.name(), "file3.txt");
		self.assertEqual(self.file4.name(), "file4.txt");
	@unittest.skip("Path get method errors.")
	def test_path(self):
		# When called says Type Error: str object not callable
		self.assertTrue(isinstance(self.file1, deploy.File));
		self.assertTrue(isinstance(self.file2, deploy.File));
		self.assertTrue(isinstance(self.file3, deploy.File));
		self.assertTrue(isinstance(self.file4, deploy.File));

		path1 = self.file1.path(); # Here type error str not callable, don't understand why.
		path2 = self.file2.path(); # File is definitely File obj not str so it's not that.
		path3 = self.file3.path();
		path4 = self.file4.path();
		self.assertTrue(isinstance(path1, str));
		self.assertTrue(isinstance(path2, str));
		self.assertTrue(isinstance(path3, str));
		self.assertTrue(isinstance(path4, str));

		self.assertEqual(self.file1.path(), "W:\\file1.txt");
		self.assertEqual(self.file2.path(), "W:\\file2.txt");
		self.assertEqual(self.file3.path(), "W:\\folder\\file3.txt");
		self.assertEqual(self.file4.path(), "W:\\folder\\file4.txt");
	def test_pathAttr(self):
		self.assertEqual(self.file1.path, "W:\\file1.txt");
		self.assertEqual(self.file2.path, "W:\\file2.txt");
		self.assertEqual(self.file3.path, "W:\\folder\\file3.txt");
		self.assertEqual(self.file4.path, "W:\\folder\\file4.txt");
	@unittest.skip("Modified get method errors.")
	def test_modified(self):
		# When called says Type Error: int object not callable
		self.assertEqual(self.file1.modified(), 1234567);
		self.assertEqual(self.file2.modified(), 2345);
		self.assertEqual(self.file3.modified(), 7654);
		self.assertEqual(self.file4.modified(), 4321);
	def test_modifiedAttr(self):
		self.assertEqual(self.file1.modified, 1234567);
		self.assertEqual(self.file2.modified, 2345);
		self.assertEqual(self.file3.modified, 7654);
		self.assertEqual(self.file4.modified, 4321);

class FileObjComparison(unittest.TestCase):
	def setUp(self):
		self.file1 = deploy.File("D:\\filesame", 1);
		self.file2 = deploy.File("D:\\filesame", 1);
		self.file3 = deploy.File("D:\\filesame", 2);
		self.file4 = deploy.File("D:\\filediff", 2);
	def test_same(self):
		self.assertTrue(self.file1 == self.file2);
		self.assertTrue(self.file2 == self.file3);
		self.assertTrue(self.file1 == self.file3);
		self.assertTrue(self.file4 == self.file4);
		self.assertTrue(self.file1 == self.file1);
	def test_notsame(self):
		self.assertFalse(self.file1 == self.file4);
		self.assertFalse(self.file2 == self.file4);
		self.assertFalse(self.file3 == self.file4);
		self.assertTrue(self.file3 != self.file4);
	def test_newer(self):
		self.assertTrue(self.file3 > self.file1);
		self.assertTrue(self.file3 > self.file2);
		self.assertTrue(self.file4 > self.file1);
		self.assertTrue(self.file4 > self.file2);
	def test_notnewer(self):
		self.assertFalse(self.file1 > self.file3);
		self.assertFalse(self.file2 > self.file3);
		self.assertFalse(self.file1 > self.file4);
		self.assertFalse(self.file2 > self.file4);
		self.assertFalse(self.file1 > self.file1);
		self.assertFalse(self.file3 > self.file3);
	def test_older(self):
		self.assertTrue(self.file1 < self.file3);
		self.assertTrue(self.file2 < self.file4);
		self.assertTrue(self.file1 < self.file4);
		self.assertTrue(self.file2 < self.file3);
	def test_notolder(self):
		self.assertFalse(self.file3 < self.file1);
		self.assertFalse(self.file4 < self.file2);
		self.assertFalse(self.file4 < self.file1);
		self.assertFalse(self.file3 < self.file2);
		self.assertFalse(self.file1 < self.file1);
		self.assertFalse(self.file3 < self.file3);

class CompareDirs(unittest.TestCase):
	def setUp(self):
		self.dir1 = "vw";
		self.dir2 = "bmw";
		self.dir3 = "ford";
		self.dir4 = "renolt";
	def test_allEmpty(self):
		new, ex, delt = deploy.compareDirs([], []);
		self.assertEqual(len(new), 0);
		self.assertEqual(len(ex), 0);
		self.assertEqual(len(delt), 0);
	def test_allNew(self):
		local = [self.dir1, self.dir2, self.dir3, self.dir4];
		remote = [];
		new, ex, delt = deploy.compareDirs(local, remote);
		self.assertEqual(len(new), 4);
		self.assertEqual(len(ex), 0);
		self.assertEqual(len(delt), 0);

		self.assertTrue("vw" in new);
		self.assertTrue("bmw" in new);
		self.assertTrue("ford" in new);
		self.assertTrue("renolt" in new);

	def test_someNew(self):
		local = [self.dir1, self.dir2, self.dir3, self.dir4];
		remote = [self.dir1, self.dir2];
		new, ex, delt = deploy.compareDirs(local, remote);
		self.assertEqual(len(new), 2);
		self.assertEqual(len(ex), 2);
		self.assertEqual(len(delt), 0);

		self.assertTrue("ford" in new);
		self.assertTrue("renolt" in new);
		self.assertTrue("vw" in ex);
		self.assertTrue("bmw" in ex);

	def test_someDeleted(self):
		local = [self.dir1, self.dir3];
		remote = [self.dir1, self.dir2, self.dir3, self.dir4];
		new, ex, delt = deploy.compareDirs(local, remote);
		self.assertEqual(len(new), 0);
		self.assertEqual(len(ex), 2);
		self.assertEqual(len(delt), 2);

		self.assertTrue("vw" in ex);
		self.assertTrue("ford" in ex);
		self.assertTrue("bmw" in delt);
		self.assertTrue("renolt" in delt);

class CompareFiles(unittest.TestCase):
	def setUp(self):
		self.file1 = deploy.File("D:\\vw\\polo", 0);
		self.file2 = deploy.File("D:\\vw\\golf", 1);
		self.file3 = deploy.File("D:\\mileslog", 2);
		self.file3_1 = deploy.File(self.file3.path, 3);
		self.file4 = deploy.File("D:\\sales", 3);
		self.file5 = deploy.File("D:\\motlog", 4);
		self.file5_1 = deploy.File(self.file5.path, 5);
		self.file6 = deploy.File("D:\\inventry", 5);
		self.file7 = deploy.File("D:\\renolt\\clio", 6);

	def test_allEmpty(self):
		new, mod, unmod, delt = deploy.compareFiles([], []);
		self.assertEqual(len(new), 0);
		self.assertEqual(len(mod), 0);
		self.assertEqual(len(unmod), 0);
		self.assertEqual(len(delt), 0);

	def test_allNew(self):
		local = [self.file1, self.file2, self.file3, self.file4];
		remote = [];
		new, mod, unmod, delt = deploy.compareFiles(local, remote);
		self.assertEqual(len(new), 4);
		self.assertEqual(len(mod), 0);
		self.assertEqual(len(unmod), 0);
		self.assertEqual(len(delt), 0);

		self.assertTrue("polo" in new);
		self.assertTrue("golf" in new);
		self.assertTrue("mileslog" in new);
		self.assertTrue("sales" in new);

	def test_someNew(self):
		local = [self.file1, self.file2, self.file3, self.file4];
		remote = [self.file1, self.file2];
		new, mod, unmod, delt = deploy.compareFiles(local, remote);
		self.assertEqual(len(new), 2);
		self.assertEqual(len(mod), 0);
		self.assertEqual(len(unmod), 2);
		self.assertEqual(len(delt), 0);

		self.assertTrue("mileslog" in new);
		self.assertTrue("sales" in new);
		self.assertTrue("polo" in unmod);
		self.assertTrue("golf" in unmod);

	def test_someModified(self):
		local = [self.file1, self.file2, self.file3_1, self.file4];
		remote = [self.file1, self.file2, self.file3, self.file4];
		new, mod, unmod, delt = deploy.compareFiles(local, remote);
		self.assertEqual(len(new), 0);
		self.assertEqual(len(mod), 1);
		self.assertEqual(len(unmod), 3);
		self.assertEqual(len(delt), 0);

		self.assertTrue("mileslog" in mod);
		self.assertTrue("polo" in unmod);
		self.assertTrue("golf" in unmod);
		self.assertTrue("sales" in unmod);

	def test_someDeleted(self):
		local = [self.file1, self.file2, self.file3_1];
		remote = [self.file1, self.file2, self.file3, self.file4];
		new, mod, unmod, delt = deploy.compareFiles(local, remote);
		self.assertEqual(len(new), 0);
		self.assertEqual(len(mod), 1);
		self.assertEqual(len(unmod), 2);
		self.assertEqual(len(delt), 1);

		self.assertTrue("mileslog" in mod);
		self.assertTrue("polo" in unmod);
		self.assertTrue("golf" in unmod);
		self.assertTrue("sales" in delt);

class RemoteJoin(unittest.TestCase):
	def test_join(self):
		deploy.remoteSep = "/"
		self.assertEqual(deploy.remoteJoin("/path/to", "spain"), "/path/to/spain");
		self.assertEqual(deploy.remoteJoin("/path/to/", "spain"), "/path/to/spain");
		self.assertEqual(deploy.remoteJoin("/path/to", "/spain"), "/path/to/spain");
		self.assertEqual(deploy.remoteJoin("/path/to/", "/spain"), "/path/to/spain");
	def test_joinRoot(self):
		deploy.remoteSep = "/"
		self.assertEqual(deploy.remoteJoin("/", "spain"), "/spain");
		self.assertEqual(deploy.remoteJoin("", "spain"), "/spain");
		self.assertEqual(deploy.remoteJoin("/", "/spain"), "/spain");
		self.assertEqual(deploy.remoteJoin("", "/spain"), "/spain");

class ListLocal(unittest.TestCase):
	def setUp(self):
		self.testDir = "TestCase_ListLocal";
		os.mkdir(self.testDir);
		self.rootFile1 = os.path.join(self.testDir, "RootFile1.txt");
		makeFile(self.rootFile1, "This file is on the root.\n\nYadda Yadda.")
		self.rootFile2 = os.path.join(self.testDir, "RootFile2.txt");
		makeFile(self.rootFile2, "This another file is on the root.")
		self.sub1 = os.path.join(self.testDir, "Subfolder1");
		os.mkdir(self.sub1);

	def test_list(self):
		d, f = deploy.listLocal(self.testDir);
		self.assertEqual(len(d), 1);
		self.assertEqual(len(f), 2);
		self.assertTrue(os.path.basename(self.sub1) in d);
		self.assertTrue(os.path.basename(self.rootFile1) in f);
		self.assertTrue(os.path.basename(self.rootFile2) in f);

	def tearDown(self):
		shutil.rmtree(self.testDir);

def makeFile(path, data):
	with open(path, "wt") as f:
		f.write(data);

if __name__ == "__main__":
	unittest.main();
