import urllib2
import sys
import socket
import os
from paramiko import SSHClient
from scp import SCPClient
from paramiko.ssh_exception import SSHException
import StringIO

machine={'xx.xx.xx.xx':'22'}

#get ssh object
def DoLogin(ip):
	ssh = SSHClient()
	ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
	ssh.connect(ip, username='devil1', password='admin')
	return ssh

#Checking Machine
def checkmachine(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        return True
    except socket.error as e:
        return False
    s.close()

#Copying File
def copyfile(ip,filename):
    try:
        ssh = DoLogin(ip)
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(filename)
        return True
    except SSHException as e:
        print "error copying file : %s" % e
        return False

#Extracting File
def extractfile(ip,filename):
    try:
        ssh = DoLogin(ip)
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command("unzip " + filename)
        channel.recv_exit_status()
        return True
    except Exception as e:
        print "error extracting file : %s" % e
        return False

#Removing Zip File
def removefile(ip,filename):
    try:
        ssh = DoLogin(ip)
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command("rm " + filename)
        channel.recv_exit_status()
        return True
    except Exception as e:
        print "error deleting file : %s" % e
        return False

#Running Servlet For Pre-Process all.csv
def servlet_run(ip,port,action,path):
    try:
        endurl = "http://" + ip + ":" + port + "/Service/" + action + ".jsp?dir=" + path + "&updateNumberType=true"
        print endurl
        resp = urllib2.urlopen(endurl)
        if resp.getcode() == 200:
            return True
        else:
        #print resp.read()
            return False
    except Exception as e:
        print "error reading path : %s" % e
        return False


#Compress  output Files
def compressfile(ip,filename):
    try:
        ssh = DoLogin(ip)
        transport = ssh.get_transport()
        channel = transport.open_session()
        cmd1="zip " + filename.split('.')[0] + "-process.zip " + filename.split('.')[0] + "/all/*.txt ; mv " + filename.split('.')[0] + " " + filename.split('.')[0] + "-Preprocess"
        channel.exec_command(cmd1)
        channel.recv_exit_status()
        return True

    except SSHException as e:
        return False

#Copying New Compressed  zip files on Local
def getfile(ip,filename):
    try:
        ssh = DoLogin(ip)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get(filename.split('.')[0] + "-process.zip")
        return True
    except SSHException as e:
        print "error fetching file : %s" % e
        return False

file1="myfile1.zip"
for i in machine:
	print checkmachine(i, machine[i])
	print copyfile(i,file1)
	print extractfile(i,file1)