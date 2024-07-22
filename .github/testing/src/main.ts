import { List } from 'immutable';
import * as affected from './affected';
import * as git from './git';
import { global } from './config/global';
import { python } from './config/python';

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
      .map((tests, pkg) => ({ package: pkg, tests: tests }))
      .values()
  ),
};
console.log(JSON.stringify(strategyMatrix));
