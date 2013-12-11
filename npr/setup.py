from cx_Freeze import setup, Executable
from  scipy.sparse.linalg.isolve.iterative import _iterative
from  scipy.sparse.linalg.dsolve.linsolve import umfpack

buildOptions = dict(packages = [], excludes = [], includes=['matplotlib.backends.backend_qt4agg',
 'scipy.sparse.csgraph._validation',
 # 'scipy.sparse.linalg.isolve.iterative._iterative' 
 ])

executables = [
    Executable('imageSketch.py', 'Console')
]

setup(name='imageSketch',
      version = '1.0',
      description = 'npr homework: pencil sketch',
      options = dict(build_exe = buildOptions),
      executables = executables)
