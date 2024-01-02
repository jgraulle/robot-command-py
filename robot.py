from jsonRpcTcpClient import JsonRpcTcpClient
import threading
import enum
import time
from collections import namedtuple
from typing import Any


class Robot:
    class MotorIndex(enum.Enum):
        RIGHT = enum.auto()
        LEFT = enum.auto()

    class EventType(enum.Enum):
        IR_DISTANCE = enum.auto()
        LINE_TRACK_IS_DETECTED = enum.auto()
        LINE_TRACK_VALUE = enum.auto()
        WHEEL_STEP = enum.auto()
        SWITCH = enum.auto()
        ULTRASOUNDS_DISTANCE = enum.auto()

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
                self._robot.notify(self._eventType, changedCount)

    def __init__(self, hostIpAddress: str, tcpPort: int):
        self._jsonRpcTcpClient = JsonRpcTcpClient(hostIpAddress, tcpPort)
        self._event = threading.Event()
        self._lastNotifiedEventType = dict()
        self._lastNotifiedEventTypeMutex = threading.Lock()
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
        self._wheelsStep = Robot.Values(self, Robot.EventType.WHEEL_STEP)
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

    def setMotorSpeed(self, motorIndex: MotorIndex, value: float):
        self._jsonRpcTcpClient.callNotification("setMotorSpeed", {"motorIndex": motorIndex.name, "value": value})

    def setMotorsSpeed(self, rightValue: float, leftValue: float):
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

    def waitChanged(self, eventType: EventType|set[EventType], timeout: float|None=None) -> EventType|None:
        return self._waitChangedHelper(self._waitParamHelper(eventType), timeout)

    def notify(self, eventType: EventType, changedCount: int):
        with self._lastNotifiedEventTypeMutex:
            self._lastNotifiedEventType[eventType] = changedCount
        self._event.set()

    def close(self):
        self._jsonRpcTcpClient.close()

    def _setIsReadyHandle(self, params):
        assert(params == None)
        self._isReadySemaphore.release()

    def _waitParamHelper(self, eventTypes: EventType|set[EventType]) -> dict[EventType, int]:
        toReturn = dict()
        with self._lastNotifiedEventTypeMutex:
            if isinstance(eventTypes, Robot.EventType):
                toReturn[eventTypes] = self._lastNotifiedEventType[eventTypes]
            else:
                for eventType in eventTypes:
                    if eventType in self._lastNotifiedEventType:
                        toReturn[eventType] = self._lastNotifiedEventType[eventType]
        return toReturn

    def _waitChangedHelper(self, eventTypes: dict[EventType, int], timeout: float|None) -> EventType|None:
        startTime = time.time()
        self._event.clear()
        while True:
            if timeout!=None:
                remainingTime = timeout-(time.time()-startTime)
                if (remainingTime<0):
                    return None
            else:
                remainingTime = None
            if not self._event.wait(remainingTime):
                return None
            self._event.clear()
            with self._lastNotifiedEventTypeMutex:
                for eventType, changedCountBegin in eventTypes.items():
                    changedCountNew = self._lastNotifiedEventType.get(eventType)
                    if ((changedCountBegin == None and changedCountNew != None)
                        or (changedCountBegin != None and changedCountNew>changedCountBegin)):
                        return eventType
