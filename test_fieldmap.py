import unittest
import bomberman as bm

class Test_FieldMap(unittest.TestCase):
    def setUp(self):
        self.fmap = bm.FieldMap()
        pass

    def tearDown(self):
        pass

    def test_get_type(self):
        c0 = self.fmap.get((0,0))
        self.assertEqual(c0,bm.Type.HARD,"got value is invalid")
        c1 = self.fmap.get((1,1))
        self.assertEqual(c1,bm.Type.FREE,"got value is invalid")
        c2 = self.fmap.get((bm.CHIPNUM_W-1,bm.CHIPNUM_H-1))
        self.assertEqual(c2,bm.Type.HARD,"got value is invalid")

    def test_put_get(self):
        self.fmap.put((1,1),bm.Type.SOFT)
        chType = self.fmap.get((1,1))
        self.assertEqual(chType,bm.Type.SOFT,"put or get incorrect")

#    def test_getXY(self):
#        self.fmap.getXY(bm.CHIPSIZE+

if __name__ == '__main__':
    unittest.main()
