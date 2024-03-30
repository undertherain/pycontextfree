import logging

import contextfree.core as core

from .core import _state
from .random import prnd

# import .core.MAX_DEPTH as MAX_DEPTH


_rules = {}
__all__ = [
    "check_limits",
    "rule",
]
MAX_ELEMENTS = 1000000
SIZE_MIN_FEATURE = 0.5

logger = logging.getLogger(__name__)


def check_limits(user_rule):
    """Stop recursion if resolution is too low on number of components is too high"""

    def wrapper(*args, **kwargs):
        """The body of the decorator"""
        global _state
        _state["cnt_elements"] += 1
        _state["depth"] += 1
        matrix = _state["ctx"].get_matrix()
        # TODO: add check of transparency = 0
        if _state["depth"] >= core.MAX_DEPTH:
            logger.info(
                "stop recursion by reaching max depth {}".format(core.MAX_DEPTH)
            )
        else:
            min_size_scaled = SIZE_MIN_FEATURE / min(core.WIDTH, core.HEIGHT)
            current_scale = max([abs(matrix[i]) for i in range(2)])
            if current_scale < min_size_scaled:
                logger.info("stop recursion by reaching min feature size")
                # TODO: check feature size with respect to current ink size
            else:
                if _state["cnt_elements"] > MAX_ELEMENTS:
                    logger.info("stop recursion by reaching max elements")
                else:
                    user_rule(*args, **kwargs)
        _state["depth"] -= 1

    return wrapper


def rule(proba=1):
    def real_decorator(function):
        name = function.__name__

        def wrapper(*args, **kwargs):
            if args:
                raise NotImplementedError(
                    "Passing parameters to rules not implemented yet"
                )
            call_rule(name)

        logger.info("registering rule " + name)
        if name not in _rules:
            _rules[name] = []
            last_proba = 0
        else:
            last_proba = _rules[name][-1][0]
        _rules[name].append((last_proba + proba, function))
        return wrapper

    return real_decorator


@check_limits
def call_rule(name):
    rules = _rules[name]
    die_roll = prnd(rules[-1][0])
    for i in range(len(rules)):
        if die_roll < rules[i][0]:
            rules[i][1]()
            break
