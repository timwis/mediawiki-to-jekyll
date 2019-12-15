import re
from os.path import join

import click
import untangle
import pypandoc
from slugify import slugify

@click.command()
@click.argument('xmlfile', type=click.File('rb'))
@click.option('--output-dir', type=click.Path(exists=True,
              dir_okay=True, file_okay=False))
def main(xmlfile, output_dir):
  obj = untangle.parse(xmlfile)
  for page in obj.mediawiki.page:
    title = page.title.cdata
    filename = slugify(title) + '.md'
    permalink = '/' + wikimedia_slugify(title)
    author = page.revision.contributor.username.cdata
    date = page.revision.timestamp.cdata
    body = page.revision.text.cdata
    body_without_category = re.sub(r"\[\[Category:[^\]]+\]\]", '', body)
    category_match = re.search(r"\[\[Category:([^\]]+)\]\]", body)
    category = '' if category_match is None else category_match[1]

    try:
      body_md = pypandoc.convert_text(body_without_category, 'gfm',
                 format='mediawiki')

      contents = """---
title: {}
permalink: {}
layout: page
author: {}
date: {}
category: {}
---
{}
""".format(title, permalink, author, date, category, body_md)

      click.echo(title)

      filepath = join(output_dir, filename)
      with open(filepath, 'w') as file:
        file.write(contents)

    except Exception as e:
      click.echo(e, err=True)

def wikimedia_slugify(input):
  return input.replace(' ', '_')

if __name__ == '__main__':
  main()
