def import_concrete_hooks():
    from .correct_tag_names import CorrectTagNames
    from .warn_on_task_congestion import WarnOnTaskCongestion
    from .auto_tag_based_on_tags import AutoTagBasedOnTags

__all__ = ["import_concrete_hooks"]
