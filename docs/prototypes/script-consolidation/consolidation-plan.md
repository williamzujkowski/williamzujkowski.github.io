# Script Consolidation Plan

## Current State
- **Total scripts**: 60
- **Total lines**: 24,626
- **Categories**: 11

## Scripts by Category
- unknown: 17 scripts
- blog_management: 9 scripts
- link_validation: 7 scripts
- academic_research: 6 scripts
- utilities: 5 scripts
- optimization: 5 scripts
- image_management: 4 scripts
- utility: 2 scripts
- content_optimization: 2 scripts
- content_validation: 2 scripts
- maintenance: 1 scripts


## Consolidation Opportunities

Found 3 consolidation opportunities:

### HIGH: link-validator-unified

**Scripts to consolidate**: 7
- batch-link-fixer.py (420 lines)
- link-report-generator.py (457 lines)
- link-validator.py (561 lines)
- link-monitor.py (501 lines)
- citation-report.py (265 lines)
- advanced-link-repair.py (503 lines)
- link-extractor.py (350 lines)

**Common patterns**: requests, validate_url, check_link
**Estimated line reduction**: 2,180

**Consolidation approach**:
1. Extract common functionality to `scripts/lib/link-validator-unified.py`
2. Create unified CLI with subcommands
3. Maintain backward compatibility via wrapper scripts
4. Update documentation and examples

### MEDIUM: image-processor-unified

**Scripts to consolidate**: 4
- diagram-manager.py (493 lines)
- generate-og-image.py (163 lines)
- fetch-stock-images.py (344 lines)
- playwright-image-search.py (430 lines)

**Common patterns**: PIL, optimize, resize
**Estimated line reduction**: 937

**Consolidation approach**:
1. Extract common functionality to `scripts/lib/image-processor-unified.py`
2. Create unified CLI with subcommands
3. Maintain backward compatibility via wrapper scripts
4. Update documentation and examples

### MEDIUM: research-tools-unified

**Scripts to consolidate**: 6
- check-citation-hyperlinks.py (265 lines)
- add-academic-citations.py (381 lines)
- research-validator.py (344 lines)
- academic-search.py (393 lines)
- citation-updater.py (518 lines)
- citation-repair.py (620 lines)

**Common patterns**: search, citation, doi
**Estimated line reduction**: 2,256

**Consolidation approach**:
1. Extract common functionality to `scripts/lib/research-tools-unified.py`
2. Create unified CLI with subcommands
3. Maintain backward compatibility via wrapper scripts
4. Update documentation and examples

## Total Potential Reduction
- **Lines**: 5,373 (21.8%)
- **Scripts**: 14 deprecated
- **Maintainability**: Significantly improved

## Common Imports (Top 10)
- `from pathlib import Path` used in 57 scripts
- `import json` used in 50 scripts
- `import sys` used in 38 scripts
- `import re` used in 34 scripts
- `from datetime import datetime` used in 34 scripts
- `import argparse` used in 32 scripts
- `import logging` used in 18 scripts
- `import os` used in 16 scripts
- `from typing import Dict, List, Tuple` used in 13 scripts
- `import asyncio` used in 12 scripts


## Recommended Implementation Order

1. **Phase 1** (HIGH priority): Blog validators, Link validators
   - High duplication, frequently used
   - Create `blog-validator-unified.py` and `link-validator-unified.py`

2. **Phase 2** (MEDIUM priority): Image processors, Research tools
   - Moderate duplication, specialized use cases
   - Create `image-processor-unified.py` and `research-tools-unified.py`

3. **Phase 3** (LOW priority): Remaining utilities
   - Low duplication, infrequent use
   - Consolidate into `utilities-toolkit.py`

## Backward Compatibility

Maintain all existing script names as thin wrappers:

```python
#!/usr/bin/env -S uv run python3
# Legacy wrapper for backward compatibility
from scripts.lib.blog_validator_unified import main, ValidationType

if __name__ == '__main__':
    # Old script behavior preserved
    main(validation_type=ValidationType.FRONTMATTER)
```

## Migration Guide

For each consolidated script:
1. Document old → new command mapping
2. Provide migration examples
3. Update CLAUDE.md references
4. Add deprecation notices (6-month sunset period)
