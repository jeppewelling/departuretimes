# Quick start-stop-daemon example, derived from Debian /etc/init.d/ssh
set -e
# Thanks to:
# http://stackoverflow.com/questions/8251933/how-can-i-log-the-stdout-of-a-process-started-by-start-stop-daemon 
# Must be a valid filename
 
export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"
 
test -x $DAEMON || exit 0

. /lib/lsb/init-functions

case "$1" in
  start)
        echo -n "Starting daemon: $NAME logfile located at: /var/log/$NAME.log"
	start-stop-daemon  --background --start --quiet --pidfile $PIDFILE -m \
	    --startas /bin/bash -- -c "exec $DAEMON $DAEMON_OPTS > /var/log/$NAME.log 2>&1" 
        echo "."
	;;
  stop)
        echo -n "Stopping daemon: "$NAME
	start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
        echo "."
	;;
  restart)
	echo -n "Restarting daemon: $NAME logfile located at: /var/log/$NAME.log"
	start-stop-daemon --stop --quiet --oknodo --retry 30 --pidfile $PIDFILE


	start-stop-daemon  --background --start --quiet --pidfile $PIDFILE -m \
	    --startas /bin/bash -- -c "exec $DAEMON $DAEMON_OPTS > /var/log/$NAME.log 2>&1" 
	echo "."
	;;
  status)
	status_of_proc -p $PIDFILE  $DAEMON $NAME  && exit 0 || exit $?
	;;

 
  *)
	echo "Usage: "$1" {start|stop|restart}"
	exit 1
esac
 
exit 0
