from game.player import HumanPlayer, AIPlayer, NetworkPlayer
from game.game import Game
import sys
import telnetlib

if __name__ == '__main__':

    print("\nSelect type of game for the AI to play:\n\t1)Human Player\n\t2)Server Player\n\t"
          "3)Itself\n\t4)Human vs Human")
    choice = input("--> ")
    if choice == "1":  # Human/AI
        print("\nWho goes first?\n\t1)You\n\t2)AI")
        first = input("--> ")
        p0 = HumanPlayer('Player 0')
        p1 = AIPlayer()
        if first == "1":
            g = Game(p0, p1)
        elif first == "2":
            g = Game(p1, p0)
        winner = g.run_all()
        print(winner)
    elif choice == "2":  # Network/AI
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
            if "Player:1" in str(res, "utf-8"):
                p0 = NetworkPlayer(tn)
                p1 = AIPlayer(tn)
                g = Game(p1, p0)
                break
            elif "Player:2" in str(res, "utf-8"):
                p0 = NetworkPlayer(tn, str(res, "utf-8"))
                p1 = AIPlayer(tn)
                g = Game(p0, p1)
                break
        winner = g.run_all()
        print(winner)

    elif choice == "3": # AI/AI
        p0 = AIPlayer()
        p1 = AIPlayer(learn = False)
        g = Game(p0, p1)
        winner = g.run_all()
        print(winner)
    elif choice == "4": # Human/Human
        p0 = HumanPlayer('Player 0')
        p1 = HumanPlayer('Player 1')
        g = Game(p0, p1)
        winner = g.run_all()
        print(winner)
    else:
        print("Try again.")
