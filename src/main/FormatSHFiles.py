from numpy import f2py
from numpy.distutils.fcompiler import new_fcompiler

compiler = new_fcompiler(compiler='intel')
compiler.dump_properties()

with open("C:/Users/ahmed.kotb/PycharmProjects/AGPS/resources/Formating_SH_files.f") as sourcefile:
    sourcecode = sourcefile.read()
    print 'Fortran code'
    print sourcecode

f2py.compile(sourcecode, modulename='add', extra_args = '--fcompiler=gfortran')