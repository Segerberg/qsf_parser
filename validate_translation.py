import re
import json
import click
from openpyxl import load_workbook


def validate_xlsx(xlsx):
    errors = {}
    """
    Parses xslx file
    :param xlsx: xslx file
    :return: parsed values as dict
    """
    wb = load_workbook(xlsx)
    texts = wb['Texts']

    with open('validations.json', 'r') as f:
        validations = json.loads(f.read())
        for k,v in validations.items():
                for val in v:
                    for key, value in val.items():
                        match = re.findall(key, texts[k].value)
                        if not match:
                            if k in errors:
                                errors[k].append(f"no match for {key}")
                            else:
                                errors[k]= [(f"no match for {key}")]

                        elif len(match) != value:
                            if k in errors:
                                errors[k].append(f"Diff in number of matches excpected {value} got {len(match)} for {k} (regex {key})")
                            else:
                                errors[k] = [f"Diff in number of matches excpected {value} got {len(match)} for {k} (regex {key})" ]

    return errors

@click.command()
@click.argument('excel_path')
def main(excel_path):
    validate = validate_xlsx(excel_path)
    if len(validate) == 0:
        print('Validates ✔')

    else:
        print("☠ Error ☠")
        for k,v in validate.items():
            for e in v:
                print(k,e)


if __name__ == "__main__":
    main()