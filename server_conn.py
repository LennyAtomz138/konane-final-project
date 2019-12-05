import sys
import telnetlib

print("Started")
tn = telnetlib.Telnet('artemis.engr.uconn.edu', '4705')
print("Connected")

tn.read_until(b"?Username:")
#name = str(input('Username:'))
tn.write(b"42069\r\n")

tn.read_until(b"?Password:")
#pwd = str(input('Password:'))
#pwd.encode('ascii') +
tn.write(b"42069\r\n")

tn.read_until(b"?Opponent:")
choice = str(input('Opponent:'))
tn.write(choice.encode('ascii') + b"\r\n")

flag = False

while True:
    res = tn.read_some()
    #print(res)
    print(str(res, "utf-8"))
    if "Player:1" in str(res, "utf-8"):
        tn.write(input("Remove: ").encode('ascii') + b"\r\n")
        flag = True
    if "Player:2" in str(res, "utf-8"):
        tn.write(input("Remove: ").encode('ascii') + b"\r\n")
        flag = True

    if flag && "Move" in str(res, "utf-8"):
        tn.write(input("Move: ").encode('ascii') + b"\r\n")

    if "Error:" in str(res, "utf-8"):
        break
    if "win" in str(res, "utf-8"):
        break

tn.close()
