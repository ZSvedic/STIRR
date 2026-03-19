`#STIRR` (**S**pecify → **T**est → **I**mplement → **R**eview → **R**epeat) is an iterative AI dev system based on text conventions and is spec/test-driven. 

`#STIRR` is tool-free, meaning that it works with any AI agent. It is "implemented" by humans and AI reading the 3 pages below (~7min read). If you don't like something, just change it.

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

  - **Hashtags** — Terms are identified by `#FooBar` hashtags, are case-insensitive, and are referenced in text or code. 

  - **Separation of ownership** — AI work is separated from human work via hashtags:
    - `#Human` - Created or reviewed by human.
    - `#AI` - Created and modified by AI.
    
    Hashtags are specified in two ways:
    - **Explicit** — Hashtags at the top of a text file. Usually placed in the top comment or [frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter "tags: #FooBar").
    - **Implicit** — A dummy directory file named `#FooBar` sets that tag for contained files. Only option for binary files.  
    
    Explicit is better for practical reasons. 
    E.g. if each text file starts with owner and feature hashtags, 
    find all signup specs by searching `#human #signup` in VSCode, GitHub search, or [CLI](https://github.com/BurntSushi/ripgrep "rg '#human' | rg '#signup'").

### `#GoalRL` — The end goal is human satisfaction
Long-term satisfaction of software users and maintainers depends on, in the decreasing order of importance: 
- correctness, 
- ease of use, 
- use of open standards, 
- maintainability, 
- speed.  

I.e. don't optimize speed if the software is not working correctly.

### `#BottleneckRL` — Human is the bottleneck
AI output is cheap. 
Human attention is not. 
In any workflow, the bottleneck is the human reading speed.
Minimize total human effort and maximize `#GoalRL`.

### `#FlawedRL` — AI is unreliable
Wrong or verbose AI outputs cause the `#BottleneckRL` problem.  
To detect errors without human review, use automated tests.  
To reduce verbosity, specify max [LOC](https://en.wikipedia.org/wiki/Source_lines_of_code "lines-of-code") or max [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity).

### `#NeedsRL` — Humans don't know their needs
Needs are discovered gradually by giving feedback on every iteration. 
That also applies to legacy systems: 
- Fully covering all behaviors often exceeds `#BrevityRL` rule below.
- Even with full coverage, implementing that will reproduce the same app—bugs, quirks, and bloat—without AI gains.

### `#SDD` — Specification-Driven Development
All implementation follows from specs. 
Because of `#NeedsRL`, start with a minimal spec for the simplest use case, on the simplest tech stack ([MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) spec). 
Keep the specification as short as possible for the given problem.

### `#CodeRL` — Code spec
Code is often part of the spec, either embedded or in a separate file with `#Human` ownership.
Code spec is used for critical parts, snippets shorter than their natural language description, and code that is considered final. 

### `#TDD` — Tests are part of the spec
Use [red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), meaning that tests are written before implementation and must fail (red). 
The goal of implementation is to make all tests green.  
`#NeedsRL` also applies to tests: humans can't predict all ways software or AI can fail.
Therefore, tests are added iteratively.

### `#ShortenRL` — Be short
Don't repeat yourself in specs or tests, because they change with every iteration.
A good rule of thumb is the Rule of Fifths:
- Specs and tests each < 20% of code size.
- If they exceed that, writing code directly is faster.

### `#JournalRL` — Journal file
A separate iteration journal, which can be longer, contains decisions, learnings, pivots, and experiments. 
It is consulted only when a spec or test decision is not clear.

### `#CommitRL` — Commit before AI
Because AI tends to be code-happy, commit human changes to a [VCS](https://en.wikipedia.org/wiki/Version_control) before AI implementation.
That will enable:
- Reviewing AI changes as [diffs](https://en.wikipedia.org/wiki/Diff),
- Rolling back and changing spec, if AI output is `#FlawedRL`. 

### `#ImplementRL` — AI implements code from specs so the tests pass
In the end, AI reports the results and learnings.  
Implementation is stateless, meaning that the only inputs are the specs and tests.  
Implementation is non-deterministic, meaning that different AIs will generate different code. This is a good thing. In the future, better models will generate better apps from the same spec.

### `#ReviewRL` — Human review
[Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop) manually tests an implementation and examines code diffs. 
After the discovery of an issue, the required specs, tests, or the journal are updated.  
Instead of fixing the underlying issue, AI will sometimes make tests pass by adding workaround code, [same as people do](https://en.wikipedia.org/wiki/Volkswagen_emissions_scandal).
If that happens, create hidden tests that are not part of the spec.

### `#RepeatRL` — Repeat
Repeat the `Specify → Test → Implement → Review` loop, incrementally expanding specs, tests, or the journal. With each iteration, more code should change to `#Human` ownership. The process is finished when the specs have the required functionality, the tests pass, and the human has nothing to add.

## Next steps
Add this document to the [repository root](https://stackoverflow.com/questions/957928/is-there-a-way-to-get-the-git-root-directory-in-one-command "git rev-parse --show-toplevel") or load as [agent skill](https://agentskills.io/home).  
To check compliance, run `./stirr` script.  
Feel free to [fork](https://en.wikipedia.org/wiki/Fork_(software_development)), `#STIRR` is MIT licensed. 
If you make major changes, don't forget to regenerate the stirr script from its `#STIRR` spec.   
