"""A python module for very basic APIs of the free dweet service with encryption.

- Author: Quan Lin
- License: MIT
"""

__version__ = "0.3.0"
__all__ = ["CryptoDweet"]

from binascii import hexlify, unhexlify
import basicdweet
from cryptomsg import CryptoMsg

BASE_URL = "https://dweet.io"


def to_bytes(msg: str) -> bytes:
    """Convert to `bytes` with `utf_8` codec.

    Args:
        msg:
            The message to convert.

    Returns:
        Message bytes with `utf_8` codec.
    """
    return msg if isinstance(msg, bytes) else msg.encode("utf-8")


def from_bytes(msg: bytes) -> str:
    """Convert to `str` with `utf_8` codec.

    Args:
        msg:
            The message bytes to convert.

    Returns:
        Message string with `utf_8` codec.
    """
    return msg.decode("utf-8") if isinstance(msg, bytes) else msg


class CryptoDweet:
    """A class for the free dweet service with encryption.

    Initialization options:

    - `CryptoDweet()`: With default key and iv, not secure.
    - `CryptoDweet("YOUR KEY")`: Only set key, and iv is the same as key.
    - `CryptoDweet("YOUR KEY", "YOUR IV")`: Set both key and iv, strongest encryption.

    The given key is padded with space to 16 bytes (if shorter than 16 bytes)
    or padded with space to 32 bytes (if length is between 16 and 32)
    or truncated to 32 bytes (if longer than 32 bytes).
    The given iv is padded with space or truncated to 16 bytes.

    Args:
        aes_cbc_key:
            The key of AES CBC mode.
        aes_cbc_iv:
            The IV of AES CBC mode.
        base_url:
            The base url of the dweet server.
    """

    def __init__(
        self,
        aes_cbc_key: bytes = b"aes_cbc_key",
        aes_cbc_iv: bytes = None,
        base_url: str = BASE_URL,
    ):
        self.aes_cbc_key = aes_cbc_key
        if aes_cbc_iv is None:
            self.aes_cbc_iv = self.aes_cbc_key
        else:
            self.aes_cbc_iv = aes_cbc_iv

        self.base_url = base_url

    def dweet_for(self, thing: str, content_dict: dict) -> dict:
        """The 'dweet for' API.

        Args:
            thing:
                The thing name.
            content_dict:
                The content dict.

        Returns:
            The result dict of 'dweet for' API.
        """
        cm = CryptoMsg(to_bytes(self.aes_cbc_key), to_bytes(self.aes_cbc_iv))
        thing_cipher = cm.encrypt_msg(to_bytes(thing))
        thing_cipher_hexlified = from_bytes(hexlify(thing_cipher))

        content_dict_cipher = {
            cm.encrypt_msg(to_bytes(k)): cm.encrypt_msg(to_bytes(v))
            for (k, v) in content_dict.items()
        }
        content_dict_cipher_hexlified = {
            from_bytes(hexlify(k)): from_bytes(hexlify(v))
            for (k, v) in content_dict_cipher.items()
        }

        return basicdweet.dweet_for(
            thing_cipher_hexlified,
            content_dict_cipher_hexlified,
            base_url=self.base_url,
        )

    def get_latest_dweet_for(self, thing: str) -> list:
        """The 'get latest dweet for' API.

        Args:
            thing:
                The thing name.

        Returns:
            The result list of dict of 'get latest dweet for' API.
        """
        cm = CryptoMsg(to_bytes(self.aes_cbc_key), to_bytes(self.aes_cbc_iv))
        thing_cipher = cm.encrypt_msg(to_bytes(thing))
        thing_cipher_hexlified = from_bytes(hexlify(thing_cipher))

        dweets_list_cipher_hexlified = basicdweet.get_latest_dweet_for(
            thing_cipher_hexlified,
            base_url=self.base_url,
        )

        dweets_list = []
        for cipher_dweet in dweets_list_cipher_hexlified:
            content_dict_cipher_hexlified = cipher_dweet["content"]
            content_dict_cipher = {
                unhexlify(to_bytes(k)): unhexlify(to_bytes(v))
                for (k, v) in content_dict_cipher_hexlified.items()
            }
            content_dict = {
                from_bytes(cm.decrypt_msg(k)): from_bytes(cm.decrypt_msg(v))
                for (k, v) in content_dict_cipher.items()
            }
            decrypted_dweet = cipher_dweet
            decrypted_dweet["thing"] = from_bytes(thing)
            decrypted_dweet["content"] = content_dict
            dweets_list.append(decrypted_dweet)

        return dweets_list

    def get_dweets_for(self, thing: str) -> list:
        """The 'get dweets for' API.

        Args:
            thing:
                The thing name.

        Returns:
            The result list of dict of 'get dweets for' API.
        """
        cm = CryptoMsg(to_bytes(self.aes_cbc_key), to_bytes(self.aes_cbc_iv))
        thing_cipher = cm.encrypt_msg(to_bytes(thing))
        thing_cipher_hexlified = from_bytes(hexlify(thing_cipher))

        dweets_list_cipher_hexlified = basicdweet.get_dweets_for(
            thing_cipher_hexlified,
            base_url=self.base_url,
        )

        dweets_list = []
        for cipher_dweet in dweets_list_cipher_hexlified:
            content_dict_cipher_hexlified = cipher_dweet["content"]
            content_dict_cipher = {
                unhexlify(to_bytes(k)): unhexlify(to_bytes(v))
                for (k, v) in content_dict_cipher_hexlified.items()
            }
            content_dict = {
                from_bytes(cm.decrypt_msg(k)): from_bytes(cm.decrypt_msg(v))
                for (k, v) in content_dict_cipher.items()
            }
            decrypted_dweet = cipher_dweet
            decrypted_dweet["thing"] = from_bytes(thing)
            decrypted_dweet["content"] = content_dict
            dweets_list.append(decrypted_dweet)

        return dweets_list
