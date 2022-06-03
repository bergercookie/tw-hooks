def import_concrete_hooks():
    from .correct_tag_names import CorrectTagNames
    from .warn_on_task_congestion import WarnOnTaskCongestion
    from .auto_tag_based_on_tags import AutoTagBasedOnTags
    from .detect_mutually_exclusive_tags import DetectMutuallyExclusiveTags
    from .post_latest_start_to_i3_status import PostLatestSTartToI3Status

__all__ = ["import_concrete_hooks"]
