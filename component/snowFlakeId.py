#generate unique id.
import time
EPOCH = 1655477539962 #int(time.time() * 1000.0)
INDEX_SIZE = 13
TIMESTAMP_SIZE = 41
NODE_SIZE = 10

TIMESTAMP_OFFSET = INDEX_SIZE + NODE_SIZE
INDEX_MASK = (1 << INDEX_SIZE) -1
TIMESTAMP_MASK = (1 << TIMESTAMP_SIZE) - 1
NODE_MASK = (1 << NODE_SIZE) - 1
INCREMENT_VALUE = (1 << NODE_SIZE)
MAX_INCREMENT_VALUE=((1<<(NODE_SIZE+INDEX_SIZE))-1)
import os,settings,random

class SnowFlack():
    def timestamp(self)->int:
        return int(time.time()*1000)
    def __init__(self)->None:
        self.nodeid = settings.NODEID
        if not self.nodeid:
            if settings.DEBUG:
                self.nodeid =66
            else:
                raise Exception("must define unique nodeid in environment")

        self.lasttime=self.timestamp()
        self.increment=0
    def getId(self)->int:

        while (timestamp:=self.timestamp())<self.lasttime: #ntpdate or other time async tools could change time.so wait time to be correct
            pass
        self.lasttime=timestamp
        self.increment = (self.increment + INCREMENT_VALUE) & MAX_INCREMENT_VALUE
        tmp = (((self.lasttime - EPOCH) & TIMESTAMP_MASK) << TIMESTAMP_OFFSET) | (self.nodeid & NODE_MASK) | self.increment
        return tmp



snowFlack=SnowFlack()
if __name__ == "__main__":
    for i in range(30):
        print(bin(snowFlack.getId()))