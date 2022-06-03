import json
from tw_hooks import OnModifyHook
from tw_hooks.base_hooks.on_add_hook import OnAddHook
from tw_hooks.types import SerTask, TagsMap
from tw_hooks.utils import get_map_from_environ


envvar = "TW_CORRECT_TAG_MAPPINGS"


class CorrectTagNames(OnModifyHook, OnAddHook):
    """Change tag names based on a predefined lookup table (Use TW_TAG_MAPPINGS envvar).

    To specify a mapping, add something like this to your shell rc file:

        TW_CORRECT_TAG_MAPPINGS='{"movies": "movie", "wor": "work"}'
    """

    def __init__(self, tag_mappings: TagsMap = get_map_from_environ(envvar)):
        self._tag_mappings = tag_mappings

    def _correct_tags(self, task: SerTask):
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

    def _on_modify(self, original_task: SerTask, modified_task: SerTask):
        del original_task
        self._correct_tags(modified_task)
        print(json.dumps(modified_task))

    def _on_add(self, added_task: SerTask):
        self._correct_tags(added_task)
        print(json.dumps(added_task))
