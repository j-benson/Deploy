import unittest;
import deploy;

class CompareFileObj(unittest.TestCase):
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

if __name__ == "__main__":
	unittest.main();
