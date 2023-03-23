from contextlib import contextmanager
from unittest import main, TestCase
from typing import Generator

import with_context


class WithContextTests(TestCase):
    def test_metadata(self) -> None:
        self.assertTrue(with_context.__author__)
        self.assertTrue(with_context.__doc__)
        self.assertTrue(with_context.__name__)
        self.assertTrue(with_context.__version__)

    def test_simple(self) -> None:
        print()
        entered = False
        exited = False

        @contextmanager
        def simple_context() -> Generator[None, None, None]:
            nonlocal entered
            nonlocal exited

            try:
                print("enter")
                entered = True
                print("yield")
                yield
                print("ok")
            finally:
                print("finally")
                exited = True

        self.assertFalse(entered)
        self.assertFalse(exited)

        print("here")
        print(f"{simple_context = !r}")

        @with_context(simple_context)
        def simple_function() -> None:
            print("simple_function")
            self.assertTrue(entered)
            self.assertFalse(exited)

        print("calling!")
        simple_function()
        self.assertTrue(entered)
        self.assertTrue(exited)


if __name__ == "__main__":
    main(verbosity=2)
