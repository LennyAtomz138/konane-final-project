from game.player import HumanPlayer, AIPlayer, NetworkPlayer
from game.game import Game
import telnetlib
import pickle


if __name__ == '__main__':

    print("\nSelect type of game to play:\n\t1)Human Player vs AI\n\t2)Server Player vs AI\n\t3)Itself\n\t4)Human vs Human\n\t5)Human vs Server Player\n\t6)Print Poly")
    choice = input("--> ")
    if (choice == "1"): # Human/AI
        print("\nWho goes first?\n\t1)You\n\t2)AI")
        first = input("--> ")
        p0 = HumanPlayer('Player 0')
        p1 = AIPlayer(None, False)
        if (first == "1"):
            g = Game(p0, p1)
        elif(first == "2"):
            g = Game(p1,p0)
        winner = g.run_all()
        print(winner)
    elif (choice == "2"): # Network/AI
        tn = telnetlib.Telnet('artemis.engr.uconn.edu', '4705')
        tn.read_until(b"?Username:")
        name = str(input('id: '))
        tn.write(name.encode('ascii') + b"\r\n")
        tn.read_until(b"?Password:")
        tn.write(name.encode('ascii') + b"\r\n")
        tn.read_until(b"?Opponent:")
        choice = str(input('Opponent:'))
        tn.write(choice.encode('ascii') + b"\r\n")
        while True:
            res = tn.read_some()
            print(str(res, "utf-8"))
            if ("Player:1" in str(res, "utf-8")):
                p0 = NetworkPlayer(tn)
                p1 = AIPlayer(tn, False)
                g = Game(p1, p0)
                break
            elif ("Player:2" in str(res, "utf-8")):
                p0 = NetworkPlayer(tn, str(res, "utf-8"))
                p1 = AIPlayer(tn, False)
                g = Game(p0, p1)
                break
        winner = g.run_all()
        print(winner)

    elif (choice == "3"): # AI/AI
        print("\nShould Learner go first?\n\t1)Yes\n\t2)No")
        first = input("--> ")
        p0 = AIPlayer()
        p1 = AIPlayer(learn = False)
        if first == "1":
            g = Game(p0, p1)
        else:
            g = Game(p1, p0)
        winner = g.run_all()
        print(winner)
    elif (choice == "4"): # Human/Human
        p0 = HumanPlayer('Player 0')
        p1 = HumanPlayer('Player 1')
        g = Game(p0, p1)
        winner = g.run_all()
        print(winner)
    elif (choice == "5"): # Human/Network
        tn = telnetlib.Telnet('artemis.engr.uconn.edu', '4705')
        tn.read_until(b"?Username:")
        name = str(input('id: '))
        tn.write(name.encode('ascii') + b"\r\n")
        tn.read_until(b"?Password:")
        tn.write(name.encode('ascii') + b"\r\n")
        tn.read_until(b"?Opponent:")
        choice = str(input('Opponent:'))
        tn.write(choice.encode('ascii') + b"\r\n")
        while True:
            res = tn.read_some()
            print(str(res, "utf-8"))
            if ("Player:1" in str(res, "utf-8")):
                p0 = NetworkPlayer(tn)
                p1 = HumanPlayer("Human", tn)
                g = Game(p1, p0)
                break
            elif ("Player:2" in str(res, "utf-8")):
                p0 = NetworkPlayer(tn, str(res, "utf-8"))
                p1 = HumanPlayer("Human", tn)
                g = Game(p0, p1)
                break
        winner = g.run_all()
        print(winner)
    elif(choice == "6"):
        poly = pickle.load(open('Memory/polynomial.data', 'rb'))
        print(poly.printCoeff())
    elif(choice == "7"):
        ii = 0
        while True:
            print("Game number: "+str(ii))
            p0 = AIPlayer()
            p1 = AIPlayer(learn = False)
            if ii % 2 == 0:
                g = Game(p0, p1)
            else:
                g = Game(p1, p0)
            winner = g.run_all()
            print(winner)
            ii += 1
    else:
        print("Try again.")
