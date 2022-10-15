import unittest
import bomberman as bm

class Test_Player(unittest.TestCase):
    def setUp(self):
        self.field_map = bm.FieldMap()
        self.player = bm.Player((1,1),self.field_map)
        self.player.speed = 2
        pass

    def tearDown(self):
        pass

    def test_movement(self):
        self.player.XY = (1,1)
        print("\n simple move to +DX for 10-loop")
        print(f"{self.player.xy}")
        ini_x,ini_y = self.player.xy
        key_input = bm.KeyInput.RIGHT
        LOOP = 10
        for _ in range(LOOP):
            self.player.control(key_input)
        sim_x = ini_x + self.player.speed * LOOP
        print(f"{self.player.xy},sim_x = {sim_x}")
        self.assertEqual(sim_x, self.player.xy[0], "movement incorrect")

    def test_sliding(self):
#        self.player.xy = (int(bm.CHIPSIZE*(self.player.XY[0]+1/2)),
#                          int(bm.CHIPSIZE*(self.player.XY[1]+1/2))-5)
        self.player.xy = (int(bm.CHIPSIZE*(1+1/2))-5,
                          int(bm.CHIPSIZE*(1+1/2)))
        #self.player.control(bm.KeyInput.NONE)
        print("\n sliding at upper-left corner +DY for 10-loop")
        print(f"{self.player.xy}")
        print(f"{self.player.XY}")
        ini_x,ini_y = self.player.xy
        key_input = bm.KeyInput.DOWN
        LOOP = 10
        for _ in range(LOOP):
            flag = self.player.control(key_input)
        sim_x = ini_x + self.player.speed * LOOP
        print(f"{self.player.xy},sim_x = {sim_x}")
        self.assertEqual(sim_x, self.player.xy[0], "movement incorrect")

if __name__ == '__main__':
    unittest.main()
