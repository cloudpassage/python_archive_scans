#!/usr/bin/python
# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread


class QueuesController(object):
    def __init__(self):
        self.threads = 5
        self.queues = {
            'files': Queue(maxsize=0),
            'scans': Queue(maxsize=0)
        }

    def setup_thread(self, do_work):
        for i in range(self.threads):
            worker = Thread(target=do_work)
            worker.setDaemon(True)
            worker.start()

    def peek(self, queue):
        return self.queues[queue].get()

    def enqueue(self, queue, data):
        self.queues[queue].put(data)

    def dequeue(self, queue):
        self.queues[queue].task_done()

    def shutdown(self, queue):
        self.queues[queue].join()
