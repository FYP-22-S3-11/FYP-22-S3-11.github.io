"""
import list of possible hash used from prototypes.py
"""
from prototypes import list_prototypes


class HashID(object):
    """
    HashID with configurable prototypes
    """

    def __init__(self, lprototypes=list_prototypes):
        super(HashID, self).__init__()

        # Set self.prototypes to a copy of prototypes to allow modification after instantiation
        self.prototypes = list(lprototypes)

    def identify_hash(self, phash):
        """
        Returns identified HashInfo
        """
        phash = phash.strip()
        for prototype in self.prototypes:
            if prototype.regex.match(phash):
                for mode in prototype.modes:
                    yield mode
