#!/usr/bin/env python3
"""Convert MFA IPA-like phone labels in timestamp JSONs into ARPABET.

This is the inverse of an ARPABET->IPA conversion used to compare against the
2019 LibriSpeech ARPABET alignments.

Input JSON schema is preserved (same keys/structure; only phone strings change).
See `timestamp_json_schema.md` for the expected structure.

Notes
-----
- MFA/english_mfa phones are IPA-like but include ASCII-ish diphthongs such as
  `aj`, `aw`, `ej`, `ow`, `ɔj` (these are also accepted alongside canonical IPA
  `aɪ`, `aʊ`, `eɪ`, `oʊ`, `ɔɪ`).
- Stress is not represented in the IPA-like phone set; when converting to
  ARPABET, vowel stress is therefore assigned by a configurable default.
- Unknown phones are left unchanged by default.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


VOWEL_BASES = {
    "AA",
    "AE",
    "AH",
    "AO",
    "AW",
    "AY",
    "EH",
    "ER",
    "EY",
    "IH",
    "IY",
    "OW",
    "OY",
    "UH",
    "UW",
}

# IPA-like -> ARPABET (stress-less where meaningful; stress is applied later).
# Include both canonical IPA and MFA ASCII-ish variants where applicable.
IPA_TO_ARPABET: Dict[str, str] = {
    # Vowels
    "ɑ": "AA",
    "æ": "AE",
    "ʌ": "AH",
    "ə": "AH0",  # schwa
    "ɔ": "AO",

    # Diphthongs (canonical IPA)
    "aɪ": "AY",
    "aʊ": "AW",
    "eɪ": "EY",
    "oʊ": "OW",
    "ɔɪ": "OY",

    # Diphthongs (MFA/english_mfa style)
    "aj": "AY",
    "aw": "AW",
    "ej": "EY",
    "ow": "OW",
    "ɔj": "OY",

    # Rhotic vowels (canonical IPA forms)
    "ɜr": "ER",
    "ər": "ER0",

    # Rhotic vowels (common single symbols)
    "ɝ": "ER",
    "ɚ": "ER0",

    # Non-rhotic high vowels
    "ɪ": "IH",
    "i": "IY",
    "ʊ": "UH",
    "u": "UW",

    # Consonants
    "b": "B",
    "tʃ": "CH",
    "d": "D",
    "ð": "DH",
    "ɛ": "EH",
    "f": "F",
    "ɡ": "G",  # LATIN SMALL LETTER SCRIPT G
    "g": "G",  # fallback
    "h": "HH",
    "dʒ": "JH",
    "k": "K",
    "l": "L",
    "m": "M",
    "n": "N",
    "ŋ": "NG",
    "p": "P",
    "r": "R",
    "ɹ": "R",
    "s": "S",
    "ʃ": "SH",
    "t": "T",
    "θ": "TH",
    "v": "V",
    "w": "W",
    "j": "Y",
    "z": "Z",
    "ʒ": "ZH",

    # Noise
    "spn": "spn",
    "sil": "sil",
}


_ARPABET_RE = re.compile(r"^[A-Z]{1,3}[0-2]?$")


def _looks_like_arpabet(s: str) -> bool:
    s = s.strip().upper()
    return s == "SPN" or bool(_ARPABET_RE.match(s))


def ipa_phone_to_arpabet(phone: str, default_stress: int | None) -> str:
    """Convert one IPA-like phone string to ARPABET.

    If the phone already looks like ARPABET (or `spn`), it is returned in the
    canonical form (uppercase for ARPABET; `spn` preserved as lowercase).

    Stress handling:
    - If the mapping returns an explicit stress-marked symbol (e.g., AH0/ER0),
      it is used as-is.
    - Otherwise, if the mapped base is a vowel base and `default_stress` is not
      None, append that stress digit.
    """
    raw = phone
    p = (phone or "").strip()
    if not p:
        return raw

    # Preserve common non-phoneme tokens.
    if p.lower() in {"spn", "sil"}:
        return p.lower()

    # If already ARPABET-like, normalize case.
    if _looks_like_arpabet(p):
        up = p.upper()
        return "spn" if up == "SPN" else up

    # Normalize a few common Unicode sequences.
    # (Keep this minimal; avoid aggressive IPA rewriting.)
    p_norm = p

    # Direct mapping.
    base = IPA_TO_ARPABET.get(p_norm)
    if base is None:
        # Try lowercase; MFA phones are often lowercase.
        base = IPA_TO_ARPABET.get(p_norm.lower())

    if base is None:
        # Unknown: leave unchanged.
        return p

    # Explicit stress in mapping.
    if base.upper().endswith(("0", "1", "2")):
        return base.upper()

    base_up = base.upper()

    # Apply default stress to vowel bases if requested.
    if base_up in VOWEL_BASES and default_stress is not None:
        return f"{base_up}{default_stress}"

    return base_up


def _convert_interval_container(container: Any, default_stress: int | None) -> None:
    """In-place conversion for a container that holds interval objects.

    Accepts either:
    - dict[str, {xmin,xmax,text,...}]
    - list[{xmin,xmax,text,...}]

    Only the 'text' field is modified.
    """
    if isinstance(container, dict):
        items = container.values()
    elif isinstance(container, list):
        items = container
    else:
        return

    for it in items:
        if isinstance(it, dict) and "text" in it and isinstance(it["text"], str):
            it["text"] = ipa_phone_to_arpabet(it["text"], default_stress)


def convert_json_obj(obj: Any, default_stress: int | None) -> Any:
    """Convert IPA-like phones to ARPABET in a loaded JSON object.

    Supports:
    - per-file object with keys including 'words'/'phones'
    - filename->per-file mapping

    The conversion applies to the `phones` field under each per-file object.
    """

    def convert_per_file(per_file: Dict[str, Any]) -> None:
        if "phones" in per_file:
            _convert_interval_container(per_file["phones"], default_stress)

    if isinstance(obj, dict) and "words" in obj and "phones" in obj:
        # Single-file object.
        convert_per_file(obj)
        return obj

    if isinstance(obj, dict):
        # filename -> per-file
        for _, per_file in obj.items():
            if isinstance(per_file, dict):
                convert_per_file(per_file)
        return obj

    # Unknown top-level type.
    return obj


def _default_outfile_for_file(in_file: Path) -> Path:
    return in_file.with_suffix(".arpa.json")


def _default_outdir_for_dir(in_dir: Path) -> Path:
    return in_dir.parent / f"{in_dir.name}_arpa"


def _iter_json_files(root: Path) -> Iterable[Path]:
    # Recursive walk; skip hidden directories.
    for p in root.rglob("*.json"):
        if any(part.startswith(".") for part in p.parts):
            continue
        if p.is_file():
            yield p


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Convert MFA IPA-like phone labels in timestamp JSONs to ARPABET "
            "while preserving the JSON schema."
        )
    )
    ap.add_argument(
        "input",
        type=str,
        help="Input JSON file or directory containing JSON files.",
    )
    ap.add_argument(
        "--out",
        type=str,
        default=None,
        help=(
            "Output JSON file (only valid when input is a file). "
            "Default: <input>.arpa.json"
        ),
    )
    ap.add_argument(
        "--out_dir",
        type=str,
        default=None,
        help=(
            "Output directory (only valid when input is a directory). "
            "Default: <input>_arpa (sibling directory)."
        ),
    )
    ap.add_argument(
        "--inplace",
        action="store_true",
        help="Overwrite input JSON(s) in-place.",
    )
    ap.add_argument(
        "--default_stress",
        type=str,
        default="1",
        help=(
            "Default stress digit to assign to vowels (0/1/2), or 'none' to "
            "emit stress-less vowel bases. Schwa (AH0) and rhotic schwa (ER0) "
            "are always emitted as 0." 
        ),
    )

    args = ap.parse_args()

    in_path = Path(args.input).expanduser()

    if args.default_stress.lower() == "none":
        default_stress: int | None = None
    else:
        try:
            default_stress = int(args.default_stress)
        except ValueError:
            raise SystemExit("--default_stress must be 0, 1, 2, or 'none'")
        if default_stress not in (0, 1, 2):
            raise SystemExit("--default_stress must be 0, 1, 2, or 'none'")

    if not in_path.exists():
        raise SystemExit(f"Input path not found: {in_path}")

    if in_path.is_file():
        if args.out_dir is not None:
            raise SystemExit("--out_dir is only valid when input is a directory")
        out_path = in_path if args.inplace else Path(args.out).expanduser() if args.out else _default_outfile_for_file(in_path)

        obj = _read_json(in_path)
        obj = convert_json_obj(obj, default_stress=default_stress)
        _write_json(out_path, obj)
        return 0

    if in_path.is_dir():
        if args.out is not None:
            raise SystemExit("--out is only valid when input is a file")
        out_dir = in_path if args.inplace else Path(args.out_dir).expanduser() if args.out_dir else _default_outdir_for_dir(in_path)

        for in_file in _iter_json_files(in_path):
            rel = in_file.relative_to(in_path)
            out_file = out_dir / rel

            obj = _read_json(in_file)
            obj = convert_json_obj(obj, default_stress=default_stress)
            _write_json(out_file, obj)

        return 0

    raise SystemExit(f"Unsupported input path type: {in_path}")


if __name__ == "__main__":
    raise SystemExit(main())
