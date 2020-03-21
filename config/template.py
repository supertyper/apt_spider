#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao


from utils.datatype import AttribDict


LogPath = "./logs/"

# global variables here
# config params and settings
config = AttribDict()

#  paths
path = dict()


az = AttribDict()


# proxy
proxys = []

# ioc_mod
ioc_ip = {
	'ip': '',
	'apt_organization': [],
	'category': [],
	'disclosure_time': '',
	'reference': '',
	'subscribe_vendor': '',
	'verify': []
}

ioc_domain = {
    'domain': '',
	'apt_organization': [''],
	'category': [''],
	'disclosure_time': '',
	'reference': '',
	'subscribe_vendor': '',
	'verify': []
}

ioc_url = {
    'url': '',
	'apt_organization': [''],
	'category': [''],
	'disclosure_time': '',
	'reference': '',
	'subscribe_vendor': '',
	'verify': []   
}

ioc_hash = {
    'file_name': '',
	'md5': '',
	'sha1': '',
	'sha256': '',
	'file_type': '',
	'file_size': None,
	'file_names': [],
	'apt_organization': [],
	'category': [],
	'disclosure_time': '',
	'reference': '',
	'subscribe_vendor': '',
	'verify': []
}

ioc_mail = {
    'email': '',
	'apt_organization': [],
	'category': [],
	'disclosure_time': '',
	'reference': '',
	'subscribe_vendor': '',
	'verify': []
}

ioc_ssl = {
    'ssl': '',
	'apt_organization': [],
	'category': [],
	'disclosure_time': '',
	'reference': '',
	'subscribe_vendor': '',
	'verify': []
}