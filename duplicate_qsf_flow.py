import json

import click


def get_embedded(data):
    """
    Function for recursively yield embedded data values
    :param data: payload from qsf FL survey element
    :return: Generator
    """
    if 'Flow' in data:
        for k in data['Flow']:
            yield k['FlowID']
            yield from get_embedded(k)


def get_flow(qsf_path, flow_id):
    """
    :param qsf_path: Path to qsf file
    :param flow_id: flowID get
    :return: flow
    """
    with open(qsf_path) as f:
        qsf = json.loads(f.read())
        for q in qsf['SurveyElements']:
            if q['Element'] == "FL":
                for flow in q['Payload']['Flow']:
                    if flow['FlowID'] == flow_id:
                        return flow


@click.command()
@click.option('-mq', '--master_qsf_path', required=True, help="Path to input qsf with flows you want to copy")
@click.option('-tq', '--target_qsf_path', required=True, help="Path to input qsf you want to insert into")
@click.option('-oq', '--output_qsf_path', required=True, help="Path to output qsf")
@click.option('-flids', '--flow_ids', required=True, help="Comma seprated FlowIDs")
def main(master_qsf_path, target_qsf_path, output_qsf_path, flow_ids):
    flows = flow_ids.split(',')
    with open(target_qsf_path) as f:
        qsf = json.loads(f.read())
        for q in qsf['SurveyElements']:
            if q['Element'] == "FL":
                taken_ids = sorted([int(i.split('_')[1]) for i in get_embedded(q['Payload'])])
                for fl in flows:
                    try:
                        new_id = taken_ids[-1:][0] + 1
                        taken_ids.append(new_id)
                        flow = get_flow(master_qsf_path, fl)
                        flow['FlowID'] = f"FL_{new_id}"
                        q['Payload']['Flow'].append(flow)
                    except TypeError as e:
                        print(f"ERROR, you probably provided a non existing flowID: {e}")

    with open(output_qsf_path, 'w') as out:
        out.write(json.dumps(qsf))


if __name__ == '__main__':
    main()
