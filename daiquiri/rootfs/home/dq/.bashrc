source /home/dq/sh/source.sh

alias env="env | sort"
alias p="python3"
alias pm='python manage.py'
alias psa='ps aux'
alias tailf="tail -F"
alias tlp='netstat -tulpen'
alias we="watchexec ${@}"
alias lsmod="ls /usr/lib/apache2/modules/"
alias sock="sudo curl --no-buffer -XGET --unix-socket /var/run/php/php7.3-fpm.sock http://index.php"
alias rephp="sudo pkill -9 php-fpm && sudo /usr/sbin/php-fpm7.3"

export EXA_COLORS="da=1;34:gm=1;34:di=1;34:b0=1;31"
alias ll="exa --long --group --header --modified --git --group-directories-first"
alias lla="exa --long --group --header --modified --created --accessed --git --all --group-directories-first"

export DQIP=$(get_container_ip)
export LC_ALL=en_US.utf8

cd "${HOME}"
