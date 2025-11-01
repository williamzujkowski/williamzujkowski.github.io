# Zero Trust VLAN Segmentation - Full Code Examples

Complete code referenced in the blog post:
**"Implementing Zero Trust Microsegmentation with VLANs"**

## Files

### 1. `firewall-rules.json`
Complete firewall rule set (54 lines) demonstrating:
- Management VLAN full access
- Trusted → Servers allowed (specific ports)
- IoT isolation (internet only)
- Guest network isolation
- Default deny policy

## Upload Instructions

```bash
# Create gists
gh gist create firewall-rules.json --desc "Zero Trust VLAN firewall rules"
```

## Blog Post Integration

**Before (54 lines):**
```json
{
  "rules": [
    // ... 54 lines of detailed rules
  ]
}
```

**After (8 lines):**
```json
{
  "rules": [
    {"name": "Allow Management to All", "action": "accept"},
    {"name": "Block Trusted to Management", "action": "drop"},
    {"name": "Block IoT to All Internal", "action": "drop"}
  ]
  // Full ruleset: [GIST_URL]
}
```

## Impact
- Reduces JSON config bloat by ~140 lines
- Improves readability
- Maintains security depth through gist
- Target: 64.8% → ~29% code ratio (-35.8pp)
