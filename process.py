class Process:
    def __init__(self, list):
        self.user = list[0]
        self.pid = list[1]
        self.cpu = list[2]
        self.mem = list[3]
        self.vsz = list[4]
        self.rss = list[5]
        self.tty = list[6]
        self.start = list[7]
        self.stat = list[8]
        self.time = list[9]
        self.command = list[10]

    def print(self):
        print("user:", self.user)
        print("pid:", self.pid)
        print("cpu:", self.cpu)
        print("mem:", self.mem)
        print("vsz:", self.vsz)
        print("rss:", self.rss)
        print("tty:", self.tty)
        print("start:", self.start)
        print("stat:", self.stat)
        print("time:", self.time)
        print("command:", self.command)

    def print_user(self):
        print("user:", self.user)
