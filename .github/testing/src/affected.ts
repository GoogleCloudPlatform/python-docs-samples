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

import { Map, List, Set } from 'immutable';

export type PackageName = string;
export type TestPath = string;
export type TestName = string;

export const TestAll = (path: string): Affected => ({ path: path, TestAll: null });
export const TestSome = (path: string, tests: Map<TestPath, Set<TestName>>): Affected => ({
  path: path,
  TestSome: tests,
});
export type Affected =
  | { path: string, TestAll: null }
  | { path: string, TestSome: Map<TestPath, Set<TestName>> };

export function mergeAffected(path: string, affected: List<Affected>): Affected {
  return affected.reduce((result, current) => {
    if ('TestSome' in result && 'TestSome' in current) {
      return TestSome(
        path,
        result.TestSome.mergeWith((xs, ys) => xs.union(ys), current.TestSome)
      );
    }
    return TestAll(path);
  }, TestSome(path || '', Map()));
}
