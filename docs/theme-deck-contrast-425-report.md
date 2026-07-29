# Theme Deck Contrast Report — Issue #425

Ratios use the generator/WCAG relative-luminance OKLCH math. State tokens are measured against `--color-bg`; syntax tokens against `--color-code-bg`; border tokens against `--color-bg`.

## Initial failures (104)

| Deck | Token | Against | Ratio | Floor |
|---|---:|---:|---:|---:|
| dracula | `--color-error` | `--color-bg` | 3.72:1 | 4.5:1 |
| dracula | `--color-success` | `--color-bg` | 3.93:1 | 4.5:1 |
| dracula | `--color-warning` | `--color-bg` | 3.88:1 | 4.5:1 |
| dracula | `--color-border` | `--color-bg` | 1.50:1 | 3.0:1 |
| dracula | `--color-syntax-keyword` | `--color-code-bg` | 3.25:1 | 4.5:1 |
| dracula | `--color-syntax-string` | `--color-code-bg` | 3.25:1 | 4.5:1 |
| dracula | `--color-syntax-constant` | `--color-code-bg` | 3.20:1 | 4.5:1 |
| dracula | `--color-syntax-comment` | `--color-code-bg` | 3.10:1 | 4.5:1 |
| dracula | `--color-syntax-function` | `--color-code-bg` | 3.21:1 | 4.5:1 |
| dracula | `--color-syntax-type` | `--color-code-bg` | 3.25:1 | 4.5:1 |
| dracula | `--color-syntax-punctuation` | `--color-code-bg` | 3.10:1 | 4.5:1 |
| nord | `--color-error` | `--color-bg` | 3.26:1 | 4.5:1 |
| nord | `--color-success` | `--color-bg` | 3.45:1 | 4.5:1 |
| nord | `--color-warning` | `--color-bg` | 3.40:1 | 4.5:1 |
| nord | `--color-border` | `--color-bg` | 1.42:1 | 3.0:1 |
| nord | `--color-border-bold` | `--color-bg` | 2.62:1 | 3.0:1 |
| nord | `--color-syntax-keyword` | `--color-code-bg` | 2.89:1 | 4.5:1 |
| nord | `--color-syntax-string` | `--color-code-bg` | 2.90:1 | 4.5:1 |
| nord | `--color-syntax-constant` | `--color-code-bg` | 2.85:1 | 4.5:1 |
| nord | `--color-syntax-comment` | `--color-code-bg` | 2.77:1 | 4.5:1 |
| nord | `--color-syntax-function` | `--color-code-bg` | 2.86:1 | 4.5:1 |
| nord | `--color-syntax-type` | `--color-code-bg` | 2.90:1 | 4.5:1 |
| nord | `--color-syntax-punctuation` | `--color-code-bg` | 2.77:1 | 4.5:1 |
| nord | `--color-syntax-link` | `--color-code-bg` | 4.06:1 | 4.5:1 |
| catppuccin-mocha | `--color-error` | `--color-bg` | 4.28:1 | 4.5:1 |
| catppuccin-mocha | `--color-warning` | `--color-bg` | 4.47:1 | 4.5:1 |
| catppuccin-mocha | `--color-border` | `--color-bg` | 1.38:1 | 3.0:1 |
| catppuccin-mocha | `--color-border-bold` | `--color-bg` | 2.68:1 | 3.0:1 |
| catppuccin-mocha | `--color-syntax-keyword` | `--color-code-bg` | 3.88:1 | 4.5:1 |
| catppuccin-mocha | `--color-syntax-string` | `--color-code-bg` | 3.88:1 | 4.5:1 |
| catppuccin-mocha | `--color-syntax-constant` | `--color-code-bg` | 3.82:1 | 4.5:1 |
| catppuccin-mocha | `--color-syntax-comment` | `--color-code-bg` | 3.70:1 | 4.5:1 |
| catppuccin-mocha | `--color-syntax-function` | `--color-code-bg` | 3.83:1 | 4.5:1 |
| catppuccin-mocha | `--color-syntax-type` | `--color-code-bg` | 3.88:1 | 4.5:1 |
| catppuccin-mocha | `--color-syntax-punctuation` | `--color-code-bg` | 3.70:1 | 4.5:1 |
| tokyonight | `--color-error` | `--color-bg` | 4.46:1 | 4.5:1 |
| tokyonight | `--color-border` | `--color-bg` | 1.34:1 | 3.0:1 |
| tokyonight | `--color-border-bold` | `--color-bg` | 2.53:1 | 3.0:1 |
| tokyonight | `--color-syntax-keyword` | `--color-code-bg` | 4.09:1 | 4.5:1 |
| tokyonight | `--color-syntax-string` | `--color-code-bg` | 4.09:1 | 4.5:1 |
| tokyonight | `--color-syntax-constant` | `--color-code-bg` | 4.03:1 | 4.5:1 |
| tokyonight | `--color-syntax-comment` | `--color-code-bg` | 3.91:1 | 4.5:1 |
| tokyonight | `--color-syntax-function` | `--color-code-bg` | 4.04:1 | 4.5:1 |
| tokyonight | `--color-syntax-type` | `--color-code-bg` | 4.10:1 | 4.5:1 |
| tokyonight | `--color-syntax-punctuation` | `--color-code-bg` | 3.91:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-error` | `--color-bg` | 4.28:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-warning` | `--color-bg` | 4.47:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-border` | `--color-bg` | 1.40:1 | 3.0:1 |
| gruvbox-dark-hard | `--color-border-bold` | `--color-bg` | 2.80:1 | 3.0:1 |
| gruvbox-dark-hard | `--color-syntax-keyword` | `--color-code-bg` | 3.86:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-syntax-string` | `--color-code-bg` | 3.86:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-syntax-constant` | `--color-code-bg` | 3.81:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-syntax-comment` | `--color-code-bg` | 3.69:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-syntax-function` | `--color-code-bg` | 3.82:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-syntax-type` | `--color-code-bg` | 3.86:1 | 4.5:1 |
| gruvbox-dark-hard | `--color-syntax-punctuation` | `--color-code-bg` | 3.69:1 | 4.5:1 |
| kanagawa-wave | `--color-error` | `--color-bg` | 4.27:1 | 4.5:1 |
| kanagawa-wave | `--color-warning` | `--color-bg` | 4.45:1 | 4.5:1 |
| kanagawa-wave | `--color-border` | `--color-bg` | 1.37:1 | 3.0:1 |
| kanagawa-wave | `--color-border-bold` | `--color-bg` | 2.64:1 | 3.0:1 |
| kanagawa-wave | `--color-syntax-keyword` | `--color-code-bg` | 3.87:1 | 4.5:1 |
| kanagawa-wave | `--color-syntax-string` | `--color-code-bg` | 3.87:1 | 4.5:1 |
| kanagawa-wave | `--color-syntax-constant` | `--color-code-bg` | 3.82:1 | 4.5:1 |
| kanagawa-wave | `--color-syntax-comment` | `--color-code-bg` | 3.70:1 | 4.5:1 |
| kanagawa-wave | `--color-syntax-function` | `--color-code-bg` | 3.83:1 | 4.5:1 |
| kanagawa-wave | `--color-syntax-type` | `--color-code-bg` | 3.88:1 | 4.5:1 |
| kanagawa-wave | `--color-syntax-punctuation` | `--color-code-bg` | 3.70:1 | 4.5:1 |
| rose-pine | `--color-border` | `--color-bg` | 1.37:1 | 3.0:1 |
| rose-pine | `--color-border-bold` | `--color-bg` | 2.82:1 | 3.0:1 |
| rose-pine | `--color-syntax-keyword` | `--color-code-bg` | 4.20:1 | 4.5:1 |
| rose-pine | `--color-syntax-string` | `--color-code-bg` | 4.20:1 | 4.5:1 |
| rose-pine | `--color-syntax-constant` | `--color-code-bg` | 4.14:1 | 4.5:1 |
| rose-pine | `--color-syntax-comment` | `--color-code-bg` | 4.01:1 | 4.5:1 |
| rose-pine | `--color-syntax-function` | `--color-code-bg` | 4.15:1 | 4.5:1 |
| rose-pine | `--color-syntax-type` | `--color-code-bg` | 4.21:1 | 4.5:1 |
| rose-pine | `--color-syntax-punctuation` | `--color-code-bg` | 4.01:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-border` | `--color-bg` | 1.30:1 | 3.0:1 |
| solarized-dark-higher-contrast | `--color-border-bold` | `--color-bg` | 2.31:1 | 3.0:1 |
| solarized-dark-higher-contrast | `--color-syntax-keyword` | `--color-code-bg` | 4.18:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-string` | `--color-code-bg` | 4.18:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-constant` | `--color-code-bg` | 4.12:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-comment` | `--color-code-bg` | 3.99:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-function` | `--color-code-bg` | 4.13:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-type` | `--color-code-bg` | 4.19:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-punctuation` | `--color-code-bg` | 3.99:1 | 4.5:1 |
| solarized-dark-higher-contrast | `--color-syntax-link` | `--color-code-bg` | 4.16:1 | 4.5:1 |
| github-light-default | `--color-border` | `--color-bg` | 1.40:1 | 3.0:1 |
| github-light-default | `--color-border-bold` | `--color-bg` | 2.66:1 | 3.0:1 |
| gruvbox-light-hard | `--color-border` | `--color-bg` | 1.33:1 | 3.0:1 |
| gruvbox-light-hard | `--color-border-bold` | `--color-bg` | 2.28:1 | 3.0:1 |
| gruvbox-light-hard | `--color-syntax-link` | `--color-code-bg` | 4.44:1 | 4.5:1 |
| catppuccin-latte | `--color-border` | `--color-bg` | 1.27:1 | 3.0:1 |
| catppuccin-latte | `--color-border-bold` | `--color-bg` | 1.98:1 | 3.0:1 |
| catppuccin-latte | `--color-syntax-link` | `--color-code-bg` | 4.37:1 | 4.5:1 |
| nord-light | `--color-border` | `--color-bg` | 1.28:1 | 3.0:1 |
| nord-light | `--color-border-bold` | `--color-bg` | 2.03:1 | 3.0:1 |
| nord-light | `--color-syntax-keyword` | `--color-code-bg` | 4.27:1 | 4.5:1 |
| nord-light | `--color-syntax-string` | `--color-code-bg` | 4.42:1 | 4.5:1 |
| nord-light | `--color-syntax-constant` | `--color-code-bg` | 4.32:1 | 4.5:1 |
| nord-light | `--color-syntax-comment` | `--color-code-bg` | 4.37:1 | 4.5:1 |
| nord-light | `--color-syntax-function` | `--color-code-bg` | 4.34:1 | 4.5:1 |
| nord-light | `--color-syntax-type` | `--color-code-bg` | 4.28:1 | 4.5:1 |
| nord-light | `--color-syntax-punctuation` | `--color-code-bg` | 4.37:1 | 4.5:1 |
| nord-light | `--color-syntax-link` | `--color-code-bg` | 4.21:1 | 4.5:1 |

## Changed tokens (173)

| Deck | Token | Hex | Ratio |
|---|---:|---:|---:|
| dracula | `--color-border` | `#3e4650` -> `#697679` | 1.50:1 -> 3.03:1 |
| dracula | `--color-error` | `#c06a63` -> `#ff6765` | 3.72:1 -> 5.00:1 |
| dracula | `--color-success` | `#569459` -> `#50fa7b` | 3.93:1 -> 10.38:1 |
| dracula | `--color-warning` | `#a4802b` -> `#f1fa8c` | 3.88:1 -> 12.74:1 |
| dracula | `--color-syntax-keyword` | `#4c87c2` -> `#bd93f9` | 3.25:1 -> 5.08:1 |
| dracula | `--color-syntax-string` | `#539156` -> `#50fa7b` | 3.25:1 -> 8.93:1 |
| dracula | `--color-syntax-constant` | `#a27d27` -> `#f1fa8c` | 3.20:1 -> 10.96:1 |
| dracula | `--color-syntax-comment` | `#82807d` -> `#8b9cd1` | 3.10:1 -> 4.53:1 |
| dracula | `--color-syntax-function` | `#9a73b8` -> `#ff79c6` | 3.21:1 -> 5.13:1 |
| dracula | `--color-syntax-type` | `#0f9293` -> `#8be9fd` | 3.25:1 -> 8.85:1 |
| dracula | `--color-syntax-punctuation` | `#82807d` -> `#8b9cd1` | 3.10:1 -> 4.53:1 |
| dracula | `--color-syntax-variable` | `#c6c4c0` -> `#f8f8f2` | 7.02:1 -> 11.49:1 |
| nord | `--color-muted` | `#989eaa` -> `#969ca8` | 4.64:1 -> 4.53:1 |
| nord | `--color-border` | `#444b57` -> `#777d89` | 1.42:1 -> 3.03:1 |
| nord | `--color-border-bold` | `#6d737f` -> `#777d89` | 2.62:1 -> 3.03:1 |
| nord | `--color-error` | `#c06a63` -> `#e9878f` | 3.26:1 -> 4.95:1 |
| nord | `--color-success` | `#569459` -> `#a3be8c` | 3.45:1 -> 6.13:1 |
| nord | `--color-warning` | `#a4802b` -> `#ebcb8b` | 3.40:1 -> 8.00:1 |
| nord | `--color-syntax-keyword` | `#4c87c2` -> `#8aaacb` | 2.89:1 -> 4.53:1 |
| nord | `--color-syntax-string` | `#539156` -> `#a3be8c` | 2.90:1 -> 5.36:1 |
| nord | `--color-syntax-constant` | `#a27d27` -> `#ebcb8b` | 2.85:1 -> 6.99:1 |
| nord | `--color-syntax-comment` | `#82807d` -> `#9ca7bd` | 2.77:1 -> 4.53:1 |
| nord | `--color-syntax-function` | `#9a73b8` -> `#c29bbb` | 2.86:1 -> 4.53:1 |
| nord | `--color-syntax-type` | `#0f9293` -> `#88c0d0` | 2.90:1 -> 5.46:1 |
| nord | `--color-syntax-punctuation` | `#82807d` -> `#9ca7bd` | 2.77:1 -> 4.53:1 |
| nord | `--color-syntax-variable` | `#c6c4c0` -> `#d8dee9` | 6.25:1 -> 8.08:1 |
| nord | `--color-syntax-link` | `#81a1c1` -> `#8aaacb` | 4.06:1 -> 4.53:1 |
| catppuccin-mocha | `--color-muted` | `#81869f` -> `#81859e` | 4.56:1 -> 4.53:1 |
| catppuccin-mocha | `--color-border` | `#353648` -> `#66697f` | 1.38:1 -> 3.03:1 |
| catppuccin-mocha | `--color-border-bold` | `#5e6177` -> `#66697f` | 2.68:1 -> 3.03:1 |
| catppuccin-mocha | `--color-error` | `#c06a63` -> `#f38ba8` | 4.28:1 -> 7.08:1 |
| catppuccin-mocha | `--color-success` | `#569459` -> `#a6e3a1` | 4.53:1 -> 11.03:1 |
| catppuccin-mocha | `--color-warning` | `#a4802b` -> `#f9e2af` | 4.47:1 -> 12.91:1 |
| catppuccin-mocha | `--color-syntax-keyword` | `#4c87c2` -> `#89b4fa` | 3.88:1 -> 6.95:1 |
| catppuccin-mocha | `--color-syntax-string` | `#539156` -> `#a6e3a1` | 3.88:1 -> 9.84:1 |
| catppuccin-mocha | `--color-syntax-constant` | `#a27d27` -> `#f9e2af` | 3.82:1 -> 11.51:1 |
| catppuccin-mocha | `--color-syntax-comment` | `#82807d` -> `#8b8ea5` | 3.70:1 -> 4.53:1 |
| catppuccin-mocha | `--color-syntax-function` | `#9a73b8` -> `#f5c2e7` | 3.83:1 -> 9.58:1 |
| catppuccin-mocha | `--color-syntax-type` | `#0f9293` -> `#94e2d5` | 3.88:1 -> 9.82:1 |
| catppuccin-mocha | `--color-syntax-punctuation` | `#82807d` -> `#8b8ea5` | 3.70:1 -> 4.53:1 |
| catppuccin-mocha | `--color-syntax-variable` | `#c6c4c0` -> `#cdd6f4` | 8.38:1 -> 10.11:1 |
| tokyonight | `--color-muted` | `#8187a6` -> `#7d82a0` | 4.83:1 -> 4.53:1 |
| tokyonight | `--color-border` | `#303141` -> `#62667f` | 1.34:1 -> 3.03:1 |
| tokyonight | `--color-border-bold` | `#575a71` -> `#62667f` | 2.53:1 -> 3.03:1 |
| tokyonight | `--color-error` | `#c06a63` -> `#f7768e` | 4.46:1 -> 6.46:1 |
| tokyonight | `--color-success` | `#569459` -> `#9ece6a` | 4.72:1 -> 9.35:1 |
| tokyonight | `--color-warning` | `#a4802b` -> `#e0af68` | 4.66:1 -> 8.55:1 |
| tokyonight | `--color-syntax-keyword` | `#4c87c2` -> `#7aa2f7` | 4.09:1 -> 6.13:1 |
| tokyonight | `--color-syntax-string` | `#539156` -> `#9ece6a` | 4.09:1 -> 8.44:1 |
| tokyonight | `--color-syntax-constant` | `#a27d27` -> `#e0af68` | 4.03:1 -> 7.71:1 |
| tokyonight | `--color-syntax-comment` | `#82807d` -> `#818aae` | 3.91:1 -> 4.53:1 |
| tokyonight | `--color-syntax-function` | `#9a73b8` -> `#bb9af7` | 4.04:1 -> 6.67:1 |
| tokyonight | `--color-syntax-type` | `#0f9293` -> `#7dcfff` | 4.10:1 -> 8.99:1 |
| tokyonight | `--color-syntax-punctuation` | `#82807d` -> `#818aae` | 3.91:1 -> 4.53:1 |
| tokyonight | `--color-syntax-variable` | `#c6c4c0` -> `#c0caf5` | 8.83:1 -> 9.56:1 |
| gruvbox-dark-hard | `--color-muted` | `#7e907c` -> `#798b79` | 4.81:1 -> 4.53:1 |
| gruvbox-dark-hard | `--color-border` | `#303a3a` -> `#5b6e65` | 1.40:1 -> 3.03:1 |
| gruvbox-dark-hard | `--color-border-bold` | `#566961` -> `#5b6e65` | 2.80:1 -> 3.03:1 |
| gruvbox-dark-hard | `--color-error` | `#c06a63` -> `#f75344` | 4.28:1 -> 4.89:1 |
| gruvbox-dark-hard | `--color-success` | `#569459` -> `#98971a` | 4.53:1 -> 5.29:1 |
| gruvbox-dark-hard | `--color-warning` | `#a4802b` -> `#d79921` | 4.47:1 -> 6.61:1 |
| gruvbox-dark-hard | `--color-syntax-keyword` | `#4c87c2` -> `#5a9a9d` | 3.86:1 -> 4.53:1 |
| gruvbox-dark-hard | `--color-syntax-string` | `#539156` -> `#98971a` | 3.86:1 -> 4.70:1 |
| gruvbox-dark-hard | `--color-syntax-constant` | `#a27d27` -> `#d79921` | 3.81:1 -> 5.87:1 |
| gruvbox-dark-hard | `--color-syntax-comment` | `#82807d` -> `#9c8d7e` | 3.69:1 -> 4.53:1 |
| gruvbox-dark-hard | `--color-syntax-function` | `#9a73b8` -> `#c8779b` | 3.82:1 -> 4.53:1 |
| gruvbox-dark-hard | `--color-syntax-type` | `#0f9293` -> `#689d6a` | 3.86:1 -> 4.59:1 |
| gruvbox-dark-hard | `--color-syntax-punctuation` | `#82807d` -> `#9c8d7e` | 3.69:1 -> 4.53:1 |
| gruvbox-dark-hard | `--color-syntax-variable` | `#c6c4c0` -> `#ebdbb2` | 8.33:1 -> 10.61:1 |
| kanagawa-wave | `--color-muted` | `#a28a83` -> `#99817d` | 5.08:1 -> 4.53:1 |
| kanagawa-wave | `--color-border` | `#3b353f` -> `#7a656a` | 1.37:1 -> 3.03:1 |
| kanagawa-wave | `--color-border-bold` | `#6f5c63` -> `#7a656a` | 2.64:1 -> 3.03:1 |
| kanagawa-wave | `--color-error` | `#c06a63` -> `#e76160` | 4.27:1 -> 4.87:1 |
| kanagawa-wave | `--color-success` | `#569459` -> `#77956b` | 4.51:1 -> 4.88:1 |
| kanagawa-wave | `--color-warning` | `#a4802b` -> `#c0a36e` | 4.45:1 -> 6.78:1 |
| kanagawa-wave | `--color-syntax-keyword` | `#4c87c2` -> `#7e9cd8` | 3.87:1 -> 5.31:1 |
| kanagawa-wave | `--color-syntax-string` | `#539156` -> `#7a986e` | 3.87:1 -> 4.53:1 |
| kanagawa-wave | `--color-syntax-constant` | `#a27d27` -> `#c0a36e` | 3.82:1 -> 6.05:1 |
| kanagawa-wave | `--color-syntax-comment` | `#82807d` -> `#919087` | 3.70:1 -> 4.53:1 |
| kanagawa-wave | `--color-syntax-function` | `#9a73b8` -> `#9b85bf` | 3.83:1 -> 4.53:1 |
| kanagawa-wave | `--color-syntax-type` | `#0f9293` -> `#6d988c` | 3.88:1 -> 4.53:1 |
| kanagawa-wave | `--color-syntax-punctuation` | `#82807d` -> `#919087` | 3.70:1 -> 4.53:1 |
| kanagawa-wave | `--color-syntax-variable` | `#c6c4c0` -> `#dcd7ba` | 8.36:1 -> 10.06:1 |
| rose-pine | `--color-muted` | `#89879a` -> `#817f92` | 5.02:1 -> 4.53:1 |
| rose-pine | `--color-border` | `#32303f` -> `#656375` | 1.37:1 -> 3.03:1 |
| rose-pine | `--color-border-bold` | `#605e70` -> `#656375` | 2.82:1 -> 3.03:1 |
| rose-pine | `--color-error` | `#c06a63` -> `#eb6f92` | 4.61:1 -> 6.07:1 |
| rose-pine | `--color-success` | `#569459` -> `#4c8eaa` | 4.88:1 -> 4.86:1 |
| rose-pine | `--color-warning` | `#a4802b` -> `#f6c177` | 4.81:1 -> 10.77:1 |
| rose-pine | `--color-syntax-keyword` | `#4c87c2` -> `#9ccfd8` | 4.20:1 -> 9.30:1 |
| rose-pine | `--color-syntax-string` | `#539156` -> `#4f91ad` | 4.20:1 -> 4.53:1 |
| rose-pine | `--color-syntax-constant` | `#a27d27` -> `#f6c177` | 4.14:1 -> 9.67:1 |
| rose-pine | `--color-syntax-comment` | `#82807d` -> `#8a86a3` | 4.01:1 -> 4.53:1 |
| rose-pine | `--color-syntax-function` | `#9a73b8` -> `#c4a7e7` | 4.15:1 -> 7.57:1 |
| rose-pine | `--color-syntax-type` | `#0f9293` -> `#ebbcba` | 4.21:1 -> 9.38:1 |
| rose-pine | `--color-syntax-punctuation` | `#82807d` -> `#8a86a3` | 4.01:1 -> 4.53:1 |
| rose-pine | `--color-syntax-variable` | `#c6c4c0` -> `#e0def4` | 9.07:1 -> 12.02:1 |
| solarized-dark-higher-contrast | `--color-muted` | `#698c91` -> `#65898d` | 4.75:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-border` | `#14333c` -> `#4a6c72` | 1.30:1 -> 3.03:1 |
| solarized-dark-higher-contrast | `--color-border-bold` | `#395a61` -> `#4a6c72` | 2.31:1 -> 3.03:1 |
| solarized-dark-higher-contrast | `--color-error` | `#c06a63` -> `#f44743` | 4.51:1 -> 4.81:1 |
| solarized-dark-higher-contrast | `--color-success` | `#569459` -> `#6cbe6c` | 4.77:1 -> 7.59:1 |
| solarized-dark-higher-contrast | `--color-warning` | `#a4802b` -> `#ad7f19` | 4.71:1 -> 4.81:1 |
| solarized-dark-higher-contrast | `--color-syntax-keyword` | `#4c87c2` -> `#3b8cdf` | 4.18:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-syntax-string` | `#539156` -> `#6cbe6c` | 4.18:1 -> 6.92:1 |
| solarized-dark-higher-contrast | `--color-syntax-constant` | `#a27d27` -> `#b0821d` | 4.12:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-syntax-comment` | `#82807d` -> `#4292b8` | 3.99:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-syntax-function` | `#9a73b8` -> `#ee4a90` | 4.13:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-syntax-type` | `#0f9293` -> `#2e998c` | 4.19:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-syntax-punctuation` | `#82807d` -> `#4292b8` | 3.99:1 -> 4.53:1 |
| solarized-dark-higher-contrast | `--color-syntax-variable` | `#c6c4c0` -> `#9cc2c3` | 9.03:1 -> 8.20:1 |
| solarized-dark-higher-contrast | `--color-syntax-link` | `#259286` -> `#2e998c` | 4.16:1 -> 4.53:1 |
| github-light-default | `--color-muted` | `#727176` -> `#77767a` | 4.81:1 -> 4.53:1 |
| github-light-default | `--color-border` | `#dbdada` -> `#959397` | 1.40:1 -> 3.03:1 |
| github-light-default | `--color-border-bold` | `#a09ea1` -> `#959397` | 2.66:1 -> 3.03:1 |
| github-light-default | `--color-error` | `#a34945` -> `#cf222e` | 5.85:1 -> 5.36:1 |
| github-light-default | `--color-success` | `#2f7434` -> `#116329` | 5.69:1 -> 7.39:1 |
| github-light-default | `--color-warning` | `#846305` -> `#4d2d00` | 5.56:1 -> 12.42:1 |
| github-light-default | `--color-syntax-keyword` | `#2569a8` -> `#0969da` | 5.03:1 -> 4.56:1 |
| github-light-default | `--color-syntax-string` | `#2b7132` -> `#116329` | 5.22:1 -> 6.49:1 |
| github-light-default | `--color-syntax-constant` | `#816000` -> `#4d2d00` | 5.09:1 -> 10.90:1 |
| github-light-default | `--color-syntax-comment` | `#68645e` -> `#57606a` | 5.16:1 -> 5.61:1 |
| github-light-default | `--color-syntax-function` | `#7e539c` -> `#814edd` | 5.11:1 -> 4.53:1 |
| github-light-default | `--color-syntax-type` | `#017273` -> `#157980` | 5.05:1 -> 4.53:1 |
| github-light-default | `--color-syntax-punctuation` | `#68645e` -> `#57606a` | 5.16:1 -> 5.61:1 |
| github-light-default | `--color-syntax-variable` | `#27241f` -> `#1f2328` | 13.64:1 -> 13.87:1 |
| gruvbox-light-hard | `--color-muted` | `#736a62` -> `#776e66` | 4.80:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-border` | `#ddd5bc` -> `#958b7e` | 1.33:1 -> 3.03:1 |
| gruvbox-light-hard | `--color-border-bold` | `#aca292` -> `#958b7e` | 2.28:1 -> 3.03:1 |
| gruvbox-light-hard | `--color-error` | `#a34945` -> `#cc241d` | 5.31:1 -> 4.97:1 |
| gruvbox-light-hard | `--color-success` | `#2f7434` -> `#706e00` | 5.17:1 -> 4.88:1 |
| gruvbox-light-hard | `--color-warning` | `#846305` -> `#985d00` | 5.05:1 -> 4.88:1 |
| gruvbox-light-hard | `--color-syntax-keyword` | `#2569a8` -> `#317174` | 4.66:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-string` | `#2b7132` -> `#6d6b00` | 4.82:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-constant` | `#816000` -> `#955b00` | 4.71:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-comment` | `#68645e` -> `#746657` | 4.77:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-function` | `#7e539c` -> `#9c4f73` | 4.73:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-type` | `#017273` -> `#407343` | 4.67:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-punctuation` | `#68645e` -> `#746657` | 4.77:1 -> 4.53:1 |
| gruvbox-light-hard | `--color-syntax-variable` | `#27241f` -> `#3c3836` | 12.62:1 -> 9.41:1 |
| gruvbox-light-hard | `--color-syntax-link` | `#cc241d` -> `#ca221b` | 4.44:1 -> 4.53:1 |
| catppuccin-latte | `--color-fg-muted` | `#696d84` -> `#686d83` | 4.50:1 -> 4.53:1 |
| catppuccin-latte | `--color-muted` | `#696d84` -> `#686d83` | 4.50:1 -> 4.53:1 |
| catppuccin-latte | `--color-border` | `#d4d7df` -> `#858a9d` | 1.27:1 -> 3.03:1 |
| catppuccin-latte | `--color-border-bold` | `#a8adbb` -> `#858a9d` | 1.98:1 -> 3.03:1 |
| catppuccin-latte | `--color-error` | `#a34945` -> `#d20f39` | 5.17:1 -> 4.80:1 |
| catppuccin-latte | `--color-success` | `#2f7434` -> `#107b00` | 5.04:1 -> 4.82:1 |
| catppuccin-latte | `--color-warning` | `#846305` -> `#a25600` | 4.92:1 -> 4.82:1 |
| catppuccin-latte | `--color-syntax-keyword` | `#2569a8` -> `#135cea` | 4.62:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-string` | `#2b7132` -> `#0b7900` | 4.78:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-constant` | `#816000` -> `#9f5300` | 4.67:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-comment` | `#68645e` -> `#63667c` | 4.73:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-function` | `#7e539c` -> `#aa3b90` | 4.69:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-type` | `#017273` -> `#00737a` | 4.63:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-punctuation` | `#68645e` -> `#63667c` | 4.73:1 -> 4.53:1 |
| catppuccin-latte | `--color-syntax-variable` | `#27241f` -> `#4c4f69` | 12.51:1 -> 6.43:1 |
| catppuccin-latte | `--color-syntax-link` | `#d20f39` -> `#cf0637` | 4.37:1 -> 4.53:1 |
| nord-light | `--color-fg-muted` | `#5f6674` -> `#626977` | 4.77:1 -> 4.53:1 |
| nord-light | `--color-muted` | `#5f6674` -> `#626977` | 4.77:1 -> 4.53:1 |
| nord-light | `--color-border` | `#cacfd8` -> `#7f8592` | 1.28:1 -> 3.03:1 |
| nord-light | `--color-border-bold` | `#9fa5b0` -> `#7f8592` | 2.03:1 -> 3.03:1 |
| nord-light | `--color-error` | `#a34945` -> `#a24752` | 4.80:1 -> 4.83:1 |
| nord-light | `--color-success` | `#2f7434` -> `#536c3d` | 4.68:1 -> 4.83:1 |
| nord-light | `--color-warning` | `#846305` -> `#7e601d` | 4.56:1 -> 4.83:1 |
| nord-light | `--color-syntax-keyword` | `#2569a8` -> `#476582` | 4.27:1 -> 4.53:1 |
| nord-light | `--color-syntax-string` | `#2b7132` -> `#51693b` | 4.42:1 -> 4.53:1 |
| nord-light | `--color-syntax-constant` | `#816000` -> `#7b5e1a` | 4.32:1 -> 4.53:1 |
| nord-light | `--color-syntax-comment` | `#68645e` -> `#4c566a` | 4.37:1 -> 5.49:1 |
| nord-light | `--color-syntax-function` | `#7e539c` -> `#7a5774` | 4.34:1 -> 4.53:1 |
| nord-light | `--color-syntax-type` | `#017273` -> `#326a78` | 4.28:1 -> 4.53:1 |
| nord-light | `--color-syntax-punctuation` | `#68645e` -> `#4c566a` | 4.37:1 -> 5.49:1 |
| nord-light | `--color-syntax-variable` | `#27241f` -> `#414858` | 11.57:1 -> 6.82:1 |
| nord-light | `--color-syntax-link` | `#865880` -> `#81537b` | 4.21:1 -> 4.53:1 |

## Visual notes

- Border tokens are the visible shift: most decks move from faint decorative rules to functional 3:1 rules, so diagrams and framed controls will look more deliberate.
- Syntax/state colors keep their deck ANSI hue families; light decks darken ANSI colors, dark decks lighten them. Nord Light uses a deepened red accent already selected by the existing accent picker.
- In several decks `--color-border` and `--color-border-bold` converge because both share the same 3:1 target and the old bold border sat below that floor.

