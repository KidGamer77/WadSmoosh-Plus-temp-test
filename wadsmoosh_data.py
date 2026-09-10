##-----------------------------------------------------------------------------
##
## Copyright 2024 Owlet VII, Vanessa Kindell
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
##-----------------------------------------------------------------------------
##
## Derived from wadsmoosh-freedoom
## The MIT License (MIT)
## Copyright (c) 2016-2024 JP LeBreton
## Copyright (c) 2023-2024 Exequiel Mleziva
##
## KidGamer77 / UZDoom 5.x tables
## Issue #34: extra PWADs must not overwrite vanilla weapon/player sprites.
## Issue #45: do not extract tntr sprites or merge TNTR.deh into DEHACKED.txt.
## mapinfo/doom2_secret_levels.txt must be packed; mapinfo.txt includes it.
##
## jm-e4 (JM-E4.wad, Remnants of Earth):
##   maps prefix JE4_  ->  maps/JE4_MAP01.wad ... JE4_MAP08.wad
##   music list data/music_jm-e4 renames D_E4M* / D_EVIL / D_VICTOR
##   to music/JE4_E4M1.mid ... JE4_EVIL.mid
##   Place the source file in source_wads/ as jm-e4.wad (lowercase).
##
## CyberMastermind (Lost Episodes ZDoom Patch 2.0):
##   res/decorate.txt  actor doomednum 32000 (NOT 3115 — ID24 torso conflict)
##   res/sprites/CYMM*.lmp from the patch WAD only
##   After extract, edit maps/JE4_MAP08.wad thing 3115 -> 32000
##-----------------------------------------------------------------------------

# Pre-authored resources copied from res/ into the IPK3.
RES_FILES = [
    'mapinfo.txt', 'language.txt', 'endoom', 'smooshed.txt', 'iwadinfo.txt',
    'decorate.txt',
    'textures.common', 'textures.doom1', 'textures.doom2',
    'textures.freedoom1', 'textures.freedoom2', 'textures.id1', 'textures.doomzero',
    'textures.tnt', 'textures.plut', 'textures.perdgate', 'animdefs.txt',
    'textures.hell2pay', 'textures.neis', 'textures.tntr', 'textures.tnt2', 'textures.pl2',
    'graphics/M_DOOM.lmp', 'graphics/TITLEPIC.lmp',
    'graphics/M_HELL.lmp', 'graphics/M_NOREST.lmp',
    'graphics/M_MASTER.lmp', 'graphics/M_TNT.lmp',
    'graphics/M_PLUT.lmp', 'graphics/M_ID1.lmp',
    'mapinfo/doom1_levels.txt', 'mapinfo/doom2_levels.txt',
    'mapinfo/doom2_secret_levels.txt',
    'mapinfo/tnt_levels.txt', 'mapinfo/plutonia_levels.txt',
    'mapinfo/masterlevels.txt', 'mapinfo/sigil_levels.txt',
    'mapinfo/sigil2_levels.txt', 'mapinfo/perdgate_levels.txt',
    'mapinfo/id1_levels.txt', 'mapinfo/tnt2_levels.txt', 'mapinfo/doomzero_levels.txt',
    'mapinfo/hell2pay_levels.txt', 'mapinfo/neis_levels.txt',
    'mapinfo/freedoom1_levels.txt', 'mapinfo/freedoom2_levels.txt',
    'mapinfo/tntr_levels.txt', 'mapinfo/pl2_levels.txt', 'mapinfo/prcp_levels.txt',
    'mapinfo/jptr_levels.txt',
    'mapinfo/jme4_levels.txt',
    'menudef.txt', 'cvarinfo.txt', 'zscript.txt', 'DEHACKED.txt',
    'zscript/wf_handler.zs',
    'zscript/wf_music.zs',
    'zscript/wf_xbox.zs',
    'zscript/wf_sbar.zs',
    'zscript/wf_sbar.id1.zs',
    'zscript/wf_id1weap.zs',
    'zscript/wf_je4boss.zs',
    'zscript/wf_pl2boss.zs',
    # CyberMastermind sprites (LostEpisodes2-1_Patch.wad). Files live in res/sprites/.
    'sprites/CYMMA1.lmp', 'sprites/CYMMA2.lmp', 'sprites/CYMMA3.lmp', 'sprites/CYMMA4.lmp',
    'sprites/CYMMA5.lmp', 'sprites/CYMMA6.lmp', 'sprites/CYMMA7.lmp', 'sprites/CYMMA8.lmp',
    'sprites/CYMMB1.lmp', 'sprites/CYMMB2.lmp', 'sprites/CYMMB3.lmp', 'sprites/CYMMB4.lmp',
    'sprites/CYMMB5.lmp', 'sprites/CYMMB6.lmp', 'sprites/CYMMB7.lmp', 'sprites/CYMMB8.lmp',
    'sprites/CYMMC1.lmp', 'sprites/CYMMC2.lmp', 'sprites/CYMMC3.lmp', 'sprites/CYMMC4.lmp',
    'sprites/CYMMC5.lmp', 'sprites/CYMMC6.lmp', 'sprites/CYMMC7.lmp', 'sprites/CYMMC8.lmp',
    'sprites/CYMMD1.lmp', 'sprites/CYMMD2.lmp', 'sprites/CYMMD3.lmp', 'sprites/CYMMD4.lmp',
    'sprites/CYMMD5.lmp', 'sprites/CYMMD6.lmp', 'sprites/CYMMD7.lmp', 'sprites/CYMMD8.lmp',
    'sprites/CYMME1.lmp', 'sprites/CYMME2.lmp', 'sprites/CYMME3.lmp', 'sprites/CYMME4.lmp',
    'sprites/CYMME5.lmp', 'sprites/CYMME6.lmp', 'sprites/CYMME7.lmp', 'sprites/CYMME8.lmp',
    'sprites/CYMMF1.lmp', 'sprites/CYMMF2.lmp', 'sprites/CYMMF3.lmp', 'sprites/CYMMF4.lmp',
    'sprites/CYMMF5.lmp', 'sprites/CYMMF6.lmp', 'sprites/CYMMF7.lmp', 'sprites/CYMMF8.lmp',
    'sprites/CYMMG1.lmp', 'sprites/CYMMG2.lmp', 'sprites/CYMMG3.lmp', 'sprites/CYMMG4.lmp',
    'sprites/CYMMG5.lmp', 'sprites/CYMMG6.lmp', 'sprites/CYMMG7.lmp', 'sprites/CYMMG8.lmp',
    'sprites/CYMMH1.lmp', 'sprites/CYMMH2.lmp', 'sprites/CYMMH3.lmp', 'sprites/CYMMH4.lmp',
    'sprites/CYMMH5.lmp', 'sprites/CYMMH6.lmp', 'sprites/CYMMH7.lmp', 'sprites/CYMMH8.lmp',
    'sprites/CYMMI1.lmp', 'sprites/CYMMI2.lmp', 'sprites/CYMMI3.lmp', 'sprites/CYMMI4.lmp',
    'sprites/CYMMI5.lmp', 'sprites/CYMMI6.lmp', 'sprites/CYMMI7.lmp', 'sprites/CYMMI8.lmp',
    'sprites/CYMMJ1.lmp', 'sprites/CYMMJ2.lmp', 'sprites/CYMMJ3.lmp', 'sprites/CYMMJ4.lmp',
    'sprites/CYMMJ5.lmp', 'sprites/CYMMJ6.lmp', 'sprites/CYMMJ7.lmp', 'sprites/CYMMJ8.lmp',
    'sprites/CYMMK1.lmp', 'sprites/CYMMK2.lmp', 'sprites/CYMMK3.lmp', 'sprites/CYMMK4.lmp',
    'sprites/CYMMK5.lmp', 'sprites/CYMMK6.lmp', 'sprites/CYMMK7.lmp', 'sprites/CYMMK8.lmp',
    'sprites/CYMML0.lmp', 'sprites/CYMMM0.lmp', 'sprites/CYMMN0.lmp', 'sprites/CYMMO0.lmp',
    'sprites/CYMMP0.lmp', 'sprites/CYMMQ0.lmp', 'sprites/CYMMR0.lmp', 'sprites/CYMMS0.lmp',
    'sprites/CYMMT0.lmp', 'sprites/CYMMU0.lmp',
]

# Files inside DEST_DIR removed before a new run.
TIDY_DIR_EXTENSIONS = {
    'flats/': ['lmp'],
    'graphics/': ['lmp'],
    'patches/': ['lmp'],
    'sounds/': ['lmp'],
    'sprites/': ['lmp'],
    'music/': ['mus', 'mp3', 'ogg', 'lmp', 'mid', 'midi'],
    'mapinfo/': ['txt'],
    'maps/': ['wad'],
    'zscript/': ['zs', 'txt'],
    './': ['lmp', 'txt']
}

# WADs the extractor will open if present in source_wads/.
WADS = [
    'doom', 'doom2', 'doom2bfg', 'tnt', 'plutonia', 'nerve', 'sigil', 'sigil_shreds',
    'sigil2', 'sigil2_shreds', 'doomunity', 'doom2unity', 'nerveu', 'tntu',
    'tnt2_beta6', 'plutoniau', 'extras', 'perdgate', 'hell2pay',
    'neis', 'freedoom1', 'freedoom2', 'doom3do', 'tntr', 'pl2', 'prcp',
    'jptr_v40', 'jm-e4', 'id1', 'id1-res', 'id24res', 'doomzero'
]

# Logged when found, even if not in WADS (Xbox bonus maps, Master Levels PWADs).
REPORT_WADS = [
    'doom', 'sigil', 'sigil_shreds', 'sigil2', 'sigil2_shreds',
    'doom2', 'nerve', 'attack', 'tnt', 'plutonia',
    'sewers', 'betray', 'e1m4b', 'e1m8b',
    'doomunity', 'doom2unity',
    'nerveu', 'tntu', 'plutoniau', 'extras', 'perdgate',
    'hell2pay', 'neis', 'pl2', 'prcp', 'tntr', 'tnt2_beta6', 'jptr_v40',
    'jm-e4',
    'freedoom1', 'freedoom2', 'doom3do',
    'id1', 'id1-res', 'id24res', 'doomzero'
]

COMMON_LUMPS = [
    'data_common', 'flats_common', 'graphics_common', 'patches_common',
    'sounds_common', 'sprites_common'
]

DOOM1_LUMPS = [
    'graphics_doom1', 'music_doom1', 'patches_doom1', 'sounds_doom1',
    'txdefs_doom1'
]

DOOM2_LUMPS = [
    'flats_doom2', 'graphics_doom2', 'music_doom2', 'patches_doom2',
    'sounds_doom2', 'sprites_doom2', 'txdefs_doom2'
]

# IWADs allowed to write vanilla sprite names (SHT2, PLAY, CHGG, ...).
VANILLA_SPRITE_SOURCES = ('doom', 'doom2', 'id1', 'id24res', 'id1-res')

# Issue #34: extra campaigns must never dump these prefixes into sprites/.
VANILLA_SPRITE_BLOCKLIST = (
    'SHT2', 'SHTG', 'SHTF',
    'CHGG', 'CHGF',
    'PISG', 'PISF',
    'PUNG', 'SAWG',
    'MISG', 'MISF',
    'PLSG', 'PLSF',
    'BFGG', 'BFGF',
    'PLAY',
)

# data/<name> list files extracted from each source WAD.
# nerve, doom2bfg, jptr_v40, id1-res: maps only.
# jm-e4: maps + renamed music list data/music_jm-e4.
WAD_LUMP_LISTS = {
    'doom': COMMON_LUMPS + DOOM1_LUMPS,
    'doom2': COMMON_LUMPS + DOOM2_LUMPS,
    'tnt': ['graphics_tnt', 'music_tnt', 'patches_tnt'],
    'plutonia': ['graphics_plutonia', 'music_plutonia', 'patches_plutonia'],
    'sigil': ['graphics_sigil', 'music_sigil', 'patches_sigil', 'data_sigil'],
    'sigil_shreds': ['music_sigil_shreds'],
    'sigil2': ['graphics_sigil2', 'music_sigil2', 'patches_sigil2', 'data_sigil2', 'flats_sigil2'],
    'sigil2_shreds': ['music_sigil2_shreds'],
    'id1': ['data_id1', 'flats_id1', 'graphics_id1', 'music_id1', 'patches_id1', 'sounds_id1', 'sprites_id1'],
    'id24res': ['graphics_id24res'],
    'doomunity': ['graphics_doomunity'],
    'doom2unity': ['graphics_doom2unity'],
    'nerveu': ['graphics_nerveu'],
    'tntu': ['graphics_tntu'],
    'plutoniau': ['graphics_plutoniau'],
    'tntr': ['graphics_tntr', 'patches_tntr', 'flats_tntr', 'music_tntr'],
    'tnt2_beta6': ['graphics_tnt2', 'patches_tnt2', 'flats_tnt2', 'music_tnt2'],
    'pl2': ['graphics_pl2', 'patches_pl2', 'flats_pl2', 'music_pl2'],
    'prcp': ['graphics_prcp', 'patches_prcp', 'flats_prcp', 'music_prcp'],
    'perdgate': ['graphics_perdgate', 'music_perdgate'],
    'hell2pay': ['graphics_hell2pay', 'patches_hell2pay', 'flats_hell2pay', 'music_hell2pay'],
    'neis': ['graphics_neis', 'patches_neis', 'flats_neis'],
    'doomzero': ['graphics_doomzero', 'patches_doomzero', 'flats_doomzero',
                 'music_doomzero', 'sounds_doomzero', 'sprites_doomzero'],
    'extras': ['sounds_unity', 'music_extras'],
    'doom3do': ['music_doom3do'],
    'freedoom1': ['graphics_freedoom1', 'patches_freedoom1', 'flats_freedoom1', 'music_freedoom1'],
    'freedoom2': ['graphics_freedoom2', 'patches_freedoom2', 'flats_freedoom2', 'music_freedoom2'],
    'jm-e4': ['music_jm-e4'],
}

WAD_MAP_PREFIXES = {
    'doom': '',
    'doom2': '',
    'tnt': 'TN_',
    'plutonia': 'PL_',
    'nerve': 'NV_',
    'masterlevels': 'ML_',
    'sigil': '',
    'sigil2': '',
    'id1': 'LR_',
    'hell2pay': 'HP_',
    'perdgate': 'PG_',
    'neis': 'NS_',
    'freedoom1': 'FD1_',
    'freedoom2': 'FD2_',
    'tntr': 'TR_',
    'tnt2_beta6': 'T2_',
    'pl2': 'P2_',
    'doomzero': 'DZ_',
    'prcp': 'PRCP_',
    'jptr_v40': 'JPTR_',
    'jm-e4': 'JE4_',
}

MAP_NAME_GRAPHICS_DIRS = []

MASTER_LEVELS_PATCHES = {
    'combine': ('RSKY1', 'ML_SKY1'),
    'manor':   ('STARS', 'ML_SKY2'),
    'virgil':  ('RSKY1', 'ML_SKY3'),
}

MASTER_LEVELS_SKIES = {
    'combine':  'ML_SKY1',
    'manor':    'ML_SKY2',
    'ttrap':    'ML_SKY2',
    'virgil':   'ML_SKY3',
    'minos':    'ML_SKY3',
    'nessus':   'ML_SKY3',
    'geryon':   'ML_SKY3',
    'vesperas': 'ML_SKY3',
    'blacktwr': 'RSKY3',
}

MASTER_LEVELS_MUSIC = {
    'attack':   'RUNNIN',
    'canyon':   'STALKS',
    'catwalk':  'COUNTD',
    'combine':  'BETWEE',
    'fistula':  'DOOM',
    'garrison': 'THE_DA',
    'manor':    'SHAWN',
    'paradox':  'DDTBLU',
    'subspace': 'IN_CIT',
    'subterra': 'DEAD',
    'ttrap':    'STLKS2',
    'virgil':   'COUNTD',
    'minos':    'DOOM',
    'bloodsea': 'SHAWN',
    'mephisto': 'OPENIN',
    'nessus':   'SHAWN',
    'geryon':   'DDTBLU',
    'vesperas': 'IN_CIT',
    'blacktwr': 'ADRIAN',
    'teeth':    'EVIL',
    'teeth2':   'ULTIMA',
}

MASTER_LEVELS_MAP07_SPECIAL = ['bloodsea', 'mephisto']

MASTER_LEVELS_SECRET_DEF = """
map ML_MAP21 lookup "ML_TEETH_SECRET"
{
    next = "%s"
    sky1 = "RSKY1"
    music = "$MUSIC_%s"
    Author = "$%s_%s"
}
"""

MASTER_LEVELS_CLUSTER_DEF = """
cluster 24
{
    flat = "$BGFLAT06"
    music = "$MUSIC_READ_M"
    exittext = lookup, "M1TEXT"
}
"""

MASTER_LEVELS_AUTHOR_PREFIX = 'WS_AU'

MASTER_LEVELS_AUTHORS = {
    'attack':   'WILLITS_CHASAR',
    'canyon':   'WILLITS_CHASAR',
    'catwalk':  'KLIE',
    'fistula':  'KLIE',
    'combine':  'KLIE',
    'subspace': 'KLIE',
    'paradox':  'MUSTAINE',
    'subterra': 'KLIE',
    'garrison': 'KLIE',
    'blacktwr': 'KVERNMO',
    'virgil':   'ANDERSON',
    'minos':    'ANDERSON',
    'nessus':   'ANDERSON',
    'geryon':   'ANDERSON',
    'vesperas': 'ANDERSON',
    'manor':    'FLYNN',
    'ttrap':    'FLYNN',
    'teeth':    'KVERNMO',
    'bloodsea': 'KVERNMO',
    'mephisto': 'KVERNMO',
    'teeth2':   'KVERNMO',
}

MASTER_LEVELS_MAPINFO_HEADER = """
// master levels for doom 2
// generated from file '%s' by WadSmoosh

defaultmap
{
    cluster = 24
}

"""

SIGIL_ALT_FILENAMES = [
    'sigil_v1_0', 'sigil_v1_1', 'sigil_v1_2', 'sigil_v1_21',
    'sigil_v1_23', 'sigil',
]
SIGIL2_ALT_FILENAMES = [
    'sigil_ii_v1_0', 'sigil_ii_mp3_v1_0', 'sigil2',
]

# Present only in BFG / Xbox IWADs; used to detect that flavour.
BFG_ONLY_LUMP = 'DMENUPIC'