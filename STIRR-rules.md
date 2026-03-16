# `#STIRR`
**S**pecify → **T**est → **I**mplement → **R**eview → **R**epeat is an AI development workflow that is: 
text-based, convention-based, spec-driven, test-driven, and iterative. 

This doc is intended for both human and AI consumption.

## Rules

- **Text / `#TextRL`** — Because LLMs prefer plain text, use text for everything:
specs ([markdown](https://en.wikipedia.org/wiki/Markdown)), 
diagrams ([mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) or [SVG](https://en.wikipedia.org/wiki/SVG)), 
tabular data ([CSV](https://en.wikipedia.org/wiki/Comma-separated_values)), 
hierarchical data ([JSON](https://www.json.org/json-en.html) and [YAML](https://yaml.org/)), 
scripting ([CLI](https://en.wikipedia.org/wiki/Command-line_interface) and [bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell))), 
initial user interface ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)), 
task management (markdown or [Org Mode](https://orgmode.org/)), 
etc.
Avoid specs in binary format, because they require issue-prone conversion to text. 
If you need images, use formats that multimodal LLMs understand (JPEG/PNG). 

- **Convention over configuration / `#ConventionRL`** — Because plain text lacks metadata and to avoid configuration file hell, use [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) instead.

- **Hashtags / `#HashRL`** — Terms are identified by `#FooBar` hashtags, and referenced from text, code, or filenames. 
Hashtags are case-insensitive, so `#foobar` is the same as `#FooBar`.
Hashtags are prefered over links or x.y.z numbers because they are short, descriptive, rarely change, and work everywhere (local, web, commit messages, etc). 

- **Separation of control / `#ControlRL`** — AI work is separated from human work, via control hashtags:
  - `#HC` - **H**uman **C**ontroled 
  - `#RH` - **R**eviewed by **H**uman 
  - `#AI` - **AI** controled
  - `#Mix` - **Mix**ed control  
  
  Leftmost extension `.#[HC/RH/AI/Mix]` in a file/directory name indicates control.  
  E.g. dir `forms.#RH` indicates that AI agent can change contained files, but each change must be approved by a human before a commit. 
  Rename to `forms.#HC` stop AI suggesting changes to any form.  
  Text/markdown/code files with `.#Mix` extension will mark blocks as `#[HC/RH/AI]`, in any form human and AI will understand. 

- **Tree inheritance / `#TreeRL`** — When ommited, `#HashRL` and `#ControlRL` are inherited from a parent in a filesystem or document tree.
E.g. `SelfContained.#mix.ipynb` [Jupyter notebook](https://jupyter.org/) has text cells marked as `#HC`, code cells marked as `#AI`, and testing section marked with `#RH`.

- **The end goal is human satisfaction / `#GoalRL`** — Long-term satisfaction of software users and maintainers depends on, 
in the decreasing order of importance: 
correctness, ease of use, use of open standards, maintainability, and speed. 
I.e. don't optimize speed if software is not working correctly.

- **Human is the bottleneck / `#BottleneckRL`** — AI output is cheap. 
Human attention is not. 
In any workflow, the bottleneck is the human reading speed.
The optimal process minimizes total human effort, and maximizes `#GoalRL`.

- **AI output is often flawed / `#FlawedRL`** — Wrong or verbose AI outputs causes the `#BottleneckRL` problem.

- **Humans don't know their needs / `#NeedsRL`** — Needs are discovered gradually, by giving feedback on every iteration. 

- **Specification-Driven Development / `#SDD`** — All implementation follows from specs. 
Because of `#NeedsRL`, start with a minimal spec for the simplest use case, on the simplest tech stack ([MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) spec). 
Keep specification as short as possible for the given problem.
Two types of spec: code-spec and general spec

- **Immutable Code / `#ImCodeRL`** — Code can also be part of the spec, if marked as such.
It is used for critical code, code snippets shorter than their natural language description, and for code considered final. 

- **Red Green Test-Driven Development / `#TDD`** — Tests are part of the spec.
Use [Reed/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), 
meaning that tests are writen before implementation and must fail (red). 
Goal of implementation is to make all tests green.
`#NeedsRL` also applies to tests: humans can't predict all ways in software or AI can fail.
Therefore, new tests are added on every iteration.

- **Brevity / `#BrevityRL`** — Don't repeat yourself (`#DRY`) in specs or tests, because they change with every iteration.
Good rule of thumb is rule of fifths. 
Both specs size and tests size should be less than 1/5th of the implemented code size. 
Larger sizes don't make sense because it is faster to write code dicrectly than to read and edit specs and tests.

- **Journal / `#JournalRL`** — Specs and tests need to be concise because they are constantly read and modified.
Decisions, learnings, pivots, and experiments are appended to a separate daily journal, that can be longer. 
It is consulted only when a spec or test decision is not clear.

- **AI implementation / `#ImplementRL`** — AI tries to generate code from specs that passes tests. 
In the end AI reports the results and learnings.
Implementation is stateless, meaning that only inputs are specs + tests.

- **Commit / `#CommitRL`** — If the implementation succeeded, changes are commited to [VCS](https://en.wikipedia.org/wiki/Version_control).

- **Human review / `#ReviewRL`** - [Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop) manually tests an implementation and examines code diffs. 
After discovery of an issue, required specs, tests or journal are updated.
[Same as people](https://en.wikipedia.org/wiki/Volkswagen_emissions_scandal), instead of fixing the underlying issue, AI will sometimes make test pass by adding workaround code.
If that happens, create hidden test that are not part of the specification and run them manually.

- **Repeat / `#RepeatRL`** — Repeat Specify → Test → Implement → Review loop, incrementaly expanding specs, tests or journal. 
