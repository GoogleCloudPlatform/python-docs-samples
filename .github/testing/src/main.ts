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

import * as git from './git';
import { Config } from './config';
import { python } from './config/python';
import { Affected } from './affected';

function getConfig(lang: string): Config {
  switch (lang) {
    case 'python':
      return python;
  }
  throw `unsupported language: ${lang}`;
}

function main(command: string) {
  switch (command) {
    case 'affected': {
      const config = getConfig(process.argv[3]);
      const head = process.argv[4] || git.branchName();
      const main = process.argv[5] || 'main';
      const affected = config.affected(head, main);
      console.log(JSON.stringify(affected));
      return;
    }
    case 'tests': {
      const config = getConfig(process.argv[3]);
      const affected: Affected = JSON.parse(process.env[process.argv[4]] || "");
      config.test(affected);
      return;
    }
  }
  throw `unsupported command: ${command}`;
}

main(process.argv[2]);
