import os

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.module_utils.six import string_types
from ansible.module_utils.common.collections import is_sequence

def path_join(paths):
    ''' takes a sequence or a string, and return a concatenation
        of the different members '''
    if isinstance(paths, string_types):
        return os.path.join(paths)
    elif is_sequence(paths):
        return os.path.join(*paths)
    else:
        raise AnsibleFilterError("|path_join expects string or sequence, got %s instead." % type(paths))

class FilterModule(object):

    def filters(self):
        return {
            'path_join': path_join
        }
