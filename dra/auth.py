from dra import models

def get_account_repository_permissions(account, repository):
    """ This calculates pull,push rights for a user to a repository """

    repository = models.Repository.objects.filter(name=repository).first()

    if repository is None:
        return False, False

    pull = repository.public

    f = repository.repositorypermissions_set.filter(group__account=account)
    if f.exists():
        pull = True
        push = f.filter(write=True).exists()
    else:
        push = False

    return pull, push
