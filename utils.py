from itertools import count
from typing import Literal


class Program:
    def __init__(self, *, filename: str = "rules.txt", debug: bool = __debug__) -> None:
        self._ids = count(1)
        self._cache = {"INIT": "INIT", "HALT": "HALT"}

        self._file = open(filename, "w", newline="\n", encoding="utf-8")
        self._debug = debug

    @staticmethod
    def _encode(n: int) -> str:
        chars = "".join(chr(i) for i in range(33, 127) if chr(i) != "/")
        base = len(chars)
        s = ""
        while n:
            s = chars[n % base] + s
            n //= base
        return s or chars[0]

    def _compress(self, s: str) -> str:
        if self._debug:
            return s

        if s in self._cache:
            return self._cache[s]
        else:
            replacement = self._encode(next(self._ids))
            self._cache[s] = replacement
            return replacement

    def __call__(
        self, from_: str, symbol: str, to: str, new_symbol: str, dir: Literal["L", "R"]
    ) -> None:
        line = f"{self._compress(from_)} {symbol} {self._compress(to)} {new_symbol} {dir}\n"
        self._file.write(line)
