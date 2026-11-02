<script lang="ts">
  import { tick } from 'svelte';

  type GameMode = 'battle' | 'adventure' | 'terminal';

  interface ThemeOption {
    id: string;
    name: string;
    bg: string;
    fg: string;
    prompt: string;
    accent: string;
    frame: string;
  }

  const THEMES: ThemeOption[] = [
    {
      id: 'midnight-arcade',
      name: 'Midnight Arcade',
      bg: '#0b1220',
      fg: '#f8fafc',
      prompt: '#22d3ee',
      accent: '#e879f9',
      frame: '#22d3ee',
    },
    {
      id: 'synthwave',
      name: "Synthwave '84",
      bg: '#161320',
      fg: '#dad9c7',
      prompt: '#19cde6',
      accent: '#f6188f',
      frame: '#f6188f',
    },
    {
      id: 'c64',
      name: 'Commodore 64',
      bg: '#40318d',
      fg: '#a89fe0',
      prompt: '#bfce72',
      accent: '#bfce72',
      frame: '#6657b3',
    },
    {
      id: 'gameboy',
      name: 'Game Boy DMG',
      bg: '#8bac0f',
      fg: '#0f380f',
      prompt: '#306230',
      accent: '#8b1e42',
      frame: '#306230',
    },
    {
      id: 'pipboy',
      name: 'Pip-Boy 3000',
      bg: '#07130a',
      fg: '#1bfd9c',
      prompt: '#24ffaa',
      accent: '#24ffaa',
      frame: '#1bfd9c',
    },
    {
      id: 'dracula',
      name: 'Dracula',
      bg: '#282a36',
      fg: '#f8f8f2',
      prompt: '#50fa7b',
      accent: '#bd93f9',
      frame: '#6272a4',
    },
  ];

  let currentTheme = THEMES[0];
  let currentMode: GameMode = 'battle';
  let scanlines = true;
  let textGlow = true;
  let audioEnabled = true;

  let adventureContainer: HTMLElement | null = null;
  let terminalContainer: HTMLElement | null = null;
  let battleLogContainer: HTMLElement | null = null;
  let adventureInputEl: HTMLInputElement | null = null;
  let terminalInputEl: HTMLInputElement | null = null;

  async function scrollToBottom(el: HTMLElement | null, formSelector?: string) {
    await tick();
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
    if (formSelector && typeof document !== 'undefined') {
      const form = document.querySelector(formSelector);
      form?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  async function switchMode(mode: GameMode) {
    currentMode = mode;
    playBleep(mode === 'battle' ? 440 : mode === 'adventure' ? 520 : 600);
    await tick();
    if (mode === 'adventure') {
      await scrollToBottom(adventureContainer);
      adventureInputEl?.focus();
    } else if (mode === 'terminal') {
      await scrollToBottom(terminalContainer);
      terminalInputEl?.focus();
    } else if (mode === 'battle') {
      await scrollToBottom(battleLogContainer);
    }
  }

  // Web Audio 8-bit sound generator
  let audioCtx: AudioContext | null = null;

  function initAudio() {
    if (!audioCtx && typeof window !== 'undefined') {
      const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  function playBleep(freq = 440, type: 'sine' | 'square' | 'sawtooth' | 'triangle' = 'square', duration = 0.08) {
    if (!audioEnabled) return;
    try {
      initAudio();
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch {
      // Audio autoplay policy fallback
    }
  }

  function playFanfare() {
    [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
      setTimeout(() => playBleep(freq, 'triangle', 0.15), idx * 120);
    });
  }

  // RPG Battle State
  interface BattleState {
    heroHp: number;
    heroMaxHp: number;
    heroMp: number;
    heroMaxMp: number;
    bossHp: number;
    bossMaxHp: number;
    bossName: string;
    defending: boolean;
    logs: string[];
    isOver: boolean;
    victory: boolean;
  }

  let battle: BattleState = {
    heroHp: 280,
    heroMaxHp: 280,
    heroMp: 60,
    heroMaxMp: 60,
    bossHp: 800,
    bossMaxHp: 800,
    bossName: 'CYBER-DRAGON',
    defending: false,
    logs: [
      '>> Encountered CYBER-DRAGON LV.99!',
      '>> The boss readies its compiler fire breath...',
      '>> Choose your command below!',
    ],
    isOver: false,
    victory: false,
  };

  function resetBattle() {
    battle = {
      heroHp: 280,
      heroMaxHp: 280,
      heroMp: 60,
      heroMaxMp: 60,
      bossHp: 800,
      bossMaxHp: 800,
      bossName: 'CYBER-DRAGON',
      defending: false,
      logs: ['>> New battle initiated!', '>> The boss roars with binary fury.'],
      isOver: false,
      victory: false,
    };
    playBleep(300, 'sawtooth', 0.2);
  }

  function heroAction(action: 'attack' | 'spell' | 'defend' | 'potion') {
    if (battle.isOver) return;

    battle.defending = false;

    if (action === 'attack') {
      let heroDmg = Math.floor(Math.random() * 80) + 70;
      const isCrit = Math.random() > 0.75;
      if (isCrit) heroDmg = Math.floor(heroDmg * 1.6);
      battle.bossHp = Math.max(0, battle.bossHp - heroDmg);
      battle.logs = [
        ...battle.logs,
        `⚔️ Hero strikes with Sudo Sword! ${isCrit ? 'CRITICAL HIT!' : ''} Deals ${heroDmg} dmg.`,
      ];
      playBleep(isCrit ? 880 : 440, 'square', 0.1);
    } else if (action === 'spell') {
      if (battle.heroMp < 20) {
        battle.logs = [...battle.logs, '⚠️ Out of mana! Need 20 MP to cast Aegis Flare.'];
        playBleep(150, 'sawtooth', 0.1);
        return;
      }
      battle.heroMp -= 20;
      const heroDmg = Math.floor(Math.random() * 120) + 110;
      battle.bossHp = Math.max(0, battle.bossHp - heroDmg);
      battle.logs = [
        ...battle.logs,
        `✨ Hero casts DEFENSIVE AEGIS FLARE! Blasts boss for ${heroDmg} magic dmg.`,
      ];
      playBleep(700, 'sine', 0.25);
    } else if (action === 'defend') {
      battle.defending = true;
      battle.logs = [
        ...battle.logs,
        '🛡️ Hero assumes Secure Boot Stance! Incoming damage halved.',
      ];
      playBleep(350, 'triangle', 0.15);
    } else if (action === 'potion') {
      const heal = 100;
      battle.heroHp = Math.min(battle.heroMaxHp, battle.heroHp + heal);
      battle.heroMp = Math.min(battle.heroMaxMp, battle.heroMp + 25);
      battle.logs = [
        ...battle.logs,
        `🧪 Hero drinks Fresh Espresso! Restored ${heal} HP and 25 MP.`,
      ];
      playBleep(600, 'sine', 0.2);
    }

    scrollToBottom(battleLogContainer);

    // Check boss defeat
    if (battle.bossHp <= 0) {
      battle.isOver = true;
      battle.victory = true;
      battle.logs = [
        ...battle.logs,
        `🎉 ${battle.bossName} WAS DEFEATED!`,
        '🏆 VICTORY! 3,500 EXP gained. Dad joke buffer overflowing.',
      ];
      scrollToBottom(battleLogContainer);
      playFanfare();
      return;
    }

    // Boss Turn
    setTimeout(() => {
      if (battle.isOver) return;
      let bossDmg = Math.floor(Math.random() * 60) + 40;
      if (battle.defending) {
        bossDmg = Math.floor(bossDmg * 0.5);
      }
      battle.heroHp = Math.max(0, battle.heroHp - bossDmg);
      battle.logs = [
        ...battle.logs,
        `🔥 ${battle.bossName} retaliates with Stack Overflow! Deals ${bossDmg} dmg.`,
      ];
      playBleep(220, 'sawtooth', 0.15);

      if (battle.heroHp <= 0) {
        battle.isOver = true;
        battle.victory = false;
        battle.logs = [...battle.logs, '💀 GAME OVER. Hero was deallocated.'];
        playBleep(100, 'sawtooth', 0.4);
      }
      scrollToBottom(battleLogContainer);
    }, 400);
  }

  // Zork Adventure State
  let adventureInput = '';
  let adventureHistory = [
    ' West of House                             Score: 10/100   Moves: 4 ',
    '────────────────────────────────────────────────────────────────────────',
    ' You are standing in an open field west of a white house, with a boarded',
    ' front door. There is a small mailbox here.',
    ' [ EXITS: NORTH | EAST | SOUTHWEST ]',
  ];

  function handleAdventureCommand() {
    const cmd = adventureInput.trim().toLowerCase();
    if (!cmd) return;
    playBleep(520, 'square', 0.05);

    const newHistory = [...adventureHistory, `> ${cmd}`];

    if (cmd.includes('open') && cmd.includes('mailbox')) {
      newHistory.push('Opening the small mailbox reveals a leaflet.');
    } else if (cmd.includes('read') && cmd.includes('leaflet')) {
      newHistory.push('"WELCOME TO ZORK! A game of adventure, danger, and low cunning."');
      newHistory.push('"Type LOOK, INVENTORY, NORTH, SOUTH, TAKE, or EXAMINE."');
    } else if (cmd === 'look') {
      newHistory.push('You are standing west of the white house. Birdsong chirps in the forest.');
      newHistory.push('A small wooden mailbox stands nearby.');
    } else if (cmd.includes('north') || cmd === 'n') {
      newHistory.push('North of House: The windows here are all barred shut. A dark path leads deeper into the woods.');
    } else if (cmd.includes('east') || cmd === 'e') {
      newHistory.push('The front door is boarded shut. You cannot enter without heavy tools.');
    } else if (cmd.includes('take') || cmd.includes('get')) {
      newHistory.push('Taken.');
    } else if (cmd === 'xyzzy') {
      newHistory.push('A hollow voice says: "Fool."');
    } else if (cmd.includes('grue')) {
      newHistory.push('It is pitch black. You are likely to be eaten by a grue.');
    } else if (cmd.includes('help')) {
      newHistory.push('Valid verbs: LOOK, OPEN, READ, TAKE, GO, NORTH, SOUTH, EAST, WEST, INVENTORY.');
    } else {
      newHistory.push(`I don't know the word "${cmd.split(' ')[0]}". Try LOOK or HELP.`);
    }

    adventureHistory = newHistory;
    adventureInput = '';
    scrollToBottom(adventureContainer, '.adventure-form');
  }

  // Interactive Terminal REPL State
  let terminalInput = '';
  let terminalLines = [
    "william@homelab:~$ welcome",
    "WILLIAM'S INTERACTIVE DEV TERMINAL v2026.11",
    "Type 'help' to list available commands.",
    "",
  ];

  const DAD_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache!",
    "Why was the function sad after the break up? It had no closure!",
    "How do you comfort a JavaScript bug? You console it!",
    "Why did the pentester bring a ladder to work? To escalate privileges!",
    "What do you call a CVE nobody patches? An invitation.",
    "Why did the homelabber buy a fourth UPS? Redundancy for the rest!",
  ];

  function runTerminalCommand() {
    const raw = terminalInput.trim();
    if (!raw) return;
    playBleep(480, 'square', 0.05);

    const [cmd, ...args] = raw.split(' ');
    const lowerCmd = cmd.toLowerCase();

    let output: string[] = [`william@homelab:~$ ${raw}`];

    switch (lowerCmd) {
      case 'help':
        output.push(
          "Available commands:",
          "  help           Show this manual",
          "  dad-joke       Fetch a signature William dad joke",
          "  neofetch       Display system & identity card",
          "  konami         Inject classic cheat sequence",
          "  weather        Check current homelab conditions",
          "  clear          Clear the terminal screen",
          "  theme <name>   Switch active theme (c64, synthwave, gameboy, pipboy, etc.)",
          "  whoami         Identity check",
        );
        break;
      case 'dad-joke':
      case 'joke':
        output.push(DAD_JOKES[Math.floor(Math.random() * DAD_JOKES.length)]!);
        break;
      case 'neofetch':
        output.push(
          "       ___          william@homelab",
          "      /   \\         ----------------",
          "     ( o.o )        OS: DadOS LTS (Linux + Coffee)",
          "      > ^ <         Role: Security Engineer · Multi-Agent AI",
          "     /     \\        Homelab: Dell R910 (256GB RAM) + 3x Pi Cluster",
          "    (_/   \\_)       Projects: nexus-agents, aegis-boot, svg-terminal",
        );
        break;
      case 'konami':
        output.push(
          "[ ↑ ] [ ↑ ] [ ↓ ] [ ↓ ] [ ← ] [ → ] [ ← ] [ → ] [ B ] [ A ]",
          "★ CHEAT CODE VERIFIED: 30 LIVES GRANTED // GOD MODE ACTIVE ★",
        );
        playFanfare();
        break;
      case 'weather':
        output.push("Harrisburg, PA: 54°F, Overcast, Humidity 56%, Racks Healthy.");
        break;
      case 'whoami':
        output.push("william (Security Engineer · Builder · Dad-Joke Archivist)");
        break;
      case 'theme':
        if (args[0]) {
          const match = THEMES.find(t => t.id === args[0]?.toLowerCase());
          if (match) {
            currentTheme = match;
            output.push(`Theme switched to: ${match.name}`);
          } else {
            output.push(`Unknown theme. Choose: ${THEMES.map(t => t.id).join(', ')}`);
          }
        } else {
          output.push(`Current theme: ${currentTheme.name}`);
        }
        break;
      case 'clear':
        terminalLines = [];
        terminalInput = '';
        return;
      default:
        output.push(`Command not found: ${raw}. Type 'help' for options.`);
    }

    terminalLines = [...terminalLines, ...output, ""];
    terminalInput = '';
    scrollToBottom(terminalContainer, '.terminal-form');
  }

  function makeGauge(current: number, max: number, width = 12): string {
    const ratio = Math.max(0, Math.min(1, current / max));
    const filled = Math.round(ratio * width);
    const empty = width - filled;
    return '█'.repeat(filled) + '░'.repeat(empty);
  }
</script>

<div
  class="arcade-cabinet"
  style="
    --term-bg: {currentTheme.bg};
    --term-fg: {currentTheme.fg};
    --term-prompt: {currentTheme.prompt};
    --term-accent: {currentTheme.accent};
    --term-border: {currentTheme.frame};
  "
>
  <!-- Controls Toolbar -->
  <div class="arcade-toolbar">
    <div class="mode-tabs">
      <button
        class:active={currentMode === 'battle'}
        on:click={() => switchMode('battle')}
      >
        ⚔️ RPG Boss Battle
      </button>
      <button
        class:active={currentMode === 'adventure'}
        on:click={() => switchMode('adventure')}
      >
        📜 Zork Adventure
      </button>
      <button
        class:active={currentMode === 'terminal'}
        on:click={() => switchMode('terminal')}
      >
        ⌨️ Live REPL
      </button>
    </div>

    <div class="theme-picker">
      <label for="theme-select">Theme:</label>
      <select
        id="theme-select"
        bind:value={currentTheme}
        on:change={() => playBleep(700)}
      >
        {#each THEMES as t (t.id)}
          <option value={t}>{t.name}</option>
        {/each}
      </select>

      <button
        class="toggle-btn"
        class:active={scanlines}
        on:click={() => scanlines = !scanlines}
        title="Toggle CRT Scanlines"
      >
        📺 CRT
      </button>

      <button
        class="toggle-btn"
        class:active={audioEnabled}
        on:click={() => audioEnabled = !audioEnabled}
        title="Toggle 8-bit Audio"
      >
        {audioEnabled ? '🔊 Sound' : '🔇 Mute'}
      </button>
    </div>
  </div>

  <!-- Screen Container -->
  <div class="terminal-screen" class:scanlines class:glow={textGlow}>
    <!-- Title Bar -->
    <div class="terminal-header">
      <div class="header-buttons">
        <span class="btn close"></span>
        <span class="btn min"></span>
        <span class="btn max"></span>
      </div>
      <div class="header-title">william@homelab: ~/arcade/{currentMode}</div>
    </div>

    <!-- Mode 1: Boss Battle -->
    {#if currentMode === 'battle'}
      <div class="mode-content battle-mode">
        <div class="boss-display">
          <pre class="boss-sprite">
       / \__
      (    @\___
      /         O    [{battle.bossName}] LV.99
     /   (_____/     HP [{makeGauge(battle.bossHp, battle.bossMaxHp, 16)}] {battle.bossHp}/{battle.bossMaxHp}
    /_____/   U
          </pre>
        </div>

        <div class="battle-log" bind:this={battleLogContainer}>
          {#each battle.logs.slice(-5) as log, i (i)}
            <div class="log-line">{log}</div>
          {/each}
        </div>

        <div class="party-status">
          <div class="party-row">
            <span class="member-name">HERO:</span>
            <span class="gauge-label">HP [{makeGauge(battle.heroHp, battle.heroMaxHp)}] {battle.heroHp}/{battle.heroMaxHp}</span>
            <span class="gauge-label">MP [{makeGauge(battle.heroMp, battle.heroMaxMp, 8)}] {battle.heroMp}/{battle.heroMaxMp}</span>
            <span class="status-pill">{battle.defending ? 'SHIELD' : 'READY'}</span>
          </div>
        </div>

        <div class="command-bar">
          <span class="prompt-text">COMMAND &gt;</span>
          <button on:click={() => heroAction('attack')} disabled={battle.isOver}>⚔️ Attack</button>
          <button on:click={() => heroAction('spell')} disabled={battle.isOver}>✨ Aegis Flare (20 MP)</button>
          <button on:click={() => heroAction('defend')} disabled={battle.isOver}>🛡️ Defend</button>
          <button on:click={() => heroAction('potion')} disabled={battle.isOver}>🧪 Espresso</button>
          {#if battle.isOver}
            <button class="reset-btn" on:click={resetBattle}>🔄 Play Again</button>
          {/if}
        </div>
      </div>
    {/if}

    <!-- Mode 2: Zork Adventure -->
    {#if currentMode === 'adventure'}
      <div class="mode-content adventure-mode">
        <div class="adventure-history" bind:this={adventureContainer}>
          {#each adventureHistory as line, i (i)}
            <div class="adv-line">{line}</div>
          {/each}
        </div>
        <form class="adventure-form" on:submit|preventDefault={handleAdventureCommand}>
          <span class="prompt-text">&gt;</span>
          <input
            bind:this={adventureInputEl}
            type="text"
            bind:value={adventureInput}
            placeholder="e.g. open small mailbox, look, go north"
            autocomplete="off"
            spellcheck="false"
          />
          <button type="submit">Send</button>
        </form>
      </div>
    {/if}

    <!-- Mode 3: Live Terminal REPL -->
    {#if currentMode === 'terminal'}
      <div class="mode-content terminal-mode">
        <div class="terminal-history" bind:this={terminalContainer}>
          {#each terminalLines as line, i (i)}
            <div class="term-line">{line}</div>
          {/each}
        </div>
        <form class="terminal-form" on:submit|preventDefault={runTerminalCommand}>
          <span class="prompt-text">william@homelab:~$</span>
          <input
            bind:this={terminalInputEl}
            type="text"
            bind:value={terminalInput}
            placeholder="type 'help', 'dad-joke', 'neofetch', 'konami'..."
            autocomplete="off"
            spellcheck="false"
          />
        </form>
      </div>
    {/if}
  </div>
</div>

<style>
  .arcade-cabinet {
    font-family: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace);
    max-width: 58rem;
    margin: 2rem auto;
    border-radius: 10px;
    background: var(--color-surface);
    border: 2px solid var(--color-border-bold);
    box-shadow: 0 14px 40px var(--color-shadow);
    overflow: hidden;
  }

  .arcade-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: var(--color-code-bg);
    border-bottom: 1px solid var(--color-border);
  }

  .mode-tabs {
    display: flex;
    gap: 0.5rem;
  }

  .mode-tabs button {
    background: var(--color-surface);
    color: var(--color-fg-muted);
    border: 1px solid var(--color-border);
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.15s ease;
  }

  .mode-tabs button.active {
    background: var(--color-accent);
    color: var(--color-bg);
    border-color: var(--color-accent);
  }

  .theme-picker {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: var(--color-fg-muted);
  }

  .theme-picker select {
    background: var(--color-surface);
    color: var(--color-fg);
    border: 1px solid var(--color-border);
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
    font-size: 0.82rem;
  }

  .toggle-btn {
    background: var(--color-surface);
    color: var(--color-fg-muted);
    border: 1px solid var(--color-border);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.82rem;
  }

  .toggle-btn.active {
    background: var(--color-accent);
    color: var(--color-bg);
    border-color: var(--color-accent);
  }

  .terminal-screen {
    position: relative;
    background: var(--term-bg);
    color: var(--term-fg);
    min-height: 480px;
    padding-bottom: 1rem;
    transition: background 0.2s ease, color 0.2s ease;
  }

  .terminal-screen.glow {
    text-shadow: 0 0 4px var(--term-prompt);
  }

  .terminal-screen.scanlines::after {
    content: " ";
    display: block;
    position: absolute;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%); /* allow-raw-color: CRT scanlines */
    background-size: 100% 4px;
    z-index: 10;
    pointer-events: none;
    opacity: 0.6;
  }

  .terminal-header {
    display: flex;
    align-items: center;
    padding: 0.5rem 0.85rem;
    background: rgba(0, 0, 0, 0.35); /* allow-raw-color: terminal header overlay */
    border-bottom: 1px solid rgba(255, 255, 255, 0.08); /* allow-raw-color: terminal header border */
  }

  .header-buttons {
    display: flex;
    gap: 0.4rem;
  }

  .header-buttons .btn {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
  }

  .btn.close { background: #ff5f56; /* allow-raw-color: macOS window red */ }
  .btn.min { background: #ffbd2e; /* allow-raw-color: macOS window yellow */ }
  .btn.max { background: #27c93f; /* allow-raw-color: macOS window green */ }

  .header-title {
    margin: 0 auto;
    font-size: var(--text-micro, 0.8125rem);
    opacity: 0.75;
    letter-spacing: 0.04em;
  }

  .mode-content {
    padding: 1.25rem 1.5rem;
  }

  /* Battle Mode */
  .boss-display {
    margin-bottom: 1rem;
    border: 1px dashed var(--term-border);
    padding: 0.75rem 1rem;
    border-radius: 6px;
  }

  .boss-sprite {
    font-family: inherit;
    font-size: 0.9rem;
    line-height: 1.35;
    margin: 0;
    color: var(--term-accent);
  }

  .battle-log {
    background: rgba(0, 0, 0, 0.25); /* allow-raw-color: terminal log overlay */
    border: 1px solid rgba(255, 255, 255, 0.08); /* allow-raw-color: terminal log border */
    padding: 0.75rem 1rem;
    border-radius: 6px;
    min-height: 110px;
    max-height: 130px;
    overflow-y: auto;
    scroll-behavior: smooth;
    overscroll-behavior: contain;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .log-line {
    color: var(--term-fg);
  }

  .party-status {
    margin-bottom: 1.25rem;
  }

  .party-row {
    display: flex;
    gap: 1.25rem;
    align-items: center;
    font-size: 0.88rem;
    flex-wrap: wrap;
  }

  .member-name {
    font-weight: bold;
    color: var(--term-prompt);
  }

  .status-pill {
    background: var(--term-prompt);
    color: var(--term-bg);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    font-size: var(--text-micro, 0.8125rem);
    font-weight: bold;
  }

  .command-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    border-top: 1px solid rgba(255, 255, 255, 0.1); /* allow-raw-color: terminal divider */
    padding-top: 1rem;
  }

  .prompt-text {
    font-weight: bold;
    color: var(--term-prompt);
    margin-right: 0.25rem;
  }

  .command-bar button, .adventure-form button {
    background: transparent;
    color: var(--term-prompt);
    border: 1px solid var(--term-prompt);
    padding: 0.35rem 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.85rem;
    transition: all 0.15s ease;
  }

  .command-bar button:hover:not(:disabled), .adventure-form button:hover {
    background: var(--term-prompt);
    color: var(--term-bg);
  }

  .command-bar button:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .command-bar button.reset-btn {
    border-color: var(--term-accent);
    color: var(--term-accent);
  }

  /* Adventure & Terminal Modes */
  .adventure-history, .terminal-history {
    min-height: 320px;
    font-size: 0.9rem;
    line-height: 1.45;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    max-height: 440px;
    overflow-y: auto;
    scroll-behavior: smooth;
    overscroll-behavior: contain;
  }

  .adventure-form, .terminal-form {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1); /* allow-raw-color: terminal divider */
    padding-top: 0.75rem;
  }

  .adventure-form input, .terminal-form input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--term-fg);
    font-family: inherit;
    font-size: 0.9rem;
    outline: none;
  }
</style>
