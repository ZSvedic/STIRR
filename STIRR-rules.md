`#STIRR` (**S**pecify → **T**est → **I**mplement → **R**eview → **R**epeat) is an iterative AI dev system based on text conventions and is spec/test-driven. 

`#STIRR` is tool-free, meaning it works with any AI agent. It is "implemented" by humans and AI reading the 7 rules below (~7min read). If you don't like something, just change it.

## Rules

### `#TextRL` — Text for everything
Because LLMs prefer plain text, use text for:
- specs ([Markdown](https://en.wikipedia.org/wiki/Markdown)), 
- diagrams ([Mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) or [SVG](https://en.wikipedia.org/wiki/SVG)), 
- tabular data ([CSV](https://en.wikipedia.org/wiki/Comma-separated_values)), 
- hierarchical data ([JSON](https://www.json.org/json-en.html), [YAML](https://yaml.org/), or [TOML](https://toml.io/en/)), 
- scripting ([CLI](https://en.wikipedia.org/wiki/Command-line_interface) and [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell))), 
- initial user interface ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)), 
- task management (markdown or [Org Mode](https://orgmode.org/)), etc.  

Avoid specs in binary format, as they require error-prone conversion to text. 
If you need images, use formats that multimodal LLMs understand (JPEG or PNG). 

### `#ConventionRL` — Convention over configuration 
To make text files manageable, use the following [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration):

- **Hashtags** — Terms are identified by case-insensitive `#FooBar` hashtags. 

- **Separation of ownership** — AI work is separated from human work via hashtags:
  - `#Human` - Created or reviewed by human.
  - `#AI` - Created and modified by AI.
  
- **Referencing hastags** — Hashtags are specified in two ways:
  - **Explicit** — First hashtag at the top of a text file. Usually placed in the top comment or [frontmatter](https://jekyllrb.com/docs/front-matter/ "tags: #FooBar").
  - **Implicit** — A dummy directory file named `#FooBar` sets that tag for contained files. Only option for binary files.  
  
  Explicit is better for practical reasons. 
  E.g. if each text file starts with owner and feature hashtags, 
  find all signup specs by searching `#human #signup` in VSCode, GitHub search, or [CLI](https://github.com/BurntSushi/ripgrep "rg '#human' | rg '#signup'").

### `#SDD` — Specification-Driven Development
All implementation follows from specs. 

- **Be short** — Start minimal, for the simplest use case, on the simplest tech stack ([MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) spec).  
A good rule of thumb is the Rule of Fifths:
  - Specs and tests each <20% of code size.
  - If they exceed that, writing code directly is faster.

- **Example is worth a thousand words** — LLMs infer more [from one example](https://arxiv.org/abs/2005.14165) than from paragraphs of text. 
Give multiple examples and AI will infer a generalization.
Examples are in [text](#textrl--text-for-everything) with irrelevant parts shortened with `...`, AI can figure it out. 

- **Code spec** — Code is often part of the spec, either embedded or in a separate file with `#Human` ownership.
Code spec is used for critical parts, snippets shorter than their natural language description, and code that is considered final. 

- **Journal file** — A separate, append-only iteration journal can be longer.
It contains decisions, learnings, pivots, and experiments. 
It is loaded in context only when a history of decisions is needed.

- **Humans don't know their needs** — Needs are discovered gradually through feedback in each iteration.  
That also applies to legacy systems: 
  - Fully covering all legacy system behavior produces specs that are too long.
  - Even with full coverage, implementing that will reproduce the same app—with bugs, quirks, and bloat—without AI gains.

### `#TDD` — Test-Driven Development
Tests are part of the spec. 
Use [red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), meaning that tests are written before implementation and must fail (red). 
The goal of implementation is to make all tests green.  
Humans can't predict all ways software or AI can fail. Therefore, tests are added iteratively.

### `#ImplementRL` — AI implementation 
AI implements specs in code so the tests pass.  

- **Use [VCS](https://en.wikipedia.org/wiki/Version_control)** — Commit human edits before AI implementation. That will enable:
  - Reviewing AI changes as [diffs](https://en.wikipedia.org/wiki/Diff),
  - Rolling back and changing spec, if AI output is flawed  

- **Implementation is stateless** — the inputs are the specs and tests.  

- **Implementation is non-deterministic** — different AIs will generate different code. This is a good thing. In the future, better models will generate better apps from the same spec.

### `#HITL` — [Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop)
The human manually tests an implementation and examines code diffs. 
After discovering an issue, the required specs, tests, or the journal are updated. 

- **The end goal is human satisfaction** — Long-term satisfaction of software users and maintainers depends on, 
in the decreasing order of importance: correctness, ease of use, use of open standards, maintainability, and speed.  
I.e. don't optimize speed if the software is not working correctly.

- **Human is the bottleneck** — AI output is cheap. 
Human attention is not. 
In any workflow, the bottleneck is the human reading speed.  
To reduce AI verbosity, specify:
  - Max logical lines-of-code ([LOC](https://en.wikipedia.org/wiki/Source_lines_of_code)) without cheating:  
  exclude blanks and comments (humans need them), break lines at 80-char limit, no line-packing, etc. 
  - Max [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity). 

- **Hidden tests** — Instead of fixing the underlying issue, AI will sometimes make tests pass by adding workaround code, [just as people do](https://en.wikipedia.org/wiki/Volkswagen_emissions_scandal).
If that happens, create hidden tests that are not part of the spec.

### `#RepeatRL` — Repeat
Repeat the `Specify→Test→Implement→Review` loop, incrementally expanding specs, tests, or the journal. With each iteration, more code should change to `#Human` ownership. The process is finished when the specs have the required functionality, the tests pass, and the human has nothing to add.

## Next steps
Add this document to the [repository root](https://stackoverflow.com/questions/957928/is-there-a-way-to-get-the-git-root-directory-in-one-command "git rev-parse --show-toplevel") or it as an [agent skill](https://agentskills.io/home).  
To check compliance, run `./stirr` script.  
Feel free to [fork](https://en.wikipedia.org/wiki/Fork_(software_development)), `#STIRR` is MIT licensed. 
If you make major changes, don't forget to regenerate the stirr script from its `#STIRR` spec.  
