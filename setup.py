from setuptools import setup

setup(
    name="code_point_open_transformer",
    version="2.0",
    packages=["code_point_open_transformer"],
    install_requires=[
        "click==7.0",
    ],
    entry_points="""
      [console_scripts]
      mediawikitojekyll=mediawiki_to_jekyll.cli:main
      codepointopen=code_point_open_transformer.cli:main
    """,
)
