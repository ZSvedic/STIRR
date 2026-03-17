# `#STIRR`
**S**pecify → **T**est → **I**mplement → **R**eview → **R**epeat is an iterative AI development workflow that is based on text conventions, and is spec/test-driven. 

This document is intended for both human and AI consumption.

## Rules

- **Text / `#TextRL`** — Because LLMs prefer plain text, use text for everything:
  - specs ([markdown](https://en.wikipedia.org/wiki/Markdown)), 
  - diagrams ([mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) or [SVG](https://en.wikipedia.org/wiki/SVG)), 
  - tabular data ([CSV](https://en.wikipedia.org/wiki/Comma-separated_values)), 
  - hierarchical data ([JSON](https://www.json.org/json-en.html) and [YAML](https://yaml.org/)), 
  - scripting ([CLI](https://en.wikipedia.org/wiki/Command-line_interface) and [bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell))), 
  - initial user interface ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)), 
  - task management (markdown or [Org Mode](https://orgmode.org/)), etc.  

  Avoid specs in binary format, as they require error-prone conversion to text. 
  If you need images, use formats that multimodal LLMs understand (JPEG/PNG). 

- **Convention over configuration / `#ConventionRL`** — Because plain text lacks metadata and to avoid configuration file hell, use [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) instead.

- **Hashtags / `#HashRL`** — Terms are identified by `#FooBar` hashtags, and referenced from text, code, or filenames. 
Hashtags are case-insensitive, so `#foobar` is the same as `#FooBar`.
Hashtags are preferred over links or x.y.z numbers because they are short, descriptive, rarely change, and work everywhere (local, web, commit messages, etc). 

- **Separation of control / `#ControlRL`** — AI work is separated from human work via control hashtags:
  - `#HC` - **H**uman **C**ontroled 
  - `#RH` - **R**eviewed by **H**uman 
  - `#AI` - **AI** controlled
  - `#Mix` - **Mix**ed control  
  
  Leftmost extension `.#[HC/RH/AI/Mix]` in a file/directory name indicates control.  
  E.g. directory name `forms.#RH` indicates that an AI can change contained files, but each change must be approved by a human before a commit. 
  Rename to `forms.#HC` to stop AI suggesting changes.  
  Text/markdown/code files with the `.#Mix` extension mark blocks as `#[HC/RH/AI]`, in any form humans and AI will understand. 

- **Tree inheritance / `#TreeRL`** — When omitted, `#HashRL` and `#ControlRL` are inherited from a parent in a filesystem or document tree.
E.g. `SelfContained.#mix.ipynb` [Jupyter notebook](https://jupyter.org/) has text cells marked as `#HC`, code cells marked as `#AI`, and testing section marked with `#RH`.

- **The end goal is human satisfaction / `#GoalRL`** — Long-term satisfaction of software users and maintainers depends on, in the decreasing order of importance: 
  - correctness, 
  - ease of use, 
  - use of open standards, 
  - maintainability, 
  - speed.  

  I.e. don't optimize speed if software is not working correctly.

- **Human is the bottleneck / `#BottleneckRL`** — AI output is cheap. 
Human attention is not. 
In any workflow, the bottleneck is the human reading speed.
The optimal process minimizes total human effort, and maximizes `#GoalRL`.

- **AI output is often flawed / `#FlawedRL`** — Wrong or verbose AI outputs cause the `#BottleneckRL` problem.  
To detect errors without human review, use automated tests.  
To reduce verbosity, specify max lines-of-code (LOC) or max [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity).

- **Humans don't know their needs / `#NeedsRL`** — Needs are discovered gradually, by giving feedback on every iteration. 

- **Specification-Driven Development / `#SDD`** — All implementation follows from specs. 
Because of `#NeedsRL`, start with a minimal spec for the simplest use case, on the simplest tech stack ([MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) spec). 
Keep specification as short as possible for the given problem.

- **Immutable Code / `#ImCodeRL`** — Code can also be part of the spec, if marked as such.
Immutable code is used for critical parts, snippets shorter than their natural language description, and for code considered final. 

- **Red Green Test-Driven Development / `#TDD`** — Tests are part of the spec.
Use [red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), 
meaning that tests are written before implementation and must fail (red). 
Goal of implementation is to make all tests green.
`#NeedsRL` also applies to tests: humans can't predict all ways in software or AI can fail.
Therefore, new tests are added on every iteration.

- **Brevity / `#BrevityRL`** — Don't repeat yourself (`#DRY`) in specs or tests, because they change with every iteration.
A good rule of thumb is the rule of fifths:
both specs size and tests size should be less than 1/5 of the implemented code size. 
Larger sizes don't make sense as then it is faster to write code directly.

- **Journal / `#JournalRL`** — Specs and tests need to be concise because they are constantly read and modified.
Separate daily journal that can be longer contains decisions, learnings, pivots, and experiments. 
It is consulted only when a spec or test decision is not clear.

- **AI implementation / `#ImplementRL`** — AI tries to generate code from specs so the tests pass. 
In the end AI reports the results and learnings.
Implementation is stateless, meaning that the only inputs are specs and tests.

- **Commit / `#CommitRL`** — If the implementation succeeded, changes are committed to [VCS](https://en.wikipedia.org/wiki/Version_control).

- **Human review / `#ReviewRL`** - [Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop) manually tests an implementation and examines code diffs. 
After discovery of an issue, the required specs, tests, or journal are updated.  
Instead of fixing the underlying issue, AI will sometimes make tests pass by adding workaround code, [same as people do](https://en.wikipedia.org/wiki/Volkswagen_emissions_scandal).
If that happens, create hidden tests that are not part of the specification and run them manually.

- **Repeat / `#RepeatRL`** — Repeat the Specify → Test → Implement → Review loop, incrementally expanding specs, tests, or the journal. With each iteration, more code should be marked as finished with #HC. The process is complete when the specs have the required functionality, tests pass, and the human has nothing to add.
