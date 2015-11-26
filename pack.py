from distutils.core import setup
import py2exe
setup(
	options = {'py2exe': {
		'bundle_files': 2
	}},
    console = [{'script': 'clawer_1.py'}],
	#zipfile = None
)