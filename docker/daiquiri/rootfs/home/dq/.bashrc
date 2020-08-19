alias env="env | sort"
alias p="python"
alias pm='python manage.py'
alias psa='ps faux'
alias tailf="tail -F"
alias tlp='netstat -tulpen'
alias tlps='sudo netstat -tulpen'
alias we="watchexec"

# don't have exa? you'd probably enjoy https://github.com/ogham/exa.git
export EXA_COLORS="da=1;34:gm=1;34:di=1;34:b0=1;31"
alias ll="exa --long --group --header --modified --git --group-directories-first"
alias la="exa --long --group --header --modified --created --accessed --git --all --group-directories-first"

cd "${HOME}"
