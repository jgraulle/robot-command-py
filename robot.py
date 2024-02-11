from jsonRpcTcpClient import JsonRpcTcpClient
import threading
import enum
import time
from collections import namedtuple
from typing import Any


class Robot:
    class EventType(enum.Enum):
        IR_DISTANCE = enum.auto()
        LINE_TRACK_IS_DETECTED = enum.auto()
        LINE_TRACK_VALUE = enum.auto()
        ENCODER_WHEEL = enum.auto()
        SWITCH = enum.auto()
        ULTRASOUNDS_DISTANCE = enum.auto()

    RIGHT:int = 0
    LEFT:int = 1

    class Values:
        Value = namedtuple('Value', ['value', 'changedCount'])

        def __init__(self, robot: "Robot", eventType: "Robot.EventType"):
            self._robot = robot
            self._eventType = eventType
            self._values = dict()
            self._mutex = threading.Lock()

        def getValue(self, index: int) -> Any:
            with self._mutex:
                assert(index in self._values)
                return self._values[index].value

        def receiveHandle(self, params):
            assert("index" in params)
            index = params["index"]
            assert("value" in params)
            value = params["value"]
            assert("changedCount" in params)
            changedCount = params["changedCount"]
            with self._mutex:
                if index in self._values:
                    assert(self._values[index].changedCount+1 == changedCount)
                self._values[index] = Robot.Values.Value(value, changedCount)
                self._robot.notify(self._eventType)

    def __init__(self, hostIpAddress: str, tcpPort: int):
        self._jsonRpcTcpClient = JsonRpcTcpClient(hostIpAddress, tcpPort)
        self._event = threading.Event()
        self._toNotifiedEventTypes = set()
        self._toNotifiedEventTypesMutex = threading.Lock()
        self._notifiedEventTypes = None
        # Values binding
        self._irsDistance = Robot.Values(self, Robot.EventType.IR_DISTANCE)
        self._jsonRpcTcpClient.bindNotification("irProximityDistanceDetected",
                lambda params: self._irsDistance.receiveHandle(params))
        self._lineTracksIsDetected = Robot.Values(self, Robot.EventType.LINE_TRACK_IS_DETECTED)
        self._jsonRpcTcpClient.bindNotification("lineTrackIsDetected",
                lambda params: self._lineTracksIsDetected.receiveHandle(params))
        self._lineTracksValue = Robot.Values(self, Robot.EventType.LINE_TRACK_VALUE)
        self._jsonRpcTcpClient.bindNotification("lineTrackValue",
                lambda params: self._lineTracksValue.receiveHandle(params))
        self._wheelsStep = Robot.Values(self, Robot.EventType.ENCODER_WHEEL)
        self._jsonRpcTcpClient.bindNotification("speedValue",
                lambda params: self._wheelsStep.receiveHandle(params))
        self._switchs = Robot.Values(self, Robot.EventType.SWITCH)
        self._jsonRpcTcpClient.bindNotification("switchIsDetected",
                lambda params: self._switchs.receiveHandle(params))
        self._ultrasoundsDistance = Robot.Values(self, Robot.EventType.ULTRASOUNDS_DISTANCE)
        self._jsonRpcTcpClient.bindNotification("ultrasoundDistanceDetected",
                lambda params: self._ultrasoundsDistance.receiveHandle(params))
        # Start
        self._isReadySemaphore = threading.Semaphore(1)
        self._jsonRpcTcpClient.bindNotification("setIsReady",
                lambda params: self._setIsReadyHandle(params))
        self._jsonRpcTcpClient.startReceive()

    def waitReady(self):
        self._isReadySemaphore.acquire()
        time.sleep(1.0)

    def setMotorsPower(self, rightValue: float, leftValue: float):
        self._jsonRpcTcpClient.callNotification("setMotorsSpeed", {"rightValue": rightValue, "leftValue": leftValue})

    def getLineTracksIsDetected(self, index: int) -> bool:
        return self._lineTracksIsDetected.getValue(index)

    def getLineTracksValue(self, index: int) -> int:
        return self._lineTracksValue.getValue(index)

    def getWheelsStep(self, index: int) -> int:
        return self._wheelsStep.getValue(index)

    def getSwitchs(self, index: int) -> bool:
        return self._switchs.getValue(index)

    def getUltrasoundsDistance(self, index: int) -> int:
        return self._ultrasoundsDistance.getValue(index)

    def waitChanged(self, eventTypes: EventType|set[EventType], timeout: float|None=None) -> EventType|None:
        # For eventTypes to be a set
        if isinstance(eventTypes, Robot.EventType):
            eventTypes = {eventTypes}
        # Save event type set
        with self._toNotifiedEventTypesMutex:
            assert(len(self._toNotifiedEventTypes)==0)
            assert(self._notifiedEventTypes == None)
            assert(not self._event.is_set())
            self._toNotifiedEventTypes = eventTypes
        # Wait event
        self._event.wait(timeout)
        with self._toNotifiedEventTypesMutex:
            self._toNotifiedEventTypes.clear()
            toReturn = self._notifiedEventTypes
            self._notifiedEventTypes = None
            self._event.clear()
            return toReturn

    def notify(self, eventType: EventType):
        with self._toNotifiedEventTypesMutex:
            if eventType in self._toNotifiedEventTypes:
                self._notifiedEventTypes = eventType
                self._event.set()

    def close(self):
        self._jsonRpcTcpClient.close()

    def _setIsReadyHandle(self, params):
        assert(params == None)
        self._isReadySemaphore.release()
