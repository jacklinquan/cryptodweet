# -*- coding: utf-8 -*-
"""A simple python package for the free dweet service with encryption.

Dweet is a simple machine-to-machine (M2M) service from https://dweet.io/ .
The free service is public and any data is accessible by anyone.
This package adds encryption to it and make it a bit more secure.
Only the minimal APIs are supported.
Only bytes and str types are supported.

Author: Quan Lin
License: MIT
Requires: dweepy, cryptomsg

:Example:
>>> from cryptodweet import CryptoDweet
>>> cd = CryptoDweet('YOUR KEY')
>>> cd.dweet_for('YOUR THING', {'YOUR DATA': 'YOUR VALUE'})
{u'content': {u'8c94428bc640de621c7c3ceea1d00b96': u'05d6f2dbc1ce3afa7e6072c0c4
c6f6a7'}, u'thing': u'9ee9b47833d5a13043c5f47e8802596a', u'transaction': u'd45a
1e08-fc5c-49b6-a9c5-7ee87713c059', u'created': u'2019-02-10T21:59:34.270Z'}
>>> cd.get_latest_dweet_for('YOUR THING')
[{u'content': {u'YOUR DATA': u'YOUR VALUE'}, u'thing': u'YOUR THING', u'created
': u'2019-02-10T21:59:34.270Z'}]
"""

# Project version
__version__ = '0.2.0'
__all__ = ['CryptoDweet']

from codecs import encode, decode
from binascii import hexlify, unhexlify
import dweepy
from cryptomsg import CryptoMsg

def to_bytes(msg):
    """Convert to bytes with utf_8 codec.
    
    :param msg: the message to convert.
    :type msg: bytes, str(unicode).
    :returns: bytes with utf_8 codec.
    :rtype: bytes
    """
    if isinstance(msg, bytes):
        return msg
    else:
        return encode(msg, 'utf_8')

def from_bytes(msg):
    """Convert to unicode with utf_8 codec.
    
    :param msg: the message to convert.
    :type msg: bytes, str(unicode).
    :returns: unicode string with utf_8 codec.
    :rtype: str(unicode)
    """
    if isinstance(msg, bytes):
        return decode(msg, 'utf_8')
    else:
        return msg
        
class CryptoDweet(object):
    """A class for the free dweet service with encryption.
    
    Initialization options:
        # With default key and iv, not secure.
        CryptoDweet()
        # Only set key, and iv is the same as key.
        CryptoDweet('YOUR KEY')
        # Set both key and iv, strongest encryption. 
        CryptoDweet('YOUR KEY', 'YOUR IV')
        
    The given key is padded with space to 16 bytes (if shorter than 16 bytes)
    or padded with space to 32 bytes (if length is between 16 and 32)
    or truncated to 32 bytes (if longer than 32 bytes).
    The given iv is padded with space or truncated to 16 bytes.
    """
    def __init__(self, aes_cbc_key=b'aes_cbc_key', aes_cbc_iv=None):
        self.aes_cbc_key = aes_cbc_key
        if aes_cbc_iv is None:
            self.aes_cbc_iv = self.aes_cbc_key
        else:
            self.aes_cbc_iv = aes_cbc_iv
    
    def dweet_for(self, thing, content_dict):
        """The 'dweet for' API.
        
        :param thing: the thing name.
        :param content_dict: the thing content.
        :type thing: bytes, str.
        :type content_dict: dict with key-value pairs of bytes or str type.
        :returns: the 'dweet for' result.
        :rtype: dict
        """
        cm = CryptoMsg(to_bytes(self.aes_cbc_key), to_bytes(self.aes_cbc_iv))
        thing_cipher = cm.encrypt_msg(to_bytes(thing))
        thing_cipher_hexlified = from_bytes(hexlify(thing_cipher))
        
        content_dict_cipher = {
            cm.encrypt_msg(to_bytes(k)): cm.encrypt_msg(to_bytes(v)) \
            for (k, v) in content_dict.items()
        }
        content_dict_cipher_hexlified = {
            from_bytes(hexlify(k)): from_bytes(hexlify(v)) \
            for (k, v) in content_dict_cipher.items()
        }
        
        return dweepy.dweet_for(
            thing_cipher_hexlified,
            content_dict_cipher_hexlified
        )
       
    def get_latest_dweet_for(self, thing):
        """The 'get latest dweet for' API.
        
        :param thing: the thing name.
        :type thing: bytes, str.
        :returns: the 'get latest dweet for' result.
        :rtype: list
        """
        cm = CryptoMsg(to_bytes(self.aes_cbc_key), to_bytes(self.aes_cbc_iv))
        thing_cipher = cm.encrypt_msg(to_bytes(thing))
        thing_cipher_hexlified = from_bytes(hexlify(thing_cipher))
        
        dweets_list_cipher_hexlified = \
            dweepy.get_latest_dweet_for(thing_cipher_hexlified)
        
        dweets_list = []
        for cipher_dweet in dweets_list_cipher_hexlified:
            content_dict_cipher_hexlified = \
                cipher_dweet['content']
            content_dict_cipher = {
                unhexlify(to_bytes(k)): unhexlify(to_bytes(v)) \
                for (k, v) in content_dict_cipher_hexlified.items()
            }
            content_dict = {
                from_bytes(cm.decrypt_msg(k)): from_bytes(cm.decrypt_msg(v)) \
                for (k, v) in content_dict_cipher.items()
            }
            decrypted_dweet = cipher_dweet
            decrypted_dweet[u'thing'] = from_bytes(thing)
            decrypted_dweet[u'content'] = content_dict
            dweets_list.append(decrypted_dweet)
        
        return dweets_list
        
    def get_dweets_for(self, thing):
        """The 'get dweets for' API.
        
        :param thing: the thing name.
        :type thing: bytes, str.
        :returns: the 'get dweets for' result.
        :rtype: list
        """
        cm = CryptoMsg(to_bytes(self.aes_cbc_key), to_bytes(self.aes_cbc_iv))
        thing_cipher = cm.encrypt_msg(to_bytes(thing))
        thing_cipher_hexlified = from_bytes(hexlify(thing_cipher))
        
        dweets_list_cipher_hexlified = \
            dweepy.get_dweets_for(thing_cipher_hexlified)
        
        dweets_list = []
        for cipher_dweet in dweets_list_cipher_hexlified:
            content_dict_cipher_hexlified = \
                cipher_dweet['content']
            content_dict_cipher = {
                unhexlify(to_bytes(k)) : unhexlify(to_bytes(v)) \
                for (k, v) in content_dict_cipher_hexlified.items()
            }
            content_dict = {
                from_bytes(cm.decrypt_msg(k)): from_bytes(cm.decrypt_msg(v)) \
                for (k, v) in content_dict_cipher.items()
            }
            decrypted_dweet = cipher_dweet
            decrypted_dweet[u'thing'] = from_bytes(thing)
            decrypted_dweet[u'content'] = content_dict
            dweets_list.append(decrypted_dweet)
        
        return dweets_list
    
    