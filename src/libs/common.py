# coding=utf-8

from hashlib import md5
import time


def create_uuid(*args):
    id = md5()
    timestamp = time.time()
    m_str = None
    if args:
        m_str = '%s%f' % (''.join(args).encode('utf-8'), timestamp)
    else:
        m_str = '%f' % timestamp
    m_str = m_str.encode('utf-8')
    id.update(m_str)
    id = id.hexdigest()[8:-8].strip().lower()
    return id


def get_device_uuid(m_sn=None):
    m = md5()
    m.update(m_sn.upper())
    uuid = m.hexdigest()[8:-8].lower()

    return uuid
