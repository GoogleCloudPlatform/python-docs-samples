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

import * as fs from 'node:fs';
import * as git from './git';
import * as path from 'path';
import {Change, TestAll} from './affected';
import {List} from 'immutable';
import {minimatch} from 'minimatch'; /* eslint-disable  @typescript-eslint/no-explicit-any */

export class Config {
  match: List<string>;
  ignore: List<string>;
  packageConfig: List<string>;

  constructor({
    match,
    ignore,
    packageConfig,
  }: {
    match?: string[];
    ignore?: string[];
    packageConfig?: string[];
  }) {
    this.match = List(match || ['**']);
    this.ignore = List(ignore || []);
    this.packageConfig = List(packageConfig || []);
  }

  matchFile = (diff: git.Diff): boolean =>
    this.match.some(p => minimatch(diff.filename, p)) &&
    this.ignore.some(p => !minimatch(diff.filename, p));

  changes = (diff: git.Diff): Change => ({
    package: this.findPackage(diff.filename),
    affected: TestAll(), // TOOD: discover affected tests
  });

  findPackage = (filename: string): string => {
    const dir = path.dirname(filename);
    if (dir === '.' || this.isPackage(dir)) {
      return dir;
    }
    return this.findPackage(dir);
  };

  isPackage = (dir: string): boolean =>
    this.packageConfig.some(file =>
      fs.existsSync(path.join(git.root(), dir, file))
    );
}
