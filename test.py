#!/usr/bin/python
# -*- coding: utf-8 -*-


# Schnorr Protocol over Elliptic Curves
# Sistemas de Software Seguro (Secure Software Systems)
# Computer Science MSc
# Universidade da Beira Interior
# Manuel Meruje, m6620


import sys
import ecc
import Crypto.Util.number
import socket 

usage='''
 Usage: ./schnorr [OPTION]... [ARGS]...
 Authenticates someone using Schnorr Protocol over Elliptic Curves
 Shows this message if none of options is used.

 Mandatory arguments to long options are mandatory for short options too.
  -gk,\t--generate-keys\tGenerates a Key Pair.
  -a,\t--authenticator\tUses a Public Key to authenticate a client.
  -s,\t--supplicant\tUses the Private Key to authenticate itself to a server.\n
'''

host = 'localhost' 
port = 10000
dataSize = 2048

p = ecc.ECcurve().p
q = ecc.ECcurve().q

# --generate_keys
def generate_keys():
	""" 
	Supplicant Mode - Key Generation
	""" 
	
	# Select an elliptic curve [it is defined in ecc.py]
	ec=ecc.ECcurve()

	# a = r <- {0, ..., Q − 1} [Alice calculates the private key.]
	print("*  Generating an a random number. (Private Key)")

	a = Crypto.Util.number.getRandomRange(0, (q-1))
	a = 1742413906660797398263574261320583321084828220183690165741

	# v = −a.G(modP) [Alice calculates the public key v (a point in the elliptic curve).]
	# v = (-a*ec_G) % p

	# atenção à coordenada y! G = (xi, xf)
	print("*  Generating an elliptic curve point. (Public Key)")
	pbp = ecc.ECPoint(ec.xi, ec.yi)
	pbp = pbp.multiplyPointByScalar(a)
	pbp = pbp.simmetric()

	print("--- BEGIN PRIVATE KEY ---")
	print(a)
	print("--- BEGIN PUBLIC KEY ---")
	print("v(x,-) = " + str(pbp.x))
	print("v(-,y) = " + str(pbp.y))
	
	return [a,pbp.x,pbp.y]


def main():
	keys=generate_keys()


if __name__ == "__main__":
	main()

