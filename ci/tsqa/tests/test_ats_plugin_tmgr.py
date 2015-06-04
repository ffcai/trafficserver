#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import requests
import helpers
import tsqa.test_cases
import tsqa.utils


class TestPluginTrafficManager(helpers.EnvironmentCase):
    @classmethod
    def setUpEnv(cls, env):
        cls.configs['remap.config'].add_line('map / http://origin.yahoo.com')
        cls.configs['plugin.config'].add_line('ats_plugin_tmgr.so -d /tmp/dir /tmp/grp')

    def test_filter_sample_bcookie(self):
        server_ports = self.configs['records.config']['CONFIG']['proxy.config.http.server_ports']

        headers1 = {'Cookie': 'B=bqfno1habsafl&b=4&d=xVBu5qNpYEJ5gR3CUS8mPw--&s=fg&i=ttbuwSrAil6n_MkkOdk'}
        headers2 = {'Cookie': 'B=9ojoklpa7nlok&b=4&d=xVBu5qNpYEJ5gR3CUS8mPw--&s=au&i=Wod_3yvRw43V47J_hTFL'}

        r = requests.get('http://127.0.0.1:{0}/get'.format(server_ports), headers=headers1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['url'], 'http://origin.yahoo.com/get')

        r = requests.get('http://127.0.0.1:{0}/get'.format(server_ports), headers=headers2)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['url'], 'https://origin.yahoo.com/get')
