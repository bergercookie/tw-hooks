# tw_hooks

TODO Add logo
TODO Register app in coveralls - set COVERALLS_REPO_TOKEN

<a href="https://github.com/bergercookie/tw-hooks/actions" alt="CI">
<img src="https://github.com/bergercookie/tw-hooks/actions/workflows/ci.yml/badge.svg" /></a>
<a href="https://github.com/pre-commit/pre-commit">
<img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>

<a href='https://coveralls.io/github/bergercookie/tw-hooks?branch=master'>
<img src='https://coveralls.io/repos/github/bergercookie/tw-hooks/badge.svg?branch=master' alt='Coverage Status' /></a>
<a href="https://github.com/bergercookie/tw-hooks/blob/master/LICENSE.md" alt="LICENSE">
<img src="https://img.shields.io/github/license/bergercookie/tw-hooks.svg" /></a>
<a href="https://pypi.org/project/tw_hooks/" alt="pypi">
<img src="https://img.shields.io/pypi/pyversions/tw-hooks.svg" /></a>
<a href="https://badge.fury.io/py/tw_hooks">
<img src="https://badge.fury.io/py/tw_hooks.svg" alt="PyPI version" height="18"></a>
<a href="https://pepy.tech/project/tw_hooks">
<img alt="Downloads" src="https://pepy.tech/badge/tw_hooks"></a>
<a href="https://github.com/psf/black">
<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Description

This is a Work-In-Progress collection of [Taskwarrior
hooks](https://taskwarrior.org/docs/hooks_guide.html) that I use in my
day-to-day workflows. The hooks are structured as classes under the
`tw_hooks/hooks` directory.

## Installation

[TODO] Install it from `PyPI`:

```sh
pip3 install --user --upgrade tw_hooks
```

To get the latest version install directly from source:

```sh
pip3 install --user --upgrade git+https://github.com/bergercookie/tw-hooks
```

After the installation, you have to run the `install_hook_shims` executable
(which by this point should be in your `$PATH`). This will create shims (wrapper
scripts) under `~/.task/hooks` in order to register all the hooks with
Taskwarrior.

## Structure of a Hook

The purpose of this package is to facilitate the development and distribution of
Taskwarrior hooks. To this purpose it includes a hook autodetection mechanism
both for the hooks in this repo as well as the hooks that you specify in the
`TW_ADDITIONAL_HOOKS` environment variable before the call to
`install_hook_shims`.

This is an example of a taskwarrior hook in this format:

```python
from tw_hooks import OnExitHook
class WarnOnTaskCongestion(OnExitHook):
    """Warn the user if there are too many tasks."""
    def on_exit(self, _):
      # ...
      return 0
```

TODO If you add the path to the script above in `TW_ADDITIONAL_HOOKS` before
executing `install_hook_shims`, then it will be automatically installed and
executed `on-exit` by Taskwarrior

```sh
t add +test kalimera
Created task 719.
[WarnOnTaskCongestion] Too many due:today tasks [threshold=9]
```

## Miscellaneous

- [Contributing Guide](CONTRIBUTING.md)

## Self Promotion

If you find this tool useful, please [star it on
Github](https://github.com/bergercookie/tw-hooks)
and consider donating.

## TODO List

See [ISSUES
list](https://github.com/bergercookie/tw-hooks/issues)
for the things that I'm currently either working on or interested in
implementing in the near future. In case there's something you are interesting
in working on, don't hesitate to either ask for clarifications or just do it and
directly make a PR.
