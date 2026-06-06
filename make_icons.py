import struct, zlib, math, os

def make_png(size):
    def chunk(name, data):
        crc = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', crc)

    cx = cy = size / 2
    arm   = size * 0.36   # crosshair arm half-length
    thick = max(2, size // 48)
    dot_r = max(2, size // 32)
    gap   = size * 0.08   # gap around centre dot

    rows = []
    for y in range(size):
        row = bytearray([0])  # PNG filter byte
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = math.hypot(dx, dy)
            on_h = abs(dy) <= thick and gap < abs(dx) <= arm
            on_v = abs(dx) <= thick and gap < abs(dy) <= arm
            on_dot = dist <= dot_r
            if on_h or on_v or on_dot:
                row += bytes([255, 230, 0, 255])   # yellow, opaque
            else:
                row += bytes([0, 0, 0, 255])        # black, opaque
        rows.append(bytes(row))

    raw = b''.join(rows)
    ihdr_data = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)  # RGBA
    png  = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr_data)
    png += chunk(b'IDAT', zlib.compress(raw, 9))
    png += chunk(b'IEND', b'')
    return png

out = os.path.dirname(os.path.abspath(__file__))
for size in (192, 512):
    path = os.path.join(out, f'icon-{size}.png')
    with open(path, 'wb') as f:
        f.write(make_png(size))
    print(f'created {path}')
