from .vendor.fastscan import scan


def parse(text):
    return dict(_pairs(scan(text)))


def _pairs(tokens):
    # Taken from https://stackoverflow.com/a/312464 (answer by Ned Batchelder)
    it = iter(tokens)
    return zip(it, it)
