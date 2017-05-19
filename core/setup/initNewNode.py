from pexpect import pxssh

def setup(username, password, role, ip):
    try:
        s = pxssh.pxssh()

        s.login(ip, username, password)
        s.sendline()
        s.prompt()
        s.before
        s.logout()
    except pxssh.ExceptionPxssh:
        pass
