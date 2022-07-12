import os
import sys
import uuid
import json
# import tempfile
import click
import subprocess as sp

LABEL_CHOICES = {
    'pronunciation': '发音',
    'paraphrase': '释义',
    'extra': '其他'
}

@click.command()
@click.argument('search')
@click.option('--force-update/--no-force-update', ' /-F', default=False)
def cli(search, force_update):
    os.chdir('/home/chen/Code/cli/dict/')
    filename = f'/home/chen/Code/cli/dict/tmp/{search}.json'
    # _, fp = tempfile.mkstemp('.json', 'dict_')
    # filename = '/tmp/{}.json'.format(str(uuid.uuid4()))
    if not os.path.exists(filename) or force_update:
        if os.path.exists(filename):
            os.remove(filename)

        sp.check_output(['scrapy', 'crawl', 'bing', '--nolog', '-a', 'search={}'.format(search), '-o', filename])

    if os.path.getsize(filename) == 0:
        click.secho('Nothing Found', fg='yellow')
        sys.exit()

    with open(filename) as f:
        try:
            res = json.loads(f.read())[-1]
            for key, value in res.items():
                click.secho('\n%s:' % LABEL_CHOICES[key], fg='green')
                click.echo(value)
        except Exception as e:
            click.secho(filename)
            click.secho(e, fg='red')


if __name__ == '__main__':
    cli()
