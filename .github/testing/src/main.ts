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

import {List} from 'immutable';
import * as affected from './affected';
import * as git from './git';
import {global} from './config/global';
import {python} from './config/python';

const diffsCommit =
  process.argv.length > 2 //
    ? process.argv[2]
    : git.branchName();

const baseCommit =
  process.argv.length > 3 //
    ? process.argv[3]
    : 'main';

const diffs = git.diffs(diffsCommit, baseCommit).filter(global.matchFile);

const strategyMatrix = {
  python: List(
    diffs
      .filter(python.matchFile)
      .map(python.changes)
      .groupBy(change => change.package)
      .map(change => change.map(pkg => pkg.affected))
      .map(affected.merge)
      .map((tests, pkg) => ({package: pkg, tests: tests}))
      .values()
  ),
};
console.log(JSON.stringify(strategyMatrix));
