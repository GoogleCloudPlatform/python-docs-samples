import 'core-js/actual';

import * as git from './git';
import { Affected } from './affected';
import { global } from './config/global';
import { python } from './config/python';

function zipWith<a, b, c>(f: (x: a, y: b) => c, xs: a[], ys: b[]): c[] {
  return xs.map((x, i) => f(x, ys[i]));
}

function zip<a, b>(xs: a[], ys: b[]): [a, b][] {
  return zipWith((x, y) => [x, y], xs, ys);
}

function mapMap<k, a, b>(kvs: Map<k, a>, f: (k: k, x: a) => b): Map<k, b> {
  const keys = [...kvs.keys()];
  const values = zipWith((k, vs) => f(k, vs), keys, [...kvs.values()]);
  return new Map(zip(keys, values));
}

function groupBy<k, a, b>(xs: a[], key: (x: a) => k, merge: (xs: a[]) => b): Map<k, b> {
  return mapMap(Map.groupBy(xs, key), (_, vs) => merge(vs))
}

function groupByPackage(affected: Affected[]): Affected[] {
  const packages = groupBy(
    affected,
    x => x.package,
    xs => xs.flatMap(x => x.tests)
  );
  return affected;
}

const affected = [
  { package: 'language/v2', tests: { tag: 'TestAll' } },
  { package: 'language/v2', tests: { tag: 'TestAll' } },
];

const diffsCommit =
  process.argv.length > 2 //
    ? process.argv[2]
    : git.branchName();

const baseCommit =
  process.argv.length > 3 //
    ? process.argv[3]
    : 'main';

const diffs = git //
  .diffs(diffsCommit, baseCommit)
  .filter(global.matchFile);

const affectedPython = groupByPackage(
  diffs //
    .filter(python.matchFile)
    .map(python.affected)
);

console.log('affectedPython:', affectedPython);
