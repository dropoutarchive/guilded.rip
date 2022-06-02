import hashlib

class Hashing:

    def stag(username: str):
        data = "%s-%s-eucalyptus" % (username, len(username))
        stag = hashlib.new("md4", data.encode("utf-8")).hexdigest()
        return stag