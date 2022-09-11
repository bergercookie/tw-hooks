import json
import re
from typing import cast

from tw_hooks import OnAddHook, OnModifyHook
from tw_hooks.types import MapOfTags, TaskT
from tw_hooks.utils import get_json_from_environ

envvar = "TW_AUTO_TAG_MAPPINGS"


class AutoTagBasedOnTags(OnModifyHook, OnAddHook):
    """
    Inspect the list of tags in the added/modified tasks provided and add additional tags if required.

    To specify a mapping, add something like this to your shell rc file:

        TW_AUTO_TAG_MAPPINGS='{"python": "programming", "cpp": "programming", "github.*": "programming"}'
    """

    def __init__(self, tag_mappings=get_json_from_environ(envvar)):
        if tag_mappings is None:
            tag_mappings = {}
        self._tag_mappings = cast(MapOfTags, tag_mappings)

    def _check_and_apply_extra_tags(self, task: TaskT):
        if "tags" not in task:
            return

        tags = task["tags"]
        old_tags = list(tags)
        for tag_pattern in self._tag_mappings.keys():
            if not any(re.match(tag_pattern, tag) for tag in tags):
                continue

            new_tags = self._tag_mappings[tag_pattern]
            tags.extend(new_tags)
            if set(old_tags) != set(tags):
                self.log(f"Applying extra tags (due to pattern {tag_pattern}): {new_tags}")

    def _on_modify(self, original_task: TaskT, modified_task: TaskT):
        del original_task
        self._check_and_apply_extra_tags(modified_task)
        print(json.dumps(modified_task))

    def _on_add(self, added_task: TaskT):
        self._check_and_apply_extra_tags(added_task)
        print(json.dumps(added_task))
