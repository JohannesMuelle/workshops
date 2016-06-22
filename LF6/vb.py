#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess
import sys, traceback
import crypt

# Passwort für den User vbox
print("Dieses Skript installiert VirtualBox und phpVirtualBox auf dem System")
print("Es ist zu unterscheiden zwischen dem Benutzer unter dem die Anwendung läuft und dem Benutzer, der sich auf der Weboberfläche anmeldet.")
print("Die Anmeldung auf der Weboberfläche ist zu Beginn admin/admin und wird aufgerufen über IP/phpvirtualbox bzw. Servername/phpvirtualbox")
print("Sie werden jetzt nach dem Passwort gefragt für den Benutzer vbox. Der Benutzer vbox ist der Benutzer unter dem die Anwendung VirtualBox ausgeführt wird.")

print ( "This script installed VirtualBox and phpVirtualBox on the system")
print ( "It is necessary to distinguish between the user under which the application is running and the user who logs on to the web interface.")
print ( "The registration on the web interface is called at the beginning admin / admin and is under IP/phpvirtualbox or ServerName/phpvirtualbox")
print ( "You are now asked for the password for the user vbox. The user is the user vbox under which VirtualBox is running.")
print ("Please enter the password for the user vbox a:")
password = input("Bitte geben Sie das Passwort für den Benutzer vbox ein:")

pass1 = "'"+password+"'"
print("UPDATE")
try:
    cmd1 = os.system("apt-get -y -qq update && sudo apt-get -y -qq upgrade")
except:
    print("Update fehlgeschlagen!")
try:
    print("Installation von einigen Basisprogrammen")
    cmd1 = os.system("apt -y -qq install screen emacs wget python-software-properties")
except:
    print("Installation fehlgeschlagen")
try:
    print("Repository hinzufügen")
    output = subprocess.check_output("lsb_release -sc", shell = True)
    lsb = str(output, 'utf-8').strip()    
    cmd1 = os.system("add-apt-repository 'deb http://download.virtualbox.org/virtualbox/debian "+lsb+" contrib'")
    cmd1 = os.system("add-apt-repository --remove 'deb-src http://download.virtualbox.org/virtualbox/debian "+lsb+" contrib'")
    # Änderung des Schlüssel für das Repository ab Ubuntu 16.04 (xenial)
    if lsb == "xenial":
        cmd1 = os.system("wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -")
    else:
        cmd1 = os.system("wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -")    
    cmd1 = os.system("apt-get -qq update")
except:
    print("Repository hinzufügen fehlgeschlagen")
    print("Unexpected error:", sys.exc_info()[0])
    raise
try:
    print("Instalation VirtualBox")
    output = subprocess.check_output("uname -r", shell = True)
    Kernel = str(output, 'utf-8').strip()
    cmd1 = os.system("apt-get install -y -qq linux-headers-"+Kernel)
    cmd1 = os.system("apt-get install -y -qq build-essential virtualbox-5.0 dkms")
    cmd1 = os.system("apt-get install -y -qq --allow-unauthenticated virtualbox-5.0")
    cmd1 = os.system("apt-get install -y -qq --allow-unauthenticated dkms >> vb.log")
#    cmd1 = os.system ("wget -q http://download.virtualbox.org/virtualbox/5.0.16/Oracle_VM_VirtualBox_Extension_Pack-5.0.16.vbox-extpack")
#    cmd1 = os.system("VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-5.0.16.vbox-extpack >>vb.log")
    version = os.system("vboxmanage -v")
    

    encPass = crypt.crypt(password,"22")
    cmd1 = os.system("useradd -m -p "+encPass+" vbox -G vboxusers")
except:
    print("Installation von VirtualBox fehlgeschlagen")
try:
    print("Installation von phpVirtualBox")
    print("Vorbereitung ...")
    # Datei /etc/default/virtualbox anlegen und User eintragen
    datei = open("/etc/default/virtualbox", "w")
    datei.write("VBOXWEB_USER=vbox")
    datei.close()
except:
    print("Installation von phpVirtualBox fehlgeschlagen")
try:
    print("Web-Server installieren ..")
    if lsb == "xenial":
        cmd1 = os.system("apt-get -y -qq install php7.0 apache2-utils")
        cmd1 = os.system("apt-get -y -qq install php7.0-mysql")
        cmd1 = os.system("apt-get -y -qq install apache2")
        cmd1 = os.system("apt-get -y -qq install apache2-utils")
# Neues Modul ab Ubuntu 16.04: https://sourceforge.net/p/phpvirtualbox/discussion/help/thread/ae25b8e7/
        cmd1 = os.system("apt-get -y -qq install php7.0-xml")
        cmd1 = os.system("apt-get -y -qq install php-soap")
        cmd1 = os.system("apt-get -y -qq install php7.0-soap")
        cmd1 = os.system("apt-get -y -qq install libapache2-mod-php")
    else:
        cmd1 = os.system("apt-get -y -qq install php5 php5-mysql")
        cmd1 = os.system("apt-get -y -qq install apache2")
        cmd1 = os.system("apt-get -y -qq install apache2-utils")
        cmd1 = os.system("apt-get -y -qq install php5-mysql")
    cmd1 = os.system("wget -q 'http://sourceforge.net/projects/phpvirtualbox/files/latest/download' --content-disposition")
    cmd1 = os.system ("apt-get -y -qq install unzip")
    cmd1 = os.system("unzip -qq -o phpvirtualbox-5.0-5.zip -d /var/www/htm")
    cmd1 = os.system("ln -s /var/www/html/phpvirtualbox-5.0-5 /var/www/html/phpvirtualbox")
    cmd1 = os.system("chown -R www-data.www-data /var/www")
    cmd1 = os.system("service vboxweb-service stop")
    cmd1 = os.system("/sbin/rcvboxdrv setup")
    cmd1 = os.system("service vboxweb-service start")
    cmd1 = os.system("cp /var/www/html/phpvirtualbox/config.php-example /var/www/html/phpvirtualbox/config.php")
#Datei einlesen
    f = open('/var/www/html/phpvirtualbox/config.php','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("'pass'",pass1)
    f = open('/var/www/html/phpvirtualbox/config.php','w')
    f.write(newdata)
    f.close()
except:
    print("Web-Server fehlgeschlagen")
