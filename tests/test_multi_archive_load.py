# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the Foundry project
import os
import struct
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_SO = ROOT / "python" / "foundry" / "libcuda_hook.so"


def _write_regular_archive(
    archive_dir: Path,
    binary_hash: int,
    payload: bytes,
) -> None:
    archive_dir.mkdir(parents=True)
    image = (
        struct.pack("@Q", binary_hash)
        + struct.pack("@N", len(payload))
        + payload
    )
    (archive_dir / "fatbin_image_packed.img").write_bytes(image)
    (archive_dir / "fatbin_entrypoint_packed.txt").write_text(
        f"{binary_hash:016x}\n"
        "cuModuleLoadData,binary_flags=0\n"
        "1\n"
        "test_kernel\n"
        "---\n",
        encoding="utf-8",
    )


def _run_validation_subprocess(*archive_dirs: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        filter(
            None,
            [str(ROOT / "python"), env.get("PYTHONPATH", "")],
        )
    )
    env["LD_PRELOAD"] = os.pathsep.join(
        filter(None, [str(HOOK_SO), env.get("LD_PRELOAD", "")])
    )
    return subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--expect-error",
            *(str(path) for path in archive_dirs),
        ],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_multi_archive_loader_rejects_missing_packed_files(tmp_path: Path):
    missing_archive = tmp_path / "missing"
    missing_archive.mkdir()

    result = _run_validation_subprocess(missing_archive)

    assert result.returncode == 0, result.stderr
    assert "packed image or metadata file is missing" in result.stdout


def test_multi_archive_loader_rejects_conflicting_binary_hashes(tmp_path: Path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    _write_regular_archive(first, 0x1234, b"first payload")
    _write_regular_archive(second, 0x1234, b"second payload")

    result = _run_validation_subprocess(first, second)

    assert result.returncode == 0, result.stderr
    assert "Conflicting Foundry binary hash" in result.stdout
    assert str(first) in result.stdout
    assert str(second) in result.stdout


def _expect_validation_error(archive_dirs: list[str]) -> None:
    import foundry

    try:
        foundry.load_cuda_modules_and_libraries_from_archives(archive_dirs)
    except RuntimeError as exc:
        print(exc)
        return
    raise AssertionError("Expected malformed packed archives to be rejected")


if __name__ == "__main__" and sys.argv[1] == "--expect-error":
    _expect_validation_error(sys.argv[2:])
