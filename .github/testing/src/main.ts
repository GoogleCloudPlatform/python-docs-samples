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

import {Map, List} from 'immutable';
import * as affected from './affected';
import * as git from './git';
import {global} from './config/global';
import {python} from './config/python';

const language =
  process.argv.length > 2 //
    ? process.argv[2]
    : '<undefined>';

const diffsCommit =
  process.argv.length > 3 //
    ? process.argv[3]
    : git.branchName();

const baseCommit =
  process.argv.length > 4 //
    ? process.argv[4]
    : 'main';

const diffs = git.diffs(diffsCommit, baseCommit).filter(global.matchFile);

const config = Map({
  python: python,
}).get(language);

if (!config) {
  throw `unsupported language: ${language}`;
}

const affectedTests = List(
  diffs
    .filter(config.matchFile)
    .map(config.changes)
    .groupBy(change => change.package)
    .map(change => change.map(pkg => pkg.affected))
    .map(affected.merge)
    .map((tests, pkg) => ({package: pkg, ...tests}))
    .values()
);

console.log(JSON.stringify(affectedTests));
