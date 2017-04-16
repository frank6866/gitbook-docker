# busybox
busybox是一个提供了unix工具集的程序，可以运行在多款POSIX环境的操作系统（比如Linux）。由于busybox可执行文件大小比较小，并通常适用于Linux内核，使得它非常合适使用于嵌入式操作系统。

由于busybox功能强大，它被称为嵌入式Linux中的瑞士军刀。  



# 下载
下载地址，[https://busybox.net/downloads/binaries/](https://busybox.net/downloads/binaries/)。  

这里以1.21.1为例，下载x86_64的文件。

```
# wget https://busybox.net/downloads/binaries/1.21.1/busybox-x86_64
# chmod a+x busybox-x86_64
```

# 使用
## 查看帮助信息
```
# ./busybox-x86_64
BusyBox v1.21.1 (2013-07-08 11:34:59 CDT) multi-call binary.
BusyBox is copyrighted by many authors between 1998-2012.
Licensed under GPLv2. See source distribution for detailed
copyright notices.

Usage: busybox [function [arguments]...]
   or: busybox --list[-full]
   or: busybox --install [-s] [DIR]
   or: function [arguments]...

	BusyBox is a multi-call binary that combines many common Unix
	utilities into a single executable.  Most people will create a
	link to busybox for each function they wish to use and BusyBox
	will act like whatever it was invoked as.

Currently defined functions:
	[, [[, acpid, add-shell, addgroup, adduser, adjtimex, arp, arping, ash, awk, base64, basename, beep, blkid, blockdev, bootchartd, brctl, bunzip2, bzcat, bzip2, cal,
	cat, catv, chat, chattr, chgrp, chmod, chown, chpasswd, chpst, chroot, chrt, chvt, cksum, clear, cmp, comm, conspy, cp, cpio, crond, crontab, cryptpw, cttyhack, cut,
	date, dc, dd, deallocvt, delgroup, deluser, depmod, devmem, df, dhcprelay, diff, dirname, dmesg, dnsd, dnsdomainname, dos2unix, du, dumpkmap, dumpleases, echo, ed,
	egrep, eject, env, envdir, envuidgid, ether-wake, expand, expr, fakeidentd, false, fbset, fbsplash, fdflush, fdformat, fdisk, fgconsole, fgrep, find, findfs, flock,
	fold, free, freeramdisk, fsck, fsck.minix, fsync, ftpd, ftpget, ftpput, fuser, getopt, getty, grep, groups, gunzip, gzip, halt, hd, hdparm, head, hexdump, hostid,
	hostname, httpd, hush, hwclock, id, ifconfig, ifdown, ifenslave, ifplugd, ifup, inetd, init, insmod, install, ionice, iostat, ip, ipaddr, ipcalc, ipcrm, ipcs, iplink,
	iproute, iprule, iptunnel, kbd_mode, kill, killall, killall5, klogd, last, less, linux32, linux64, linuxrc, ln, loadfont, loadkmap, logger, login, logname, logread,
	losetup, lpd, lpq, lpr, ls, lsattr, lsmod, lsof, lspci, lsusb, lzcat, lzma, lzop, lzopcat, makedevs, makemime, man, md5sum, mdev, mesg, microcom, mkdir, mkdosfs,
	mke2fs, mkfifo, mkfs.ext2, mkfs.minix, mkfs.vfat, mknod, mkpasswd, mkswap, mktemp, modinfo, modprobe, more, mount, mountpoint, mpstat, mt, mv, nameif, nanddump,
	nandwrite, nbd-client, nc, netstat, nice, nmeter, nohup, nslookup, ntpd, od, openvt, passwd, patch, pgrep, pidof, ping, ping6, pipe_progress, pivot_root, pkill, pmap,
	popmaildir, poweroff, powertop, printenv, printf, ps, pscan, pstree, pwd, pwdx, raidautorun, rdate, rdev, readahead, readlink, readprofile, realpath, reboot,
	reformime, remove-shell, renice, reset, resize, rev, rm, rmdir, rmmod, route, rpm, rpm2cpio, rtcwake, run-parts, runlevel, runsv, runsvdir, rx, script, scriptreplay,
	sed, sendmail, seq, setarch, setconsole, setfont, setkeycodes, setlogcons, setserial, setsid, setuidgid, sh, sha1sum, sha256sum, sha3sum, sha512sum, showkey, slattach,
	sleep, smemcap, softlimit, sort, split, start-stop-daemon, stat, strings, stty, su, sulogin, sum, sv, svlogd, swapoff, swapon, switch_root, sync, sysctl, syslogd, tac,
	tail, tar, tcpsvd, tee, telnet, telnetd, test, tftp, tftpd, time, timeout, top, touch, tr, traceroute, traceroute6, true, tty, ttysize, tunctl, udhcpc, udhcpd, udpsvd,
	umount, uname, unexpand, uniq, unix2dos, unlzma, unlzop, unxz, unzip, uptime, users, usleep, uudecode, uuencode, vconfig, vi, vlock, volname, wall, watch, watchdog,
	wc, wget, which, who, whoami, whois, xargs, xz, xzcat, yes, zcat, zcip
```

## 执行命令
比如执行busybox中的ls命令:  

```
# ./busybox-x86_64 ls
busybox-x86_64  dockerd.log
```	








# 参考
* https://busybox.net
* https://zh.wikipedia.org/wiki/BusyBox
