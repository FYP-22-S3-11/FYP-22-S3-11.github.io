from prototypes import list_prototypes


class HashID(object):
    def __init__(self, lprototypes=list_prototypes):
        super(HashID, self).__init__()
        self.prototypes = list(lprototypes)

    def identify_hash(self, phash):
        phash = phash.strip()
        for prototype in self.prototypes:
            if prototype.regex.match(phash):
                for mode in prototype.modes:
                    yield mode
