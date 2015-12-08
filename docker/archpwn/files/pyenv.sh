export WORKON_HOME=~/.virtualenvs
if [[ ! -d "$WORKON_HOME" ]]; then
    mkdir -p "$WORKON_HOME"
fi
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/bin/virtualenvwrapper.sh
