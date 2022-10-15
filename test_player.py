import unittest
import bomberman as bm

class Test_Player(unittest.TestCase):
    def setUp(self):
        self.field_map = bm.FieldMap()
        self.player = bm.Player((1,1),self.field_map)
        pass

    def tearDown(self):
        pass

    def test_isMovable(self):
        WIDTH = int(bm.CHIPSIZE*0.8/2)

        flag = self.player.isMovable(int(bm.CHIPSIZE*0.1))
        self.assertEqual(flag, False, "judgement is invalid.")
        flag = self.player.isMovable(int(bm.CHIPSIZE*0.9))
        self.assertEqual(flag, False, "judgement is invalid.")
        flag = self.player.isMovable(bm.CHIPSIZE//2)
        self.assertEqual(flag, True, "judgement is invalid.")

        flag = self.player.isMovable(bm.CHIPSIZE*3 + int(bm.CHIPSIZE*0.1))
        self.assertEqual(flag, False, "judgement is invalid.")
        flag = self.player.isMovable(bm.CHIPSIZE*3 + int(bm.CHIPSIZE*0.9))
        self.assertEqual(flag, False, "judgement is invalid.")

if __name__ == '__main__':
    unittest.main()
