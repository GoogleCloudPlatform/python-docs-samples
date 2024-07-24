// Copyright 2024 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import * as path from 'path'
import * as subprocess from '../subprocess';
import { Config } from '../config';

export const python = new Config({
  match: ['**'],
  ignore: ['**/README.md'],
  packageFile: [
    'noxfile_config.py',
    'requirements.txt',
    'pyproject.toml',
    'setup.py',
    'setup.cfg',
  ],
  testAll: args => {
    subprocess.run('cp', [path.join(args.root, 'noxfile-template.py'), 'noxfile.py'])
    subprocess.run('nox', ['-s', 'py-3.11']);
  },
  testSome: args => {
    subprocess.run('cp', [path.join(args.root, 'noxfile-template.py'), 'noxfile.py'])
    throw `TODO: config/python.ts testSome ${JSON.stringify(args)}`;
  },
});
