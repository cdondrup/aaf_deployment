#!/bin/bash

if [ -z "$1" ]; then
	echo "usage: $0 <user:password> <destionation-dir> <FILES...>" >&1
	exit 2
fi

LOGIN="$1"
shift
DESTDIR="$1"
shift
URL_BASE="https://lcas.lincoln.ac.uk/owncloud/remote.php/webdav/"


for f in "$@"; do
	bn=`basename "$f"`
	echo "uploading $f. check /tmp/curl.$USER.log for details" >& 2
	curl -X PUT --user $LOGIN --data-binary "@$f" "$URL_BASE/$DESTDIR/$bn" > /tmp/curl.$USER.log
done
