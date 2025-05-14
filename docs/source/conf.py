import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'App Stock DB'
copyright = '2025, Mario Tomé Core'
author = 'Mario Tomé Core'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
