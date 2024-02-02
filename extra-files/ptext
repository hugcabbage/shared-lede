#!/usr/bin/env python3
import argparse
import json

from tools.process_text import simplify_config


def _to_file_or_print(text, to_file=None):
    if to_file:
        with open(to_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'{to_file} has been generated.')
    else:
        print(text)


def _xlsx2dict(file) -> dict:
    """convert xlsx file to dict"""
    from openpyxl import load_workbook

    wb = load_workbook(file)
    sheet = wb.active
    dict_data = {}

    # exclude title row, first column is key, convert other columns to list as value
    for i in range(2, sheet.max_row + 1):
        key = sheet.cell(row=i, column=1).value
        value = []
        for j in range(2, sheet.max_column + 1):
            value.append(sheet.cell(row=i, column=j).value)
        dict_data[key] = value

    return dict_data


def toml2json(file, json_ident=None, to_file=None):
    import toml

    with open(file, encoding='utf-8') as f:
        data = toml.load(f)
    jdata = json.dumps(data, ensure_ascii=False, indent=json_ident)
    _to_file_or_print(jdata, to_file)


def xlsx2headers(file, json_ident=None, to_file=None):
    jdata = json.dumps(_xlsx2dict(file), ensure_ascii=False, indent=json_ident)

    # make key and value be one line
    if json_ident:
        it1 = ' ' * json_ident
        it2 = it1 * 2
        jdata = (jdata.replace(f'[\n{it2}', '[')
                 .replace(f',\n{it2}', ', ')
                 .replace(f'"\n{it1}', '"'))

    _to_file_or_print(jdata, to_file)


def config2mini(file, to_file=None):
    text = simplify_config(file, backup=False, ptext=True)
    _to_file_or_print(text, to_file)


def _parse_command_line():
    parser = argparse.ArgumentParser(description='Convert some simple text files.')

    types = ('toml2json', 't2j', 'xlsx2headers', 'x2h', 'config2mini', 'c2m')
    parser.add_argument('command', choices=types, help='what type of file to process')

    f_group = parser.add_mutually_exclusive_group()
    f_group.add_argument('file', nargs='?', metavar='<in path>', help='input file')
    f_group.add_argument('--file', dest='file_flag', default=None, metavar='<in path>', help='input file')

    tf_group = parser.add_mutually_exclusive_group()
    tf_group.add_argument('to_file', nargs='?', metavar='<out path>', help='output file')
    tf_group.add_argument('--to-file', dest='to_file_flag', default=None, metavar='<out path>', help='output file')

    parser.add_argument('--json-indent', type=int, metavar='<N>', default=None, help='json indent level')

    args = parser.parse_args()
    if args.file_flag is not None:
        args.file = args.file_flag
    if args.to_file_flag is not None:
        args.to_file = args.to_file_flag
    for i, c in enumerate(types[::2]):
        if args.command == c:
            args.command = types[i * 2 + 1]
            break
    if args.command == 'c2m' and args.json_indent is not None:
        raise UserWarning('config2mini no json_indent')

    return args


def ptext():
    args = _parse_command_line()
    if args.command == 't2j':
        toml2json(args.file, args.json_indent, args.to_file)
    elif args.command == 'x2h':
        xlsx2headers(args.file, args.json_indent, args.to_file)
    elif args.command == 'c2m':
        config2mini(args.file, args.to_file)


if __name__ == '__main__':
    ptext()
