# File System Simulator

class File:
    def __init__(self, name, size=1, permissions="rw"):
        self.name = name
        self.size = size
        self.permissions = permissions


class Directory:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.permissions = "rwx"
        self.parent = None


class FileSystem:

    def __init__(self, quota=50):
        self.root = Directory("/")
        self.root.parent = self.root
        self.current = self.root
        self.quota = quota
        self.used = 0


    # mkdir command
    def mkdir(self, name):

        if name in self.current.children:
            print("Directory already exists")
            return

        new_dir = Directory(name)
        new_dir.parent = self.current

        self.current.children[name] = new_dir

        print("Directory created")


    # touch command
    def touch(self, name, size=1):

        if name in self.current.children:
            print("File already exists")
            return

        if self.used + size > self.quota:
            print("Disk quota exceeded")
            return

        new_file = File(name, size)

        self.current.children[name] = new_file
        self.used += size

        print("File created")


    # ls command
    def ls(self):

        if not self.current.children:
            print("Empty directory")
            return

        for name, obj in self.current.children.items():

            if isinstance(obj, Directory):
                print("[DIR]", name)

            else:
                print("[FILE]", name, "(size:", obj.size, ")")


    # cd command
    def cd(self, name):

        if name == "/":
            self.current = self.root
            return

        if name == "..":
            self.current = self.current.parent
            return

        if name not in self.current.children:
            print("Directory not found")
            return

        obj = self.current.children[name]

        if isinstance(obj, File):
            print("Cannot cd into file")
            return

        self.current = obj


    # rm command
    def rm(self, name):

        if name not in self.current.children:
            print("Not found")
            return

        obj = self.current.children[name]

        if isinstance(obj, File):
            self.used -= obj.size

        del self.current.children[name]

        print("Removed")


    # pwd command
    def pwd(self):

        temp = self.current
        path = []

        while temp != self.root:
            path.append(temp.name)
            temp = temp.parent

        print("/" + "/".join(reversed(path)))


    # quota command
    def quota_status(self):

        print("Used:", self.used)
        print("Free:", self.quota - self.used)
        print("Total:", self.quota)


# Interactive Shell

fs = FileSystem(quota=20)

print("Virtual File System Started")
print("Commands:")
print("mkdir <name>")
print("touch <name> <size>")
print("ls")
print("cd <name>")
print("cd ..")
print("cd /")
print("rm <name>")
print("pwd")
print("quota")
print("exit")


while True:

    cmd = input("\nEnter command: ").strip().split()

    if not cmd:
        continue

    command = cmd[0]

    if command == "mkdir":

        if len(cmd) < 2:
            print("Usage: mkdir <name>")
        else:
            fs.mkdir(cmd[1])


    elif command == "touch":

        if len(cmd) < 2:
            print("Usage: touch <name> <size>")
        else:
            size = int(cmd[2]) if len(cmd) > 2 else 1
            fs.touch(cmd[1], size)


    elif command == "ls":
        fs.ls()


    elif command == "cd":

        if len(cmd) < 2:
            print("Usage: cd <name>")
        else:
            fs.cd(cmd[1])


    elif command == "rm":

        if len(cmd) < 2:
            print("Usage: rm <name>")
        else:
            fs.rm(cmd[1])


    elif command == "pwd":
        fs.pwd()


    elif command == "quota":
        fs.quota_status()


    elif command == "exit":
        print("Exiting File System")
        break


    else:
        print("Invalid command")