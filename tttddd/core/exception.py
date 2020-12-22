__all__ = (
    'InternalServerError',
    'RepositoryStorageError',
)


class InternalServerError(Exception):
    pass


class RepositoryStorageError(InternalServerError):
    pass
