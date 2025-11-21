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
        assert "Power = True" in str(self.tv1)

        self.tv1.power()
        assert "Power = False" in str(self.tv1)

    def test_mute(self):
        self.tv1.power()
        self.tv1.volume_up()
        self.tv1.mute()
        assert "Volume = 1" in str(self.tv1)

        self.tv1.mute()
        assert "Volume = 1" in str(self.tv1)


        self.tv1.power()
        self.tv1.mute()
        assert "Power = False" in str(self.tv1)