##-----------------------------------------------------------------------------
## WadSmoosh Plus - UZDoom 5.x
## Perdition's Gate crates:
##   TEXTURE1 CRATE* emitted as CRATE* AND PGCRATE* (BCRATE*/GCRATE*)
##   textures.hell2pay CRATE* rewritten to HP_CRATE*
##   0CRAT*/0CRTP* come ONLY from patches/Perditions Gate (Xtras, already
##     renamed so they do not clash with Doom / Doom II / HtP texture names)
##   hell2pay.wad and perdgate.wad crate/ICF lumps are never extracted
##   textures.zzz_crates written last
##   BCRATE*/GCRATE* restored from doom2.wad after perdgate extract
##
## Remnants of Earth (jm-e4):
##   After extract, JE4_MAP08 thing type 3115 is rewritten to 32000
##   so decorate.txt CyberMastermind (not ID24 torso 3115) is what spawns.
##   wf_sbar.id1.zs must NEVER replace wf_sbar.zs (duplicate class).
##-----------------------------------------------------------------------------

import os, sys, time, struct, traceback, re
from shutil import copyfile, copy2, rmtree
from zipfile import ZipFile, ZIP_DEFLATED

import omg

VERSION_FILENAME = 'version'
should_extract = True

SRC_WAD_DIR = 'source_wads/'
DATA_DIR = 'data/'
DEST_DIR = 'ipk3/'
DEST_FILENAME = 'wadsmoosh+.ipk3'
LOG_FILENAME = 'wadsmoosh.log'
RES_DIR = 'res/'
DATA_TABLES_FILE = 'wadsmoosh_data.py'
ML_ORDER_FILENAME = 'masterlevels_order_xaser.txt'
ML_MAPINFO_FILENAME = DEST_DIR + 'mapinfo/masterlevels.txt'

XTRAS_PG_PATCHES = os.path.join('patches', 'Perditions Gate')
XTRAS_PG_PATCHES_DIRS = [
    os.path.join('patches', 'Perditions Gate'),
]

RES_FILES = []
WADS = []
REPORT_WADS = []
COMMON_LUMPS = []
DOOM1_LUMPS = []
DOOM2_LUMPS = []
WAD_LUMP_LISTS = {}
WAD_MAP_PREFIXES = {}
MAP_NAME_GRAPHICS_DIRS = []
MASTER_LEVELS_PATCHES = {}
MASTER_LEVELS_SKIES = {}
MASTER_LEVELS_MUSIC = {}
MASTER_LEVELS_MAP07_SPECIAL = []
MASTER_LEVELS_AUTHOR_PREFIX = ''
MASTER_LEVELS_AUTHORS = {}
MASTER_LEVELS_MAPINFO_HEADER = []
SIGIL_ALT_FILENAMES = []
SIGIL2_ALT_FILENAMES = []
BFG_ONLY_LUMP = ''

logfile = None
exec(open(DATA_TABLES_FILE).read())
MASTER_LEVELS_MAP_PREFIX = WAD_MAP_PREFIXES.get('masterlevels', '')
num_maps = 0
num_errors = 0

DATA_MUSIC_LISTS = (
    'music_extras',
    'music_sigil_shreds',
    'music_sigil2_shreds',
    'music_doom3do',
    'music_jm-e4',
)

SKIP_NON_PATCH = {
    'PLAYPAL', 'COLORMAP', 'ENDOOM', 'GENMIDI', 'DMXGUS', 'DMXGUSC',
    'TEXTURE1', 'TEXTURE2', 'PNAMES', 'DEMO1', 'DEMO2', 'DEMO3',
    '_DEUTEX_', 'HELP', 'HELP1', 'HELP2', 'CREDIT', 'TITLEPIC',
    'INTERPIC', 'ENDPIC', 'VICTORY2', 'PFUB1', 'PFUB2',
    'P_START', 'P_END', 'PP_START', 'PP_END',
    'F_START', 'F_END', 'FF_START', 'FF_END',
    'S_START', 'S_END', 'SS_START', 'SS_END',
}

PG_SKIP_EMIT = {
    'SKY1', 'SKY2', 'SKY3', 'RSKY1', 'RSKY2', 'RSKY3',
}

PG_CRATE_RENAME = {
    'CRATE1':   'PGCRATE1',
    'CRATE2':   'PGCRATE2',
    'CRATE3':   'PGCRATE3',
    'CRATELIT': 'PGCRATLT',
    'CRATINY':  'PGCRATIN',
    'CRATWIDE': 'PGCRATWD',
}

HTP_CRATE_RENAME = {
    'CRATE1':   'HP_CRATE1',
    'CRATE2':   'HP_CRATE2',
    'CRATE3':   'HP_CRATE3',
    'CRATELIT': 'HP_CRATLT',
    'CRATINY':  'HP_CRATIN',
    'CRATWIDE': 'HP_CRATWD',
}

VANILLA_CRATE_PATCHES = {
    'BCRATEL1', 'BCRATER1', 'BCRATEM1',
    'GCRATEL1', 'GCRATER1', 'GCRATEM1',
    'SGCRATE2', 'VGCRATE1', 'BCRAT16', 'SMCRATG',
}

# Lost Episodes / Remnants of Earth boss. 3115 collides with ID24.
JE4_OLD_BOSS_EDNUM = 3115
JE4_NEW_BOSS_EDNUM = 32000

XTRAS_PG_DEFS = '''
// Skies + screens only. Crates come from perdgate TEXTURE1 (BCRATE*/GCRATE*).
WallTexture "PG_SKY1", 1024, 128
{
    Patch "PGSKY1A", 0, 0
    Patch "PGSKY1B", 256, 0
    Patch "PGSKY1C", 512, 0
    Patch "PGSKY1D", 768, 0
}
WallTexture "PG_SKY2", 1024, 128
{
    Patch "SKY2N", 0, 0
    Patch "SKY2E", 256, 0
    Patch "SKY2S", 512, 0
    Patch "SKY2W", 768, 0
}
WallTexture "PG_SKY3", 1024, 128
{
    Patch "PG3-1E", 0, 0
    Patch "PG3-2E", 256, 0
    Patch "PG3-3E", 512, 0
    Patch "PG3-4E", 768, 0
}
WallTexture "PLANETPG", 128, 128
{
    Patch "PLANET01", 0, 0
}
WallTexture "BIGSCRN1", 256, 128
{
    Patch "BIGSCRN1", 0, 0
}
WallTexture "BIGSCRN2", 256, 128
{
    Patch "BIGSCRN2", 0, 0
}
'''

ZZZ_CRATE_DEFS = '''
// Last TEXTURES file. Force vanilla/PG UAC crates onto CRATE*.
WallTexture "CRATE1", 64, 128
{
    Patch "BCRATEL1", 0, 0
    Patch "BCRATER1", 32, 0
    Patch "BCRATEL1", 0, 64
    Patch "BCRATER1", 32, 64
}
WallTexture "CRATE2", 64, 128
{
    Patch "GCRATEL1", 0, 0
    Patch "GCRATER1", 32, 0
    Patch "GCRATEL1", 0, 64
    Patch "GCRATER1", 32, 64
}
WallTexture "CRATE3", 64, 128
{
    Patch "GCRATEL1", 0, 0
    Patch "GCRATER1", 32, 0
    Patch "BCRATEL1", 0, 64
    Patch "BCRATER1", 32, 64
}
WallTexture "CRATELIT", 64, 128
{
    Patch "SGCRATE2", 0, 0
    Patch "SGCRATE2", 32, 0
    Patch "BCRATEL1", 0, 64
    Patch "BCRATER1", 32, 64
}
WallTexture "CRATINY", 64, 16
{
    Patch "VGCRATE1", 0, 0
    Patch "VGCRATE1", 16, 0
    Patch "VGCRATE1", 32, 0
    Patch "VGCRATE1", 48, 0
}
WallTexture "PGCRATE1", 64, 128
{
    Patch "BCRATEL1", 0, 0
    Patch "BCRATER1", 32, 0
    Patch "BCRATEL1", 0, 64
    Patch "BCRATER1", 32, 64
}
WallTexture "PGCRATE2", 64, 128
{
    Patch "GCRATEL1", 0, 0
    Patch "GCRATER1", 32, 0
    Patch "GCRATEL1", 0, 64
    Patch "GCRATER1", 32, 64
}
WallTexture "PGCRATE3", 64, 128
{
    Patch "GCRATEL1", 0, 0
    Patch "GCRATER1", 32, 0
    Patch "BCRATEL1", 0, 64
    Patch "BCRATER1", 32, 64
}
WallTexture "PGCRATLT", 64, 128
{
    Patch "SGCRATE2", 0, 0
    Patch "SGCRATE2", 32, 0
    Patch "BCRATEL1", 0, 64
    Patch "BCRATER1", 32, 64
}
WallTexture "PGCRATIN", 64, 16
{
    Patch "VGCRATE1", 0, 0
    Patch "VGCRATE1", 16, 0
    Patch "VGCRATE1", 32, 0
    Patch "VGCRATE1", 48, 0
}
'''


def logg(line, error=False):
    global logfile, num_errors
    if not logfile:
        logfile = open(LOG_FILENAME, 'w')
    print(line)
    logfile.write(line + '\n')
    if error:
        num_errors += 1


def is_htp_crate_patch(key):
    k = key.upper()
    return k.startswith('0CRAT') or k.startswith('0CRTP')


def is_crate_or_icf_patch(key):
    """Vanilla UAC crate patches + the renamed Xtras/ICF 0CRAT*/0CRTP* set."""
    k = key.upper()
    return k in VANILLA_CRATE_PATCHES or is_htp_crate_patch(k)


def skip_wad_crate_lump(wad_name, lump_name):
    """Crate/ICF patches must not be taken from hell2pay.wad or perdgate.wad.

    hell2pay.wad used to overwrite Perdition's Gate crate graphics whenever
    both IWADs were present. Those patches now live in
    patches/Perditions Gate (already renamed 0CRAT*/0CRTP*).
    BCRATE*/GCRATE* are restored from doom2.wad at the end of the build.
    """
    if wad_name not in ('hell2pay', 'perdgate'):
        return False
    return is_crate_or_icf_patch(lump_name)


def get_wad_filename(wad_name):
    wad_name += '.wad'
    for filename in os.listdir(SRC_WAD_DIR):
        if wad_name.lower() == filename.lower():
            return SRC_WAD_DIR + filename
    return None


def read_wad_directory(path):
    lumps = []
    with open(path, 'rb') as f:
        ident = f.read(4)
        if ident not in (b'IWAD', b'PWAD'):
            logg('Not a WAD: %s ident=%r' % (path, ident), error=True)
            return lumps
        num, infotableofs = struct.unpack('<ii', f.read(8))
        f.seek(infotableofs)
        for _ in range(num):
            pos, size = struct.unpack('<ii', f.read(8))
            raw = f.read(8)
            name = raw.split(b'\0')[0].decode('ascii', 'replace').upper()
            lumps.append((name, pos, size))
    return lumps


def read_wad_lump(path, offset, size):
    with open(path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def read_pnames(data):
    if not data or len(data) < 4:
        return []
    n = struct.unpack_from('<i', data, 0)[0]
    names = []
    for i in range(max(0, n)):
        off = 4 + i * 8
        if off + 8 > len(data):
            break
        raw = data[off:off + 8]
        names.append(raw.split(b'\0')[0].decode('ascii', 'replace').upper())
    return names


def read_texturex(data, pnames):
    if not data or len(data) < 4:
        return []
    n = struct.unpack_from('<i', data, 0)[0]
    textures = []
    for i in range(max(0, n)):
        if 4 + i * 4 + 4 > len(data):
            break
        off = struct.unpack_from('<i', data, 4 + i * 4)[0]
        if off < 0 or off + 22 > len(data):
            continue
        name = data[off:off + 8].split(b'\0')[0].decode('ascii', 'replace').upper()
        width, height = struct.unpack_from('<hh', data, off + 12)
        pcount = struct.unpack_from('<h', data, off + 20)[0]
        patches = []
        p = off + 22
        for _ in range(max(0, pcount)):
            if p + 10 > len(data):
                break
            x, y, pidx = struct.unpack_from('<hhh', data, p)
            p += 10
            pname = pnames[pidx] if 0 <= pidx < len(pnames) else 'UNKNOWN'
            patches.append((pname, x, y))
        textures.append((name, width, height, patches))
    return textures


def sanitize_hell2pay_textures():
    path = os.path.join(DEST_DIR, 'textures.hell2pay')
    if not os.path.isfile(path):
        return
    text = open(path, 'r', newline='').read()
    changed = 0
    for old, new in HTP_CRATE_RENAME.items():
        pattern = r'(WallTexture|Texture)\s+"%s"' % re.escape(old)
        text, n = re.subn(pattern, r'\1 "%s"' % new, text, flags=re.IGNORECASE)
        changed += n
    with open(path, 'w', newline='\n') as out:
        out.write(text)
    logg('Rewrote %s CRATE* names in textures.hell2pay -> HP_CRATE*' % changed)


def write_zzz_crates():
    dest = os.path.join(DEST_DIR, 'textures.zzz_crates')
    with open(dest, 'w', newline='\n') as out:
        out.write(ZZZ_CRATE_DEFS)
    logg('Wrote %s (forced BCRATE*/GCRATE* onto CRATE*)' % dest)


def restore_doom2_crate_patches():
    wad_path = get_wad_filename('doom2') or get_wad_filename('tnt')
    if not wad_path:
        logg('No doom2/tnt WAD; cannot restore vanilla crate patches', error=True)
        return
    dest_dir = os.path.join(DEST_DIR, 'patches')
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    lumps = read_wad_directory(wad_path)
    by_name = {name: (pos, size) for name, pos, size in lumps}
    restored = []
    for name in sorted(VANILLA_CRATE_PATCHES):
        if name not in by_name:
            continue
        pos, size = by_name[name]
        if size <= 0:
            continue
        data = read_wad_lump(wad_path, pos, size)
        with open(os.path.join(dest_dir, name + '.lmp'), 'wb') as out:
            out.write(data)
        restored.append(name)
    logg('Restored %s Doom II crate patches: %s' % (len(restored), ', '.join(restored)))


def generate_perdgate_textures():
    wad_path = get_wad_filename('perdgate')
    if not wad_path:
        write_zzz_crates()
        restore_doom2_crate_patches()
        return
    lumps = read_wad_directory(wad_path)
    by_name = {}
    for name, pos, size in lumps:
        by_name[name] = (pos, size)
    logg('perdgate.wad lumps: %s (TEXTURE1=%s PNAMES=%s)' % (
        len(lumps),
        'yes' if 'TEXTURE1' in by_name else 'NO',
        'yes' if 'PNAMES' in by_name else 'NO'))
    if 'PNAMES' not in by_name or 'TEXTURE1' not in by_name:
        logg('perdgate.wad has no TEXTURE1/PNAMES in the lump directory', error=True)
        write_zzz_crates()
        restore_doom2_crate_patches()
        return
    pnames = read_pnames(read_wad_lump(wad_path, *by_name['PNAMES']))
    textures = read_texturex(read_wad_lump(wad_path, *by_name['TEXTURE1']), pnames)
    if 'TEXTURE2' in by_name:
        textures += read_texturex(read_wad_lump(wad_path, *by_name['TEXTURE2']), pnames)
    dest_dir = DEST_DIR + 'patches/'
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    in_patches = False
    written = 0
    skipped_crates = 0
    for name, pos, size in lumps:
        if name in ('P_START', 'PP_START'):
            in_patches = True
            continue
        if name in ('P_END', 'PP_END'):
            in_patches = False
            continue
        if not in_patches:
            continue
        if name in SKIP_NON_PATCH or size <= 0:
            continue
        if is_crate_or_icf_patch(name):
            skipped_crates += 1
            continue
        data = read_wad_lump(wad_path, pos, size)
        with open(os.path.join(dest_dir, name + '.lmp'), 'wb') as out:
            out.write(data)
        written += 1
    if written == 0:
        wanted = set(pnames)
        for name, pos, size in lumps:
            if name not in wanted or name in SKIP_NON_PATCH or size <= 0:
                continue
            if is_crate_or_icf_patch(name):
                skipped_crates += 1
                continue
            data = read_wad_lump(wad_path, pos, size)
            with open(os.path.join(dest_dir, name + '.lmp'), 'wb') as out:
                out.write(data)
            written += 1
        logg('No P_START found; extracted %s lumps named in PNAMES' % written)
    else:
        logg('Extracted %s patches from P_START..P_END (skipped %s crate/ICF)' % (
            written, skipped_crates))
    lines = [
        '// Generated from perdgate.wad TEXTURE1/PNAMES',
        '// CRATE* emitted as CRATE* and PGCRATE* (BCRATE*/GCRATE* UAC panels)',
        '// SKY*/RSKY* omitted so PG_SKY* below win',
        '',
    ]
    emitted = 0
    skipped_simple = 0
    skipped_conflict = 0
    crates_emitted = 0
    for name, width, height, patches in textures:
        if not name or name.startswith('-'):
            continue
        key = name.upper()
        if key in PG_SKIP_EMIT:
            skipped_conflict += 1
            continue
        out_name = PG_CRATE_RENAME.get(key, name)
        is_crate = key in PG_CRATE_RENAME
        simple = (
            not is_crate and
            len(patches) == 1 and
            patches[0][0].upper() == name.upper() and
            patches[0][1] == 0 and
            patches[0][2] == 0
        )
        if simple:
            skipped_simple += 1
            continue
        names_to_write = [out_name]
        if is_crate and out_name != name:
            names_to_write.append(name)
        for write_name in names_to_write:
            lines.append('WallTexture "%s", %s, %s' % (write_name, width, height))
            lines.append('{')
            for pname, x, y in patches:
                lines.append('    Patch "%s", %s, %s' % (pname, x, y))
            lines.append('}')
            lines.append('')
            emitted += 1
        if is_crate:
            crates_emitted += 1
            logg('  PG crate %s -> %s and %s (%s patches: %s)' % (
                key, out_name, name, len(patches),
                ', '.join('%s@%s,%s' % (p, x, y) for p, x, y in patches)))
    dest = os.path.join(DEST_DIR, 'textures.zz_perdgate')
    with open(dest, 'w', newline='\n') as out:
        out.write('\n'.join(lines))
        out.write('\n')
        out.write(XTRAS_PG_DEFS)
    stub = os.path.join(DEST_DIR, 'textures.perdgate')
    if os.path.isfile(stub):
        logg('Kept textures.perdgate (Xtras).')
    logg('Wrote %s (%s composites, %s 1:1 skipped, %s sky skipped, %s TEXTURE1 crates, %s pnames)' % (
        dest, emitted, skipped_simple, skipped_conflict, crates_emitted, len(pnames)))
    write_zzz_crates()
    restore_doom2_crate_patches()


def extract_pg_flats():
    wad_path = get_wad_filename('perdgate')
    if not wad_path:
        return
    dest_dir = os.path.join(DEST_DIR, 'flats')
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    lumps = read_wad_directory(wad_path)
    in_flats = False
    written = 0
    names = []
    for name, pos, size in lumps:
        if name in ('F_START', 'FF_START'):
            in_flats = True
            continue
        if name in ('F_END', 'FF_END'):
            in_flats = False
            continue
        if not in_flats or name in SKIP_NON_PATCH or size <= 0:
            continue
        data = read_wad_lump(wad_path, pos, size)
        with open(os.path.join(dest_dir, name + '.lmp'), 'wb') as out:
            out.write(data)
        written += 1
        names.append(name)
    logg('Extracted %s PG flats from F_START..F_END' % written)
    if 'METFLOR1' in names:
        logg('  METFLOR1 written to flats/')
    else:
        logg('  METFLOR1 not found between F_START and F_END', error=True)
        logg('  PG flats: %s' % ', '.join(names))


def log_pg_map01_textures():
    path = os.path.join(DEST_DIR, 'maps', 'PG_MAP01.wad')
    if not os.path.isfile(path):
        logg('PG_MAP01.wad not found; cannot list sidedefs')
        return
    wad = omg.WAD()
    wad.from_file(path)
    map_names = wad.maps.find('*')
    if not map_names:
        logg('PG_MAP01.wad has no maps')
        return
    ed = omg.MapEditor(wad.maps[map_names[0]])
    names = set()
    for s in ed.sidedefs:
        for key in ('tx_mid', 'tx_up', 'tx_low'):
            n = (getattr(s, key, None) or '').strip()
            if n and n != '-':
                names.add(n.upper())
    logg('PG_MAP01 sidedef textures (%s): %s' % (
        len(names), ', '.join(sorted(names))))


def _u16(buf, off):
    return buf[off] | (buf[off + 1] << 8)


def _set_u16(buf, off, val):
    buf[off] = val & 0xFF
    buf[off + 1] = (val >> 8) & 0xFF


def patch_things_bytes(data, old_type, new_type):
    """Rewrite thing types in a raw THINGS lump (Doom 10-byte or Hexen 20-byte)."""
    if not data:
        return data, 0
    buf = bytearray(data)
    n = len(buf)
    changed = 0

    hexen_hits = 0
    doom_hits = 0
    if n >= 20 and n % 20 == 0:
        for i in range(0, n, 20):
            if _u16(buf, i + 10) == old_type:
                hexen_hits += 1
    if n >= 10 and n % 10 == 0:
        for i in range(0, n, 10):
            if _u16(buf, i + 6) == old_type:
                doom_hits += 1

    if hexen_hits and hexen_hits >= doom_hits:
        for i in range(0, n, 20):
            if _u16(buf, i + 10) == old_type:
                _set_u16(buf, i + 10, new_type)
                changed += 1
        return bytes(buf), changed

    if doom_hits:
        for i in range(0, n, 10):
            if _u16(buf, i + 6) == old_type:
                _set_u16(buf, i + 6, new_type)
                changed += 1
    return bytes(buf), changed


def patch_udmf_textmap(text, old_type, new_type):
    """Rewrite thing { type = 3115; } in a UDMF TEXTMAP."""
    if not text:
        return text, 0

    def repl(match):
        return match.group(1) + str(new_type) + match.group(3)

    new_text, n = re.subn(
        r'(type\s*=\s*)%s(\s*;)' % old_type,
        repl,
        text,
        flags=re.IGNORECASE)
    return new_text, n


def patch_map_ednums(wad_path, old_type, new_type):
    """Patch one map WAD. Tries MapEditor, UMapEditor, then raw THINGS/TEXTMAP."""
    wad = omg.WAD()
    wad.from_file(wad_path)
    map_names = wad.maps.find('*')
    if not map_names:
        return 0
    total = 0
    dirty = False

    for map_name in map_names:
        group = wad.maps[map_name]

        # UDMF
        textmap = None
        for key in group.keys():
            if key.upper() == 'TEXTMAP':
                textmap = group[key]
                break
        if textmap is not None:
            raw = textmap.data
            if isinstance(raw, bytes):
                src = raw.decode('utf-8', 'replace')
            else:
                src = raw
            new_src, n = patch_udmf_textmap(src, old_type, new_type)
            if n:
                textmap.data = new_src.encode('utf-8')
                total += n
                dirty = True
            continue

        # Binary via omg MapEditor (handles Doom + Hexen thing structs)
        try:
            ed = omg.MapEditor(group)
            n = 0
            for thing in ed.things:
                if int(getattr(thing, 'type', 0)) == old_type:
                    thing.type = new_type
                    n += 1
            if n:
                wad.maps[map_name] = ed.to_lumps()
                total += n
                dirty = True
                continue
        except Exception:
            pass

        # Raw THINGS fallback
        things_key = None
        for key in group.keys():
            if key.upper() == 'THINGS':
                things_key = key
                break
        if things_key is None:
            continue
        new_data, n = patch_things_bytes(group[things_key].data, old_type, new_type)
        if n:
            group[things_key].data = new_data
            total += n
            dirty = True

    if dirty:
        wad.to_file(wad_path)
    return total


def patch_je4_boss_things():
    """JM-E4 Icon of Ruin still places the boss as ednum 3115.

    decorate.txt CyberMastermind is 32000 (3115 is an ID24 body).
    wadsmoosh_data.py documented this rewrite; the extractor never did it.
    """
    maps_dir = os.path.join(DEST_DIR, 'maps')
    if not os.path.isdir(maps_dir):
        return
    patched_maps = 0
    patched_things = 0
    for name in sorted(os.listdir(maps_dir)):
        if not name.upper().startswith('JE4_'):
            continue
        if not name.lower().endswith('.wad'):
            continue
        path = os.path.join(maps_dir, name)
        try:
            n = patch_map_ednums(path, JE4_OLD_BOSS_EDNUM, JE4_NEW_BOSS_EDNUM)
        except Exception as ex:
            logg('  JE4 boss patch failed on %s: %s' % (name, ex), error=True)
            continue
        if n:
            patched_maps += 1
            patched_things += n
            logg('  %s: %s thing(s) %s -> %s (CyberMastermind)' % (
                name, n, JE4_OLD_BOSS_EDNUM, JE4_NEW_BOSS_EDNUM))
    if patched_maps:
        logg('JE4 boss rewrite: %s map(s), %s thing(s)' % (patched_maps, patched_things))
    elif get_wad_filename('jm-e4'):
        logg('JE4 boss rewrite: no thing type %s found (already 32000, or map uses a Spider Mastermind 7)' %
             JE4_OLD_BOSS_EDNUM)


def copy_extra_pg_loose_patches():
    """Copy Xtras Perdition's Gate patches, including renamed 0CRAT*/0CRTP*.

    Those ICF crate patches are the only crate graphics that should come
    from the Xtras tree. Vanilla BCRATE*/GCRATE* stay Doom II (restored
    later). hell2pay.wad is never allowed to supply these names.
    """
    dest_dir = os.path.join(DEST_DIR, 'patches')
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    copied = 0
    skipped_vanilla = 0
    copied_icf = 0
    found_dir = False
    for src_dir in XTRAS_PG_PATCHES_DIRS:
        if not os.path.isdir(src_dir):
            continue
        found_dir = True
        n = 0
        icf_n = 0
        for name in os.listdir(src_dir):
            src = os.path.join(src_dir, name)
            if not os.path.isfile(src):
                continue
            key = os.path.splitext(name)[0].upper()
            if key in SKIP_NON_PATCH:
                continue
            # Keep Doom II UAC crate patches authoritative.
            if key in VANILLA_CRATE_PATCHES:
                skipped_vanilla += 1
                continue
            ext = os.path.splitext(name)[1]
            dest_name = (key + '.lmp') if not ext else (key + ext)
            copy2(src, os.path.join(dest_dir, dest_name))
            copied += 1
            n += 1
            if is_htp_crate_patch(key):
                icf_n += 1
                copied_icf += 1
        logg('Copied %s PG xtras patches from %s (%s ICF 0CRAT*/0CRTP*, skipped %s vanilla BCRATE*/GCRATE*)' % (
            n, src_dir, icf_n, skipped_vanilla))
    if not found_dir:
        logg('No extra PG patches at %s' % XTRAS_PG_PATCHES)
        return
    logg('Copied %s Xtras PG patches total (%s ICF crate patches)' % (copied, copied_icf))


def get_master_levels_map_order():
    order = []
    if len(sys.argv) > 1:
        order_file = ' '.join(sys.argv[1:])
        if not os.path.exists(order_file):
            order_file = ML_ORDER_FILENAME
    else:
        order_file = ML_ORDER_FILENAME
    if not os.path.exists(order_file):
        return order_file, []
    logg('Using Master Levels ordering from %s' % order_file)
    for line in open(order_file).readlines():
        line = line.strip().lower()
        if line.startswith('//') or line == '':
            continue
        if line not in MASTER_LEVELS_MUSIC:
            logg('ERROR: Unrecognized Master Level %s' % line, error=True)
            continue
        order.append(line)
    return order_file, order


def get_ml_mapinfo(wad_name, map_number):
    lines = []
    prefix = MASTER_LEVELS_MAP_PREFIX.upper()
    mapnum = str(map_number).rjust(2, '0')
    nextnum = str(map_number + 1).rjust(2, '0')
    lines.append('map %sMAP%s lookup "%s%s"' % (prefix, mapnum, prefix, wad_name.upper()))
    lines.append('{')
    next_map = '%sMAP%s' % (prefix, nextnum) if map_number < 20 else 'EndGameC'
    sky = MASTER_LEVELS_SKIES.get(wad_name, None) or 'RSKY1'
    music = MASTER_LEVELS_MUSIC[wad_name]
    author_lc = '%s_%s' % (MASTER_LEVELS_AUTHOR_PREFIX, MASTER_LEVELS_AUTHORS[wad_name])
    lines.append('    next = "%s"' % next_map)
    if wad_name == 'teeth':
        lines.append('    secretnext = "ML_MAP21"')
    lines.append('    sky1 = "%s"' % sky)
    lines.append('    music = "$MUSIC_%s"' % music)
    lines.append('    Author = "$%s"' % author_lc)
    if wad_name in MASTER_LEVELS_MAP07_SPECIAL:
        lines.append('    map07special')
    if map_number != 21:
        lines.append('    ResetHealth')
        lines.append('    ResetInventory')
    lines.append('}')
    return lines


def extract_master_levels():
    order_file, ml_map_order = get_master_levels_map_order()
    if len(ml_map_order) == 0:
        return
    if not get_wad_filename(ml_map_order[0]):
        logg('ERROR: Master Levels not found.', error=True)
        return
    logg('Processing Master Levels...')
    mapinfo = open(ML_MAPINFO_FILENAME, 'w')
    mapinfo.write(MASTER_LEVELS_MAPINFO_HEADER % order_file)
    for i, wad_name in enumerate(ml_map_order):
        wad_filename = get_wad_filename(wad_name)
        if not wad_filename:
            logg("ERROR: Couldn't find %s" % wad_name, error=True)
            continue
        in_wad = omg.WAD()
        in_wad.from_file(wad_filename)
        out_wad_filename = DEST_DIR + 'maps/' + MASTER_LEVELS_MAP_PREFIX + 'map'
        out_wad_filename += str(i + 1).rjust(2, '0') + '.wad'
        logg('  Extracting %s to %s' % (wad_filename, out_wad_filename))
        extract_map(in_wad, in_wad.maps.find('*')[0], out_wad_filename)
        mapinfo.writelines('\n'.join(get_ml_mapinfo(wad_name, i + 1)))
        mapinfo.write('\n\n')
    wad_filename = get_wad_filename('teeth')
    if wad_filename:
        out_wad_filename = DEST_DIR + 'maps/' + MASTER_LEVELS_MAP_PREFIX + 'map21' + '.wad'
        logg('  Extracting %s map32 to %s' % (wad_filename, out_wad_filename))
        in_wad = omg.WAD()
        in_wad.from_file(wad_filename)
        extract_map(in_wad, in_wad.maps.find('*')[1], out_wad_filename)
        if ml_map_order.index('teeth') == 19:
            next_map = 'EndGameC'
        else:
            next_map = '%sMAP%s' % (MASTER_LEVELS_MAP_PREFIX.upper(),
                                    ml_map_order.index('teeth') + 2)
        mapinfo.write(MASTER_LEVELS_SECRET_DEF % (next_map, MASTER_LEVELS_MUSIC['teeth2'],
                                                  MASTER_LEVELS_AUTHOR_PREFIX, MASTER_LEVELS_AUTHORS['teeth2']))
    mapinfo.writelines([MASTER_LEVELS_CLUSTER_DEF])
    mapinfo.close()
    for wad_name, patch_replace in MASTER_LEVELS_PATCHES.items():
        wad = omg.WAD()
        wad.from_file(get_wad_filename(wad_name))
        lump = wad.data[patch_replace[0]] if patch_replace[0] in wad.data else wad.patches[patch_replace[0]]
        out_filename = DEST_DIR + 'patches/' + patch_replace[1] + '.lmp'
        logg('  Extracting %s lump from %s as %s' % (patch_replace[0], wad_name, patch_replace[1]))
        lump.to_file(out_filename)


def add_secret_level(map_src_filename, map_src_name, map_dest_name):
    global num_maps
    dest_filename = DEST_DIR + 'maps/%s.wad' % map_dest_name
    copyfile(get_wad_filename(map_src_filename), dest_filename)
    wad = omg.WAD()
    wad.from_file(dest_filename)
    wad.maps.rename(map_src_name, map_dest_name)
    wad.to_file(dest_filename)
    num_maps += 1


def add_xbox_levels():
    logg('Adding Xbox bonus levels...')
    if get_wad_filename('doom'):
        add_secret_level('sewers', 'E3M1', 'E1M10')
    if get_wad_filename('doom2'):
        add_secret_level('betray', 'MAP01', 'MAP33')


def extract_map(in_wad, map_name, out_filename):
    global num_maps
    out_wad = omg.WAD()
    out_wad.maps[map_name] = in_wad.maps[map_name]
    out_wad.to_file(out_filename)
    num_maps += 1


def extract_iwad_maps(wad_name, map_prefix):
    in_wad = omg.WAD()
    in_wad.from_file(get_wad_filename(wad_name))
    for map_name in in_wad.maps.find('*'):
        logg('  Extracting map %s...' % map_name)
        extract_map(in_wad, map_name, DEST_DIR + 'maps/' + map_prefix + map_name + '.wad')


def find_lump_table(wad, lump_name):
    for table_name in ('music', 'data', 'graphics', 'patches', 'sounds', 'sprites', 'flats'):
        table = getattr(wad, table_name, None)
        if table and lump_name in table:
            return table, lump_name
    upper = lump_name.upper()
    base = os.path.splitext(lump_name)[0]
    for table_name in ('music', 'data', 'graphics', 'patches', 'sounds', 'sprites', 'flats'):
        table = getattr(wad, table_name, None)
        if not table:
            continue
        for key in table.keys():
            if key.upper() == upper or key.upper() == base.upper():
                return table, key
    return None, lump_name


def extract_lumps(wad_name):
    if wad_name not in WAD_LUMP_LISTS:
        return
    wad = omg.WAD()
    wad.from_file(get_wad_filename(wad_name))
    for lump_list in WAD_LUMP_LISTS[wad_name]:
        try:
            lump_type = lump_list[:lump_list.index('_')]
        except ValueError:
            logg("ERROR: Couldn't identify type of lump list %s" % lump_list, error=True)
            continue
        data_music = lump_list in DATA_MUSIC_LISTS or lump_list.startswith('music_extras')
        if lump_list == 'patches_sigil':
            lump_type = 'data'
        if data_music:
            lump_table = wad.data
            lump_type_out = 'music'
            lump_subdir = DEST_DIR + 'music/'
        else:
            lump_table = getattr(wad, lump_type, None)
            lump_type_out = lump_type
            if wad_name == 'sigil' and lump_list == 'patches_sigil':
                lump_subdir = DEST_DIR + 'patches/'
            elif wad_name in ('sigil', 'sigil2') and lump_type == 'data':
                lump_subdir = DEST_DIR + 'graphics/'
            elif lump_type in ['data', 'txdefs']:
                lump_subdir = DEST_DIR
            else:
                lump_subdir = DEST_DIR + lump_type + '/'
        if lump_table is None:
            logg('  skip missing type %s' % lump_type)
            continue
        if not os.path.exists(lump_subdir):
            os.makedirs(lump_subdir)
        logg('  extracting %s...' % lump_list)
        list_path = DATA_DIR + lump_list
        if not os.path.isfile(list_path):
            logg('  skip missing list %s' % list_path)
            continue
        for line in open(list_path).readlines():
            line = line.strip()
            if line.startswith('//') or line == '':
                continue
            if ':' in line:
                lump_name, out_filename = [p.strip() for p in line.split(':', 1)]
            else:
                lump_name = out_filename = line
            if skip_wad_crate_lump(wad_name, lump_name):
                logg('    skip crate/ICF lump %s from %s (Xtras/doom2 own these)' % (
                    lump_name, wad_name))
                continue
            table, real_name = find_lump_table(wad, lump_name)
            if table is None:
                logg('  skip missing lump %s' % lump_name)
                continue
            lump = table[real_name]
            base, ext = os.path.splitext(out_filename)
            if data_music:
                if ext == '':
                    out_filename = base
            elif lump_type_out == 'music':
                if ext == '':
                    out_filename = base + '.mus'
            else:
                if ext == '':
                    out_filename = base + '.lmp'
            logg('    Extracting %s' % (lump_subdir + out_filename))
            lump.to_file(lump_subdir + out_filename)


def copy_resources():
    for src_file in RES_FILES:
        src_path = RES_DIR + src_file
        if not os.path.isfile(src_path):
            logg('skip missing res file %s' % src_file)
            continue
        if src_file.startswith('textures.doom1') and not get_wad_filename('doom'):
            continue
        elif src_file == 'textures.doom2' and not get_wad_filename('doom2'):
            if not get_wad_filename('tnt'):
                continue
        elif src_file == 'textures.tnt' and not get_wad_filename('tnt'):
            continue
        elif src_file == 'textures.plut' and not get_wad_filename('plutonia'):
            continue
        elif src_file == 'textures.perdgate' and not get_wad_filename('perdgate'):
            continue
        elif src_file == 'textures.hell2pay' and not get_wad_filename('hell2pay'):
            continue
        elif src_file == 'textures.neis' and not get_wad_filename('neis'):
            continue
        elif src_file == 'textures.tntr' and not get_wad_filename('tnt'):
            continue
        elif src_file == 'textures.pl2' and not get_wad_filename('plutonia'):
            continue
        dest_path = DEST_DIR + src_file
        dest_dir = os.path.dirname(dest_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        logg('Copying %s' % src_file)
        copyfile(src_path, dest_path)
    d2_wad_filename = get_wad_filename('doom2')
    if not d2_wad_filename:
        copyfile(RES_DIR + 'mapinfo/doom2_nonbfg_levels.txt',
                 DEST_DIR + 'mapinfo/doom2_secret_levels.txt')
        copyfile(RES_DIR + 'iwadinfo.txt', DEST_DIR + 'iwadinfo.txt')
        return
    d2wad = omg.WAD()
    d2wad.from_file(d2_wad_filename)
    if d2wad.graphics.get(BFG_ONLY_LUMP, None):
        copyfile(RES_DIR + 'mapinfo/doom2_bfg_levels.txt',
                 DEST_DIR + 'mapinfo/doom2_secret_levels.txt')
    else:
        copyfile(RES_DIR + 'mapinfo/doom2_nonbfg_levels.txt',
                 DEST_DIR + 'mapinfo/doom2_secret_levels.txt')
    copyfile(RES_DIR + 'iwadinfo.txt', DEST_DIR + 'iwadinfo.txt')


def copy_resources_id1():
    """LoR extras. Do NOT replace wf_sbar.zs with wf_sbar.id1.zs.

    KidGamer77 wf_sbar.zs already defines WadFusionStatusBar and the Id24
    alias. Overwriting it with wf_sbar.id1.zs double-defines those classes
    and breaks the HUD / Super Shotgun layout on UZDoom 5.
    """
    logg('Copying id1 resources...')
    weap_src = RES_DIR + 'zscript/wf_id1weap.zs'
    weap_dest = DEST_DIR + 'zscript/wf_id1weap.zs'
    if os.path.isfile(weap_src) and not os.path.isfile(weap_dest):
        copyfile(weap_src, weap_dest)

    zscript_path = DEST_DIR + 'zscript.txt'
    if os.path.isfile(zscript_path):
        with open(zscript_path, 'r') as file:
            tmp_file = file.read()
        tmp_file = tmp_file.replace(
            '//#include "zscript/wf_id1weap.zs"',
            '#include "zscript/wf_id1weap.zs"')
        if '#include "zscript/wf_id1weap.zs"' not in tmp_file:
            tmp_file += '\n#include "zscript/wf_id1weap.zs"\n'
        # Keep the unified status bar. Never pull in wf_sbar.id1.zs.
        tmp_file = tmp_file.replace('#include "zscript/wf_sbar.id1.zs"',
                                    '//#include "zscript/wf_sbar.id1.zs"')
        tmp_file = tmp_file.replace('#include "zscript/wf_sigil2boss.zs"',
                                    '//#include "zscript/wf_sigil2boss.zs"')
        with open(zscript_path, 'w') as file:
            file.write(tmp_file)

    mapinfo_path = DEST_DIR + 'mapinfo.txt'
    if os.path.isfile(mapinfo_path):
        with open(mapinfo_path, 'r') as file:
            tmp_file = file.read()
        # Do not force StatusBarClass = WadFusionStatusBarId24.
        # res/mapinfo.txt already sets WadFusionStatusBar + Id1WeaponHandler.
        if 'Id1WeaponHandler' not in tmp_file:
            tmp_file = tmp_file.replace(
                'AddEventHandlers = "WadSmooshHandler", "WadFusionHandler", "WadFusionMusicHandler"',
                'AddEventHandlers = "WadFusionHandler", "WadFusionMusicHandler", "Id1WeaponHandler"')
        with open(mapinfo_path, 'w') as file:
            file.write(tmp_file)

    if not get_wad_filename('doom'):
        for src, dest in (
            ('SKYE1.lmp', 'SKY1.lmp'),
            ('SKYE2.lmp', 'SKY2.lmp'),
            ('SKYE3.lmp', 'SKY3.lmp'),
            ('SKYE4.lmp', 'SKY4.lmp'),
        ):
            src_path = DEST_DIR + 'patches/' + src
            if os.path.isfile(src_path):
                copyfile(src_path, DEST_DIR + 'patches/' + dest)


def get_report_found():
    found = []
    for wadname in REPORT_WADS:
        if get_wad_filename(wadname):
            found.append(wadname)
    if 'doom' in found and 'sigil' not in found:
        for alt_name in SIGIL_ALT_FILENAMES:
            sigil_alt = get_wad_filename(alt_name)
            if sigil_alt:
                copyfile(sigil_alt, SRC_WAD_DIR + 'sigil.wad')
                found.insert(1, 'sigil')
                break
    if 'doom' in found and 'sigil2' not in found:
        for alt_name in SIGIL2_ALT_FILENAMES:
            sigil2_alt = get_wad_filename(alt_name)
            if sigil2_alt:
                copyfile(sigil2_alt, SRC_WAD_DIR + 'sigil2.wad')
                found.insert(2, 'sigil2')
                break
    return found


def get_eps(wads_found):
    found = set(wads_found)
    eps = []

    if 'doom' in found:
        eps += [
            'Knee-Deep in the Dead',
            'The Shores of Hell',
            'Inferno',
            'Thy Flesh Consumed',
        ]
    if 'sigil' in found and 'doom' in found:
        eps += ['Sigil']
    if 'sigil2' in found and 'doom' in found:
        eps += ['Sigil II']
    if 'doom2' in found:
        eps += ['Hell On Earth']
    if 'nerve' in found and 'doom2' in found:
        eps += ['No Rest for the Living']
    if 'attack' in found and 'doom2' in found:
        eps += ['The Master Levels']
    if 'tnt' in found:
        eps += ['TNT: Evilution']
    if 'tnt2_beta6' in found:
        eps += ['TNT: Devilution']
    if 'tntr' in found and 'tnt' in found:
        eps += ['TNT: Revilution']
    if 'plutonia' in found:
        eps += ['The Plutonia Experiment']
    if 'pl2' in found and 'plutonia' in found:
        eps += ['Plutonia 2']
    if 'prcp' in found and 'plutonia' in found:
        eps += ['Plutonia Revisited']
    if 'doomzero' in found:
        eps += ['Doom Zero']
    if 'id1' in found and 'doom2' in found and 'id1-res' in found and 'id24res' in found:
        eps += ['The Vulcan Abyss', 'Counterfeit Eden']
    if 'hell2pay' in found and 'doom2' in found:
        eps += ['Hell To Pay']
    if 'perdgate' in found and 'doom2' in found:
        eps += ["Perdition's Gate"]
    if 'neis' in found and 'doom' in found:
        eps += [
            '1994 Ways To Die',
            'The Depths of Doom',
            'Woe',
            'Blood Stained Earth',
        ]
    if 'jptr_v40' in found and 'doom' in found:
        eps += [
            'Massacre on Callisto',
            'The Killing Fields of Io',
            "Hell's Gate - The Red Spot of Jupiter",
        ]
    if 'jm-e4' in found and 'doom' in found:
        eps += ['Remnants of Earth']
    if 'freedoom1' in found and 'doom' in found:
        eps += [
            'Outpost Outbreak',
            'Military Labs',
            'Event Horizon',
            'Double Impact',
        ]
    if 'freedoom2' in found and 'doom2' in found:
        eps += ['Destination: Earth']
    return eps


def main():
    start_time = time.time()
    version = open(VERSION_FILENAME).readlines()[0].strip()
    logg('WadSmoosh v%s\n%s' % (version, '-' * 20))
    found = get_report_found()
    input_func = raw_input if sys.version_info.major < 3 else input
    if len(found) == 0:
        logg('No source WADs found!\nPlease place your WAD files into %s.' % os.path.realpath(SRC_WAD_DIR))
        if logfile:
            logfile.close()
        input_func('Press Enter to exit.\n')
        return
    files_tidied = 0
    for dirname, extensions in TIDY_DIR_EXTENSIONS.items():
        if not os.path.exists(DEST_DIR + dirname):
            continue
        for filename in os.listdir(DEST_DIR + dirname):
            for ext in extensions:
                if filename.endswith(ext):
                    path = DEST_DIR + dirname + filename
                    if os.path.exists(path):
                        os.remove(path)
                        files_tidied += 1
    for filename in RES_FILES:
        if filename != os.path.basename(filename):
            continue
        path = DEST_DIR + filename
        if os.path.exists(path):
            os.remove(path)
            files_tidied += 1
    if files_tidied > 0:
        logg('Removed %s files from a previous run.' % files_tidied)
    logg('Found in %s:\n  %s' % (SRC_WAD_DIR, ', '.join(found)))
    print('A new IPK3 format IWAD will be generated with the following episodes:')
    num_eps = 0
    for ep_name in get_eps(found):
        print('- %s' % ep_name)
        num_eps += 1
    if input_func('Press Y and then Enter to proceed, anything else to cancel: ').lower() != 'y':
        logg('Canceled.')
        if logfile:
            logfile.close()
        return
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)
    for dirname in ['flats', 'graphics', 'music', 'maps', 'mapinfo',
                    'patches', 'sounds', 'sprites', 'zscript']:
        if not os.path.exists(DEST_DIR + dirname):
            os.mkdir(DEST_DIR + dirname)
    if should_extract:
        copy_resources()
        sanitize_hell2pay_textures()
    if get_wad_filename('tnt') and not get_wad_filename('doom2'):
        WAD_LUMP_LISTS['tnt'] += DOOM2_LUMPS
        if not get_wad_filename('doom'):
            WAD_LUMP_LISTS['tnt'] += COMMON_LUMPS
    for iwad_name in WADS:
        if not get_wad_filename(iwad_name):
            logg('WAD %s not found' % iwad_name)
            continue
        rules = [
            (iwad_name == 'nerve' and not get_wad_filename('doom2')),
            (iwad_name == 'sigil' and not get_wad_filename('doom')),
            (iwad_name == 'sigil_shreds' and not get_wad_filename('sigil')),
            (iwad_name == 'sigil2' and not get_wad_filename('doom')),
            (iwad_name == 'sigil2_mp3' and not get_wad_filename('sigil2')),
            (iwad_name == 'id1' and not get_wad_filename('doom2')),
            (iwad_name == 'id1' and not get_wad_filename('id1-res')),
            (iwad_name == 'id1' and not get_wad_filename('id24res')),
            (iwad_name == 'doom3do' and not get_wad_filename('doom')),
            (iwad_name == 'perdgate' and not get_wad_filename('doom2')),
            (iwad_name == 'hell2pay' and not get_wad_filename('doom2')),
            (iwad_name == 'neis' and not get_wad_filename('doom')),
            (iwad_name == 'tntr' and not get_wad_filename('tnt')),
            (iwad_name == 'pl2' and not get_wad_filename('plutonia')),
            (iwad_name == 'jptr_v40' and not get_wad_filename('doom')),
            (iwad_name == 'jm-e4' and not get_wad_filename('doom')),
        ]
        if any(rules):
            logg('Skipping %s (missing dependency)' % iwad_name)
            continue
        logg('Processing WAD %s...' % iwad_name)
        if should_extract:
            extract_lumps(iwad_name)
            prefix = WAD_MAP_PREFIXES.get(iwad_name, None)
            if prefix is not None:
                extract_iwad_maps(iwad_name, prefix)
    if get_wad_filename('doom2') and should_extract:
        extract_master_levels()
    if get_wad_filename('sewers') and get_wad_filename('betray') and should_extract:
        add_xbox_levels()
    if (get_wad_filename('id1') and get_wad_filename('id1-res') and
            get_wad_filename('id24res') and get_wad_filename('doom2') and should_extract):
        copy_resources_id1()
    if os.path.exists(RES_DIR + 'GENMIDI.lmp'):
        copyfile(RES_DIR + 'GENMIDI.lmp', DEST_DIR + 'GENMIDI.lmp')
    # Xtras 0CRAT* AFTER wad extract so hell2pay.wad cannot leave leftover
    # crate lumps, and BEFORE zzz_crates / doom2 BCRATE restore.
    copy_extra_pg_loose_patches()
    generate_perdgate_textures()
    extract_pg_flats()
    log_pg_map01_textures()
    if should_extract and get_wad_filename('jm-e4'):
        patch_je4_boss_things()
    logg('Compressing %s...' % DEST_FILENAME)
    pk3 = ZipFile(DEST_FILENAME, 'w', ZIP_DEFLATED)
    for dir_name, x, filenames in os.walk(DEST_DIR):
        for filename in filenames:
            src_name = os.path.join(dir_name, filename)
            arc_name = src_name[len(DEST_DIR):]
            pk3.write(src_name, arc_name)
    pk3.close()
    logg('Done!')
    try:
        rmtree(DEST_DIR)
        logg('Removed staging folder %s' % DEST_DIR)
    except Exception as ex:
        logg('Could not remove %s: %s' % (DEST_DIR, ex))
    logg('Generated %s (%.1f MB) with %s maps in %s episodes in %.2f seconds.' % (
        DEST_FILENAME, os.path.getsize(DEST_FILENAME) / 1000000.0, num_maps, num_eps, time.time() - start_time))
    if num_errors > 0:
        logg('%s errors found, see %s for details.' % (num_errors, LOG_FILENAME))
    if logfile:
        logfile.close()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
        try:
            if logfile:
                logfile.close()
        except Exception:
            pass
        try:
            input('\nBuild failed. Press Enter to close.\n')
        except Exception:
            pass