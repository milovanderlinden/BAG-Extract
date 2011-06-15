# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="miblon"
__date__ ="$Jun 13, 2011 11:34:17 AM$"

if __name__ == "__main__":
    print "Hello World"

class LogHandler:
    def __init__(self, args):
        self.args = args

    def log(self, message):
        if self.args.verbose == True:
            print message