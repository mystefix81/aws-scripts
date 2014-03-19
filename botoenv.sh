#!/bin/sh

case $1 in
	(list)
		find "$HOME/.aws/" -maxdepth 1 -name '*.boto' |sed 's%^.*/%  %;s%\.boto$%%'
		;;
	(set)
		if [ -z "$2" ]
		then
			echo "No destination given."
			exit 1
		fi
		dst="$HOME/.aws/$2.boto"
		if [ ! -f "$dst" ]
		then
			echo "$dst is not a file."
			exit 1
		elif [ ! -r "$dst" ]
		then
			echo "$dst is not readable."
			exit 1
		else
			echo "Switching to $2."
			ln -nfs "$dst" "$HOME/.boto"
		fi
		;;
	(get)
		echo "Currently set to:"
		readlink "$HOME/.boto" |sed 's%^.*/%  %;s%\.boto$%%'
		;;
	(*)
		echo "I don't know what you want."
		exit 1
		;;
esac
