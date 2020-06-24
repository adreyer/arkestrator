class CompilationError(Exception):
    pass

class TagDoesNotExist(CompilationError):
    pass

class UnnamedTagException(CompilationError):
    pass

