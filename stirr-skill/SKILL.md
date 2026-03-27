---
name: stirr-skill
description: STIRR (Specify → Test → Implement → Review → Repeat) is an iterative AI dev system based on text conventions and is spec/test-driven. Use when directly invoked, when stirr is mentioned, or when the user is asking about TDD or SDD dev processes. 
license: MIT
metadata:
  author: Zeljko Svedic
  version: "0.4"
---

## Rules

### `#TextRL` — Text for everything
Because [agents](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/), [VCS](https://en.wikipedia.org/wiki/Version_control), and [diffs](https://en.wikipedia.org/wiki/Diff) all work on plain text, use text for:
- specs ([Markdown](https://en.wikipedia.org/wiki/Markdown)), 
- diagrams ([Mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) or [SVG](https://en.wikipedia.org/wiki/SVG)), 
- tabular data ([CSV](https://en.wikipedia.org/wiki/Comma-separated_values)), 
- hierarchical data ([JSON](https://www.json.org/json-en.html), [YAML](https://yaml.org/), or [TOML](https://toml.io/en/)), 
- scripting ([CLI](https://en.wikipedia.org/wiki/Command-line_interface) and [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell))), 
- mock text UI ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)), 
- user UI ([HTML, CSS, and JS](https://en.wikipedia.org/wiki/Front-end_web_development)).
- task management (Markdown or [Org Mode](https://orgmode.org/)), etc.  

Avoid specs in binary format.
If you need images, use formats that multimodal LLMs understand (JPEG or PNG). 

### `#ConventionRL` — Convention over configuration 
To make text files manageable, use the following [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration):

- **Hashtags** — Terms are identified by case-insensitive `#FooBar` hashtags. 

- **Separation of ownership** — AI work is separated from human work via hashtags:
  - `#Human` - Created or reviewed by human.
  - `#AI` - Created and modified by AI.
  
- **Referencing hashtags** — Hashtags are specified in two ways:
  - **Explicit** — First hashtag at the top of a text file. 
  Usually placed in the top comment or [frontmatter](https://jekyllrb.com/docs/front-matter/ "tags: #FooBar").
  - **Implicit** — A dummy directory file named `#Foo[.#Bar...]`  sets that tag(s) for contained files. 
  Only option for binary files.  
  
  Explicit is better for practical reasons. 
  E.g., if each text file starts with owner and feature hashtags, 
  find all signup specs by searching `#human #signup` in VSCode, GitHub search, or [rg in CLI](https://github.com/BurntSushi/ripgrep "rg '#human' | rg '#signup'").

### `#SDD` — Specification-Driven Development
Write specs before implementation:

- **Be short** — Start minimal, for the simplest use case, on the simplest tech stack ([MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) spec).  
A good rule of thumb is that spec size should be <30% of generated code size.
If the spec is larger, it is usually faster to write code directly.

- **Example is worth a thousand words** — LLMs infer more [from one example](https://arxiv.org/abs/2005.14165) than from paragraphs of text. 
Give multiple examples and AI will infer a generalization.
Examples are in [text](#textrl--text-for-everything) with irrelevant parts shortened with `...`; the AI can figure it out. 
Bootstrap examples using modified outputs from the previous iteration for the next. 

- **Code spec** — Code is often part of the spec, either embedded or in a separate file with `#Human` ownership.
Code spec is used for critical parts, snippets shorter than their natural language description, and code that is considered final. 

- **Journal file** — A separate, append-only iteration journal can be longer.
It contains decisions, learnings, pivots, and experiments. 
It is loaded in context only when a history of decisions is needed.

- **Humans don't know their needs** — Needs are discovered gradually through feedback in each iteration.  
That also applies to legacy systems. Fully covering all legacy system behavior produces specs that are too long. Even with full coverage spec, implementing it will reproduce the same app—with bugs, quirks, and bloat—without AI gains.

### `#TDD` — Test-Driven Development
Tests are generated from the spec. 
If AI-generated, they are reviewed by humans.  
Use [red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), meaning that tests are written before implementation and must initially fail (red). 
The goal of implementation is to make all tests green.  
Humans can't predict all ways software or AI can fail. Therefore, tests are added iteratively.

### `#ImplementRL` — AI implementation 
AI implements specs in code so that the tests pass. 

Commit human edits *before* AI implementation to allow:
- Reviewing AI changes as diffs.
- Rolling back and changing spec, if AI went in completely wrong direction.  

*Implementation is non-deterministic* — different AIs will generate different code. This is a good thing. In the future, better models will generate better apps from the same spec.

### `#HITL` — [Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop)
The human manually tests an implementation and examines code diffs. 
After discovering an issue, the required specs, tests, or the journal are updated. 

- **The end goal is human satisfaction** — Long-term satisfaction of software users and maintainers depends on, 
in the decreasing order of importance: correctness, usability, interoperability, maintainability, and speed.  
I.e., don't optimize speed if the software is not working correctly.

- **Human is the bottleneck** — AI output is cheap. 
Human attention is not. 
In any workflow, the bottleneck is human reading speed.  
To reduce AI verbosity, specify a max lexical token count (LTOK).
As identifiers are one LTOK, the AI has no incentive to use short names.
For most programming languages, 1 [LOC](https://en.wikipedia.org/wiki/Source_lines_of_code "line-of-code") is ~10 LTOK. 
The `stirr-tree.py` script displays a simple LTOK calculation for all text/code files. 

- **Hidden tests** — Instead of fixing the underlying issue, AI will sometimes make tests pass by adding workaround code, [just as people do](https://en.wikipedia.org/wiki/Volkswagen_emissions_scandal). 
If that happens, create hidden tests that are executed manually.

### `#RepeatRL` — Repeat
Repeat the `Specify → Test → Implement → Review` loop by incrementally expanding specs, tests, or the journal. With each iteration, more code should change to `#Human` ownership. The process is finished when the specs cover the required functionality, the tests pass, and the human has nothing to add.

## Checking compliance
- Run [`./stirr-tree.py`](./stirr-tree.py) to display the project file tree with LTOK counts and hashtags.
- Run [`./stirr-check.sh`](./stirr-check.sh) to check compliance with the rules. 
  It sends `stirr-tree.py` output to CLI coding agent of your choice (Codex/Claude).