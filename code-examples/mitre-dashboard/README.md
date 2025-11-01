# MITRE ATT&CK Dashboard - Full Code Examples

Complete code referenced in the blog post:
**"Building Your Own MITRE ATT&CK Threat Intelligence Dashboard"**

## Files

### 1. `plotly-heatmap.py`
Plotly-based visualization (61 lines) for:
- ATT&CK technique frequency heatmap
- Threat activity timeline
- Interactive charts with severity indicators

### 2. Additional scripts (if needed)
- Email alerting integration
- API data fetching
- CISA alert mapping

## Upload Instructions

```bash
# Create gists
gh gist create plotly-heatmap.py --desc "MITRE ATT&CK Plotly visualization"

# Or upload manually at: https://gist.github.com/
```

## Usage in Blog Post

Replace verbose code blocks with essentials:

**Before (61 lines):**
```python
import plotly.graph_objects as go
# ... 61 lines of implementation
```

**After (12 lines):**
```python
# Visualization layer (simplified)
class ThreatVisualizer:
    def create_attack_heatmap(self):
        """Interactive heatmap using Plotly"""
        fig = go.Figure(data=go.Heatmap(
            x=tactics, y=techniques, z=frequencies,
            colorscale='Reds'
        ))
        return fig

# Full implementation: [GIST_URL]
```

## Impact

- Reduces code bloat by ~150 lines
- Improves readability
- Maintains technical depth through gist references
- Target: 68% → ~27% code ratio (-41 percentage points)
