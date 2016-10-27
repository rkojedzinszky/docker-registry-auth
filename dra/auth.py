from dra import models

def get_user_repository_permissions(user, repository):
    """ This calculates pull,push rights for a user to a repository """

    repository = models.Repository.objects.filter(name=repository).first()

    if repository is None:
        return False, False

    pull = repository.public

    perm = repository.repositorypermissions_set.filter(group__user=user).first()
    if perm is not None:
        pull = True
        push = perm.write
    else:
        push = False

    return pull, push
