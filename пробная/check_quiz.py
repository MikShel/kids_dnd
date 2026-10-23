#!/usr/bin/env python3
"""Проверка баланса домашнего опросника.

Запуск: python3 пробная/check_quiz.py пробная/опросник.md
Формат строки ответа: - ⬜ <текст> → <эмодзи1> <эмодзи2>
"""
import re
import sys
from itertools import combinations

VS = "\ufe0f"
HEROES = ["⚔", "✨", "🏹", "🌿", "🐾", "🎵", "🗝", "🔨"]
QUESTIONS = 6
ANSWERS = 4


def norm(s):
    return s.replace(VS, "").strip()


def fail(msg):
    print("ОШИБКА: " + msg)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail("использование: check_quiz.py <опросник.md>")
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as e:
        fail("не удалось прочитать файл: %s" % e)

    questions = []  # список (номер, [пары])
    current = None
    for line in lines:
        m = re.match(r"^###\s+Вопрос\s+(\d+)", line)
        if m:
            current = (int(m.group(1)), [])
            questions.append(current)
            continue
        if line.startswith("#"):
            current = None
            continue
        if current is None:
            continue
        m = re.match(r"^- ⬜ (.+) → (.+)$", line)
        if m:
            tokens = [norm(t) for t in m.group(2).split()]
            current[1].append(tokens)

    if len(questions) != QUESTIONS:
        fail("вопросов %d, нужно %d" % (len(questions), QUESTIONS))

    seen_pairs = {}
    for num, answers in questions:
        if len(answers) != ANSWERS:
            fail("вопрос %d: ответов %d, нужно %d" % (num, len(answers), ANSWERS))
        counts = {h: 0 for h in HEROES}
        for tokens in answers:
            if len(tokens) != 2 or tokens[0] == tokens[1]:
                fail("вопрос %d: у ответа должно быть 2 разных героя: %s" % (num, tokens))
            for t in tokens:
                if t not in counts:
                    fail("вопрос %d: неизвестный герой %r" % (num, t))
                counts[t] += 1
            pair = frozenset(tokens)
            if pair in seen_pairs:
                fail("пара %s повторяется в вопросах %d и %d"
                     % (" ".join(sorted(pair)), seen_pairs[pair], num))
            seen_pairs[pair] = num
        for h, c in counts.items():
            if c != 1:
                fail("вопрос %d: герой %s встречается %d раз, нужно 1" % (num, h, c))

    print("OK")


if __name__ == "__main__":
    main()
