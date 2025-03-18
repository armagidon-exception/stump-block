from cx_Freeze import setup, Executable
import distutils
import opcode
import os


# opcode is not a virtualenv module, so we can use it to find the stdlib; this is the same
# trick used by distutils itself it installs itself into the virtualenv
# distutils_path = os.path.join(os.path.dirname(opcode.__file__),'site-packages', 'setuptools')
# tree_sitter_path = os.path.join(os.path.dirname(opcode.__file__),'site-packages', 'tree_sitter')
build_exe_options = {'packages': ['typing_extensions'], 'include_files': [('build/languages.so', 'build/languages.so'), "parsers/"], 'include_path': ['parsers/'] }
# Dependencies are automatically detected, but it might need
# fine tuning.
base = 'console'

executables = [
    Executable('__init__.py', base=base, target_name = 'stumpblock')
]

setup(name='StumpBlock',
      version = '1.0',
      description = 'Generates flowcharts from C# programs',
      options = {'build_exe': build_exe_options},
      executables = executables)
