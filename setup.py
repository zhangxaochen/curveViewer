from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], includes=['lxml._elementpath', ])

executables = [
    Executable('main.py', 'Console')
]

setup(name='dist',
      version = '1.0',
      description = 'the mobile sensor signal browser',
      options = dict(build_exe = buildOptions),
      executables = executables)
