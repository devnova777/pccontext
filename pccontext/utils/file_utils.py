"""
File utilities
"""

import base64
import errno
import json
from os import strerror
from pathlib import Path

from pccontext.logging import logger

__all__ = [
    "check_file_exists",
    "check_file_not_exists",
    "check_file",
    "check_socket",
    "load_file",
    "load_json_file",
    "dump_file",
    "dump_json_file",
    "cleanup_file",
    "base64_encoded_file",
    "file_size",
]


def check_file_exists(fpath: Path) -> None:
    """
    Checks if the file exists and is a file
    :raise FileNotFoundError: If the file does not exist
    :param fpath: The path to the file
    :return: None
    """
    if not fpath.exists() or not fpath.is_file():
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), fpath.as_posix())


def check_file_not_exists(fpath: Path) -> None:
    """
    Checks if the file does not exist
    :raise FileExistsError: If the file exists
    :param fpath: The path to the file
    :return: None
    """
    if fpath.exists():
        raise FileExistsError(errno.EEXIST, strerror(errno.EEXIST), fpath.as_posix())


def check_file(file: Path) -> None:
    """
    Checks if the file exists does not exist and prints a warning and exit if it does
    :param file: The path to the file
    :return: None
    """
    try:
        check_file_not_exists(file)
    except FileExistsError:
        logger.warning(f"{file.name} already present, delete it or use another name!")
        raise FileExistsError(errno.EEXIST, strerror(errno.EEXIST), file.as_posix())


def check_socket(fpath: Path) -> None:
    """
    Checks if the file exists and is a socket
    :param fpath: The path to the file
    :return: None
    """
    if not fpath.exists():
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), fpath.as_posix())
    elif not fpath.is_socket():
        raise TypeError(f"{fpath.name} is not a socket")


def load_file(fpath: Path) -> str:
    """
    Reads the text file and return its contents

    :param fpath: The path of the file
    :return: text: The contents of the file
    """
    check_file_exists(fpath)
    with open(fpath, encoding="utf-8") as file:
        text = file.read()
    return text.strip()


def load_json_file(fpath: Path) -> dict:
    """
    Reads the json file and return its contents as a dictionary

    :param fpath: The path of the file
    :return: text: The contents of the file
    """
    check_file_exists(fpath)
    with open(fpath, encoding="utf-8") as file:
        output_json = json.load(file)
    return output_json


def dump_file(fpath: Path, data: str) -> None:
    """
    Write data to a text file

    :param fpath: The path of the file
    :param data: The data to write to the file
    :return: None
    """
    with open(fpath, "w", encoding="utf-8") as file:
        file.write(data)


def dump_json_file(fpath: Path, data: dict) -> None:
    """
    Write json dict to a file

    :param fpath: The path of the file
    :param data: The data to write to the file
    :return: None
    """
    dump_file(fpath, json.dumps(data, indent=4))


def cleanup_file(fpath: Path):
    """
    Cleanup the file by removing it

    :param fpath:
    :return: None
    """
    fpath.unlink()


def base64_encoded_file(fpath: Path) -> bytes:
    """
    Base64 encode the file

    :param fpath: The file to be encoded
    :return: The base64 encoded version of the file
    """
    with open(fpath, "rb") as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
    return base64_encoded_data


def file_size(fpath: Path) -> int:
    """
    Return the size of the file in bytes
    :param fpath: The path to the file
    :return: The size of the file in bytes
    """

    try:
        check_file_exists(fpath)
        return fpath.stat().st_size
    except FileNotFoundError:
        return 0
