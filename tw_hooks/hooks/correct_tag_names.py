import json
from typing import cast

from tw_hooks import OnModifyHook
from tw_hooks.base_hooks.on_add_hook import OnAddHook
from tw_hooks.types import MapOfTags, TaskT
from tw_hooks.utils import get_json_from_environ

envvar = "TW_CORRECT_TAG_MAPPINGS"


class CorrectTagNames(OnModifyHook, OnAddHook):
    """Change tag names based on a predefined lookup table (Use TW_TAG_MAPPINGS envvar).

    To specify a mapping, add something like this to your shell rc file:

        TW_CORRECT_TAG_MAPPINGS='{"movies": "movie", "wor": "work"}'
    """

    def __init__(self, tag_mappings=get_json_from_environ(envvar)):
        if tag_mappings is None:
            tag_mappings = {}
        self._tag_mappings = cast(MapOfTags, tag_mappings)

    def _correct_tags(self, task: TaskT):
        if "tags" not in task:
            return

        tags = task["tags"]
        for bad_tag in self._tag_mappings.keys():
            try:
                bad_idx = tags.index(bad_tag)
                tags[bad_idx] = self._tag_mappings[bad_tag]
                self.log(f"Correcting tag: {bad_tag} -> {self._tag_mappings[bad_tag]}")
            except ValueError:
                pass

    def _on_modify(self, original_task: TaskT, modified_task: TaskT):
        del original_task
        self._correct_tags(modified_task)
        print(json.dumps(modified_task))

    def _on_add(self, added_task: TaskT):
        self._correct_tags(added_task)
        print(json.dumps(added_task))
