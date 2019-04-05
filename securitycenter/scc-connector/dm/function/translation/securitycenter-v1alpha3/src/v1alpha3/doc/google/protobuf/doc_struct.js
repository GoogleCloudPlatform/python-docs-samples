// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Note: this file is purely for documentation. Any contents are not expected
// to be loaded as the JS file.

/**
 * `Struct` represents a structured data value, consisting of fields
 * which map to dynamically typed values. In some languages, `Struct`
 * might be supported by a native representation. For example, in
 * scripting languages like JS a struct is represented as an
 * object. The details of that representation are described together
 * with the proto support for the language.
 *
 * The JSON representation for `Struct` is JSON object.
 *
 * @property {Object.<string, Object>} fields
 *   Unordered map of dynamically typed values.
 *
 * @typedef Struct
 * @memberof google.protobuf
 * @see [google.protobuf.Struct definition in proto format]{@link https://github.com/google/protobuf/blob/master/src/google/protobuf/struct.proto}
 */
var Struct = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * `Value` represents a dynamically typed value which can be either
 * null, a number, a string, a boolean, a recursive struct value, or a
 * list of values. A producer of value is expected to set one of that
 * variants, absence of any variant indicates an error.
 *
 * The JSON representation for `Value` is JSON value.
 *
 * @property {number} nullValue
 *   Represents a null value.
 *
 *   The number should be among the values of [NullValue]{@link google.protobuf.NullValue}
 *
 * @property {number} numberValue
 *   Represents a double value.
 *
 * @property {string} stringValue
 *   Represents a string value.
 *
 * @property {boolean} boolValue
 *   Represents a boolean value.
 *
 * @property {Object} structValue
 *   Represents a structured value.
 *
 *   This object should have the same structure as [Struct]{@link google.protobuf.Struct}
 *
 * @property {Object} listValue
 *   Represents a repeated `Value`.
 *
 *   This object should have the same structure as [ListValue]{@link google.protobuf.ListValue}
 *
 * @typedef Value
 * @memberof google.protobuf
 * @see [google.protobuf.Value definition in proto format]{@link https://github.com/google/protobuf/blob/master/src/google/protobuf/struct.proto}
 */
var Value = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * `ListValue` is a wrapper around a repeated field of values.
 *
 * The JSON representation for `ListValue` is JSON array.
 *
 * @property {Object[]} values
 *   Repeated field of dynamically typed values.
 *
 *   This object should have the same structure as [Value]{@link google.protobuf.Value}
 *
 * @typedef ListValue
 * @memberof google.protobuf
 * @see [google.protobuf.ListValue definition in proto format]{@link https://github.com/google/protobuf/blob/master/src/google/protobuf/struct.proto}
 */
var ListValue = {
  // This is for documentation. Actual contents will be loaded by gRPC.
};

/**
 * `NullValue` is a singleton enumeration to represent the null value for the
 * `Value` type union.
 *
 *  The JSON representation for `NullValue` is JSON `null`.
 *
 * @enum {number}
 * @memberof google.protobuf
 */
var NullValue = {

  /**
   * Null value.
   */
  NULL_VALUE: 0
};