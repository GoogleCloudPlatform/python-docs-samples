// Copyright 2022 Google LLC
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

// [START dataflow_extensible_template_udf]
/**
 * User-defined function (UDF) to transform events
 * as part of a Dataflow template job.
 *
 * @param {string} inJson input Pub/Sub JSON message (stringified)
 */
 function process(inJson) {
    // Nashorn engine is only ECMAScript 5.1 (ES5) compliant. Newer ES6
    // JavaScript keywords like `let` or `const` will cause syntax errors.
    var obj = JSON.parse(inJson);
    var includePubsubMessage = obj.data && obj.attributes;
    var data = includePubsubMessage ? obj.data : obj;

    if (!data.hasOwnProperty('url')) {
      throw new Error("No url found");
    } else if (data.url !== "https://beam.apache.org/") {
      throw new Error("Unrecognized url");
    }

    return JSON.stringify(obj);
  }
// [END dataflow_extensible_template_udf]
