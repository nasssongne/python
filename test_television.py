import pytest
from television import *

class Test:

    def setup_method(self):
        self.tv1 = Television()

    def teardown_method(self):
        self.tv1 = None

    def test_init(self):
        assert str(self.tv1) == "Power = False, Channel = 0, Volume = 0"

    def test_power(self):
        self.tv1.power()
        assert str(self.tv1) == "Power = True, Channel = 0, Volume = 0"

        self.tv1.power()
        assert str(self.tv1) == "Power = False, Channel = 0, Volume = 0"

    def test_mute(self):
        self.tv1.power()
        self.tv1.volume_up()
        self.tv1.mute()
        assert str(self.tv1) == "Power = True, Channel = 0, Volume = 0"

        self.tv1.mute()
        assert str(self.tv1) == "Power = True, Channel = 0, Volume = 1"

        self.tv1.power()
        self.tv1.mute()
        assert str(self.tv1) == "Power = False, Channel = 0, Volume = 0"
