import click

from .handlers import Data, Template, ExtraVar
from .exceptions import InvalidInput


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.option('--data', '-d', help="PATH to YAML or JSON data file, URL or '-' for stdin.")
@click.option('--template', '-t', help="PATH to any file that uses Jinja, URL or '-' for stdin.")
@click.option('--verbose', '-v', is_flag=True)
@click.option('--no-trim-blocks', '-tb', default=True, is_flag=True, help='Disable trim blocks.')
@click.option('--no-lstrip-blocks', '-lb', default=True, is_flag=True, help='Disable lstrip blocks.')
@click.option('--output', '-o', type=click.Path(), help='PATH for output, stdout by default.')
@click.option('--extra-var', '-e', multiple=True, help="key value pair separated by '='. "
              "'value' will be treated as JSON or as a string in case of JSON decoding error. "
              "This will take precedence over 'data'.")
def render(data, template, verbose, no_trim_blocks, no_lstrip_blocks, output, extra_var):
    if data == '-' and template == '-':
        raise InvalidInput()

    if data is not None:
        data = Data(data, verbose).get_data()

    if extra_var is not None:
        extra_var = ExtraVar(extra_var, verbose).get_extra_vars()
        if data is not None:
            data.update(extra_var)
        else:
            data = extra_var

    if template is not None:
        out = Template(template, verbose, data, no_trim_blocks,
                       no_lstrip_blocks).get_rendered_template()
        if out is not None:
            if output is not None:
                with open(output, 'w+') as output_file:
                    output_file.write(out)
            else:
                print(out)
