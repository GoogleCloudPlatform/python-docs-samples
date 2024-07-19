import * as fs from 'node:fs';
import * as path from 'path';
import {minimatch} from 'minimatch'; /* eslint-disable  @typescript-eslint/no-explicit-any */
import * as git from './git';

// AffectedTests = TestAll | TestSome {String: String[]}
export type AffectedTests = TestAll | TestSome;
export interface TestAll {
  tag: 'TestAll';
}
export interface TestSome {
  tag: 'TestSome';
  values: Map<string, string[]>; // {path: testNames}
}

export type Affected = {
  package: string;
  tests: AffectedTests;
};

export class Config {
  match: string[];
  ignore: string[];
  packageConfig: string[];

  constructor({match, ignore, packageConfig}: any) {
    this.match = match || ['**'];
    this.ignore = ignore || [];
    this.packageConfig = packageConfig || [];
  }

  matchFile = (diff: git.Diff): boolean =>
    this.match.some(p => minimatch(diff.filename, p)) &&
    this.ignore.some(p => !minimatch(diff.filename, p));

  affected = (diff: git.Diff): Affected => ({
    package: this.findPackage(diff.filename),
    tests: {tag: 'TestAll'}, // TODO: discover affected tests
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
