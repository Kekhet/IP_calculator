import sys
import json
import socket


def getIPTab(rawInput, mask, IPTab):
    buffer = rawInput.split('/')
    IPTab = buffer[0].split('.')
    if len(IPTab) != 4 or int(mask) > 32:
        print("WRONG INPUT")
        exit(-1)
    for x in range(4):
        try:
            if int(IPTab[x]) > 255:
                print("WRONG INPUT")
                exit(-1)
        except ValueError:
            print("WRONG INPUT")
            exit(-1)
    return IPTab



def dec_to_bin(x):
    binary = ""
    temp = 128
    for y in range(8):
        if x >= temp:
            x -= temp
            temp /= 2
            binary += "1"
        else:
            temp /= 2
            binary += "0"
    return binary


def getMask(rawInput):
    buffer = rawInput.split('/')
    mask = buffer[1]
    return mask


def IPtoBinary(IP):
    buffer = IP.split('/')
    IPTab = buffer[0].split('.')
    IP_binary = ""
    IP_binary += dec_to_bin(int(IPTab[0])) + "."
    IP_binary += dec_to_bin(int(IPTab[1])) + "."
    IP_binary += dec_to_bin(int(IPTab[2])) + "."
    IP_binary += dec_to_bin(int(IPTab[3]))
    return IP_binary


def maskToBinary(mask):
    retVal = ""
    temp = mask
    dotIter = 0
    while temp > 0:
        retVal += "1"
        temp -= 1
        dotIter += 1
        if dotIter == 8:
            retVal += "."
            dotIter = 0
    temp = 32 - int(mask)
    while temp > 0:
        retVal += "0"
        temp -= 1
        dotIter += 1
        if dotIter == 8:
            retVal += "."
            dotIter = 0
    retVal = retVal[:-1]
    return retVal


def calcNetAddress(IP_binary, mask_binary):
    netAddress = ""
    iter = 0
    while iter < 35:
        if IP_binary[iter] == mask_binary[iter]:
            if IP_binary[iter] == "1":
                netAddress += "1"
            elif IP_binary[iter] == ".":
                netAddress += "."
            else:
                netAddress += "0"
            iter += 1
        else:
            netAddress += "0"
            iter += 1
    return netAddress


def calcAddressFromBinToDec(addres_binary):
    tab = addres_binary.split(".")
    retVal = ""
    retVal += str(int(tab[0], 2)) + "."
    retVal += str(int(tab[1], 2)) + "."
    retVal += str(int(tab[2], 2)) + "."
    retVal += str(int(tab[3], 2))
    return retVal


def networkClass(IP_binary):
    if IP_binary[0] == "0":
        return "A"
    elif IP_binary[0] == "1" and IP_binary[1] == "0":
        return "B"
    elif IP_binary[0] == "1" and IP_binary[1] == "1" and IP_binary[2] == "0":
        return "C"
    elif IP_binary[0] == "1" and IP_binary[1] == "1" and IP_binary[2] == "1" and IP_binary[3] == "0":
        return "D"
    elif IP_binary[0] == "1" and IP_binary[1] == "1" and IP_binary[2] == "1" and IP_binary[3] == "1":
        return "E"
    else:
        return "ERROR"


def broadcast(network_address, mask_binary):
    maskTemp = ""
    for x in range(len(mask_binary)):
        if mask_binary[x] == "1":
            maskTemp += "0"
        elif mask_binary[x] == "0":
            maskTemp += "1"
        elif mask_binary[x] == ".":
            maskTemp += "."
    maskTemp = calcAddressFromBinToDec(maskTemp)
    maskTab = maskTemp.split('.')
    addressTab = network_address.split('.')
    val1 = str(int(maskTab[0])+int(addressTab[0]))
    val2 = str(int(maskTab[1])+int(addressTab[1]))
    val3 = str(int(maskTab[2])+int(addressTab[2]))
    val4 = str(int(maskTab[3])+int(addressTab[3]))
    retVal = ""
    retVal += val1 + "." + val2 + "." + val3 + "." + val4
    return retVal


def maxHost(mask):
    expo = 32 - mask
    mult = 1
    while expo > 0:
        mult *= 2
        expo -= 1
    mult -= 2
    return mult

def first_host_IP(network_address):
    temp = network_address.split(".")
    val1 = temp[0]
    val2 = temp[1]
    val3 = temp[2]
    val4 = str(int(temp[3]) + 1)
    retVal = ""
    retVal += val1 + "." + val2 + "." + val3 + "." + val4
    return retVal


def last_host_IP(broadcast_address):
    temp = broadcast_address.split(".")
    val1 = temp[0]
    val2 = temp[1]
    val3 = temp[2]
    val4 = str(int(temp[3]) - 1)
    retVal = ""
    retVal += val1 + "." + val2 + "." + val3 + "." + val4
    return retVal


def writeToJson(data):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


try:
    rawInput = sys.argv[1]
except IndexError:
    rawInput = socket.gethostbyname(socket.gethostname())
try:
    mask = int(getMask(rawInput))
except IndexError:
    mask = 24

IPTab = 0
IPTab = getIPTab(rawInput, mask, IPTab)

IP = ".".join(IPTab) + "/" + str(mask)
print("IP address: {0}".format(IP))
IP_binary = str(IPtoBinary(IP))
print("IP address binary: {0}".format(IP_binary))

network_class = networkClass(IP_binary)
print("Network class: {0}".format(network_class))

mask_binary = maskToBinary(mask)
mask_decimal = calcAddressFromBinToDec(mask_binary)
print("Mask decimal: {0}".format(mask_decimal))
print("Mask binary: {0}".format(mask_binary))

network_address_binary = calcNetAddress(IP_binary, mask_binary)
network_address_decimal = calcAddressFromBinToDec(network_address_binary)
print("Network address: {0}".format(network_address_decimal))
print("Network address binary: {0}".format(network_address_binary))


broadcastAddress = broadcast(network_address_decimal, mask_binary)
print("Broadcast address: {0}".format(broadcastAddress))
broadcastAddress_binary = IPtoBinary(broadcastAddress)
print("Broadcast address binary: {0}".format(broadcastAddress_binary))

max_num_host = maxHost(mask)
print("Max host: {0}".format(max_num_host))
print("Max host binary: {0:b}".format(max_num_host))

firstHost = first_host_IP(network_address_decimal)
print("First host address: {0}".format(firstHost))
firstHost_binary = IPtoBinary(firstHost)
print("First host address binary: {0}".format(firstHost_binary))

lastHost = last_host_IP(broadcastAddress)
print("Last host address: {0}".format(lastHost))
lastHost_binary = IPtoBinary(lastHost)
print("Last host address binary: {0}".format(lastHost_binary))

dict = {'IP Address': IP, 'IP Address Binary': IP_binary,
        'Network class': network_class,
        'Mask': mask_decimal, 'Mask binary': mask_binary,
        'Network address': network_address_decimal, 'Network address binary': network_address_binary,
        'Broadcast address': broadcastAddress, 'Broadcast address binary': broadcastAddress_binary,
        'Max host': max_num_host,
        'First host': firstHost, 'First host binary':firstHost_binary,
        'Last host': lastHost, 'Last host binary':lastHost_binary
        }

writeToJson(dict)