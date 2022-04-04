import os

os.system("rm -rf follower* leader")


os.system("mkdir leader")
os.system("cp yabd/Telematica\ -\ Yadb/leader/*.py leader")
for i in range(0,6):

        os.system("mkdir follower"+str(i))
        os.system("cp yabd/Telematica\ -\ Yadb/follower/*.py follower"+str(i) )