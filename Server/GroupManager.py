from threading import Thread
from Constants import BUFFERSIZE
from MessageReceiver import messageReceiver
from MessageSender import messageSender
from Crypto.Random import get_random_bytes
import binascii


class GroupManager(object):
    def __init__(self):
        self.groups = {}
        self.keys = {}

    def generateGroupKey(self):
        key = get_random_bytes(24)
        return binascii.b2a_hex(key).decode(encoding='utf-8') 

    def createGroup(self, userName, groupName):
        key = self.generateGroupKey()
        self.keys[groupName] = key
        self.groups[groupName] = [userName]
        return key
    
    def joinGroup(self, userName, groupName):
        if(groupName not in self.groups.keys()):
            key = self.createGroup(userName, groupName)
        else:
            self.groups[groupName].append(userName)
            key = self.keys[groupName]
        return key

    def listGroup(self):
        groups_information = {}
        for i in self.groups:
            groups_information[i] = len(self.groups[i])

        return groups_information

    def getParticipants(self, groupName):
        return self.groups[groupName]

groupManager = GroupManager()