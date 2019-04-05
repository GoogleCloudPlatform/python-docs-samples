import argparse
import json
import random
import uuid

def create_parser():
    '''CLI parser'''
    parser = argparse.ArgumentParser(
        description='Generate findings randomically')

    parser.add_argument('-f',
                        '--file',
                        help='Objects file contain Instances and Projects IDs',
                        dest='objects_file',
                        required=True)
    parser.add_argument('-df',
                        '--destine_file',
                        help='Name or path to save the file',
                        dest='destine_file',
                        required=True)
   
    parser.add_argument('-s',
                        '--sample_file',
                        help='File used as base to create findings.',
                        dest='sample_file',
                        default='tools/samples/findings_generator/findings_sample.json' )
    parser.add_argument('-n',
                        '--number_of_findings',
                        help='Quantity of findings to be generated. Integer number',
                        dest='quantity',
                        default=100 )

    return parser

def open_json_file(path):
    with open(path) as json_data:
        return json.load(json_data)

def main():
    parser = create_parser()
    args = parser.parse_args()

    projects_data = open_json_file(args.objects_file)

    findings_sample = open_json_file(args.sample_file)

    lines = []

    for i in range(int(args.quantity)):
        selected_data = random.choice(projects_data)
        project_id = selected_data['project']
        finding = random.choice(findings_sample).copy()
        assetId = finding["assetIds"][0]

        if "{project_id}" in assetId:
            finding["assetIds"] = [project_id]
        else:
            finding["assetIds"] = [selected_data['instance']['id']]

        finding_id = finding['id']
        finding['id'] = finding_id.format(
            sequential_id = uuid.uuid4(),
            project_id = project_id)

        lines.append(finding)

    with open(args.destine_file, 'w') as f:
        json.dump(lines, f, ensure_ascii=False, indent = 2)

if __name__ == '__main__':
    main()
    