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
