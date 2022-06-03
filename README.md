# Taskwarrior Hooks

<p align="center">
  <img src="https://raw.githubusercontent.com/bergercookie/tw-hooks/master/misc/logo.png"/>
</p>

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

This is a collection of [Taskwarrior
hooks](https://taskwarrior.org/docs/hooks_guide.html) that I use in my
day-to-day workflows. It comes along a detection and easy-registration mechanism
that should make it easy to develop and then distribute your own hooks. The
hooks are structured as classes under the `tw_hooks/hooks` directory.

## Installation

Install it from `PyPI`:

```sh
pip3 install --user --upgrade tw_hooks
```

To get the latest version install directly from source:

```sh
pip3 install --user --upgrade git+https://github.com/bergercookie/tw-hooks
```

After the installation, you have to run the `install_hook_shims` executable
(which by this point should be in your `$PATH`). Running it will create shims
(thin wrapper scripts) under `~/.task/hooks` in order to register all the hooks
with Taskwarrior.

## Available hooks

Currently the following hooks are available:

TODO

## Structure of a Hook

The purpose of this package is to facilitate the development and distribution of
Taskwarrior hooks. To this purpose `install_hook_shims` allows you to easily
register your own hooks, without having to manually copy items over to the
taskwarrior hooks location. `install_hook_shims` will install a shim which will
call your hook automatically when required.

This is an example of a Taskwarrior hook that will be executed on Taskwarrior
exit:

```python
from tw_hooks import OnExitHook
class WarnOnTaskCongestion(OnExitHook):
    """Warn the user if there are too many tasks."""
    def _on_exit(self, _):  # <--- Mandatory to implement this signature
      # ...
      return 0
```

Assuming that this hook is in a module called `warn_on_task_congestion.py` and
that the directory of this module is in your python path (e.g., by adding it
explicitly to `$PYTHONPATH`), then you can run the following to register your
hook with taskwarrior:

```sh
install_hook_shims -r warn_on_task_congestion
```

During your next Taskwarrior operation, if there are too many due:today tasks,
you should see something like this:

```sh
t add +test kalimera
Created task 719.
[WarnOnTaskCongestion] Too many due:today tasks [threshold=9]
```

## Hooks API

TODO

## Usage instructions for `install_hook_shims`

TODO

## Miscellaneous

- [Contributing Guide](CONTRIBUTING.md)

## Self Promotion

If you find this tool useful, please [star it on
Github](https://github.com/bergercookie/tw-hooks)
and consider donating.

## Support

If something doesn't work, feel free to open an issue. You can also find me in
the [#taskwarrior Libera Chat](https://matrix.to/#/#taskwarrior:libera.chat).

## TODO List

See [ISSUES
list](https://github.com/bergercookie/tw-hooks/issues)
for the things that I'm currently either working on or interested in
implementing in the near future. In case there's something you are interesting
in working on, don't hesitate to either ask for clarifications or just do it and
directly make a PR.
