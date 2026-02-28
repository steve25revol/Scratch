#!/usr/bin/env python3
"""Package all assets into a valid .sb3 file for Scratch 3.0."""

import hashlib
import json
import os
import struct
import zipfile

from generate_svgs import generate_all_svgs
from generate_sounds import generate_all_sounds
from build_project_json import (
    build_stage_target,
    build_hero_target,
    build_coworker_target,
    build_computer_target,
    build_explosion_target,
    build_parachute_target,
    build_debris_target,
    build_debris2_target,
    build_theend_target,
    build_sound_controller_target,
    build_project,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "stickman-office-escape.sb3")

# Tiny transparent SVG for invisible sprites
TRANSPARENT_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1">'
    '<rect width="1" height="1" fill="none"/></svg>'
)


def md5_of(data):
    """Compute MD5 hex digest of bytes or string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.md5(data).hexdigest()


def make_costume_entry(name, svg_string):
    """Create a costume dict and return (entry, md5ext, data_bytes)."""
    data = svg_string.encode("utf-8")
    asset_id = md5_of(data)
    md5ext = f"{asset_id}.svg"
    entry = {
        "assetId": asset_id,
        "name": name,
        "bitmapResolution": 1,
        "md5ext": md5ext,
        "dataFormat": "svg",
        "rotationCenterX": 240,
        "rotationCenterY": 180,
    }
    return entry, md5ext, data


def make_costume_entry_with_center(name, svg_string, cx, cy):
    """Create a costume dict with custom rotation center."""
    data = svg_string.encode("utf-8")
    asset_id = md5_of(data)
    md5ext = f"{asset_id}.svg"
    entry = {
        "assetId": asset_id,
        "name": name,
        "bitmapResolution": 1,
        "md5ext": md5ext,
        "dataFormat": "svg",
        "rotationCenterX": cx,
        "rotationCenterY": cy,
    }
    return entry, md5ext, data


def _wav_sample_count(wav_bytes):
    """Parse WAV bytes and return (sample_rate, sample_count)."""
    rate = 22050
    sample_count = 0
    channels = 1
    bits_per_sample = 16
    i = 12  # skip RIFF header + WAVE tag
    while i < len(wav_bytes) - 8:
        chunk_id = wav_bytes[i:i + 4]
        chunk_size = struct.unpack('<I', wav_bytes[i + 4:i + 8])[0]
        if chunk_id == b'fmt ':
            fmt = struct.unpack('<HHIIHH', wav_bytes[i + 8:i + 24])
            channels = fmt[1]
            rate = fmt[2]
            bits_per_sample = fmt[5]
        elif chunk_id == b'data':
            bytes_per_sample = (bits_per_sample // 8) * channels
            if bytes_per_sample > 0:
                sample_count = chunk_size // bytes_per_sample
        i += 8 + chunk_size
        if chunk_size % 2:
            i += 1  # WAV chunks are word-aligned
    return rate, sample_count


def make_sound_entry(name, wav_bytes):
    """Create a sound dict and return (entry, md5ext, data_bytes)."""
    asset_id = md5_of(wav_bytes)
    md5ext = f"{asset_id}.wav"
    rate, sample_count = _wav_sample_count(wav_bytes)
    entry = {
        "assetId": asset_id,
        "name": name,
        "dataFormat": "wav",
        "md5ext": md5ext,
        "rate": rate,
        "sampleCount": sample_count,
    }
    return entry, md5ext, wav_bytes


def main():
    print("Generating SVG costumes...")
    all_svgs = generate_all_svgs()

    print("Generating WAV sounds...")
    all_sounds = generate_all_sounds()

    # Assets dict: md5ext -> bytes
    assets = {}

    # ============================
    # BACKDROPS (Stage costumes)
    # ============================
    backdrop_costumes = []
    for name, svg in all_svgs["backdrops"].items():
        entry, md5ext, data = make_costume_entry(name, svg)
        backdrop_costumes.append(entry)
        assets[md5ext] = data

    # ============================
    # STAGE SOUNDS (office hum for ambiance)
    # ============================
    stage_sounds = []
    for sname in ["office-hum"]:
        entry, md5ext, data = make_sound_entry(sname, all_sounds[sname])
        stage_sounds.append(entry)
        assets[md5ext] = data

    # ============================
    # STICKMAN HERO
    # ============================
    hero_costumes = []
    for name, svg in all_svgs["StickmanHero"].items():
        entry, md5ext, data = make_costume_entry(name, svg)
        hero_costumes.append(entry)
        assets[md5ext] = data
    hero_sounds = []  # Hero doesn't play sounds directly

    # ============================
    # COWORKERS
    # ============================
    def _make_coworker_costumes(key):
        costumes = []
        for name, svg in all_svgs[key].items():
            entry, md5ext, data = make_costume_entry(name, svg)
            costumes.append(entry)
            assets[md5ext] = data
        return costumes

    coworkerA_costumes = _make_coworker_costumes("CoworkerA")
    coworkerB_costumes = _make_coworker_costumes("CoworkerB")
    coworkerC_costumes = _make_coworker_costumes("CoworkerC")

    # ============================
    # COMPUTER
    # ============================
    computer_costumes = []
    for name, svg in all_svgs["Computer"].items():
        entry, md5ext, data = make_costume_entry(name, svg)
        computer_costumes.append(entry)
        assets[md5ext] = data

    # ============================
    # EXPLOSION
    # ============================
    explosion_costumes = []
    for name, svg in all_svgs["Explosion"].items():
        # Explosion SVGs have varying sizes; use their own center
        if "flash" in name:
            cx, cy = 50, 50
        elif "dissipate" in name:
            cx, cy = 175, 175
        else:
            cx, cy = 175, 175
        entry, md5ext, data = make_costume_entry_with_center(name, svg, cx, cy)
        explosion_costumes.append(entry)
        assets[md5ext] = data
    explosion_sounds = []
    for sname in ["explosion"]:
        entry, md5ext, data = make_sound_entry(sname, all_sounds[sname])
        explosion_sounds.append(entry)
        assets[md5ext] = data

    # ============================
    # PARACHUTE
    # ============================
    parachute_costumes = []
    for name, svg in all_svgs["Parachute"].items():
        entry, md5ext, data = make_costume_entry(name, svg)
        parachute_costumes.append(entry)
        assets[md5ext] = data

    # ============================
    # DEBRIS
    # ============================
    debris_costumes = []
    for name, svg in all_svgs["Debris"].items():
        entry, md5ext, data = make_costume_entry_with_center(name, svg, 7, 7)
        debris_costumes.append(entry)
        assets[md5ext] = data

    # ============================
    # THE END
    # ============================
    theend_costumes = []
    for name, svg in all_svgs["TheEnd"].items():
        entry, md5ext, data = make_costume_entry(name, svg)
        theend_costumes.append(entry)
        assets[md5ext] = data

    # ============================
    # SOUND CONTROLLER
    # ============================
    sc_sounds = []
    for sname in all_sounds:
        entry, md5ext, data = make_sound_entry(sname, all_sounds[sname])
        sc_sounds.append(entry)
        assets[md5ext] = data

    # Transparent costume for sound controller
    trans_entry, trans_md5, trans_data = make_costume_entry_with_center(
        "transparent", TRANSPARENT_SVG, 0, 0
    )
    assets[trans_md5] = trans_data

    # ============================
    # BUILD ALL TARGETS
    # ============================
    stage = build_stage_target(backdrop_costumes, stage_sounds)

    hero = build_hero_target(hero_costumes, hero_sounds)

    coworkerA = build_coworker_target(
        "CoworkerA", "coworkerA", coworkerA_costumes, [], -150, 10, idle_delay=0.3)
    coworkerB = build_coworker_target(
        "CoworkerB", "coworkerB", coworkerB_costumes, [], 130, 20, idle_delay=0.35)
    coworkerC = build_coworker_target(
        "CoworkerC", "coworkerC", coworkerC_costumes, [], -160, -60, idle_delay=0.4)

    computer = build_computer_target(computer_costumes, [])
    explosion = build_explosion_target(explosion_costumes, explosion_sounds)
    parachute = build_parachute_target(parachute_costumes, [])
    debris = build_debris_target(debris_costumes, [])
    debris2 = build_debris2_target(debris_costumes, [])
    theend = build_theend_target(theend_costumes, [])

    sound_ctrl = build_sound_controller_target(sc_sounds)
    sound_ctrl["costumes"] = [trans_entry]

    targets = [
        stage, hero, coworkerA, coworkerB, coworkerC,
        computer, explosion, parachute, debris, debris2,
        theend, sound_ctrl,
    ]

    project = build_project(targets)
    project_json = json.dumps(project, indent=None, separators=(',', ':'))

    # ============================
    # PACKAGE .sb3
    # ============================
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Packaging {OUTPUT_FILE}...")
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("project.json", project_json)
        for md5ext, data in assets.items():
            zf.writestr(md5ext, data)

    # ============================
    # VALIDATION
    # ============================
    print("Validating...")
    with zipfile.ZipFile(OUTPUT_FILE, 'r') as zf:
        names = set(zf.namelist())
        assert "project.json" in names, "Missing project.json"

        pj = json.loads(zf.read("project.json"))

        # Check all referenced assets exist
        missing = []
        for target in pj["targets"]:
            for costume in target.get("costumes", []):
                if costume["md5ext"] not in names:
                    missing.append(f"costume {costume['name']} -> {costume['md5ext']}")
            for sound in target.get("sounds", []):
                if sound["md5ext"] not in names:
                    missing.append(f"sound {sound['name']} -> {sound['md5ext']}")

        if missing:
            print("MISSING ASSETS:")
            for m in missing:
                print(f"  {m}")
            raise RuntimeError("Asset validation failed!")

        # Stats
        total_size = sum(zf.getinfo(n).file_size for n in names)
        compressed = os.path.getsize(OUTPUT_FILE)
        n_targets = len(pj["targets"])
        n_blocks = sum(len(t.get("blocks", {})) for t in pj["targets"])
        n_costumes = sum(len(t.get("costumes", [])) for t in pj["targets"])
        n_sounds = sum(len(t.get("sounds", [])) for t in pj["targets"])

        print(f"  Targets: {n_targets}")
        print(f"  Blocks: {n_blocks}")
        print(f"  Costumes: {n_costumes}")
        print(f"  Sounds: {n_sounds}")
        print(f"  Assets in ZIP: {len(names) - 1}")
        print(f"  Uncompressed size: {total_size / 1024:.1f} KB")
        print(f"  .sb3 file size: {compressed / 1024:.1f} KB")

    print(f"\nDone! File saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
