import unittest
import bomberman as bm

class Test_Player(unittest.TestCase):
    def setUp(self):
        self.field_map = bm.FieldMap()
        self.player = bm.Player((1,1),self.field_map)
        pass

    def tearDown(self):
        pass

    def test_movement(self):
        flag = self.player.control()
        self.assertEqual(flag, False, "movement incorrect")

if __name__ == '__main__':
    unittest.main()
