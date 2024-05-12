from socket import *
import time
import ecc
import Crypto.Util.number

p = ecc.ECcurve().p
q = ecc.ECcurve().q
dataSize = 2048


class Server(object):
    _serverSocket = None
    _serverName = None
    _serverPort = None
    _R = None
    _c = None
    _z = None
    _PK = None
    _server_random_num = None
    _client_random_num = None
    _connectionSocket = None
    _addr = None
    _des_key = None

    def connect(self):
        self._serverPort = 13000
        self._serverSocket = socket(AF_INET, SOCK_STREAM)  # 建立TCP套接字，使用IPv4协议
        self._serverSocket.bind(('', self._serverPort))  # 将TCP欢迎套接字绑定到指定端口
        self._serverSocket.listen(1)  # 最大连接数为5
        self._connectionSocket, self._addr = self._serverSocket.accept()  # 接收到客户连接请求后，建立新的TCP连接套接字
        print('Accept new connection...')

    def verify(self):
        self.receive_pk()
        self.receive_R()
        self.send_c()
        self.receive_z()
        self.check()

    def receive_pk(self):
        print("\n****************************************")
        print("Received PK")
        PKx = self._connectionSocket.recv(dataSize).decode('utf-8')
        PKy = self._connectionSocket.recv(dataSize).decode('utf-8')
        self._PK = ecc.ECPoint(int(PKx), int(PKy))

        print("PK x:", int(self._PK.x))
        print("PK y:", int(self._PK.y))

    def receive_R(self):
        print("\n****************************************")
        print("Received R")
        xx = self._connectionSocket.recv(dataSize).decode('utf-8')
        xy = self._connectionSocket.recv(dataSize).decode('utf-8')
        self._R = ecc.ECPoint(int(xx), int(xy))

        print("Rx:", int(self._R.x))
        print("Ry:", int(self._R.y))

    def send_c(self):
        # generates e
        print("\n****************************************")
        print("send c")
        self._c = Crypto.Util.number.getRandomRange(0, 2 ** 80)
        print("c generated: ", int(self._c))
        # send e
        self._connectionSocket.send(str(int(self._c)).encode('utf-8'))
        print("c sent.")

    def receive_z(self):
        print("\n****************************************")
        print("receive z")
        self._z = self._connectionSocket.recv(dataSize).decode('utf-8')
        print("z:", int(self._z))

    def check(self):
        print("\n****************************************")
        print("check")
        ec = ecc.ECcurve()
        G = ecc.ECPoint(ec.xi, ec.yi)
        z = G.multiplyPointByScalar(int(self._z))
        cPK = self._PK.multiplyPointByScalar(self._c)
        z = z.sum(cPK)

        print("z.x", z.x)
        print("z.y", z.y)
        print("R.x", self._R.x)
        print("R.y", self._R.y)

        if z.x == self._R.x and z.y == self._R.y:
            print("Verified")
        else:
            print("Not Verified")

        self._connectionSocket.close()
        print("Connection closed\n")


if __name__ == "__main__":
    serverSocket = Server()
    # ### socket 连接
    print("wait for connecting...")
    serverSocket.connect()  # 向服务器发起连接

    # ###	进行TLS握手协议	####
    serverSocket.verify()
