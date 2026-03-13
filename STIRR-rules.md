# `#STIRR`
**S**pecify → **T**est → **I**mplement → **R**eview → **Repeat** is a tool-free iterative AI development workflow. 

Currently, AI agents tooling is in its infancy.
But AI agents work great with plain text, command line, git, and bash.
`#STIRR` uses [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) to create a text-based workflow.  

This doc is intended for both human and AI consumption.

## Rules

- **Text / `#TextRL`** — Specs are in plain text, [markdown](https://en.wikipedia.org/wiki/Markdown), [mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) diagrams, [JSON](https://www.json.org/json-en.html) or [YAML](https://yaml.org/). 
Avoid binary format specs as LLMs and CLI tools prefer text. If you need images, use JPEG or PNG.

- **Hashtags / `#HashRL`** — Terms are identified by `#FooBar` hashtags, and referenced from text, code, or filenames. 
Hashtags are case-insensitive, so `#foobar` is the same as `#FooBar`.
Hashtags are prefered over links or x.y.z numbers as they are easier to refactor without breaking. 

- **Control tags / `#ControlRL`** — Control hashtags are:
  - `#HC` - **H**uman **C**ontroled 
  - `#RH` - **R**eviewed by **H**uman 
  - `#AI` - **AI** controled
  - `#Mix` - **Mix**ed control  
  For files and dirs, leftmost extension `.#[HC/RH/AI/Mix]` in a filename indicates control. 
  E.g. dir `forms.#RH` indicates that AI agent can change contained files, but each change must be approved by a human before a commit. 
  Rename to `forms.#HC` stop AI suggesting changes to any form.
  Text/markdown/code files with `.#Mix` extension prefix mark blocks as `#[HC/RH/AI]`, in any way human and AI will understand.   

- **Tree inheritance / `#TreeRL`** — When ommited, `#HashRL` and `#ControlRL` are inherited from a parent in a filesystem tree.

- **Goal / `#GoalRL`** — The end goal is software that makes humans happy.
Human long-term happines depends on the following, in the decreasing order:
  1. Correctness — works for main use cases.
  2. UX - easy to learn and use.
  3. Openness — uses open standards.
  4. Maintainability — less lines of code, less dependencies, less complexity.
  5. Speed — works fast. 
I.e. don't work on speed if software is not working correctly.

- 


## Examples


E.g. Multiuser feature is given `#MULTIUSER-FT` name on the first mention. AI agents or humans can search for context relevant to `#MULTIUSER-FT` via local [ripgrep](https://github.com/BurntSushi/ripgrep), web search, or find inside editor. Folder with required binaries is named `binary.#MULTIUSER-FT`. 

- 
