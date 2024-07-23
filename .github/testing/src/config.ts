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
import { List, Map, Set } from 'immutable';
import { minimatch } from 'minimatch'; /* eslint-disable  @typescript-eslint/no-explicit-any */
import {
  Affected,
  PackageName,
  TestAll,
  TestName,
  TestPath,
  mergeAffected,
} from './affected';

export class Config {
  match: List<string>;
  ignore: List<string>;
  packageFile: List<string>;
  testAll: (path: PackageName) => void;
  testSome: (path: PackageName, tests: Map<TestPath, Set<TestName>>) => void;

  constructor({
    match,
    ignore,
    packageFile,
    testAll,
    testSome,
  }: {
    match?: string[];
    ignore?: string[];
    packageFile?: string[];
    testAll?: (path: PackageName) => void;
    testSome?: (path: PackageName, tests: Map<TestPath, Set<TestName>>) => void;
  }) {
    this.match = List(match || ['**']);
    this.ignore = List(ignore);
    this.packageFile = List(packageFile);
    this.testAll = testAll || (path => { });
    this.testSome = testSome || ((path, tests) => { });
  }

  affected = (head: string, main: string): List<Affected> =>
    List(
      git
        .diffs(head, main)
        .filter(this.matchFile)
        .map(this.findAffected)
        .groupBy(affected => affected.path)
        .map((affected, path) => mergeAffected(path, affected))
        .values()
    );

  test = (affected: Affected) => {
    const cwd = process.cwd()
    process.chdir(git.root())
    if ('TestAll' in affected) {
      this.testAll(affected.path)
    }
    if ('TestSome' in affected) {
      this.testSome(affected.path, affected.TestSome)
    }
    process.chdir(cwd)
  }

  matchFile = (diff: git.Diff): boolean =>
    this.match.some(p => minimatch(diff.filename, p)) &&
    this.ignore.some(p => !minimatch(diff.filename, p));

  findAffected = (diff: git.Diff): Affected => {
    const path = this.findPackage(diff.filename)
    return TestAll(path) // TOOD: discover affected tests only
  }

  findPackage = (filename: string): string => {
    const dir = path.dirname(filename);
    if (dir === '.' || this.isPackage(dir)) {
      return dir;
    }
    return this.findPackage(dir);
  };

  isPackage = (dir: string): boolean =>
    this.packageFile.some(file =>
      fs.existsSync(path.join(git.root(), dir, file))
    );
}
