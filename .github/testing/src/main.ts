import * as git from './git';
import { Affected } from './affected';
import { global } from './config/global';
import { python } from './config/python';

function mergeAffected(affected: Affected[]): Affected[] {
  console.log("TODO: main.ts:mergeAffected")
  return affected;
}

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

const affectedPython = mergeAffected(
  diffs //
    .filter(python.matchFile)
    .map(python.affected)
);

console.log('affectedPython:', affectedPython);
