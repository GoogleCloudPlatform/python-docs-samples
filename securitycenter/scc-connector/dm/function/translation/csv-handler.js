'use strict';

// Imports
const parse = require('csv-parse');
const moment = require('moment')
const get = require('get-value');
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
        case 'parse_date':
            // Convert date to google.protobuf.Timestamp format
            const str_date = from[to[to_prop_name].path] || null;
            if (str_date) {
                const millis = moment.utc(str_date, to[to_prop_name].format).valueOf();
                to[to_prop_name] = {
                    seconds: millis / 1000,
                    nanos: (millis % 1000) * 1000000
                };
            } else {
                to[to_prop_name] = null;
            }
            break;
        case 'to_array':
            const value = from[to[to_prop_name].path] || null;
            to[to_prop_name] = [];
            if (value) {
                to[to_prop_name].push(value);
            }
            break;
        case 'mapped_value':
            const val = get(from, to[to_prop_name].path, { default: null });
            to[to_prop_name] = [];
            if (val) {
                to[to_prop_name].push(mapped[val])
            }
            break;
        case 'concat_organization_id':
            const id = get(from, to[to_prop_name].path, { default: null });
            const org_id = org_name.replace('organizations/', '');
            const compose_org_id = org_id + '-' + id
            to[to_prop_name] = compose_org_id
            break;
        default:
            to[to_prop_name] = from[to[to_prop_name]] || null;
            break;
    }

    if (encloseWithType) {
        let to_enclose = to[to_prop_name] || 'BLANK';
        if (!(to_enclose instanceof String) && typeof to_enclose != 'string') {
            to_enclose = JSON.stringify(to_enclose);
        }
        to[to_prop_name] = { stringValue: to_enclose };
    }
}

/**
 * Handle the contents from CSV file.
 * 
 * @param {!ReadStream} contents The file contents.
 * @param {!Object} mapper The mapper to use on parse.
 * @returns Returns a Promise.
 */
function handle(contents, mapper) {
    return new Promise((resolve, reject) => {

        const output = [];
        const parser = parse({ delimiter: mapper.delimiter, columns: true })
            .on('readable', () => {
                const baseObject = JSON.stringify(mapper.api_to_columns);
                let data = null;
                while (data = parser.read()) {
                    // Mapping CSV columns to API fields
                    const prop = JSON.parse(baseObject);
                    for (let propKey in prop) {
                        if (propKey === 'properties') {
                            const finding_properties = prop[propKey]
                            prop[propKey] = { fields: finding_properties };
                            for (let fpKey in finding_properties) {
                                transform(data, finding_properties, fpKey, mapper.mapped_ips, mapper.org_name, true);
                            }
                            finding_properties['scc_status'] = { stringValue: 'ACTIVE' };
                            finding_properties['scc_source_category_id'] = { stringValue: prop['category'] };
                        } else {
                            transform(data, prop, propKey, mapper.mapped_ips, mapper.org_name);
                        }
                    }
                    output.push(Object.assign(prop, mapper.fixed_fields));
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
