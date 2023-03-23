# Copyright Amethyst Reese
# Licensed under the MIT license

"""
Context managers as decorators
"""

import sys
from functools import wraps
from types import ModuleType
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    ContextManager,
    Generic,
    TypeVar,
    Union,
)

from typing_extensions import ParamSpec

from .__version__ import __version__ as __version__

__author__ = "Amethyst Reese"

C = ParamSpec("C")
P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")

CTXTypes = Union[AsyncContextManager, ContextManager]
CTXTypeOrCallable = Union[Callable[C, CTXTypes], CTXTypes]
FN = Callable[P, R]
CTXDecorator = Callable[[Callable[P, R]], Callable[P, R]]


class with_context(Generic[P, R]):
    """
    Use a context manager as a function decorator.

    Decorated functions, when called, will automatically call and enter the given
    context manager before running, and exit the context manager when finished.

    Roughly equivalent to adding a top-level ``with`` statement wrapping the contents
    of the function:

    .. code:: python

        @with_context(context_manager)
        def some_function():
            ...

    .. code:: python

        def some_function():
            with context_manager:
                ...

    Any positional or keyword arguments passed to :func:`with_context` will be passed
    to the context manager when calling it:

    .. code:: python

        @with_context(warnings.catch_warnings, category=DeprecationWarning)
        def noisy_workflow():
            ...

    .. code:: python

        def noisy_workflow():
            with warnings.catch_warnings(category=DeprecationWarning):
                ...

    :func:`with_context` can also be used to decorate async coroutines, with either
    async or normal context managers:

    .. code:: python

        @with_context(asyncio.timeout, 10)
        async def make_request():
            ...

    .. code:: python

        async def make_request():
            async with asyncio.timeout(10):
                ...

    """

    def __init__(
        self,
        manager: Union[Callable[C, ContextManager[T]], ContextManager[T]],
        *manager_args: C.args,
        **manager_kwargs: C.kwargs,
    ) -> None:
        self._manager = manager
        self._manager_args = manager_args
        self._manager_kwargs = manager_kwargs

    def __call__(self, fn: Callable[P, R]) -> Callable[P, R]:
        # wraps(fn)(self)
        self._fn = fn
        return self.call

    def call(self, *fn_args: P.args, **fn_kwargs: P.kwargs) -> R:
        if isinstance(self._manager, ContextManager):
            ctx = self._manager
        else:
            ctx = self._manager(*self._manager_args, **self._manager_kwargs)

        with ctx:
            return self._fn(*fn_args, **fn_kwargs)


class ModuleWrapper(ModuleType):
    def __init__(self, real: ModuleType):
        super().__init__(name=real.__name__, doc=real.__doc__)
        self._real = real

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)

    @wraps(with_context)
    def __call__(
        self,
        context: Union[Callable[C, ContextManager[T]], ContextManager[T]],
        *args: C.args,
        **kwargs: C.kwargs,
    ) -> with_context[P, R]:
        return with_context(context, *args, **kwargs)


wrapper = ModuleWrapper(sys.modules[__name__])
wrapper.__author__ = __author__  # type: ignore
wrapper.__version__ = __version__  # type: ignore
sys.modules[__name__] = wrapper
