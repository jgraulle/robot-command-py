import socket
import threading
import json
import io


class JsonRpcTcpClient:
    SEPARATOR = chr(0xA)

    def __init__(self, hostIpAddress: str, tcpPort: int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((hostIpAddress, tcpPort))
        self._socketReadBuffer = self._socket.makefile(mode='r', encoding='utf-8', newline=self.SEPARATOR)
        self._socketWriteBuffer = self._socket.makefile(mode='w', encoding="utf-8", newline=self.SEPARATOR)
        self._isStartReceive = False
        self._notificationHandles = dict()
        self._receiveThread = threading.Thread(target=self._receive)
        self._receiveThreadEnd = False
        self._receiveMethodResponseSem = threading.Semaphore(1)
        self._receiveMethodResponseJsonValue = None
        self._jsonRpcId = 0

    def bindNotification(self, methodName: str, notificationHandle):
        assert(not self._isStartReceive)
        self._notificationHandles[methodName] = notificationHandle

    def startReceive(self):
        self._isStartReceive = True
        self._receiveThread.start()

    def callNotification(self, methodName: str, params):
        # Prepare message
        message = {"jsonrpc": "2.0", "method": methodName, "params": params}

        # Send message
        json.dump(message, self._socketWriteBuffer)
        self._socketWriteBuffer.write("\n")
        self._socketWriteBuffer.flush()

    def callMethod(self, methodName: str, params):
        # Prepare message
        message = {"jsonrpc": "2.0", "method": methodName, "params": params, "id": self._jsonRpcId}

        # Send message
        json.dump(message, self._socketWriteBuffer)
        self._socketWriteBuffer.write("\n")
        self._socketWriteBuffer.flush()

        # Wait response
        self._receiveMethodResponseSem.acquire()
        assert(self._receiveMethodResponseJsonValue != None)
        responseJson = self._receiveMethodResponseJsonValue
        assert("id" in responseJson)
        assert(responseJson.get("id") == self._jsonRpcId)
        assert("result" in responseJson)
        self._receiveMethodResponseJsonValue = None

        # Return response and prepare next id
        self._jsonRpcId = self._jsonRpcId + 1
        return responseJson.get("result")

    def close(self):
        self._socket.close()
        self._receiveThreadEnd = True
        self._receiveThread.join()

    def _receive(self):
        while (not self._receiveThreadEnd):
            # Wait message
            line = self._socketReadBuffer.readline()
            message = json.loads(line)

            # If method response
            if ("id" in message):
                # Store result to use it in callMethod
                assert(self._receiveMethodResponseJsonValue == None)
                self._receiveMethodResponseJsonValue = message
                self._receiveMethodResponseSem.release()
            # If notification
            else:
                # Call corresponding notification handle
                assert("method" in message)
                methodName = message["method"]
                assert(methodName in self._notificationHandles)
                assert("params" in message)
                self._notificationHandles[methodName](message["params"])
