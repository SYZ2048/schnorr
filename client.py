from socket import *
import ecc
import Crypto.Util.number
import time

p = ecc.ECcurve().p
q = ecc.ECcurve().q
dataSize = 2048


class Client(object):
    _clientSocket = None
    serverName = '10.102.120.69'
    serverPort = 13000
    _a = None
    _r = None
    _R = None
    _c = None
    _pbp = None
    _z = None

    # def __init__(self):

    def connect(self):
        # serverName =   指定服务器IP地址
        # serverPort = 12000
        self._clientSocket = socket(AF_INET, SOCK_STREAM)  # 建立TCP套接字，使用IPv4协议
        print("try to connect with server...")
        self._clientSocket.connect((self.serverName, self.serverPort))
        print("Connect successfully!start to Schnorr on client...")

    def signature(self):
        self.generate_keys()
        self.send_R()
        self.receive_c()
        self.send_z()

    # generate public and private key, send Public key to server
    def generate_keys(self):
        print("\n****************************************")
        # Select an elliptic curve [it is defined in ecc.py]
        ec = ecc.ECcurve()

        # generate Private key a = r <- {0, ..., Q − 1}
        print("Generating an a random number. (Private Key)")
        # *self._a = Crypto.Util.number.getRandomRange(0, (q - 1))
        self._a = 1742413906660797398263574261320583321084828220183690165741

        # v = −a.G(modP) [Alice calculates the public key v (a point in the elliptic curve).]
        # v = (-a*G) % p

        # generate Public key
        print("Generating an elliptic curve point. (Public Key)")
        self._pbp = ecc.ECPoint(ec.xi, ec.yi)
        self._pbp = self._pbp.multiplyPointByScalar(self._a)
        self._pbp = self._pbp.simmetric()

        print("--- BEGIN PRIVATE KEY ---")
        print(self._a)
        print("--- BEGIN PUBLIC KEY ---")
        print("\tPK x:", int(self._pbp.x))
        print("\tPK y:", int(self._pbp.y))
        print("Send PK=a*G")
        self._clientSocket.send(str(int(self._pbp.x)).encode('utf-8'))
        self._clientSocket.send(str(int(self._pbp.y)).encode('utf-8'))
        time.sleep(1)

    def send_R(self):
        print("\n****************************************")
        print("send R")
        # Generate a number r to use in  [ R=r.G(modP) ] to calculate a point on the elliptic curve
        print("generating a r random number.")
        ec = ecc.ECcurve()
        # *self._r = Crypto.Util.number.getRandomRange(0, (q - 1))
        self._r = 3837380130218306619887300089875165037457360467027876097965
        print("Number r generated:\tr = " + str(self._r))
        print("calculate point R on the elliptic curve.")
        R = ecc.ECPoint(ec.xi, ec.yi)
        self._R = R.multiplyPointByScalar(self._r)

        # send x
        print("\tRx: ", self._R.x)
        print("\tRx: ", int(self._R.x))
        print("\tRy: ", int(self._R.y))
        self._clientSocket.send(str(int(self._R.x)).encode('utf-8'))
        self._clientSocket.send(str(int(self._R.y)).encode('utf-8'))
        print("sent R")
        time.sleep(1)

    def receive_c(self):
        print("\n****************************************")
        print("receive c")
        self._c = self._clientSocket.recv(dataSize).decode('utf-8')
        self._c = int(self._c)
        print("received c:", int(self._c))
        if self._c < 2 ** 80:
            print("c is valid.")
        else:
            print("c is not valid.")
            return

    def send_z(self):
        print("\n****************************************")
        # calculate z = r + c*sk
        self._z = self._a * self._c + self._r
        print("z was calculed : ", int(self._z))
        # send  z
        self._clientSocket.send(str(int(self._z)).encode('utf-8'))
        print("z sent.")
        time.sleep(3)
        self._clientSocket.close()
        print("Connection closed.\n")


if __name__ == "__main__":
    clientSocket = Client()
    # ###	socket连接	####
    clientSocket.connect()  # 向服务器发起连接

    # ###	进行TLS握手协议	####
    clientSocket.signature()

