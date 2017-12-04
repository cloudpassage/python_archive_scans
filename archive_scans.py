#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.scans_controller import ScansController
from lib.servers_controller import ServersController
from lib.queues_controller import QueuesController
from lib.date_controller import DateController
from lib.options import Options
import lib.file_controller as File
import os


class ArchiveScans(object):
    def __init__(self):
        self.scans = ScansController()
        self.servers = ServersController()
        self.queues = QueuesController()
        self.date = DateController()
        self.opts = Options().params()
        self.path = os.path.join(os.path.dirname(__file__), 'details/')
        self.queues.setup_thread(self.files_consumer)
        self.queues.setup_thread(self.scans_consumer)

    def servers_path(self, path, server):
        return path + "%s_%s/" % (server['hostname'], server['id'])

    def scans_path(self, path, scan):
        return path + "%s_%s_%s_details.txt" % (scan['module'],
                                                scan['id'],
                                                self.date.iso8601(scan['created_at']))

    def files_consumer(self):
        while True:
            scan_data = self.queues.peek('files')
            File.write_file(scan_data['path'], scan_data['data'])
            print "%s_%s" % (scan_data['data']['id'], scan_data['data']['module'])
            self.queues.dequeue('files')

    def scans_consumer(self):
        while True:
            scan_data = self.queues.peek('scans')
            scan_details = self.scans.show(scan_data['scan']['id'])['scan']
            self.queues.enqueue('files', {'path': scan_data['path'], 'data': scan_details})
            self.queues.dequeue('scans')

    def producer(self):
        servers_index = self.servers.index()
        if servers_index['servers']:
            for server in servers_index['servers']:
                server_path = self.servers_path(self.path, server)
                File.write_dir(server_path)

                kwargs = {
                    'server_id': server['id'],
                    'since': self.opts['since'],
                    'until': self.opts['until']
                }

                scans_index = self.scans.index(**kwargs)
                if scans_index['scans']:
                    for scan in scans_index['scans']:
                        scan_path = self.scans_path(server_path, scan)
                        if not os.path.isfile(scan_path):
                            self.queues.enqueue('scans', {'path': scan_path, 'scan': scan})

        self.queues.shutdown('files')
        self.queues.shutdown('scans')

if __name__ == "__main__":
    ArchiveScans().producer()
