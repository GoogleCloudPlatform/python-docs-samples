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

import { spawnSync } from 'child_process';

export function run(cmd: string, args: string[]) {
  const p = spawnSync(cmd, args, { stdio: 'inherit' });
  process.exitCode = p.status || undefined;
}

export function output(cmd: string, args: string[]): string {
  const p = spawnSync(cmd, args);
  process.exitCode = p.status || undefined;
  return p.stdout.toString().trim();
}

