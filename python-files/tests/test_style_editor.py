import pytest

from karaoke.style_editor import StyleEditor

def test_print_regex_replace_tuples():
    style_editor = StyleEditor()
    regex_replace_pairs = []
    regex_replace_pairs.append(("hello", "world"))
    regex_replace_pairs.append(("how", "you do"))
    style_editor.print_regex_replace_tuples(regex_replace_pairs)