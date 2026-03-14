# `#STIRR`
**S**pecify → **T**est → **I**mplement → **R**eview → **R**epeat is a tool-free, iterative AI development workflow. 

Currently, AI agents tooling is in its infancy.
But AI agents work great with plain text, command line, git, and bash.
`#STIRR` uses [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) to create a text-based workflow.  

This doc is intended for both human and AI consumption.

## Rules

- **The end goal is human satisfaction / `#GoalRL`** — Long-term satisfaction of software users and maintainers depends on, 
in the decreasing order of importance: 
correctness, ease of use, use of open standards, maintainability, and speed. 
I.e. don't optimize speed if software is not working correctly.

- **Human is the bottleneck / `#BottleneckRL`** — AI output is cheap. 
Human attention is not. 
In any workflow, the bottleneck is the human reading speed.
The optimal process minimizes total human effort, and maximizes `#GoalRL`.

- **AI output is often flawed / `#FlawedRL`** — Wrong or verbose AI outputs causes the `#BottleneckRL` problem.

- **Humans don't know their needs / `#NeedsRL`** — 

- **Specification-Driven Development / `#SDD`** — Because of `#NeedsRL`, start with a minimal spec for the simplest use case, on the simplest tech stack.

- **Test-Driven Development / `#TDD`** —

- **AI implements specs and checks tests / `#ImplementRL`** —

- **Human in the loop / `#HITL`** - Human must manually test the implementation even if all automated tests pass. 
That is because `#NeedsRL` also applies to tests: humans can't predict all ways in software or AI can fail.  




## Conventions

- **Text / `#TextRL`** — Specs are in plain text, [markdown](https://en.wikipedia.org/wiki/Markdown), [mermaid diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams), [JSON](https://www.json.org/json-en.html) or [YAML](https://yaml.org/). 
Avoid specs in binary format. 
If you need images, use JPEG or PNG.

- **Hashtags / `#HashRL`** — Terms are identified by `#FooBar` hashtags, and referenced from text, code, or filenames. 
Hashtags are case-insensitive, so `#foobar` is the same as `#FooBar`.
Hashtags are prefered over links or x.y.z numbers as they are easier to refactor without breaking. 

- **Control tags / `#ControlRL`** — Control hashtags are:
  - `#HC` - **H**uman **C**ontroled 
  - `#RH` - **R**eviewed by **H**uman 
  - `#AI` - **AI** controled
  - `#Mix` - **Mix**ed control  
  
  Leftmost extension `.#[HC/RH/AI/Mix]` in a file/directory name indicates control.  
  E.g. dir `forms.#RH` indicates that AI agent can change contained files, but each change must be approved by a human before a commit. 
  Rename to `forms.#HC` stop AI suggesting changes to any form.  
  Text/markdown/code files with `.#Mix` extension will mark blocks as `#[HC/RH/AI]`, in any way human and AI will understand.   

- **Tree inheritance / `#TreeRL`** — When ommited, `#HashRL` and `#ControlRL` are inherited from a parent in a filesystem tree.


## Examples


E.g. Multiuser feature is given `#MultiuserFT` name on the first mention. AI agents or humans can search for context relevant to `#multiuserft` via local [ripgrep](https://github.com/BurntSushi/ripgrep), web search, or find inside editor. Folder with required binaries is named `binary.#MultiuserFT`. 

- 
