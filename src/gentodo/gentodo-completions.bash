#!/usr/bin/env bash

_gentodo() {
	local re='^[0-9]+$'

	if [ "$3" == "add" ]; then
		COMPREPLY=( $(compgen -W "-t --title -d --details -h --help" -- "$2") )
	elif [ "$3" == "del" ]; then
		COMPREPLY=( $(compgen -W "-t -d --title --details -h --help" -- "$2") )
	elif [ "$3" == "edit" ]; then 
		case "$4" in
			''|*[!0-9]*) COMPREPLY=( $(compgen -W "<id>" -- "$2") ) ;;
			*) COMPREPLY=( $(compgen -W "-t -d" -- "$2") ) ;;
		esac

		#if [[ "$4" =~ $re ]]; then
		#	COMPREPLY=( $(compgen -W "-t --title -d --details -h --help" -- "$2") )
		#fi
	else
		COMPREPLY=( $(compgen -W "add del search edit count" -- "$2") )
	fi
}
#complete -W "-t -d" gentodo add
#complete -W "-t -d" gentodo edit
#complete -W "add del count edit search" gentodo
complete -F _gentodo gentodo
