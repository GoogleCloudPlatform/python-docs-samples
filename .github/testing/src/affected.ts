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

import {Map, List, Set} from 'immutable';

export type PackageName = string;
export type TestPath = string;
export type TestName = string;

export interface TestAll {
  tag: 'TestAll';
}
export const TestAll = (): Affected => ({tag: 'TestAll'});
export interface TestSome {
  tag: 'TestSome';
  tests: Map<TestPath, Set<TestName>>;
}
export const TestSome = (tests: Map<TestPath, Set<TestName>>): Affected => ({
  tag: 'TestSome',
  tests: tests,
});
export type Affected = TestAll | TestSome;

export type Change = {package: PackageName; affected: Affected};

export function merge(affected: List<Affected>): Affected {
  return affected.reduce((result, current) => {
    if (result.tag === 'TestSome' && current.tag === 'TestSome') {
      return TestSome(
        result.tests.mergeWith((xs, ys) => xs.union(ys), current.tests)
      );
    }
    return TestAll();
  }, TestSome(Map()));
}
