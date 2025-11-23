class Television:
    """
    A television that turned off/on, volume change, channel change.
    """

    MIN_VOLUME = 0
    MAX_VOLUME = 2
    MIN_CHANNEL = 0
    MAX_CHANNEL = 3

    def __init__(self) -> None:
        """Initialize the Television."""
        self.__status = False
        self.__muted = False
        self.__volume = Television.MIN_VOLUME
        self.__previous_volume = self.__volume
        self.__channel = Television.MIN_CHANNEL

    def power(self) -> None:
        """Switch the power on/off."""
        self.__status = not self.__status

    def mute(self) -> None:
        """Switch to mute when the television is on."""
        if self.__status:
            if not self.__muted:
                self.__previous_volume = self.__volume
                self.__volume = 0
                self.__muted = True
            else:
                self.__volume = self.__previous_volume
                self.__muted = False

    def channel_up(self) -> None:
        """Increase channel number."""
        if self.__status:
            if self.__channel == Television.MAX_CHANNEL:
                self.__channel = Television.MIN_CHANNEL
            else:
                self.__channel += 1

    def channel_down(self) -> None:
        """Decrease channel number."""
        if self.__status:
            if self.__channel == Television.MIN_CHANNEL:
                self.__channel = Television.MAX_CHANNEL
            else:
                self.__channel -= 1

    def volume_up(self) -> None:
        """Increase the volume when TV is on."""
        if self.__status:
            if self.__muted:
                self.__muted = False
                self.__volume = self.__previous_volume

            if self.__volume < Television.MAX_VOLUME:
                self.__volume += 1
            self.__previous_volume = self.__volume

    def volume_down(self) -> None:
        """Decrease the volume when TV is on.."""
        if self.__status:
            if self.__muted:
                self.__muted = False
                self.__volume = self.__previous_volume

            if self.__volume > Television.MIN_VOLUME:
                self.__volume -= 1
            self.__previous_volume = self.__volume

    def __str__(self) -> str:
        """Return to the formatted state of the television."""
        return (
            f"Power = {self.__status}, "
            f"Channel = {self.__channel}, "
            f"Volume = {self.__volume}"
        )
