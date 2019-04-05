'use strict';

// Imports
const JSONStream = require('JSONStream');
const get = require('get-value');
const moment = require('moment');

/**
 * Make a transformation between from and to objects.
 * 
 * @param {!Object} from The partner object from JSON.
 * @param {!Object} to The object which will be sent to CSCC.
 * @param {!String} to_prop_name The property name from to object.
 * @param {!Array<String>} mapped The map to use on transform.
 * @param {!String} org_name The organization name.
 * @param {!Boolean} encloseWithType If enclose property inside type property.
 */
function transform(from, to, to_prop_name, mapped, org_name, encloseWithType) {
    switch (to[to_prop_name].transform) {
        case 'to_array':
            const obj = get(from, to[to_prop_name].path, { default: null });
            to[to_prop_name] = obj ?
                Object.keys(obj).map(prop => {
                    return { [prop]: obj[prop] };
                }) :
                null;
            break;
        case 'mapped_value':
            let val = get(from, to[to_prop_name].path, { default: null });
            to[to_prop_name] = [];
            if (val) {
                if(mapped[val]){
                    to[to_prop_name].push(mapped[val]);
                }
                else{
                    if (val.indexOf("projects/") != -1) {
                        val = val.substr(val.indexOf('projects/') + 9, val.length);
                    }
                    to[to_prop_name].push(val);
                }
            }
            break;
        case 'combined':
            const prefix_org_id = org_name.replace('organizations/', '');
            to[to_prop_name] = prefix_org_id+'-'+to[to_prop_name].paths.map(item => {
                return get(from, item, { default: null });
            })
                .join('#');
            break;
        case 'parse_date':
            // Convert date to google.protobuf.Timestamp format
            const str_date = get(from, to[to_prop_name].path, { default: null });
            if (str_date) {
                const date_in_millis = moment.utc(str_date, to[to_prop_name].format).valueOf();
                to[to_prop_name] = convertToTimestamp(date_in_millis);
            } else {
                to[to_prop_name] = null;
            }
            break;
        case 'time_already_in_millis':
            // Convert date to google.protobuf.Timestamp format
            const date_in_millis = get(from, to[to_prop_name].path, { default: null });
            if (date_in_millis) {
                to[to_prop_name] = convertToTimestamp(date_in_millis);
            } else {
                to[to_prop_name] = null;
            }
            break;
        case 'time_to_millis':
            // Convert date to google.protobuf.Timestamp format
            const date = get(from, to[to_prop_name].path, { default: null });
            if (date) {
                const unit = to[to_prop_name].unit;
                const date_in_millis = date / unit;
                to[to_prop_name] = convertToTimestamp(date_in_millis);
            } else {
                to[to_prop_name] = null;
            }
            break;
        case 'cloudflare_category':
            const original_category = get(from, to[to_prop_name].path, { default: null });
            if (original_category) {
                to[to_prop_name] = original_category;
            } else {
                let action = get(from, 'action', { default: null });
                let rule_info = get(from, 'rule_info', { default: null });
                to[to_prop_name] = [action, 'rule', rule_info.type, rule_info.value].join(', ');
            }
            break;
        case 'to_array_asset_ids':
            let value = get(from, to[to_prop_name].path, { default: null });
            to[to_prop_name] = [];
            if (value) {
                if (value.indexOf("projects/") != -1) {
                    value = value.substr(value.indexOf('projects/') + 9, value.length);
                }
                to[to_prop_name].push(value);
            }
            break;
        case 'concat_organization_id':
            const id = get(from, to[to_prop_name].path, { default: null });
            const org_id = org_name.replace('organizations/','');
            const compose_org_id = org_id+'-'+id
            to[to_prop_name] = compose_org_id
            break;
        default:
            to[to_prop_name] = get(from, to[to_prop_name], { default: null });
            break;
    }

    if (encloseWithType) {
        let to_enclose = to[to_prop_name] || 'BLANK';
        if (!(to_enclose instanceof String) && typeof to_enclose != 'string') {
            to_enclose = JSON.stringify(to_enclose);
        } 
        to[to_prop_name] = {stringValue: to_enclose};
    }
}

function convertToTimestamp(date_in_millis) {
    return {
        seconds: Math.trunc(date_in_millis / 1000),
        nanos: Math.trunc((date_in_millis % 1000) * 1000000)
    }
}

/**
 * Make a deep navigation on data object to get fields to populate finding object.
 * If data object has a inner array with fields, it makes a recursive navigation until ends the fields to populate.
 * 
 * @param {!Object} data The data object read from JSON.
 * @param {!Array<String>} levels The levels to navigate in data object.
 * @param {!Array<Object>} output Array to add mapped objects.
 * @param {!Object} baseObject The base object to be populated with mapped fields.
 * @param {!Object} mapper The mapper to use on parse.
 */
function deepMapping(data, levels, output, baseObject, mapper) {
    if (!levels || !levels.length) {
        // Mapping JSON fields to API fields
        const prop = JSON.parse(baseObject);
        for (let propKey in prop) {
            if (propKey === 'properties') {
                const finding_properties = prop[propKey]
                prop[propKey] = {fields: finding_properties};
                for (let fpKey in finding_properties) {
                    transform(data, finding_properties, fpKey, mapper.mapped_ips, mapper.org_name, true);
                }
                finding_properties['scc_status'] =  {stringValue: 'ACTIVE'};
                finding_properties['scc_source_category_id'] = {stringValue: prop['category']};
            } else {
                transform(data, prop, propKey, mapper.mapped_ips,mapper.org_name);
            }
        }
        output.push(Object.assign(prop, mapper.fixed_fields));
    } else {
        const level = levels.shift();
        const items = data[level];
        data[level] = undefined;
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (item instanceof Object) {
                deepMapping(Object.assign(data, item), levels, output, baseObject, mapper);
            } else {
                // Resolve non Object item like Array<String> of finding_id
                data[level] = item;
                deepMapping(data, levels, output, baseObject, mapper);
            }
        }
    }
}

/**
 * Handle the contents from JSON file.
 * 
 * @param {!ReadStream} contents The file contents.
 * @param {!Object} mapper The mapper to use on parse.
 * @returns Returns a Promise.
 */
function handle(contents, mapper) {
    return new Promise((resolve, reject) => {
        const baseObject = JSON.stringify(mapper.api_to_fields);

        const output = [];
        const parser = JSONStream.parse(mapper.root_element)
            .on('data', data => {
                if (!Array.isArray(data)) {
                    const levels = mapper.deep_levels ? mapper.deep_levels.slice() : null;
                    deepMapping(data, levels, output, baseObject, mapper);
                } else {
                    for (let i = 0; i < data.length; i++) {
                        const levels = mapper.deep_levels ? mapper.deep_levels.slice() : null;
                        deepMapping(data[i], levels, output, baseObject, mapper);
                    };
                }
            })
            .on('end', () => {
                console.log(JSON.stringify(output));
                resolve(output);
            })
            .on('error', error => {
                reject(error);
            });
        contents.pipe(parser);
    });
}

module.exports.handle = handle;
