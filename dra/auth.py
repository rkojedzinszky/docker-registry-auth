""" Get repository permissions for an account """

# The lookup process is:
# loop:
#   lookup repository
#   if found
#     set pull rights accoring to public flag if not set already
#
#     lookup rights granted to this repo
#     if found:
#         grant pull rights
#         set push rights
#         return
#
#     strip one path from repository for next cycle
#
# return pull, False
#
# So, in short:
# - During recursive lookup, if a matching repo/group permission record exists
#   then pull rights are granted, push writes are based on the entry
# - If no repo/group explicit permission record exists, then pull rights are
#   based on longest repo match, push writes are denied
#
# Example:
#
# A repo like:
#   org (private) / public (public) / private (private)
#
# gr1 has write rights for org
# user1 is member of gr1
#
# gr2 has read rights for org/public
# user1 is member of gr2 too
#
# Then, user1 will not be able to write org/public/private
#

import logging
from django.db.models import F
from dra.models import Repository

logger = logging.getLogger(__name__)

def get_account_repository_permissions(account, repository: str):
    """ This calculates pull,push rights for a user to a repository """

    # Pull rights
    pull: bool = None
    push = False

    repository = repository.split('/')
    reponame = ""

    while repository:
        reponame = '/'.join(repository)
        repo = Repository.objects.filter(name=reponame).first()

        if repo is not None:
            Repository.objects.filter(pk=repo.pk).update(requests=F('requests') + 1)

            perms = repo.repositorypermissions_set.filter(group__account=account)
            if perms.exists():
                perms.update(requests=F('requests') + 1)

                pull = True
                push = perms.filter(write=True).exists()
                break

            if pull is None:
                pull = repo.public

        repository.pop()

    pull = pull is True

    return pull, push
