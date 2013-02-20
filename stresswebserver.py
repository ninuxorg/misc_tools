from subprocess import call
import threading

SITE="http://127.0.0.1"

class LittleStresser(threading.Thread):
    def __init__(self, id, f):
        threading.Thread.__init__(self, name="ComputeThread-%d" % (id,))
        self.f = f
    def run(self):
        s = self.f.readline()
        url = s.split()[6]
        print "GETting url: %s%s" % (SITE,url)        call(["wget", SITE+url , "-o", "/dev/null", "-O", "/dev/null", "&"])


def main():
        f = open('access_log', 'r')
        c = 1
        while c != 0:
                c = int( input("Number? ") )
                for i in range(1, c+1):
                        LittleStresser(c, f).start()

if __name__ == "__main__":
    main()

