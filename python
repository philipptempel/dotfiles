# where to create the virtual envs in
export WORKON_HOME=${HOME}/.virtualenvs
if [ ! -d ${WORKON_HOME} ]; then
    mkdir -p $WORKON_HOME
fi

source /opt/local/bin/virtualenvwrapper.sh-3.7

virtualenv --always-copy --python=python2.7 "$WORKON_HOME/python2.7"
workon python2.7
pip install --upgrade pip
deactivate

virtualenv --always-copy --python=python3.7 "$WORKON_HOME/python3.7"
workon python3.7
pip install --upgrade pip
pip install tox wheel cookiecutter bump2version
deactivate

virtualenv --always-copy --python=python3.7 "$WORKON_HOME/scientific"
workon scientific
pip install --upgrade pip
pip install numpy scipy sympy pandas matplotlib plotly
deactivate

virtualenv --always-copy --python=python3.7 "$WORKON_HOME/latex"
workon latex
pip install --upgrade pip
pip install pygments
deactivate
