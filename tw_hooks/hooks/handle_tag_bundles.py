import json
from typing import cast

from tw_hooks import OnModifyHook
from tw_hooks.types import MapOfTags, TaskT
from tw_hooks.utils import get_json_from_environ

envvar = "TW_BUNDLE_TAGS"


class HandleTagBundles(OnModifyHook):
    """
    When a task that is tagged as being part of a specific bundle is modified  execute a particular action to all the tasks that are also defined in this bundle.

    A few more details on what this hook is about:

    It reads its configuration from the :py:data:`envvar` environment variable. This should be
    a dictionary like the following:

    .. code-block:: bash

        TW_BUNDLE_TAGS='{"start_together": ["tag1", "tag2"], "stop_together": ["tag2"], "notify_start_together": ["eow", "oem", "bundle_*"], "notify_stop_together": ["eow", "oem", "bundle_*"]}'

    The above basically means that:

    - Whenever a (pending) tasks that is tagged with ``eow`` or ``eom`` or a tag that starts
      with ``bundle_*` is started, this hook will ping the user (i.e., print in the console) to
      consider starting the other pending tasks that also have any of these tags (if these
      tasks are stopped).
    - Whenever a (pending) tasks that is tagged with ``eow`` or ``eom`` or a tag that starts
      with ``bundle_*` is stopped, this hook will ping the user (i.e., print in the console) to
      consider stopping the other pending tasks that also have any of these tags (if these
      tasks are started).
    - When a task tagged with tag1 or tag2 is started, this hook will automatically start all
      other tasks that have any of these  tags and inform the user about it.
    - When a task tagged with tag3 or tag4 is stopped, this hook will automatically stop all
      other tasks that have any of these tags and inform the user about it.
    """

    def __init__(self, tag_mappings=get_json_from_environ(envvar)):
        if tag_mappings is None:
            tag_mappings = {}
        self._tag_mappings = cast(MapOfTags, tag_mappings)

    def _on_modify(self, original_task: TaskT, modified_task: TaskT):
        print(json.dumps(modified_task))
