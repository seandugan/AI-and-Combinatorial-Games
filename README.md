# Game Analyzer

A browser-based tool for analyzing combinatorial games using N/P position classification.

**To open:** double-click `game_analyzer.html`, or run `open game_analyzer.html` in a terminal. No server or installation required — it runs entirely in your browser.

## What it does

Given a game position, the analyzer tells you:

- **N-position** (Next player wins) — the player whose turn it is can force a win with optimal play.
- **P-position** (Previous player wins) — the player whose turn it is will lose against a perfect opponent.

It also shows all winning moves available from an N-position and renders the full game tree so you can see how each branch plays out.

## Games

### Nim

Players take turns removing any number of stones from a single pile. Whoever takes the last stone wins.

Enter pile sizes as comma-separated numbers (e.g. `3, 4, 5`). The analyzer computes the XOR (nim-value) of all pile sizes alongside the N/P verdict — a nim-value of 0 always means P-position.

**Input limits:** up to 8 piles, total stones ≤ 40. Tree visualization requires total stones ≤ 25.

### Toads & Frogs

A one-dimensional board where Toads (`T`) move right and Frogs (`F`) move left. On each turn, a piece can either:
- Slide into an adjacent empty cell, or
- Jump over exactly one opponent piece into the empty cell beyond it.

The player with no legal moves loses.

Enter the board as a string of `T`, `F`, and `_` characters (e.g. `TT_FF`) and select which side moves first.

**Input limit:** board length ≤ 12 cells.

### Cram

Players alternate placing a **1×2 domino** (horizontal or vertical) onto any two adjacent empty cells of a rectangular grid. The player who can't place a domino loses. Cram is the impartial cousin of Domineering, where each player would be restricted to a single orientation.

Enter the board dimensions as rows × columns. The analyzer renders the current board, shows every winning domino placement as a clickable mini-board (each highlighting where the new domino would go), and lets you play forward through the game — the **Back** button steps you back out of any moves you've drilled into.

**Input limits:** each dimension between 1 and 6, total cells ≤ 20 (e.g. 4×5 fits). The game tree is rendered only when total cells ≤ 16; larger boards still get a full N/P verdict and winning-move list.

### Hackenbush

A Hackenbush string is a sequence of Blue (B) and Red (R) edges stacked on a ground line. Each string corresponds to a dyadic rational (a fraction whose denominator is a power of 2) via the surreal-number sign-expansion algorithm. Blue edges represent `+` and Red edges represent `−`.

The Hackenbush tab has two converters:

**Number → String** — enter a dyadic rational and get its Hackenbush string.
- Type a value like `3/4`, `-5/8`, or `3`. The denominator must be a power of 2.
- Click **Convert** to see the value, sign sequence, B/R string notation, and an SVG diagram of the string with the ground line at the bottom.

**String → Number** — build a Hackenbush string edge by edge and find its value.
- Click **+ Blue** or **+ Red** to append an edge to the string.
- Click any edge chip in the strip to remove it; **⌫ Undo** removes the last edge; **✕ Clear** resets.
- Or paste a string like `BRB` or `+-+` into the text field and click **Load**.
- The numeric value updates immediately as you add or remove edges.

A row of **quick examples** at the bottom of the tab shows common values — click any pill to load it into the Number → String converter.

**Input limit:** max 32 edges.

## Features

### Winning move navigation
Clicking any winning move loads that position and re-analyzes it. A **Back** button appears so you can retrace your steps through the move sequence.

### Game tree
The game tree renders as an SVG diagram where each node is color-coded by classification:
- Filled circle — N-position
- Hollow circle — P-position

Winning moves (from the current player's perspective) are shown first at each level. Use the **Depth** slider to control how many levels deep the tree expands.

Each node draws at most **3 children** to keep the diagram readable. When a position has more legal moves than that:

- **`+N`** under a node — N additional child moves exist at that level but aren't drawn. The displayed children are prioritized: winning moves first, then losing moves, with `+N` standing in for everything past the first 3. You're never missing a winning line — the hidden branches are always lower-priority once the winning ones are already in view.
- **`…`** under a node — the subtree exists but the renderer stopped recursing because it hit the Depth slider's limit. Raise the slider to expand further.

Click the tree to open a fullscreen view with pan and zoom:
- **Scroll** to zoom in and out, anchored under the cursor
- **Click and drag** to pan around the tree
- **+** / **−** buttons or keyboard shortcuts to zoom
- **0** to fit the whole tree back into view
- **Esc** to close

## How the solver works

The solver uses memoized recursion over the P/N definition:
- A terminal position (no legal moves) is a **P-position**.
- A position is an **N-position** if at least one move leads to a P-position.
- A position is a **P-position** if every move leads to an N-position.

A fresh memo table is created for each analysis, so exploring different starting positions doesn't accumulate memory over time.
