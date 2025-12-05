# Chessbot-Ai
ChessBot-AI is a modular, extensible chess engine built in Python with Pygame.
The project is designed with clear architectural separation between game logic, rendering, players (human + AI), and assets, making it a solid foundation for implementing search-based chess AI.
The current version supports full human–vs–human gameplay with move validation, special rules, graphical UI, and a replay/history system. AI support is under active development.

#Features
*Fully playable chess game with a clean Pygame interface
*Legal move generation for all pieces, complient with standar FIDE Rules
* Ui/graphical rendering of the game, with clear instruction for human players.
* A wiew of the games history after a finshed game
* End-of-game screen with restart controls
* Modular design intended for future AI implementation
* Possibelty for extensions an dor alteration of the games apperance, new pieces, or changed in pieces move patterns

#Design Philosophy
The engine is built around a simple architectural idea: the board is the single source of truth for all game information. Every subsystem reads from and writes to the same board state, and no other class is allowed to maintain its own competing version of the position. This avoids drift, hidden dependencies, and inconsistencies. All logic—movement, rules, legality checks, and endgame detection—flows outward from this central state.

Pieces are deliberately kept lightweight. They do not try to “own” the rules of chess or enforce legality. Their job is restricted to generating pseudo-legal moves based solely on their movement patterns. Anything that depends on game context—check, pins, castling rights, en passant, king safety—is handled by the board. This prevents pieces from becoming overly intelligent or stateful, and keeps rule enforcement in one place instead of scattered across classes.

Legality is checked by simulating moves on the board rather than by predicting outcomes through shortcuts or heuristics. This approach is slower but clearer: if you want to know whether a move leaves the king in check, you temporarily apply the move to the real game state, observe the result, and revert it. This keeps the logic explicit and reduces the chance of corner-case bugs that come from trying to outsmart the rules.

The code aims to keep state handling transparent. Whenever something changes—castling rights, en passant availability, half-move counters, captured pieces—it is updated directly on the board as part of executing a move. There is no hidden cache or secondary tracker that risks contradicting the main state.

The overall philosophy is not about clever abstractions, but about explicitness. The engine favors clear logic over optimization, centralization over distribution of responsibility, and correctness over premature efficiency. This structure makes debugging more straightforward and prepares the engine for future extensions, such as evaluation functions, search algorithms, and eventually AI components, without having to unpick tangled or overly abstract design patterns.

If you want it even more concise, harsher, or more technical, I can refine it further.

Du sade:
more techicnal 
ChatGPT sade:

Here is a more technical, architecture-focused version that stays honest and grounded in what the code actually implements.

Design Philosophy (Technical Description)

The architecture is organized around a single invariant: the Board object represents the authoritative state of the game at every moment. All subsystems—move generation, rule enforcement, graphics, history tracking, and input handling—operate strictly against this canonical state. No component is allowed to cache or reinterpret position data independently, which eliminates desynchronization and ensures that legality checks, visual rendering, and game logic always refer to the same underlying data.

Pieces are implemented as minimal data carriers with deterministic movement rules. They produce pseudo-legal move sets based solely on geometric movement, without regard to checks, pins, or global game conditions. This separation enforces a strict two-phase logic: local move pattern generation at the piece level, followed by global legality filtering at the board level. This aligns with standard engine architecture and avoids distributing rule knowledge across many classes.

Legality evaluation follows a simulation-driven pattern. The engine does not attempt static analysis to infer whether a move is legal. Instead it:

Clones or temporarily mutates the board state.

Applies the candidate move, including updates to castling rights, en passant flags, and piece captures.

Computes king safety under the mutated state.

Restores the original state.

This compositionally simple method avoids fragmented rule implementations and reduces the risk of state corruption, at the cost of performance—an acceptable trade-off for a human-time-scale GUI engine.

All rule-sensitive metadata (castling rights, en passant availability, turn counters, king locations, captured piece lists) is stored directly on the board and updated exclusively through the move execution pathway. There are no shadow states or parallel trackers; updates occur in one location through a clearly defined control flow. This keeps invariants stable: the board is always internally consistent after any executed move.

The graphical and event-handling layer operates as a pure consumer. It never modifies rules or keeps its own view of the position beyond what is necessary for rendering. Input events are forwarded into the engine, which resolves them strictly through the board’s logic. This enforces an MVC-like separation where the model (board state) is cleanly isolated from the view (rendering) and controller (event interpretation).

The design favors explicit orchestration over abstraction. Instead of relying on inheritance hierarchies, mixins, or polymorphic rule dispatch, the architecture uses direct procedural logic over a tightly controlled state object. The result is a codebase that is not abstractly elegant but is structurally predictable: every rule is handled in one place, every piece of state has one owner, and every legality question is ultimately resolved through a controlled simulation on the board.

This technical discipline—centralized truth, piece-local pseudo-moves, board-level legality filtering, and simulation-driven evaluation—forms a solid foundation for integrating AI search later. It aligns well with typical engine pipelines, where the board object becomes the basis for evaluation, move ordering, and recursive exploration without requiring major architectural changes.
