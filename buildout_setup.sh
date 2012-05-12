rm bootstrap.py
cp buildout.cfg.sample buildout.cfg
wget "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"
python bootstrap.py
bin/buildout
