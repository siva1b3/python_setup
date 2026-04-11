# Python OOP for Django — Learning Roadmap

> **How to use this file across chats:**
> At the start of every new chat, paste this entire file as the first message. Then tell Claude which step you want to resume from. Claude will read the Context block, the Learner Profile, the Teaching Contract, and the Progress Tracker — and continue exactly where you left off.
>
> After each session, update the **Progress Tracker** section at the bottom (mark completed steps, paste any notes you want to remember) and save the file. That updated file becomes the "memory" you carry into the next chat.

---

## 1. Context (read this first, every new chat)

The learner is working through a structured roadmap to learn Python Object-Oriented Programming. The end goal is to read and write Django code confidently. This file is the single source of truth for the learning plan and current progress.

The learning happens **entirely inside Claude.ai browser chat**, across multiple sessions. No external IDE. All code is written, read, and discussed in chat.

The roadmap was designed collaboratively, critiqued for incremental pacing, and finalized before learning began. **Do not modify the roadmap structure mid-learning** unless the learner explicitly asks. If a step feels too large during teaching, split it on the fly but do not renumber.

---

## 2. Learner Profile

- **Name:** Ranjit
- **Python experience:** 4 years, functional style only. No prior OOP in Python.
- **Background:** Full-stack developer (JS/Node.js), system architect, networking and load balancer engineering. Comfortable with: functions, decorators (as a user), comprehensions, modules, error handling, file I/O, virtualenvs, Docker.
- **Knows other OOP languages?** Not assumed. Teach Python OOP from scratch, but skip Python basics.
- **Native language:** Telugu. English is second language. Use clear, precise wording. Avoid idioms and unnecessarily complex phrasing.
- **End goal:** Read and write Django code (models, views, forms, mixins, `super()` calls, overridden methods) without confusion.

---

## 3. Teaching Contract (rules Claude must follow every session)

1. **One small step at a time.** Never combine two new concepts in one step. If a step feels like it has a hidden second concept, split it.
2. **No assumed knowledge of OOP.** Functional Python is assumed. OOP is not.
3. **Format per step:**
   - Concept explanation (short, precise)
   - Small code example
   - Exercise for the learner to solve in chat
   - Wait for the learner's answer
   - Review the answer, point out mistakes, confirm understanding
   - Move to the next step only after the learner confirms
4. **Format per phase:**
   - All steps in order
   - Phase recap (with one **callback question** to an earlier phase for spaced repetition)
   - **Mini-test:** mix of question types — short-answer, predict-the-output, find-the-bug — covering many cases, not just one or two
   - Wait for answers, review, then move to the next phase
5. **Reading exercises (Phases 6–10):** At the end of each of these phases, paste a small piece of class-based code (pure Python, not Django) and ask the learner to explain what it does and why. This trains the read-skill, not just the write-skill.
6. **No Django code anywhere in the roadmap.** Django is the *destination*, not part of the journey. Pure Python OOP only. A single-sentence Django connection is allowed in phase recaps, nothing more.
7. **No academic OOP topics that Django does not use.** Skip metaclasses, `__new__`, descriptors, `__slots__`, `abc` beyond `ABC`/`abstractmethod`, multiple-dispatch libraries, etc.
8. **Response style preferences:**
   - Start with the direct concept, then expand
   - No filler, no praise, no motivational language
   - Challenge the learner's wrong assumptions directly
   - Clear, precise English (second-language reader)
9. **Capstone project (Phase 10):** Claude provides the design spec. The learner only implements. Do not ask the learner to design the system.
10. **Pacing:** Never rush. If the learner gets a mini-test wrong, re-teach the failed concept before moving on.

---

## 4. The Roadmap

**Total:** 10 phases, 57 steps, 10 phase mini-tests, 1 final test, 5 reading exercises, 9 callback questions.

---

### Phase 1 — Classes and Objects
**Goal:** Understand what a class is, what an instance is, how `self` works, and how to initialize an object.

- [ ] 1.1 — What a class is, what an object is, why OOP exists
- [ ] 1.2 — Defining your first class with no attributes, creating instances
- [ ] 1.3 — Adding attributes to an instance from outside (`obj.name = "x"`); an object is a bag of attributes
- [ ] 1.4 — The problem: every caller must remember to set attributes. Motivates a constructor.
- [ ] 1.5 — `self` explained: what it is, why Python passes it automatically
- [ ] 1.6 — `__init__` with only `self` (no parameters), setting attributes inside
- [ ] 1.7 — `__init__` with parameters
- [ ] 1.8 — Instance methods (methods that use `self` to read/modify attributes)
- [ ] **Phase 1 recap + mini-test**

---

### Phase 2 — Class Attributes vs Instance Attributes
**Goal:** Understand the distinction that confuses every functional programmer entering class-based frameworks.

- [ ] 2.1 — Class attributes: defined at class level, shared across all instances
- [ ] 2.2 — Instance attributes: set on `self`, unique per instance
- [ ] 2.3 — The lookup rule: Python checks instance first, then class
- [ ] 2.4 — Common bug: mutable class attributes (the shared list trap)
- [ ] 2.5 — Decision rule: when to use a class attribute, when to use an instance attribute
- [ ] **Phase 2 recap (callback to Phase 1) + mini-test**

---

### Phase 3 — Dunder Methods
**Goal:** Understand the special methods Python calls automatically.

- [ ] 3.1 — Motivation: why `print(obj)` shows `<__main__.X object at 0x...>` and why that is ugly
- [ ] 3.2 — What dunder methods are, why Python calls them automatically
- [ ] 3.3 — `__str__`: human-readable representation
- [ ] 3.4 — `__repr__`: developer representation, and the difference from `__str__`
- [ ] 3.5 — `__eq__`: defining what it means for two objects to be equal
- [ ] 3.6 — `__hash__`: brief — why it must agree with `__eq__`
- [ ] **Phase 3 recap (callback to Phase 2) + mini-test**

---

### Phase 4 — Encapsulation and Properties
**Goal:** Control how attributes are accessed and computed.

- [ ] 4.1 — Public attributes: everything in Python is public by default
- [ ] 4.2 — The `_single_underscore` convention: a hint, not enforced
- [ ] 4.3 — The `__double_underscore` name mangling: actual Python behavior
- [ ] 4.4 — Why Java-style getters/setters are not Pythonic
- [ ] 4.5 — What `@property` actually does differently from a normal decorator (callable without `()`)
- [ ] 4.6 — `@property` — turning a method into a read-only attribute
- [ ] 4.7 — Adding a setter to a property
- [ ] 4.8 — Computed properties (e.g., `full_name` from `first_name` + `last_name`)
- [ ] **Phase 4 recap (callback to Phase 3) + mini-test**

---

### Phase 5 — Class Methods and Static Methods
**Goal:** Understand the three method types and when each applies.

- [ ] 5.1 — Instance method recap
- [ ] 5.2 — Motivation: I want a method on the class that does not need an existing instance. Show the awkward way (a function outside the class).
- [ ] 5.3 — `@classmethod` and `cls` as the clean solution
- [ ] 5.4 — `@staticmethod`: a function that lives in the class namespace but uses neither `self` nor `cls`
- [ ] 5.5 — Factory methods using `@classmethod` (e.g., `User.from_dict(data)`)
- [ ] **Phase 5 recap (callback to Phase 4) + mini-test**

---

### Phase 6 — Single Inheritance
**Goal:** Understand subclassing.

- [ ] 6.1 — What inheritance is, parent and child class
- [ ] 6.2 — Defining a subclass, inheriting attributes and methods automatically
- [ ] 6.3 — Adding new methods in the subclass
- [ ] 6.4 — Method overriding: redefining a parent method in the child
- [ ] 6.5 — `super()` for single inheritance only — calling the parent's version of a method
- [ ] 6.6 — Overriding `__init__`: what goes wrong if you forget to call the parent's `__init__`
- [ ] 6.7 — Calling `super().__init__(...)` with the right arguments
- [ ] **Phase 6 reading exercise**
- [ ] **Phase 6 recap (callback to Phase 5) + mini-test**

---

### Phase 7 — Polymorphism and Duck Typing
**Goal:** Understand how Python uses behavior over type.

- [ ] 7.1 — Polymorphism: same method name, different behavior across classes
- [ ] 7.2 — Duck typing: "if it walks like a duck and quacks like a duck"
- [ ] 7.3 — `isinstance()` and `issubclass()`: when useful, when an anti-pattern
- [ ] **Phase 7 reading exercise**
- [ ] **Phase 7 recap (callback to Phase 6) + mini-test**

---

### Phase 8 — Multiple Inheritance and Mixins
**Goal:** Understand how class-based frameworks compose behavior with mixins.

- [ ] 8.1 — Multiple inheritance basics: a class with two unrelated parents, no diamond
- [ ] 8.2 — Both parents have a method with the same name. Which one wins, and why?
- [ ] 8.3 — The diamond problem: two parents share a common grandparent
- [ ] 8.4 — MRO conceptually: Python computes a linear order, inspect with `ClassName.__mro__`
- [ ] 8.5 — `super()` revisited: in multiple inheritance, `super()` means "next in MRO," not "parent"
- [ ] 8.6 — The mixin pattern: small, focused classes designed only to be mixed in
- [ ] **Phase 8 reading exercise**
- [ ] **Phase 8 recap (callback to Phase 7) + mini-test**

---

### Phase 9 — Abstract Base Classes
**Goal:** Force subclasses to implement specific methods.

- [ ] 9.1 — Why abstract classes exist (preventing incomplete subclasses)
- [ ] 9.2 — `from abc import ABC, abstractmethod`
- [ ] 9.3 — Defining abstract methods, what happens if you forget to override
- [ ] 9.4 — The "shared base class" pattern in pure Python (e.g., a `TimestampedEntity` base)
- [ ] **Phase 9 reading exercise**
- [ ] **Phase 9 recap (callback to Phase 8) + mini-test**

---

### Phase 10 — Capstone Project
**Goal:** Apply every concept from Phases 1–9 in one small system. Claude provides the design spec; the learner implements step by step.

- [ ] 10.1 — Claude gives the full spec: a tiny "blog" domain in pure Python — `User`, `Post`, `Comment`, an abstract `TimestampedEntity` base, a `Publishable` mixin, a `PostManager`-like class with `@classmethod` factories
- [ ] 10.2 — Implement the abstract base class and the mixin
- [ ] 10.3 — Implement `User` with properties, `__str__`, `__eq__`
- [ ] 10.4 — Implement `Post` using inheritance from the base + the mixin, with overridden `__init__` and `super()`
- [ ] 10.5 — Implement `Comment` similarly
- [ ] 10.6 — Implement `PostManager` with `@classmethod` factory methods
- [ ] 10.7 — Final review: walk through the whole codebase together, Claude points out which OOP concept each piece uses
- [ ] **Phase 10 reading exercise** (a longer class-based snippet)
- [ ] **Final recap + final mini-test covering all 10 phases**

---

## 5. Progress Tracker (update this after every session)

> **Instructions for Ranjit:** After each chat session, edit this section. Mark completed steps with `[x]` in the roadmap above, then update the fields below. Paste this whole file at the start of the next chat.

- **Last completed step:** _none yet — learning has not started_
- **Next step to start:** _1.1 — What a class is, what an object is, why OOP exists_
- **Date of last session:** _—_
- **Mini-test results so far:**
  - Phase 1: _—_
  - Phase 2: _—_
  - Phase 3: _—_
  - Phase 4: _—_
  - Phase 5: _—_
  - Phase 6: _—_
  - Phase 7: _—_
  - Phase 8: _—_
  - Phase 9: _—_
  - Final: _—_

### Personal notes (things Ranjit wants to remember between chats)

_Add anything here — concepts that were confusing, mistakes you made, things you want Claude to re-explain, terminology you want to revisit, etc._

- _(empty)_

### Claude's notes (things the previous Claude instance wants the next instance to know)

_At the end of each session, Claude should write 1–3 short notes here: which concepts the learner struggled with, which to reinforce, any mid-flight step splits that happened._

- _(empty)_

---

## 6. How to resume in a new chat

1. Open a new Claude.ai chat.
2. Paste this entire file as the first message.
3. Add one line at the end: **"Resume from step X.Y."** (replace X.Y with the value of *Next step to start* from the Progress Tracker above).
4. Claude will read the Context, Learner Profile, Teaching Contract, Roadmap, and Progress Tracker, then continue teaching from that exact step in the format defined by the Teaching Contract.
5. At the end of the session, ask Claude: **"Update the progress tracker for me."** Claude will give you the updated section to copy back into this file.

---

*End of file. Do not delete sections. Update only the Progress Tracker and notes.*
