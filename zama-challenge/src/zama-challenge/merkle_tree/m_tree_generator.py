import hashlib
from io import BytesIO

def hash_data(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def calculate_merkle_root(file: BytesIO) -> str:
    file.seek(0)
    block_size = 1024
    blocks = [file.read(block_size) for _ in iter(lambda: file.read(block_size), b'')]
    hashes = [hash_data(block) for block in blocks]
    while len(hashes) > 1:
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        hashes = [hash_data((hashes[i] + hashes[i + 1]).encode()) for i in range(0, len(hashes), 2)]
    return hashes[0] if hashes else ''