import re
import cloudpassage
import os
from config import CONFIG


class ApiController():
    def build_http_session(self):
        key_id = os.environ['KEY_ID'] or CONFIG['key_id']
        secret_key = os.environ['SECRET_KEY'] or CONFIG['secret_key']
        integration_string = self.get_integration_string()
        session = cloudpassage.HaloSession(key_id,
                                           secret_key,
                                           integration_string=integration_string)
        return cloudpassage.HttpHelper(session)

    def get(self, endpoint):
        return self.build_http_session().get(endpoint)

    def find_primary_key(self, keys):
        blacklist = set(['count', 'pagination'])
        primary_key = list(set(keys) - blacklist)[0]
        return primary_key

    def get_paginated(self, endpoint, **kwargs):
        aggregate_result = []
        endpoint = endpoint + self.form_filter(**kwargs)
        index = self.get(endpoint)
        primary_key = self.find_primary_key(index.keys())
        while "pagination" in index:
            aggregate_result.extend(index[primary_key])
            if "next" in index["pagination"]:
                index = self.get(self.parse_next_endpoint(index["pagination"]["next"]))
            else:
                index[primary_key] = aggregate_result
                return index
        return self.get(endpoint)

    def parse_next_endpoint(self, next_url):
        return re.sub(r'^h.+om(:\d*)?', "", next_url)

    def form_filter(self, **kwargs):
        filter_list = []
        for filt in kwargs:
            if type(kwargs[filt]) is list:
                filter_list.append("%s=%s" % (filt, ','.join(kwargs[filt])))
            elif kwargs[filt]:
                filter_list.append("%s=%s" % (filt, kwargs[filt]))
        return "?%s" % ("&".join(filter_list))

    def get_integration_string(self):
        """Return integration string for this tool."""
        return "python_archive_scans/%s" % self.get_tool_version()

    def get_tool_version(self):
        """Get version of this tool from the __init__.py file."""
        here_path = os.path.abspath(os.path.dirname(__file__))
        init_file = os.path.join(here_path, "__init__.py")
        ver = 0
        with open(init_file, 'r') as i_f:
            rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
            ver = rx_compiled.search(i_f.read()).group(1)
        return ver

