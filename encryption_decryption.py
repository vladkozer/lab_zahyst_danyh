import cv2
import numpy as np

def lfsr(seed, taps, length):
    state = seed
    seq = []
    for _ in range(length):
        bit = 0
        for t in taps:
            bit ^= (state >> t) & 1
        state = (state >> 1) | (bit << max(taps))
        seq.append(state)
    return seq

BLOCK_SIZE = 32
SEED = 0b10101101
TAPS = [0, 2, 3, 5]

img = cv2.imread("input.jpg")
h, w, _ = img.shape

h -= h % BLOCK_SIZE
w -= w % BLOCK_SIZE
img = img[:h, :w]

blocks = []
positions = []

for y in range(0, h, BLOCK_SIZE):
    for x in range(0, w, BLOCK_SIZE):
        blocks.append(img[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE])
        positions.append((y, x))

seq = lfsr(SEED, TAPS, len(blocks))
perm = np.argsort(seq)

encrypted = np.zeros_like(img)
for i, p in enumerate(perm):
    y, x = positions[i]
    encrypted[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] = blocks[p]

cv2.imwrite("encrypted.png", encrypted)

decrypted = np.zeros_like(img)
inv_perm = np.argsort(perm)

for i, p in enumerate(inv_perm):
    y, x = positions[i]
    decrypted[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] = encrypted[
        positions[p][0]:positions[p][0]+BLOCK_SIZE,
        positions[p][1]:positions[p][1]+BLOCK_SIZE
    ]

cv2.imwrite("decrypted.png", decrypted)

print("Готово! Файли encrypted.png та decrypted.png створені.")
