import secrets

from party import Receiver, Sender



def main():
    msg0 = b"EdfbnZNu47cZ0gCq"
    msg1 = b"ZR0VPP8Z8yRPu5Xy"

    choice = secrets.randbelow(2)

    sender = Sender()
    receiver = Receiver()

    query = receiver.query(sender.public, choice)
    ct0, ct1 = sender.reply(query, msg0, msg1)
    result = receiver.elect(sender.public, choice, ct0, ct1)

    print(f"бит = {choice}")
    print(f"результат = {result!r}")


if __name__ == "__main__":
    main()
