# Analysis

## Layer 2, Head 5

This head pays most attention to the word (with apostrophe) immediately precedes it.
- Example 1: `only` → `it's`, `we're` → `that`
- Example 2: `,` → `[MASK]`, `nothing` → `have`

Example Sentences:
- It's only after we've lost everything that we're free to do [MASK].
  - Outputs: `anything`, `so`, `it`
- Without pain, without [MASK], we would have nothing.
  - Outputs: `fear`, `blood`, `pleasure`

## Layer 12, Head 8

This head pays most attention to a period, but not all, in the text.
- Example 1: All words → the period after `ourselves`
- Example 2: All words → the period between `alive` and `if`, but none of the other periods

Example Sentences:
- Maybe we have to [MASK] everything to make something better out of ourselves.
  - Outputs: `do`, `sacrifice`, `change`
- Quit your job. Start a fight. Prove you're alive. If you don't claim your [MASK] you will become a statistic.
  - Outputs: `rights`, `title`, `money`

