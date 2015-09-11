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

if __name__ == "__main__":
	unittest.main();
