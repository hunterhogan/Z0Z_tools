---
name: Docstring Standards
description: Standards for Python docstrings.
---
# Write Consistent, Precise NumPy-style Docstrings

Use [NumPy style](https://numpydoc.readthedocs.io/en/v1.10.0/format.html#docstring-standard) with the following modifications and additional requirements.

## Modifications to the NumPy Docstring Standards

1. Replace the generic "Notes" section with one or more semantic section names instead.
2. Public, non-method attributes must be documented.
3. Use Unicode for all mathematical symbols, not LaTeX.
4. Use plain text with NumPy-style section headers, not reStructuredText.

## Technical Syntax

- **Triple double quotes.** Always use `"""`, never `'''`.
- **Full stops.** End every sentence with a full stop, including the summary line.
- **No end-of-line colons in prose.** Machine parsers may interpret a trailing colon as syntax. Restructure the sentence instead.
- **No LaTeX.** Use Unicode characters for all mathematical symbols (e.g., ×, ÷, √, ∑, ≤, ∈, →).
- **No reST.** Do not use reStructuredText directives, roles, or markup (e.g., no `.. note::`, no `:param:`, no `:math:`). Write plain text with NumPy-style section headers.
- **Indentation.** Follow the project `.editorconfig` for indentation width and type. Within a docstring, indent continuation lines by one level relative to the section entry.

## Docstring Layout

### Sections and their Order Within a Docstring

1. Summary line (on the same line as the opening triple quotes)
2. (AI generated docstring) marker, if applicable
3. Extended description
4. `Parameters`
5. `Returns` or `Yields`
6. `Raises`
7. `Warns`
8. `Other Parameters`
9. `See Also`
10. Custom-named sections (e.g., `Mathematical Basis`, `Algorithm Details`)
11. `Examples`
12. `References`

### Formatting a Docstring Section

Use this exact structure for all named sections:

```text
[blank line]
Section Name
------------
entry : datatype
    Definition or description.
entry : datatype = defaultValue
    Definition or description.
```

### Formatting a Function

```python
def exampleFunction(parameterFirst: int, parameterSecond: str = "default") -> bool:
    """Validate input parameters and return success status.

    (AI generated docstring)

    You can use this function to validate input parameters before processing. The function
    checks each parameter against defined constraints and returns success status. Extended
    description uses explicit subjects to provide context. Cite references in text [1].

    Parameters
    ----------
    parameterFirst : int
        Description of the parameter.
    parameterSecond : str = "default"
        Description with default value noted after the type.

    Returns
    -------
    isValid : bool
        Description of the return value.

    References
    ----------
    [1] Relevant documentation or concept being referenced
        https://example.com/documentation
    """
```

### Formatting a Module

Place the module docstring at the very top of the file, before imports. Include a table of contents listing all public identifiers.

```python
"""Perform map-folding computations and analysis.

(AI generated docstring)

You can use this module to compute distinct foldings of multi-dimensional maps. The module
provides the core algorithms and orchestrates computation workflows. Extended description
of module purpose and organization.

Contents
--------
Functions
    functionAlpha
        One-line description of functionAlpha.
    functionBeta
        One-line description of functionBeta.

Classes
    ClassAlpha
        One-line description of ClassAlpha.

"""
import ...
```

#### Include all public identifiers in the table of contents

- List all public functions, classes, and other exported identifiers.
- If there are sections (`#======== Boolean filters ====`) and subsections (`#---- Specific filters ----`), reflect that hierarchy.
- Maintain alphabetical order within each section.
- Provide one-line descriptions for each item.
- Omit private identifiers (those starting with `_`).

### Formatting a Package `__init__.py`

Document what the package exposes and its organizational purpose. Include a table of contents of public modules and subpackages.

```python
"""Access map-folding algorithms and utilities.

(AI generated docstring)

You can use this package to compute distinct foldings of multi-dimensional maps. This package
provides implementations of various map-folding counting algorithms, state management for
parallel computations, and interfaces to OEIS sequences.

Modules
-------
basecamp
    Entry point for map-folding computations with algorithm selection.
dataBaskets
    State containers and data structures for folding computations.
filesystemToolkit
    Utilities for result persistence and caching.

Subpackages
-----------
algorithms
    Collection of map-folding algorithm implementations.
_e
    Experimental elimination-based algorithms (internal research code).
"""
```

#### Include all public modules and subpackages in the table of contents

- List public modules with brief descriptions.
- List subpackages with brief descriptions.
- Use section headers (`Modules`, `Subpackages`) with dashed underlines.
- Omit private modules (starting with `_`) unless they are documented internal APIs.

### Formatting a Top-Level Package `__init__.py`

The top-level `__init__.py` follows the same format as any package `__init__.py`, but the extended description should also state the package's purpose and scope for users encountering it for the first time.

### Documenting and Formatting Variables and "Constants"

Public class-level and instance-level variables must be documented, either in the class `Attributes` section, as an inline docstring immediately after the assignment, or both.

```python
class Configuration:
    """Store and manage configuration settings.

    (AI generated docstring)

    You can use this class to maintain configuration values across the application.

    Attributes
    ----------
    settingDefault : int
        The default setting value applied when no override is provided.
    """

    settingDefault: int = 42
    """The default setting value applied when no override is provided."""
```

Module-level constants follow the same sections as functions where applicable: summary, extended description, `See Also`, `References`, `Examples`.

## Docstring Sections

### Summary Line

**For public identifiers** (functions, classes, methods, variables without leading underscore):

The summary line must be written as **a second-person declarative clause expressing dynamic modality with an implied subject**.

- **Second person with implied subject**: Address the reader as "you" implicitly, omitting the explicit subject pronoun.
- **Declarative**: State a fact or capability, not issue a command.
- **Dynamic modality**: Express ability, possibility, or permission using modal verbs like "can", "may", "will", or present tense with capability implications.
- **Terse**: Keep the summary line concise by using Subject-Verb-Object structure with the subject implied.

**Start with the verb on the opening `"""` line and end with a full stop.**

- Start the summary on the same line as the opening triple quotes.
- Start with the verb directly (implied "you can" or "you may").
- Follow with the object and any essential modifiers.
- End with a full stop.

- ✅ Correct: "Express descending iteration or a reverse direction."
- ✅ Correct: "Compute the total number of distinct map foldings for a given shape."
- ✅ Correct: "Convert a pile range to an iterator of individual leaves."
- ✅ Correct: "Validate folding constraints before computation."

- ❌ Incorrect: "You can express descending iteration." (explicit subject - too verbose for summary)
- ❌ Incorrect: "Compute the total number of distinct map foldings." (imperative mood without modal - sounds commanding)
- ❌ Incorrect: "Computes foldings." (third person, not second person)
- ❌ Incorrect: "Returns the iterator." (too passive, not focused on reader capability)

**For private identifiers** (functions, classes, methods, variables with leading underscore):

The summary line must be written in **first-person descriptive voice** explaining how the identifier functions within the codebase architecture.

- **First person**: Use "I use this..." from the developer's perspective.
- **Descriptive**: Explain the identifier's role in relation to other code, such as control flow, shared subroutines, or something else.
- **Architectural focus**: Clarify how this private component fits into the larger system.

- ✅ Correct: "I use this shared subroutine for validating input across multiple public methods."
- ✅ Correct: "I use this to manage control flow between the preprocessing and computation phases."
- ✅ Correct: "I use this to cache intermediate results during recursive folding operations."

- ❌ Incorrect: "You can validate input." (second person - implies public API)
- ❌ Incorrect: "Validates input." (third person - too passive, doesn't explain architectural role)
- ❌ Incorrect: "Validate input before processing." (imperative - doesn't explain usage context)

### AI-Generated Marker

When creating a new docstring, place "(AI generated docstring)" on its own line after the summary line and a blank line. When reformatting an existing docstring, do NOT add or remove "(AI generated docstring)".

### Extended Description

After the terse summary line, start the body text with an **explicit subject** ("You can...", "The identifier...", "This function...") to provide context and smooth the transition from the concise summary to the detailed explanation. The extended description should clarify functionality, not discuss implementation detail or background theory.

### Parameters

- Use the parameter name exactly as it appears in the signature.
- Include the type annotation from the signature.
- If a default value exists (in signature or logic), append `= defaultValue` after the type.
- Use one level of indentation for the description.
- When a parameter accepts a fixed set of values, list them in braces with the default first: `order : {'C', 'F', 'A'}`.
- Always use PEP 585 style (`list[int]`, not `List[int]`).
- Use PEP 604 style (`int | None`, not `Optional[int]`; `int | str`, not `Union[int, str]`).

### Returns and Yields

- Use a meaningful identifier, not just the type.
- Format: `meaningfulName : returnType`
- For generators, use `Yields` instead of `Returns`.

### Raises

List exceptions that are non-obvious or have a significant chance of being raised.

### See Also

Direct users to related functions they may not be aware of. Format:

```text
See Also
--------
relatedFunction : One-line description of relatedFunction.
anotherFunction, thirdFunction
```

### Use Descriptive Section Names Instead of "Notes"

When additional information is needed beyond the standard sections, create a section with a descriptive name. Examples: `Mathematical Basis`, `Algorithm Details`, `Thread Safety`, `Concurrency`, `Memory Management`.

**Write `Mathematical Basis` sections for academic experts without simplification.** Use precise academic terms, standard Unicode notation, and establishing statements ("Let p be...") to bridge code identifiers and academic nomenclature.

**Keep mathematical notation out of general sections.** Summary, Parameters, and Returns must remain accessible to non-specialists. Reserve dense notation for dedicated custom sections.

### Draw Examples from Real Usage, Never from Invention

Private identifiers (starting with `_`) do not require an `Examples` section.

Examples must be drawn from actual usage in the codebase. To find examples, search for real invocations of the documented identifier, then select and simplify representative usage.

1. Use code search to find real invocations of the documented function/class.
2. Select representative usage that demonstrates typical or important patterns.
3. Simplify if needed, but preserve the identifier style and conventions of the codebase.
4. If no real usage exists in the codebase, note this limitation.

**Never create contrived examples.** Real code demonstrates actual patterns and validates that the function works as documented.

- Examples must follow the identifier and style conventions of the codebase.
- Include context if needed for clarity (imports, setup, etc.).
- Use triple-backtick code fences for all code examples, not REPL-style `>>>` prompts. Indent the code fence block one level deeper than the surrounding explanatory text.

### References

Docstrings must provide navigation to related code and external resources. All references should be collected in a `References` section at the end of the docstring, numbered sequentially, and cited in the text using `[1]`, `[2]`, etc.

**Reference any concept or identifier a reader might need to look up.** The following categories always need references.

1. **External packages and APIs**: Any mention of third-party libraries or their components.
   - `pandas.DataFrame`, `numpy.ndarray`, `requests.Session`
   - Use Context7 links when available for well-documented packages.
   - Use official documentation links as fallback.

2. **Standard library items** (selective):
   - Rarely used modules or functions.
   - Edge cases or subtle behaviors.
   - Complex APIs (e.g., `asyncio`, `collections.abc`, `operator`).
   - Skip universally known items (e.g., `list`, `dict`, `str`, `int`).

3. **Same-package references**:
   - Functions, classes, or methods defined elsewhere in the package.
   - Related utilities.
   - Algorithms or data structures used internally.

4. **Theoretical foundations**:
   - Mathematical concepts (group theory, graph theory, combinatorics).
   - Algorithms (sorting, searching, optimization).
   - Academic papers or textbooks.
   - Wikipedia articles for established concepts.

5. **Standards and specifications**:
   - IETF RFCs, W3C specifications, PEPs.
   - File formats (JSON, CSV, HDF5).
   - Protocols (HTTP, TCP, MQTT).

**Backticks indicate but do not determine the need for a reference.** Skip references for identifiers already in the function signature. Conversely, some concepts need references even without backticks (e.g., "Chinese numerals" refers to a cultural/linguistic system).

```python
def exampleFunction(data: list[int]) -> int:
    """Compute the sum using this positional notation system [1].

    This function implements the algorithm described in [2] using `gmpy2` [3]
    for arbitrary-precision arithmetic. The approach is related to
    `mapFolding.basecamp.countFolds` [4].

    Parameters
    ----------
    data : list[int]
        Input values in positional notation.

    Returns
    -------
    total : int
        Sum of input values.

    References
    ----------
    [1] Positional notation - Wikipedia
        https://en.wikipedia.org/wiki/Positional_notation
    [2] Knuth, D. E. (1997). The Art of Computer Programming, Volume 2:
        Seminumerical Algorithms (3rd ed.). Addison-Wesley.
    [3] gmpy2 - Context7
        https://gmpy2.readthedocs.io/en/latest/
    [4] mapFolding.basecamp.countFolds
    """
```

**Verify every link and cite references in order of first appearance.**

- When modifying an existing docstring, verify all existing links as a maintenance task.
- Cite references in the text using `[1]`, `[2]`, etc., immediately after the relevant term or concept.
- Multiple references for one concept: `[1, 2]` or `[1][2]` (be consistent within a docstring).
- List references in order of first citation.
- Include both title/description and URL for web resources.
- For packages: prefer Context7 links when available.
- For academic papers: include full citation (author, year, title, publication).
- For internal package references: use the module path only. No additional annotation is needed, but so IDEs render the section properly, put a blank line where the annotation would go.

**Prefer these documentation URLs when referencing these packages.** Add other packages as needed using the same pattern (Context7 when available, official documentation otherwise).

- `hunterMakesPy`: <https://context7.com/hunterhogan/huntermakespy>
- `astToolkit`: <https://context7.com/hunterhogan/asttoolkit>
- `numpy`: <https://numpy.org/doc/stable/reference/index.html>
- `pandas`: <https://pandas.pydata.org/docs/reference/index.html>
- `gmpy2`: <https://gmpy2.readthedocs.io/en/latest/>
- `numba`: <https://numba.readthedocs.io/en/stable/>

## Write Consistent, Precise Technical Documentation

Technical documentation requires consistency and precision. Literary prose avoids repetition through synonyms and pronouns.

### Write for Non-Native Speakers, Machine Translation, and AI Assistants

The audience for these docstrings includes developers, researchers using Python as a tool, hobbyists, machine translators, and AI assistants. Two-thirds of the human audience are non-native English speakers, and half will use some machine translation.

- **Use active voice**: "This function returns X" rather than "X is returned by this function".
- **Use technical terms, not idioms or colloquialisms**: "fails quickly" not "bails out", "prevents errors" not "catches issues".
- **Use consistent terms**: Machine translation and AI retrieval work better with repeated exact phrases.
- **Be explicit and precise**: Avoid pronouns, cultural context, and implied knowledge.
- **Short, complete sentences**: Better for parsing and translation than long, flowing prose.

### Repeat Identifiers Instead of Using Pronouns

- **Repeat nouns instead of using pronouns**: Write "`parameterFirst`" every time, not "it" or "the parameter".
- **Repeat exact identifiers**: Don't vary between "`handler`", "the handler", or "this callback".
- **Use _the_ technical term, not synonyms**: Don't alternate, for example, between "function" and "routine". Synonyms suggest false distinctions: some readers will wonder if "handler" and "callback" mean different things.

❌ **Bad** (prose-style with pronouns and synonyms):

> Process the data using the handler. It will transform the input
and pass the result to the callback, which processes it further.

✅ **Good** (technical style with repetition):

> Process `data` using `handler`. The `handler` transforms `data`
and passes `data` to `handler`, which processes `data` further.

### Always Use Backticks for Code

- Always use backticks when referring to:
  - Identifiers and other labels: `parameterName`, `className`
  - Python keywords: `try`, `except`, `class`
  - Types: `Exception`, `None`, `bool`
  - Code elements: `self`, `cls`
- Natural language discussing concepts uses standard English without backticks.
- Never write lowercase technical terms: write `Exception`, never "exception" when referring to the Python type.

### Do Not Force English Plurality on Identifiers

- **Do not force English plurality on identifiers**: `keyword` not `keywords` or `keyword`s.
- **Preserve parameter names exactly**: `handlers` (the field) not "the handlers parameter".
- **Use generalized nouns to avoid plurality**: Do not pluralize identifiers or add possessives to them. Instead, precede the strict identifier with a generalized noun or quantifier.
  - ❌ Incorrect: "Returns the `iterator`'s `leaves`." (Modified identifiers)
  - ✅ Correct: "Returns the `iterator` of `type` `int` `leaf`." (Noun "type int" precedes `leaf`)
  - ❌ Incorrect: "Enumerate `dimensionIndices`." (Pluralized identifier)
  - ✅ Correct: "Enumerate each `dimensionIndex`." (Quantifier "each" precedes `dimensionIndex`)
- **Reinforce meaning through context** rather than breaking identifiers for prose.

### Qualify Ambiguous Terms

- Qualify ambiguous terms: "Python keyword `try`" not just "`try`".
- Maintain precision: "`class` `Exception`" rather than "the `Exception` `class`".
- Avoid compound hyphenation with technical terms: not "`Exception`-free" "completion without an `Exception`".

### Never Use "Pipeline"

- Never use "pipeline". Use "assembly line" if describing a sequence of transformations.

### Separate General and Expert-Level Documentation

- **General Sections (Summary, Parameters, Returns)**: Write for a competent developer who may not be a domain expert. Avoid implementation-specific jargon (e.g., "mutable object", "thread-safe", "atomic") unless it is the primary function of the code.
- **Technical Detail Sections**: Put implementation details, hardware constraints, or expert-level warnings in well-named custom sections (e.g., `Concurrency`, `Memory Management`, `Algorithm Details`).
  - **Audience**: Experts who need to know.
  - **Tone**: Efficient, precise, technical.
  - **Constraint**: Do not explain standard concepts (like "don't share mutable objects between threads") to experts. Only document non-obvious behaviors or critical constraints.
