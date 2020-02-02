#!/usr/bin/python3
import socket
import player as pl


class bot:

    players = []

    def __init__(self):
        #Set up socket with a tcp stream
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "chat.freenode.net" # Server
        self.channel = "##bot-testing" # Channel
        self.botnick = "Quackathon"
        self.adminname = "Yelnat"
        self.exitcode = "bye " + self.botnick
        self.command = ""

    def get_player(self, name):

        for player in self.players:
            if player.get_name() == name:
                return player

        return False
    
    
    def connect(self):
        self.sock.connect((self.server, 6667)) # Here we connect to the server using the port 6667
        self.sock.send(bytes(f"USER {self.botnick} {self.botnick} bla :{self.botnick}\r\n", "UTF-8")) #Set bot username etc.
        self.sock.send(bytes(f"NICK {self.botnick}\r\n", "UTF-8")) # assign the nick to the bot

    def joinchan(self, chan): # join channel(s).
        self.channel = chan
        ircmsg = ""
        while ircmsg.find("End of /NAMES list.") == -1:
            self.sock.send(bytes(f"JOIN {self.channel} \r\n", "UTF-8"))
            ircmsg = self.sock.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('nr')
            print(ircmsg)


    def ping(self): # respond to server Pings.
        self.sock.send(bytes("PONG :pingisn", "UTF-8"))

    def sendmsg(self, msg, target="##bot-testing"): # sends messages to the target.
        self.sock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\r\n", "UTF-8"))

    def rcvmsg(self):
        ircmsg = self.sock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('nr')
        print(ircmsg)
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            self.respond(name, message)

    def attack_handler(self):
        self.sendmsg("ATTACK " + self.command.split(' ')[1] + "!")
        #TODO

    def view_handler(self):
        self.sendmsg("VIEW " + self.command.split(' ')[1] + "!")
        player = self.get_player(self.name)


        for item in player.info():
            self.sendmsg(item)


    def spend_handler(self):
        # I, 10, *name*
        self.get_player(self.name).buy_units(self.command.split(' ')[1][0],
                                                     self.command.split(' ')[2],
                                                     self.command.split(' ')[3])

    def new_user(self):

        self.players.append(pl.Player(self.name))
        self.sendmsg(f"Player {self.name} Successfully added")



    def respond(self, name, message, target="##bot-testing"):

        self.command = message
        self.name = name

        handler_table = {
            "!ATT": self.attack_handler,
            "!VIEW": self.view_handler,
            "!SPEND": self.spend_handler,
            "!ADD": self.new_user,
            "!KILL": self.stop,
        }

        if len(name) < 17 and message[0] is '!':
            if 'Hi ' + self.botnick in message:
                self.sendmsg("Hello " + name + "!")

            elif 'PING' in message:
                self.ping()

            else:
                try:
                    handler_table[message.split(' ')[0]]()
                except KeyError:
                    message = "Could not parse. The message should be in the format of ‘![command] [target]’ to work properly."
                    self.sendmsg(message, target)
        else:
            message = "Could not parse. The message should be in the format of ‘![command] [target]’ to work properly." + message
            self.sendmsg(message, target)




    def stop(self):
        self.sendmsg("oh...okay. :'(")
        self.sock.send(bytes("QUIT n", "UTF-8"))



def main():
    mybot = bot()

    mybot.connect()
    mybot.joinchan('##bot-testing')

    while True:
        mybot.rcvmsg()

main()