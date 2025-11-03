#!/usr/bin/env -S uv run python3
"""
SCRIPT: script-consolidator.py
PURPOSE: Identify and consolidate duplicate script functionality
CATEGORY: optimization
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Analyzes existing scripts for duplication and creates consolidated
    versions. Demonstrates:

    1. Code similarity detection
    2. Common pattern extraction
    3. Consolidated script generation
    4. Backward compatibility mapping

USAGE:
    # Analyze scripts for duplication
    uv run python3 scripts/utilities/script-consolidator.py --analyze

    # Generate consolidation plan
    uv run python3 scripts/utilities/script-consolidator.py --plan

    # Create consolidated scripts
    uv run python3 scripts/utilities/script-consolidator.py --consolidate

MANIFEST_REGISTRY: scripts/utilities/script-consolidator.py
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
import ast
import sys

# Path setup for centralized logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)


@dataclass
class Script:
    """Script metadata"""
    path: Path
    name: str
    category: str
    purpose: str
    imports: Set[str]
    functions: List[str]
    lines: int


@dataclass
class Consolidation:
    """Consolidation opportunity"""
    name: str
    scripts: List[Script]
    common_patterns: List[str]
    estimated_reduction: int
    priority: str


class ScriptConsolidator:
    """Identify and consolidate duplicate functionality"""

    def __init__(self, scripts_dir: Path = Path("scripts")):
        self.scripts_dir = scripts_dir
        self.scripts = self._discover_scripts()

    def _discover_scripts(self) -> List[Script]:
        """Discover all Python scripts"""
        scripts = []

        for script_path in self.scripts_dir.rglob("*.py"):
            # Skip __init__.py and lib files
            if script_path.name.startswith('__'):
                continue

            try:
                script = self._parse_script(script_path)
                scripts.append(script)
            except Exception as e:
                logger.warning(f"Warning: Could not parse {script_path}: {e}")

        return scripts

    def _parse_script(self, script_path: Path) -> Script:
        """Parse script metadata"""
        with open(script_path, 'r') as f:
            content = f.read()

        # Extract metadata from docstring
        purpose = "Unknown"
        category = "unknown"

        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1)

            purpose_match = re.search(r'PURPOSE:\s*(.+)', docstring)
            if purpose_match:
                purpose = purpose_match.group(1).strip()

            category_match = re.search(r'CATEGORY:\s*(.+)', docstring)
            if category_match:
                category = category_match.group(1).strip()

        # Extract imports
        imports = set()
        for line in content.split('\n'):
            if line.startswith('import ') or line.startswith('from '):
                imports.add(line.strip())

        # Extract function names
        functions = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
        except:
            # Fallback to regex if AST parsing fails
            functions = re.findall(r'def (\w+)\(', content)

        return Script(
            path=script_path,
            name=script_path.name,
            category=category,
            purpose=purpose,
            imports=imports,
            functions=functions,
            lines=len(content.split('\n'))
        )

    def analyze_duplication(self) -> Dict[str, any]:
        """Analyze scripts for duplication opportunities"""

        # Group by category
        by_category = defaultdict(list)
        for script in self.scripts:
            by_category[script.category].append(script)

        # Find common imports
        import_counts = defaultdict(int)
        for script in self.scripts:
            for imp in script.imports:
                import_counts[imp] += 1

        # Find common function patterns
        function_patterns = defaultdict(int)
        for script in self.scripts:
            for func in script.functions:
                # Normalize function names
                normalized = re.sub(r'[0-9]+', '', func)
                function_patterns[normalized] += 1

        # Identify consolidation opportunities
        opportunities = []

        # 1. Blog validation scripts
        blog_validators = [s for s in self.scripts if 'validat' in s.purpose.lower() and 'blog' in s.category]
        if len(blog_validators) > 1:
            opportunities.append(Consolidation(
                name="blog-validator-unified",
                scripts=blog_validators,
                common_patterns=['validate', 'frontmatter', 'markdown'],
                estimated_reduction=sum(s.lines for s in blog_validators[1:]),
                priority='HIGH'
            ))

        # 2. Link validation scripts
        link_validators = [s for s in self.scripts if 'link' in s.category.lower()]
        if len(link_validators) > 2:
            opportunities.append(Consolidation(
                name="link-validator-unified",
                scripts=link_validators,
                common_patterns=['requests', 'validate_url', 'check_link'],
                estimated_reduction=sum(s.lines for s in link_validators[2:]),
                priority='HIGH'
            ))

        # 3. Image processing scripts
        image_scripts = [s for s in self.scripts if 'image' in s.category.lower()]
        if len(image_scripts) > 1:
            opportunities.append(Consolidation(
                name="image-processor-unified",
                scripts=image_scripts,
                common_patterns=['PIL', 'optimize', 'resize'],
                estimated_reduction=sum(s.lines for s in image_scripts[1:]),
                priority='MEDIUM'
            ))

        # 4. Citation/research scripts
        research_scripts = [s for s in self.scripts if any(
            kw in s.category.lower() for kw in ['research', 'citation', 'academic']
        )]
        if len(research_scripts) > 1:
            opportunities.append(Consolidation(
                name="research-tools-unified",
                scripts=research_scripts,
                common_patterns=['search', 'citation', 'doi'],
                estimated_reduction=sum(s.lines for s in research_scripts[1:]),
                priority='MEDIUM'
            ))

        return {
            'total_scripts': len(self.scripts),
            'total_lines': sum(s.lines for s in self.scripts),
            'by_category': {cat: len(scripts) for cat, scripts in by_category.items()},
            'common_imports': [(imp, count) for imp, count in sorted(
                import_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]],
            'common_functions': [(func, count) for func, count in sorted(
                function_patterns.items(), key=lambda x: x[1], reverse=True
            ) if count > 2][:10],
            'opportunities': opportunities
        }

    def generate_consolidation_plan(self) -> str:
        """Generate detailed consolidation plan"""

        analysis = self.analyze_duplication()

        plan = f"""# Script Consolidation Plan

## Current State
- **Total scripts**: {analysis['total_scripts']}
- **Total lines**: {analysis['total_lines']:,}
- **Categories**: {len(analysis['by_category'])}

## Scripts by Category
"""

        for category, count in sorted(analysis['by_category'].items(), key=lambda x: x[1], reverse=True):
            plan += f"- {category}: {count} scripts\n"

        plan += f"""

## Consolidation Opportunities

Found {len(analysis['opportunities'])} consolidation opportunities:

"""

        total_reduction = 0
        for opp in analysis['opportunities']:
            total_reduction += opp.estimated_reduction
            plan += f"""### {opp.priority}: {opp.name}

**Scripts to consolidate**: {len(opp.scripts)}
"""
            for script in opp.scripts:
                plan += f"- {script.name} ({script.lines} lines)\n"

            plan += f"""
**Common patterns**: {', '.join(opp.common_patterns)}
**Estimated line reduction**: {opp.estimated_reduction:,}

**Consolidation approach**:
1. Extract common functionality to `scripts/lib/{opp.name}.py`
2. Create unified CLI with subcommands
3. Maintain backward compatibility via wrapper scripts
4. Update documentation and examples

"""

        plan += f"""## Total Potential Reduction
- **Lines**: {total_reduction:,} ({(total_reduction/analysis['total_lines']*100):.1f}%)
- **Scripts**: {sum(len(o.scripts)-1 for o in analysis['opportunities'])} deprecated
- **Maintainability**: Significantly improved

## Common Imports (Top 10)
"""

        for imp, count in analysis['common_imports'][:10]:
            plan += f"- `{imp}` used in {count} scripts\n"

        plan += """

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
"""

        return plan

    def generate_consolidated_example(self, consolidation: Consolidation) -> str:
        """Generate example of consolidated script"""

        template = f'''#!/usr/bin/env -S uv run python3
"""
SCRIPT: {consolidation.name}.py
PURPOSE: Unified {consolidation.name.replace('-', ' ')}
CATEGORY: consolidated
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-01

DESCRIPTION:
    Consolidated script combining functionality from:
    {chr(10).join(f"    - {s.name}" for s in consolidation.scripts)}

    Provides unified CLI with subcommands for all operations.

USAGE:
    # List available operations
    uv run python3 scripts/utilities/{consolidation.name}.py --list

    # Run specific operation
    uv run python3 scripts/utilities/{consolidation.name}.py <operation> [args]

MANIFEST_REGISTRY: scripts/utilities/{consolidation.name}.py

DEPRECATED_SCRIPTS:
    The following scripts are now wrappers to this unified script:
    {chr(10).join(f"    - {s.name} → {consolidation.name} {s.name.replace('.py', '')}" for s in consolidation.scripts)}
"""

import argparse
from pathlib import Path
from typing import List
from enum import Enum


class OperationType(Enum):
    """Available operations"""
    {chr(10).join(f'    {s.name.replace(".py", "").upper().replace("-", "_")} = "{s.name.replace(".py", "")}"' for s in consolidation.scripts)}


class {consolidation.name.replace('-', '_').title().replace('_', '')}:
    """Unified {consolidation.name}"""

    def __init__(self):
        self.operations = {{op.value: getattr(self, f"_{{op.value.replace('-', '_')}}")
                           for op in OperationType}}

    # Individual operation methods (migrated from original scripts)
    {chr(10).join(f'    def _{s.name.replace(".py", "").replace("-", "_")}(self, **kwargs):{chr(10)}        """Original: {s.purpose}"""{chr(10)}        # TODO: Migrate functionality from {s.name}{chr(10)}        pass{chr(10)}' for s in consolidation.scripts)}

    def run(self, operation: OperationType, **kwargs):
        """Execute operation"""
        if operation.value not in self.operations:
            raise ValueError(f"Unknown operation: {{operation}}")

        return self.operations[operation.value](**kwargs)


def main():
    """Main execution with unified CLI"""
    parser = argparse.ArgumentParser(
        description=f'Unified {consolidation.name}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'operation',
        choices=[op.value for op in OperationType],
        help='Operation to perform'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available operations'
    )

    args, unknown = parser.parse_known_args()

    if args.list:
        print(f"\\nAvailable operations for {consolidation.name}:\\n")
        for op in OperationType:
            print(f"  - {{op.value}}")
        return

    # Create and run unified tool
    tool = {consolidation.name.replace('-', '_').title().replace('_', '')}()
    tool.run(OperationType(args.operation))


if __name__ == '__main__':
    main()
'''

        return template


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Consolidate duplicate scripts'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze duplication'
    )
    parser.add_argument(
        '--plan',
        action='store_true',
        help='Generate consolidation plan'
    )
    parser.add_argument(
        '--consolidate',
        action='store_true',
        help='Generate consolidated scripts'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs/prototypes/script-consolidation'),
        help='Output directory'
    )

    args = parser.parse_args()

    consolidator = ScriptConsolidator()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.analyze or not any([args.plan, args.consolidate]):
        analysis = consolidator.analyze_duplication()

        logger.info("=== SCRIPT ANALYSIS ===")
        logger.info(f"Total scripts: {analysis['total_scripts']}")
        logger.info(f"Total lines: {analysis['total_lines']:,}")
        logger.info(f"Consolidation opportunities: {len(analysis['opportunities'])}")

        for opp in analysis['opportunities']:
            logger.info(f"[{opp.priority}] {opp.name}")
            logger.info(f"    Scripts: {len(opp.scripts)}")
            logger.info(f"    Line reduction: {opp.estimated_reduction:,}")

    if args.plan:
        plan = consolidator.generate_consolidation_plan()
        output_file = args.output_dir / 'consolidation-plan.md'

        with open(output_file, 'w') as f:
            f.write(plan)

        logger.info(f"✓ Consolidation plan: {output_file}")

    if args.consolidate:
        analysis = consolidator.analyze_duplication()

        for opp in analysis['opportunities']:
            example = consolidator.generate_consolidated_example(opp)
            output_file = args.output_dir / f'{opp.name}.py'

            with open(output_file, 'w') as f:
                f.write(example)

            logger.info(f"✓ Generated: {output_file}")


if __name__ == '__main__':
    main()
