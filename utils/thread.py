#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Power by daMao


from concurrent.futures import ThreadPoolExecutor
import threading


def task_thread(function_name, list_name, workernum=40):
    with ThreadPoolExecutor(workernum) as executor:
        executor.map(function_name, list_name)


def start_thread(function_name, workernum=40):
    with ThreadPoolExecutor(workernum) as executor:
        executor.submit(function_name)
