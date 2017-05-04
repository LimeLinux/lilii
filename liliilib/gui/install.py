#
#
#  Copyright 2017 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QDir
from .widget.slidewidget import Slide, SlideWidget
from ..tools import is_efi
import os
import subprocess
import shutil


class InstallWidget(QWidget):

    applyPage = pyqtSignal(bool)
    first_show = True

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.tr("System Installation"))
        self.setLayout(QVBoxLayout())

        self.slide_widget = SlideWidget()
        self.layout().addWidget(self.slide_widget)

        self.progress = QProgressBar()
        self.layout().addWidget(self.progress)

        self.desc_label = QLabel()
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.desc_label)

        self.addSlides()



    def addSlides(self):
        slide1 = Slide()
        slide1.setResource(":/images/about.svg")
        slide1.setDescription(self.tr("Deneme 1"))
        self.slide_widget.addWidget(slide1)

        slide2 = Slide()
        slide2.setResource(":/images/apply.svg")
        slide2.setDescription(self.tr("Deneme 2"))
        self.slide_widget.addWidget(slide2)

        slide3 = Slide()
        slide3.setResource(":/images/back.svg")
        slide3.setDescription(self.tr("Deneme 3"))
        self.slide_widget.addWidget(slide3)

        slide4 = Slide()
        slide4.setResource(":/images/camera.svg")
        slide4.setDescription(self.tr("Deneme 4"))
        self.slide_widget.addWidget(slide4)

        slide5 = Slide()
        slide5.setResource(":/images/disk.svg")
        slide5.setDescription(self.tr("Deneme 5"))
        self.slide_widget.addWidget(slide5)

        slide6 = Slide()
        slide6.setResource(":/images/exit.svg")
        slide6.setDescription(self.tr("Deneme 6"))
        self.slide_widget.addWidget(slide6)

    def finish(self):
        self.applyPage.emit(True)
        self.install_thread.deleteLater()

    def showEvent(self, event):
        if self.first_show:
            self.slide_widget.startSlide()
            self.applyPage.emit(False)

            self.install_thread = Install(self)
            self.install_thread.finished.connect(self.finish)
            self.install_thread.total.connect(self.progress.setMaximum)
            self.install_thread.percent.connect(self.progress.setValue)

            self.install_thread.start()
            self.first_show = False


class Install(QThread):

    total = pyqtSignal(int)
    percent = pyqtSignal(int)
    __percent = 0

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.rootfs_path = "/bootmnt/pisi/x86_64/rootfs.sqfs"
        self.desktopfs_path = "/bootmnt/pisi/x86_64/desktop.sqfs"

        self.mount_path = "/tmp/lime"

        self.hostname = self.parent.parent.lilii_settings["hostname"]
        self.locale = self.parent.parent.lilii_settings["lang"]
        self.timezone = self.parent.parent.lilii_settings["timezone"]
        self.keyboard_model = self.parent.parent.lilii_settings["keyboard_model"][0] # pc105
        self.keyboard_variant = self.parent.parent.lilii_settings["keyboard_variant"] #q = None - f
        self.keyboard_layout = self.parent.parent.lilii_settings["keyboard_layout"][0] #tr
        self.root_disk = self.parent.parent.lilii_settings["/"]
        self.home_disk = self.parent.parent.lilii_settings["/home"]

        self.boot_disk = None

        if is_efi():
            self.boot_disk = self.parent.parent.lilii_settings["/boot/efi"]

        else:
            self.boot_disk = self.parent.parent.lilii_settings["/boot"]
            self.bootloader = self.parent.parent.lilii_settings["bootloader"]

        self.username = self.parent.parent.lilii_settings["username"]
        self.realname = self.parent.parent.lilii_settings["fullname"]
        self.userpaswd = self.parent.parent.lilii_settings["password"]
        self.is_rootpasswd = self.parent.parent.lilii_settings["root_user"]
        self.autologin = self.parent.parent.lilii_settings["auto_login"]
        self.useravatar = self.parent.parent.lilii_settings["avatar"]
        self.liveuser = "limelive"

        self.rootpasswd = None

        if self.is_rootpasswd:
            self.rootpasswd = self.parent.parent.lilii_settings["password"]

        else:
            self.rootpasswd = self.parent.parent.lilii_settings["root_pass"]


    def set_preumount(self):
        command = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
        output = command.stdout.read().decode("utf-8")

        for out in output.split("\n"):
            if out.startswith("/dev/sd"):
                mount_folder = out.split()[-1]
                if not mount_folder == "/bootmnt":
                    os.system("umount --force {}".format(mount_folder))


    def set_mount(self):
        # os.makedirs(self.mount_path+"/rootfs", exist_ok=True)
        # os.makedirs(self.mount_path + "/desktop", exist_ok=True)
        # os.system("mount {} {} -t squashfs -o loop".format(self.rootfs_path, self.mount_path+"/rootfs"))
        # os.system("mount {} {} -t squashfs -o loop".format(self.desktopfs_path, self.mount_path + "/desktop"))

        #root dizinini bağla.
        os.makedirs(self.mount_path + "/root", exist_ok=True)
        os.system("mount {} {}".format(self.root_disk, self.mount_path+"/root"))
        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_unpack(self):
        subprocess.call(["unsquashfs", "-f", "-d", self.mount_path+"/root", self.rootfs_path], stdout=subprocess.PIPE)
        self.__percent += 4
        self.percent.emit(self.__percent)

        subprocess.call(["unsquashfs", "-f", "-d", self.mount_path+"/root", self.desktopfs_path], stdout=subprocess.PIPE)
        self.__percent += 8
        self.percent.emit(self.__percent)

    def set_chroot(self):
        os.makedirs(self.mount_path+"/root/dev/shm", exist_ok=True)
        os.makedirs(self.mount_path + "/root/dev/pts", exist_ok=True)
        os.makedirs(self.mount_path + "/root/sys", exist_ok=True)
        os.makedirs(self.mount_path + "/root/proc", exist_ok=True)
        os.system("mount --bind /dev/ {}/dev/".format(self.mount_path+"/root"))
        os.system("mount --bind /dev/shm {}/dev/shm".format(self.mount_path+"/root"))
        os.system("mount --bind /dev/pts {}/dev/pts".format(self.mount_path+"/root"))
        os.system("mount --bind /sys/ {}/sys/".format(self.mount_path+"/root"))
        os.system("mount --bind /proc/ {}/proc/".format(self.mount_path+"/root"))

        os.system("chmod 555 {}/sys/".format(self.mount_path + "/root"))
        os.system("chmod 555 {}/proc/".format(self.mount_path + "/root"))

        if not is_efi() and self.boot_disk:
            os.makedirs(self.mount_path + "/root/boot", exist_ok=True)
            os.system("mount {} {}/boot".format(self.boot_disk, self.mount_path+"/root"))

        elif is_efi():
            os.makedirs(self.mount_path + "/root/boot/efi", exist_ok=True)
            os.system("mount -vt vfat {} {}/boot/efi".format(self.boot_disk, self.mount_path+"/root"))
            os.system("mount -vt efivarfs efivars /sys/firmware/efi/efivars")

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_fstab(self):

        def fstab_parse():
            device_list = []
            blkid_output = subprocess.Popen("blkid", stdout=subprocess.PIPE)
            output = blkid_output.stdout.read().decode("utf-8")

            for o in output.split("\n"):
                device = []
                for i in o.split():
                    if i.startswith("/dev"):
                        device.append(i[:-1])

                    elif i.startswith("UUID="):
                        device.append(i[6:-1])

                    elif i.startswith("TYPE="):
                        device.append(i[6:-1])


                device_list.append(device)

            return device_list

        with open(self.mount_path+"/root"+"/etc/fstab", "w") as fstab_file:
            for device in fstab_parse():
                try:
                    if self.root_disk == device[0]:
                        if self.home_disk:
                            fstab_file.write('UUID={}\t / \t\t {} \t rw,errors=remount-ro\t0\t1\n'.format(device[1], device[2]))

                        else:
                            fstab_file.write('UUID={}\t / \t\t {} \t defaults\t0\t1\n'.format(device[1], device[2]))

                    elif self.home_disk == device[0]:
                        fstab_file.write('UUID={}\t /home \t\t {} \t defaults\t0\t0\n'.format(device[1], device[2]))

                    elif self.boot_disk == device[0]:
                        if is_efi():
                            fstab_file.write('UUID={}\t /boot/efi \t\t {} \t umask=0077\t0\t1\n'.format(device[1], device[2]))

                        else:
                            fstab_file.write('UUID={}\t /boot \t\t {} \t defaults\t0\t1\n'.format(device[1], device[2]))

                    elif device[2] == "swap":
                        fstab_file.write('UUID={}\t swap \t swap \t defaults\t0\t0\n'.format(device[1], device[2]))

                except IndexError:
                    print(device, "Bu ne?")

            if is_efi():
                fstab_file.write("efivarfs       /sys/firmware/efi/efivars  efivarfs  defaults  0      1\n")

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_locale(self):
        with open(self.mount_path+"/root"+"/etc/locale.conf", "w") as locale:
            locale.write("LANG={}\n".format(self.locale))
            locale.write("LC_COLLATE=C\n")
            locale.flush()
            locale.close()

        os.makedirs(self.mount_path + "/root/etc/mudur", exist_ok=True)
        with open(self.mount_path+"/root/etc/mudur/locale", "w") as locale:
            locale.write("{}\n".format(self.locale))
            locale.flush()
            locale.close()

        buffer = open(self.mount_path+"/root"+"/etc/locale.gen").readlines()
        with open(self.mount_path+"/root"+"/etc/locale.gen", "w") as locale:
            for i in buffer:
                if i.startswith("#{}".format(self.locale.split(".")[0])):
                    locale.write(i[1:])

            locale.flush()
            locale.close()

        self.chroot_command("export LANG={}".format(self.locale))
        self.chroot_command("export LANGUAGE={}".format(self.locale))
        self.chroot_command("locale-gen {}".format(self.locale))

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_timezone(self):
        self.chroot_command("ln -s /usr/share/zoneinfo/{} /etc/localtime".format(self.timezone))
        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_host(self):
        hosts_text = "# /etc/hosts\n"\
                     "#\n"\
                     "# This file describes a number of hostname-to-address\n"\
                     "# mappings for the TCP/IP subsystem.  It is mostly\n"\
                     "# used at boot time, when no name servers are running.\n"\
                     "# On small systems, this file can be used instead of a\n"\
                     "# \"named\" name server.  Just add the names, addresses\n"\
                     "# and any aliases to this file...\n"\
                     "#\n"\
                     "\n"\
                     "127.0.0.1   localhost      {}\n"\
                     "\n"\
                     "# IPV6 versions of localhost and co\n"\
                     "::1     localhost ip6-localhost ip6-loopback\n"\
                     "fe00::0 ip6-localnet\n"\
                     "ff00::0 ip6-mcastprefix\n"\
                     "ff02::1 ip6-allnodes\n"\
                     "ff02::2 ip6-allrouters\n"\
                     "ff02::3 ip6-allhosts\n".format(self.hostname)

        with open(self.mount_path+"/root"+"/etc/hostname", "w") as hostname:
            hostname.write(self.hostname)
            hostname.flush()
            hostname.close()

        with open(self.mount_path+"/root"+"/etc/hosts", "w") as hosts:
            hosts.write(hosts_text)
            hosts.flush()
            hosts.close()

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_keyboard(self):
        if not self.keyboard_variant:
            self.keyboard_variant = ""

        keyboard = "Section \"InputClass\"\n"\
                   "\t\tIdentifier \"system-keyboard\"\n"\
                   "\t\tMatchIsKeyboard \"on\"\n"\
                   "\t\tOption \"XkbModel\" \"{}\"\n"\
                   "\t\tOption \"XkbLayout\" \"{}\"\n"\
                   "\t\tOption \"XkbVariant\" \"{}\"\n"\
                   "EndSection\n".format(self.keyboard_model, self.keyboard_layout, self.keyboard_variant)

        with open(self.mount_path+"/root"+"/etc/X11/xorg.conf.d/10-keyboard.conf", "w") as keyboard_conf:
            keyboard_conf.write(keyboard)
            keyboard_conf.flush()
            keyboard_conf.close()

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_initcpio(self):
        self.chroot_command("mkinitcpio -p linux")
        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_sudoers(self):
        sudoers = "# to use special input methods. This may allow users to compromise  the root\n"\
                  "# account if they are allowed to run commands without authentication.\n"\
                  "#Defaults env_keep = \"LANG LC_ADDRESS LC_CTYPE LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT "\
                  "LC_MESSAGES LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE LC_TIME LC_ALL LANGUAGE LINGUAS "\
                  "XDG_SESSION_COOKIE XMODIFIERS GTK_IM_MODULEQT_IM_MODULE QT_IM_SWITCHER\"\n"\
                  "\n"\
                  "# User privilege specification\n"\
                  "root    ALL=(ALL) ALL\n"\
                  "\n"\
                  "# Uncomment to allow people in group wheel to run all commands\n"\
                  "%wheel  ALL=(ALL)       ALL\n"\
                  "\n"\
                  "# Same thing without a password\n"\
                  "#%wheel ALL=(ALL)       NOPASSWD: ALL\n"\
                  "{}    ALL=(ALL)       ALL".format(self.username)

        with open(self.mount_path+"/root"+"/etc/sudoers", "w") as sudoers_file:
            sudoers_file.write(sudoers)
            sudoers_file.flush()
            sudoers_file.close()

        self.__percent += 1
        self.percent.emit(self.__percent)

    def remove_user(self):
        self.chroot_command("userdel -r {}".format(self.liveuser))
        if os.path.exists(self.mount_path+"/root"+"/home/{}".format(self.liveuser)):
            os.system("rm -rf {}/home/{}".format(self.mount_path+"/root", self.liveuser))

        self.__percent += 1
        self.percent.emit(self.__percent)

    def add_user(self):
        # with open(self.mount_path+"/root"+"/tmp/user.conf", "w") as user:
        #     user.write("{}:{}\n".format(self.username, self.userpaswd))
        #     user.write("{}:{}\n".format("root", self.rootpasswd))

        groups_user = "-G audio,video,cdrom,wheel,lpadmin"
        self.chroot_command("useradd -s {} -c '{}' {} -m {}".format("/bin/bash", self.realname, groups_user, self.username))
        self.chroot_command("yes {} | passwd {}".format(self.userpaswd, self.username))  # kullanıcı şifresi belirtmek için.
        self.chroot_command("yes {} | passwd root".format(self.rootpasswd))
        #self.chroot_command("rm -rf /tmp/user.conf")

        #self.chroot_command("passwd -d root") #su ile giriş yapmayı engelliyor gibi. sudo su çalışıyor.

        if self.useravatar:
            shutil.copy(QDir.homePath() + "/.face.icon", self.mount_path+"/root"+"/home/{}".format(self.username))

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_displaymanager(self):
        #lightdm
        conf_data = []
        path = self.mount_path+"/root"+"/etc/lightdm/lightdm.conf"
        with open(path) as conf:
            for text in conf.readlines():
                if text.startswith("autologin-user="):
                    conf_data.append("autologin-user={}\n".format(self.username))
                    print("autologin", self.username)

                else:
                    conf_data.append(text)

        with open(path, "w") as conf:
            conf.write("".join(conf_data))

        self.__percent += 1
        self.percent.emit(self.__percent)

        #XOrg
        #self.chroot_command("Xorg :1 -configure")
        #self.chroot_command("cp /root/xorg.conf.new /etc/X11/xorg.conf")

    def set_network(self): pass

    def set_grupcfg(self): pass

    def install_bootloader(self):
        def boot_part(dev):
            asd = subprocess.Popen("blkid", stdout=subprocess.PIPE)
            qwe = asd.stdout.read().decode("utf-8")

            for o in qwe.split("\n"):
                i = o.split()
                try:
                    if i[0][:-1] == dev:
                        for j in i:
                            if j.startswith("PARTUUID="):
                                return j[10:-1]

                except IndexError as ex:
                    print(ex)


        if not is_efi():
            if self.boot_disk:
                self.chroot_command("grub2-install --force {}".format(self.bootloader))
            else:
                self.chroot_command("grub2-install --force {}".format(self.bootloader))

        else:
            self.chroot_command("grub2-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=\"{0}\" "\
                                "--recheck --debug --force".format("LimeLinux"))
            self.chroot_command("efibootmgr --create --gpt --disk {1} --part {2} --write-signature "\
                                "--loader \"/EFI/{0}/grubx64.efi\""
                                .format("LimeLinux", self.boot_disk, boot_part(self.boot_disk))) # --label "\"{2} {3} {2}\

        self.chroot_command("grub2-mkconfig -o /boot/grub2/grub.cfg")

        self.__percent += 1
        self.percent.emit(self.__percent)

    def set_umount(self):
        os.system("umount --force {}/dev/".format(self.mount_path + "/root"))
        os.system("umount --force {}/dev/shm".format(self.mount_path + "/root"))
        os.system("umount --force {}/dev/pts".format(self.mount_path + "/root"))
        os.system("umount --force {}/sys/".format(self.mount_path + "/root"))
        os.system("umount --force {}/proc/".format(self.mount_path + "/root"))

        #os.system("umount {}".format(self.mount_path + "/rootfs"))
        #os.system("umount {}".format(self.mount_path + "/desktop"))
        os.system("umount -lv {}".format(self.mount_path + "/root"))

        self.__percent += 1
        self.percent.emit(self.__percent)

    def chroot_command(self, command):
        os.system("chroot {} /bin/sh -c \"{}\"".format(self.mount_path+"/root", command))

    def run(self):
        self.total.emit(25)
        self.set_preumount()
        self.parent.desc_label.setText(self.tr("Files loading..."))
        self.msleep(1000)
        self.set_mount()
        self.msleep(1000)
        self.set_chroot()
        self.msleep(1000)
        self.set_unpack()
        self.msleep(1000)
        self.parent.desc_label.setText(self.tr("System configuration..."))
        self.set_fstab()
        self.msleep(1000)
        self.set_timezone()
        self.msleep(1000)
        self.set_locale()
        self.msleep(1000)
        self.set_host()
        self.msleep(1000)
        self.set_keyboard()
        self.msleep(1000)
        self.remove_user()
        self.msleep(1000)
        self.set_sudoers()
        self.msleep(1000)
        self.set_initcpio()
        self.msleep(1000)
        self.add_user()
        self.msleep(1000)
        self.set_network() #boş
        self.set_grupcfg() #boş
        self.set_displaymanager()
        self.msleep(1000)
        self.install_bootloader()
        self.msleep(1000)
        self.set_umount()
        self.parent.desc_label.setText(self.tr("System installed."))
        self.msleep(3000)
