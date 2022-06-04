import json
from typing import List, Set, cast

from tw_hooks import OnModifyHook
from tw_hooks.base_hooks.on_add_hook import OnAddHook
from tw_hooks.types import ListOfTagsList, Retcode, TaskT
from tw_hooks.utils import get_json_from_environ

envvar = "TW_INCOMPATIBLE_TAG_SETS"


class DetectMutuallyExclusiveTags(OnModifyHook, OnAddHook):
    """
    Inspect the list of tags in the added/modified tasks and see whether the user has specified an incompatible combination of tags.

    To specify a mapping of tags that don't work well with each other, add a variable like the
    following in your shell RC file:

        TW_INCOMPATIBLE_TAG_SETS='[("projectideas", "freetime")]'
    """

    def __init__(self, tag_sets=get_json_from_environ(envvar)):
        if tag_sets is None:
            tag_sets = []
        if not isinstance(tag_sets, list):
            raise RuntimeError(
                f"Parsed value from {envvar} doesn't contain a  list as expected but a"
                f" {type(tag_sets)}-> {tag_sets}"
            )
        self._tag_sets: List[Set[str]] = [set(li) for li in cast(ListOfTagsList, tag_sets)]

    def _detect_incompatible_tags(self, task: TaskT) -> Retcode:
        if "tags" not in task:
            return 0

        tags = task["tags"]
        for tag_set in self._tag_sets:
            if tag_set.issubset(tags):
                self.log(f"Can't use the following tags together -> {tag_set}")
                return 1

        return 0

    def _on_modify(self, original_task: TaskT, modified_task: TaskT) -> Retcode:
        del original_task
        ret = self._detect_incompatible_tags(modified_task)
        print(json.dumps(modified_task))
        return ret

    def _on_add(self, added_task: TaskT) -> Retcode:
        ret = self._detect_incompatible_tags(added_task)
        print(json.dumps(added_task))
        return ret
