# Taskwarrior Hooks

<p align="center">
  <img src="https://raw.githubusercontent.com/bergercookie/tw-hooks/master/misc/logo.png"/>
</p>

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
<a href="https://badge.fury.io/py/tw-hooks">
<img src="https://badge.fury.io/py/tw-hooks.svg" alt="PyPI version" height="18"></a>
<a href="https://pepy.tech/project/tw-hooks">
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

After the installation, you have to run the `install-hooks-shims` executable
(which by this point should be in your `$PATH`). Running it will create shims
(thin wrapper scripts) under `~/.task/hooks` in order to register all the hooks
with Taskwarrior.

## Available hooks

Currently the following hooks are available out-of-the-box:

<table style="undefined;table-layout: fixed; width: 823px">
<thead>
  <tr>
    <th>Hook</th>
    <th>Description</th>
    <th>Events</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><tt>AutoTagBasedOnTags</tt></td>
    <td>Inspect the list of tags in the added/modified tasks provided and add additional tags if required</td>
    <td><tt>on-modify</tt>, <tt>on-add</tt></td>
  </tr>
  <tr>
    <td><tt>CorrectTagNames</tt></td>
    <td>Change tag names based on a predefined lookup table</td>
    <td><tt>on-modify</tt>, <tt>on-add</tt></td>
  </tr>
  <tr>
    <td><tt>DetectMutuallyExclusiveTags</tt></td>
    <td>See whether the user has specified an incompatible combination of tags</td>
    <td><tt>on-modify</tt>, <tt>on-add</tt></td>
  </tr>
  <tr>
    <td><tt>PostLatestStartToI3Status</tt></td>
    <td>When a task is started, send the title of the task to i3status-rs via DBus</td>
    <td><tt>on-modify</tt></td>
  </tr>
  <tr>
    <td><tt>WarnOnTaskCongestion</tt></td>
    <td>Warn the user if there are too many tasks (due:today)</td>
    <td><tt>on-exit</tt></td>
  </tr>
</tbody>
</table>

## Structure of a Hook

The purpose of this package is to facilitate the development and distribution of
Taskwarrior hooks. To this purpose `install-hooks-shims` allows you to easily
register your own hooks, without having to manually copy items over to the
taskwarrior hooks location. `install-hooks-shims` will install a shim which will
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
install-hooks-shims -r warn_on_task_congestion
```

During your next Taskwarrior operation, if there are too many due:today tasks,
you should see something like this:

```sh
t add +test kalimera
Created task 719.
[WarnOnTaskCongestion] Too many due:today tasks [threshold=9]
```

## Hooks API

Subclass one of the following base hooks, and your method is going to be called
during that event:

- [`OnAddHook`](https://github.com/bergercookie/tw-hooks/blob/master/tw_hooks/base_hooks/on_add_hook.py)
  - Implement the `_on_add(self, added_task: TaskT)` method.
- [`OnExitHook`](https://github.com/bergercookie/tw-hooks/blob/master/tw_hooks/base_hooks/on_exit_hook.py)
  - Implement the `_on_exit(self, added_modified_tasks: List[TaskT])` method.
- [`OnLaunchHook`](https://github.com/bergercookie/tw-hooks/blob/master/tw_hooks/base_hooks/on_launch_hook.py)
  - Implement the `_on_launch(self)` method.
- [`OnModifyHook`](https://github.com/bergercookie/tw-hooks/blob/master/tw_hooks/base_hooks/on_modify_hook.py)
  - Implement the `_on_modify(self, original_task: TaskT, modified_task: TaskT)`
    method.

## Usage instructions for `install-hooks-shims`

<!-- START sniff-and-replace install-hook-shims --help START -->

```python
usage: Detect Taskwarrior hooks and register an executable shim for each one of them.
       [-h] [-t TASK_DIR] [-a] [-l]
       [-r REGISTER_ADDITIONAL [REGISTER_ADDITIONAL ...]]

optional arguments:
  -h, --help            show this help message and exit
  -t TASK_DIR, --task-dir TASK_DIR
                        Path to the taskwarrior main directory
  -a, --all-hooks       Install shims for all the hooks
  -l, --list-hooks      List the available hooks and exit
  -r REGISTER_ADDITIONAL [REGISTER_ADDITIONAL ...], --register-additional REGISTER_ADDITIONAL [REGISTER_ADDITIONAL ...]

Usage examples:
===============

- Install only the WarnOnTaskCongestion hook (assuming you've installed tw_hooks with e.g., pip3)
  install-hook-shims -r tw_hooks.hooks.warn_on_task_congestion

- Install all the available hooks from this repo (assuming you've installed tw_hooks with e.g., pip3)
  install-hook-shims --all-hooks

- Install a custom hook defined in .../dir/mod/hook_name.py. "dir" should be in your PYTHONPATH
  install-hook-shims -r mod.hook_name

- List all the available hooks and exit
  install-hook-shims --list-hooks

```

<!-- END sniff-and-replace -->

## Miscellaneous

- [Contributing Guide](CONTRIBUTING.md)

## FAQ

- Why should I use this over raw taskwarrior hooks?
  - Because this package does the heavy lifting pre-processing the input tasks
    from the command line. It does so in a robust manner making sure it does
    the right thing regardless of weather one or two commands are provided and
    being robust to errors (e.g., `utf-8` decoding errors).
  - It takes care to make the hooks fail safely even if it can't find required
    modules (e.g., if you try invoking `task` from inside a `virtualenv` where
    `tw-hooks` is not importable.
  - It gives you a class-oriented approach and lets you install multiple hooks
    from the same class, thus allowing these hooks to share common
    configuration.
  - It allows you to keep all your hooks together and keep
    them as a package in some other place in your filesystem, e.g., in your
    dotfiles and automatically adds the right glue-code so that Taskwarrior your
    scripts without having to explicitly place it in `~/.task/hooks` or
    symlinking it.

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
