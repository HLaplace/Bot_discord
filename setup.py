
# rendre un programme en .exe

from cx_Freeze import setup, Executable
base = None

file_name = ""
executables = [Executable(file_name, base=base)] # mettre ici le nom du fichier a convertir

packages = ["time"] # liste des librairies ici 
options = {
    'build_exe': {    
        'packages':packages,
    },
}
# Adaptez les valeurs des variables "name", "version", "description" à votre programme.
setup(
    name = "Mon Programme",
    options = options,
    version = "1.0",
    description = 'Voici mon programme',
    executables = executables
)

# python setup.py build