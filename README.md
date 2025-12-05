# Chessbot-Ai
ChessBot-AI is a modular, extensible chess engine built in Python with Pygame.
The project is designed with clear architectural separation between game logic, rendering, players (human + AI), and assets, making it a solid foundation for implementing search-based chess AI.
The current version supports full human–vs–human gameplay with move validation, special rules, graphical UI, and a replay/history system. AI support is under active development.

**Features**


 *Fully playable chess game with a clean Pygame interface
 *Legal move generation for all pieces, complient with standar FIDE Rules
* Ui/graphical rendering of the game, with clear instruction for human players.
* A wiew of the games history after a finshed game
* End-of-game screen with restart controls
* Modular design intended for future AI implementation
* Possibelty for extensions an dor alteration of the games apperance, new pieces, or changed in pieces move patterns

**Design Philosophy**
The engine is built around a simple architectural idea: the board is the single source of truth for all game information. Every subsystem reads from and writes to the same board state, and no other class is allowed to maintain its own competing version of the position. This avoids drift, hidden dependencies, and inconsistencies. All logic—movement, rules, legality checks, and endgame detection—flows outward from this central state.
Pieces are deliberately kept lightweight. They do not try to “own” the rules of chess or enforce legality. Their job is restricted to generating pseudo-legal moves based solely on their movement patterns. Anything that depends on game context—check, pins, castling rights, en passant, king safety—is handled by the board. This prevents pieces from becoming overly intelligent or stateful, and keeps rule enforcement in one place instead of scattered across classes.

Legality is checked by simulating moves on the board rather than by predicting outcomes through shortcuts or heuristics. However, the simulation is not doen on the board itsel, but rather on a temporary copy of the board, that is the later discarded. This approach is slower but clearer: if you want to know whether a move leaves the king in check, you temporarily apply the move to the real game state, observe the result, and revert it. This keeps the logic explicit and reduces the chance of corner-case bugs. 

The code aims to keep state handling transparent. Whenever something changes—castling rights, en passant availability, half-move counters, captured pieces—it is updated directly on the board as part of executing a move. There is no hidden cache or secondary tracker that risks contradicting the main state.

The overall philosophy is not about clever abstractions, but about explicitness. The engine favors clear logic over optimization, centralization over distribution of responsibility, and correctness over premature efficiency. This structure makes debugging more straightforward and prepares the engine for future extensions, such as evaluation functions, search algorithms, and eventually AI components, without having to unpick tangled or overly abstract design patterns.

The graphical and event-handling layer operates as a pure consumer. It never modifies rules or keeps its own view of the position beyond what is necessary for rendering. Input events are forwarded into the engine, which resolves them strictly through the board’s logic. This enforces an MVC-like separation where the model (board state) is cleanly isolated from the view (rendering) and controller (event interpretation).

The codebase follows a classical OOP style of modelling domain entities explicitly and assigning each object a narrow, well-defined responsibility. Pieces encapsulate only movement geometry and identity; the board encapsulates global state transitions and rule validation; the graphics layer encapsulates rendering; the handler classes perform orchestration without owning game logic themselves. This results in a system where objects are concrete, behavior is localized, and dependencies flow in a single direction—from high-level controllers down to the canonical board state and never the reverse.Rather than relying on polymorphism to express chess rules, the design treats chess as a state machine whose transitions are managed centrally. Polymorphism is used only for differentiating piece movement patterns, not for distributing rule knowledge. This avoids scattering special cases like castling, en passant, or check detection across multiple classes; all such rules remain inside the board’s move execution and state-evaluation pathways. In effect, the design chooses clarity and determinism over abstraction-heavy elegance.

**Map Structure**
ChessGame/
│
 ├── __init__.py

  ├── chess_engine.py        # Owns the main game logic: turn flow, rules, winner detection,
  │                          # applying Maneuvers, coordinating board + graphics + players.

  │
  ├── board.py               # Maintains full game state: where all pieces are, applying moves,
  │                          # updating positions, captures, check/checkmate logic, etc.

  │
  ├── game_graphic.py        # Responsible for drawing the game: board, pieces, highlights,
  │                          # captured pieces, promotion UI, end screen, history screen.

  │
  ├── initial.py             # Defines initial board setup and any static starting-position data.
  │

  ├── maneuver.py            # Pure data container describing a move: start/end, capture info,
  │                          # castling, promotion, en passant, piece reference, etc.

  │
  └── piece.py               # Abstract base class for all pieces. Holds common attributes
                           # (position, color, history) and shared helper methods.
                           
      │
      ├── pawn            # Pawn movement rules, captures, promotion logic, en passant.
      ├── knight          # Knight movement rules.
      ├── bishop          # Bishop movement rules.
      ├── rook            # Rook movement rules.
      ├── queen           # Queen movement rules.
      └── king            # King movement rules, castling conditions and checks.

Player/
│
  ├── __init__.py

  ├── human.py               # Handles mouse input, selection, user-driven Maneuver creation.

  └── ai.py                  # (Planned) AI player that will generate moves with heuristics,
                           # search algorithms, evaluation etc.
                           
Config/
  │
  ├── __init__.py
  ├── game_assets.py         # Window size, fonts, FPS, timers, UI layout, button surfaces.
  └── chess_assets.py        # Piece images, scaled versions, board colors, starting visuals.
  ├─  ai_asset.py            # Hold the necessary attributes and object for an functioning AI.

  Extra/
  │
  ├── __init__.py
  ├── chess_code_structure   # Documentation describing the architecture.
  ├── Notes and rules        # Your design notes: chess rules, programming rules, TODOs.
  └── Scrap_file.py          # Experimental or discardable code.


Main.py                    # Entry point: creates ChessEngine, runs main loop,
                           # switches between play mode, game-over screen, history view.
