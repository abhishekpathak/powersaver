from enum import Enum


class SleepModes(Enum):
    OFF = "off"
    STANDBY = "standby"
    SLEEP = "mem"
    HIBERNATE = "disk"
