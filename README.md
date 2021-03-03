# ATL Traffic Log
CS 4365 Semester Project

## Setup

### Materials Needed:

1. Raspberry Pi 3B+ (others may work but are untested)
2. MicroSD Card for Boot Drive (Min 16GB, Recommend Class 10)
3. USB Type-A Storage Device (Necessary size depends on number of cams and time to store, we are using 128GB flash storage drives)
4. 5V Power Supply for Pi (refer to model specific amperage recommendations)

### Software Installation:

1. Install Raspberry Pi OS to MicroSD Card to boot a clean instance. You can reuse a previous install but some pre-existing applications may interfere with the ATL Traffic Log code.

3. (Optional) - Enable VNC and/or SSH on the Pi for remote configuration. You may opt to use the Pi locally if you choose.

4. Run the following command to get the latest repository updates for the following software installs: `sudo apt-get update` .

5. Check that Python 3 is installed using the following command: `$python3 --version` .
Our OS came preinstalled with Python 3.7.3 however anything newer than this should be supported. If issues arise, consider matching our version.

6. Install Node.js using the following command: `sudo apt-get install nodejs` .

7. Install & Configure the FTP Server Software using the following steps:

    > First run the following command: `sudo apt-get install vsftpd`

    > Next open `/etc/vsftpd.conf` as super-user in your text editor of choice and uncomment the following lines:

        anonymous_enable=NO
        local_enable=YES
        write_enable=YES
        local_umask=022
        chroot_local_user=YES

    > In the same file, add the following lines:

        user_sub_token=$USER
        local_root=/home/$USER/ftp

    >> See `Example Files` folder in repository for example conf file. Note drive name cannot contain spaces.

    > Next make directories with appropriate permissions for the ftp root and camera archive:
        
        mkdir /media/pi/<external-drive-name>/ftp
        mkdir /media/pi/<external-drive-name>/ftp/archive
        chmod a-w /media/pi/<external-drive-name>/ftp

    > The following command will symbolically link the external drive folder to the home directory so it interfaces with the FTP Server as if it were internal storage:

        ln -s /media/pi/<external-drive-name>/ftp /home/pi/ftp

    > Finally restart the ftp service to apply the configuration and use a separate machine on the network to access the FTP server at the Pi's address:

        sudo service vsftpd restart
        ifconfig

    > To connect to the FTP Server using Windows (example), from File Explorer, under This PC from the Sidebar, click on "Add a network location" from the ribbon. From there the address for the FTP server will be "ftp://<your-pi-ip>". For username and password, the default username is "pi" and the password is set by the user upon first boot. From here it will connect and allow you to browse the directory as if you were on the Pi. Try seeing if files are visible such as creating a test file in the archive folder on the Pi and accessing it over the network.
