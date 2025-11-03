#!/usr/bin/env -S uv run python3
"""
SCRIPT: context-loader.py
PURPOSE: Intelligent context loading based on task requirements
CATEGORY: optimization
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Prototype for optimized context loading that dynamically determines
    which modules to load based on the current task. Demonstrates:

    1. Task pattern recognition
    2. Progressive module loading
    3. Token budget management
    4. Performance monitoring

USAGE:
    # Load context for blog writing
    uv run python3 scripts/utilities/context-loader.py --task blog-writing

    # Load context for file operations
    uv run python3 scripts/utilities/context-loader.py --task file-ops

    # Analyze token usage for a task
    uv run python3 scripts/utilities/context-loader.py --analyze git-commit

    # Interactive mode
    uv run python3 scripts/utilities/context-loader.py --interactive

MANIFEST_REGISTRY: scripts/utilities/context-loader.py
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger

# Setup logging
logger = setup_logger(__name__)


@dataclass
class Module:
    """Context module definition"""
    name: str
    file: Path
    priority: str
    tokens: int
    tags: List[str]
    dependencies: List[str]


@dataclass
class LoadPlan:
    """Context loading plan"""
    task: str
    modules: List[Module]
    total_tokens: int
    load_order: List[str]
    rationale: str


class ContextLoader:
    """Intelligent context loading based on task requirements"""

    def __init__(self, index_path: Path = Path("docs/context/INDEX.yaml")):
        self.index_path = index_path
        self.index = self._load_index()
        self.modules = self._parse_modules()

        # Task patterns (from CLAUDE.md Section 3.2)
        self.task_patterns = {
            'blog-writing': {
                'description': 'Create or edit blog posts',
                'required_tags': ['blog', 'nda', 'humanization'],
                'priority_threshold': 'HIGH',
                'max_tokens': 15000
            },
            'blog-transformation': {
                'description': 'Transform existing blog posts',
                'required_tags': ['transformation', 'humanization', 'citations'],
                'priority_threshold': 'MEDIUM',
                'max_tokens': 12000
            },
            'file-ops': {
                'description': 'File operations (create, edit, delete)',
                'required_tags': ['enforcement', 'files', 'validation'],
                'priority_threshold': 'HIGH',
                'max_tokens': 8000
            },
            'git-commit': {
                'description': 'Git operations and commits',
                'required_tags': ['enforcement', 'git', 'validation'],
                'priority_threshold': 'HIGH',
                'max_tokens': 6000
            },
            'sparc-dev': {
                'description': 'SPARC methodology development',
                'required_tags': ['sparc', 'enforcement'],
                'priority_threshold': 'MEDIUM',
                'max_tokens': 10000
            },
            'swarm-orchestration': {
                'description': 'Multi-agent swarm coordination',
                'required_tags': ['swarm', 'enforcement', 'files'],
                'priority_threshold': 'MEDIUM',
                'max_tokens': 12000
            },
            'image-management': {
                'description': 'Image generation and optimization',
                'required_tags': ['images', 'automation'],
                'priority_threshold': 'MEDIUM',
                'max_tokens': 5000
            },
            'research-citations': {
                'description': 'Add research citations to posts',
                'required_tags': ['citations', 'research', 'automation'],
                'priority_threshold': 'MEDIUM',
                'max_tokens': 8000
            }
        }

    def _load_index(self) -> Dict:
        """Load module index"""
        with open(self.index_path, 'r') as f:
            return yaml.safe_load(f)

    def _parse_modules(self) -> Dict[str, Module]:
        """Parse modules from index"""
        modules = {}

        for category_name, category_data in self.index.get('categories', {}).items():
            if 'modules' not in category_data:
                continue

            for module_data in category_data['modules']:
                module = Module(
                    name=module_data['name'],
                    file=Path(module_data['file']),
                    priority=module_data['priority'],
                    tokens=module_data['estimated_tokens'],
                    tags=module_data.get('tags', []),
                    dependencies=module_data.get('dependencies', [])
                )
                modules[module.name] = module

        return modules

    def create_load_plan(self, task: str) -> LoadPlan:
        """
        Create optimal loading plan for a task

        Strategy:
        1. Identify required modules based on task tags
        2. Add dependencies recursively
        3. Sort by priority and dependencies
        4. Apply token budget
        5. Generate load order
        """

        if task not in self.task_patterns:
            raise ValueError(f"Unknown task: {task}. Available: {list(self.task_patterns.keys())}")

        pattern = self.task_patterns[task]
        selected_modules = set()

        # 1. Select modules by tags
        for module_name, module in self.modules.items():
            # Check if module has any required tags
            if any(tag in module.tags for tag in pattern['required_tags']):
                selected_modules.add(module_name)

            # Always include enforcement for HIGH priority tasks
            if pattern['priority_threshold'] == 'HIGH' and 'enforcement' in module.tags:
                selected_modules.add(module_name)

        # 2. Add dependencies
        selected_modules = self._resolve_dependencies(selected_modules)

        # 3. Convert to Module objects and sort
        modules = [self.modules[name] for name in selected_modules]
        modules.sort(key=lambda m: (
            0 if m.priority == 'HIGH' else 1 if m.priority == 'MEDIUM' else 2,
            m.tokens
        ))

        # 4. Apply token budget
        total_tokens = sum(m.tokens for m in modules)
        if total_tokens > pattern['max_tokens']:
            modules = self._apply_token_budget(modules, pattern['max_tokens'])
            total_tokens = sum(m.tokens for m in modules)

        # 5. Generate load order (dependencies first)
        load_order = self._generate_load_order(modules)

        # 6. Create rationale
        rationale = self._create_rationale(task, pattern, modules, total_tokens)

        return LoadPlan(
            task=task,
            modules=modules,
            total_tokens=total_tokens,
            load_order=load_order,
            rationale=rationale
        )

    def _resolve_dependencies(self, module_names: Set[str]) -> Set[str]:
        """Recursively resolve module dependencies"""
        resolved = set(module_names)
        changed = True

        while changed:
            changed = False
            for name in list(resolved):
                if name not in self.modules:
                    continue

                for dep in self.modules[name].dependencies:
                    # Handle 'category/module' format
                    dep_name = dep.split('/')[-1] if '/' in dep else dep

                    if dep_name not in resolved and dep_name in self.modules:
                        resolved.add(dep_name)
                        changed = True

        return resolved

    def _apply_token_budget(self, modules: List[Module], max_tokens: int) -> List[Module]:
        """Apply token budget, keeping highest priority modules"""
        selected = []
        current_tokens = 0

        for module in modules:
            if current_tokens + module.tokens <= max_tokens:
                selected.append(module)
                current_tokens += module.tokens
            elif module.priority == 'HIGH':
                # Always include HIGH priority, even if over budget
                selected.append(module)
                current_tokens += module.tokens

        return selected

    def _generate_load_order(self, modules: List[Module]) -> List[str]:
        """Generate optimal load order (dependencies first, then priority)"""
        order = []
        remaining = {m.name for m in modules}

        while remaining:
            # Find modules with no unloaded dependencies
            ready = []
            for name in remaining:
                module = self.modules[name]
                deps_loaded = all(
                    dep.split('/')[-1] in order or dep.split('/')[-1] not in remaining
                    for dep in module.dependencies
                )
                if deps_loaded:
                    ready.append(name)

            if not ready:
                # Circular dependency or missing dep - load remaining by priority
                ready = list(remaining)

            # Sort ready modules by priority
            ready.sort(key=lambda n: (
                0 if self.modules[n].priority == 'HIGH' else
                1 if self.modules[n].priority == 'MEDIUM' else 2
            ))

            # Add to load order
            order.extend(ready)
            remaining -= set(ready)

        return order

    def _create_rationale(self, task: str, pattern: Dict, modules: List[Module], total_tokens: int) -> str:
        """Create human-readable rationale for loading plan"""

        rationale = f"Loading plan for: {pattern['description']}\n\n"
        rationale += f"Token budget: {pattern['max_tokens']:,} tokens\n"
        rationale += f"Actual usage: {total_tokens:,} tokens ({(total_tokens/pattern['max_tokens']*100):.1f}%)\n\n"

        # Group by priority
        high_priority = [m for m in modules if m.priority == 'HIGH']
        medium_priority = [m for m in modules if m.priority == 'MEDIUM']
        low_priority = [m for m in modules if m.priority == 'LOW']

        if high_priority:
            rationale += "HIGH Priority (always loaded):\n"
            for m in high_priority:
                rationale += f"  - {m.name} ({m.tokens:,} tokens): {', '.join(m.tags[:3])}\n"
            rationale += "\n"

        if medium_priority:
            rationale += "MEDIUM Priority (task-specific):\n"
            for m in medium_priority:
                rationale += f"  - {m.name} ({m.tokens:,} tokens): {', '.join(m.tags[:3])}\n"
            rationale += "\n"

        if low_priority:
            rationale += "LOW Priority (optional):\n"
            for m in low_priority:
                rationale += f"  - {m.name} ({m.tokens:,} tokens): {', '.join(m.tags[:3])}\n"
            rationale += "\n"

        return rationale

    def generate_loading_script(self, plan: LoadPlan) -> str:
        """Generate shell script to load context in optimal order"""

        script = f"""#!/bin/bash
# Context loading script for: {plan.task}
# Generated: {datetime.now().isoformat()}
# Total tokens: {plan.total_tokens:,}

echo "=== Loading context for {plan.task} ==="
echo "Token budget: {plan.total_tokens:,}"
echo ""

"""

        for module_name in plan.load_order:
            module = self.modules[module_name]
            script += f'echo "Loading {module.name} ({module.tokens:,} tokens)..."\n'
            script += f'cat {module.file}\n\n'

        script += 'echo ""\n'
        script += f'echo "✓ Loaded {len(plan.modules)} modules ({plan.total_tokens:,} tokens)"\n'

        return script

    def analyze_task_coverage(self) -> Dict[str, any]:
        """Analyze how well tasks are covered by available modules"""

        coverage = {}

        for task, pattern in self.task_patterns.items():
            # Count modules that match task tags
            matching_modules = []
            for module in self.modules.values():
                if any(tag in module.tags for tag in pattern['required_tags']):
                    matching_modules.append(module.name)

            coverage[task] = {
                'required_tags': pattern['required_tags'],
                'matching_modules': matching_modules,
                'coverage_score': len(matching_modules) / len(pattern['required_tags']),
                'max_tokens': pattern['max_tokens']
            }

        return coverage


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Intelligent context loading'
    )
    parser.add_argument(
        '--task',
        choices=['blog-writing', 'blog-transformation', 'file-ops', 'git-commit',
                 'sparc-dev', 'swarm-orchestration', 'image-management', 'research-citations'],
        help='Task to load context for'
    )
    parser.add_argument(
        '--analyze',
        metavar='TASK',
        help='Analyze loading plan for a task'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Analyze task coverage'
    )
    parser.add_argument(
        '--generate-script',
        action='store_true',
        help='Generate loading script'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs/prototypes/context-loading'),
        help='Output directory for scripts'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode'
    )

    args = parser.parse_args()

    loader = ContextLoader()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.coverage:
        coverage = loader.analyze_task_coverage()
        logger.info("\n=== TASK COVERAGE ANALYSIS ===\n")

        for task, data in coverage.items():
            logger.info(f"{task}:")
            logger.info(f"  Required tags: {', '.join(data['required_tags'])}")
            logger.info(f"  Matching modules: {len(data['matching_modules'])}")
            logger.info(f"  Coverage score: {data['coverage_score']:.1%}")
            logger.info(f"  Token budget: {data['max_tokens']:,}")
            logger.info("")

        return

    if args.analyze or args.task:
        task = args.analyze or args.task

        try:
            plan = loader.create_load_plan(task)

            logger.info("\n=== LOADING PLAN ===\n")
            logger.info(plan.rationale)
            logger.info("Load order:")
            for i, module_name in enumerate(plan.load_order, 1):
                module = loader.modules[module_name]
                logger.info(f"  {i}. {module_name} ({module.tokens:,} tokens)")

            if args.generate_script:
                script = loader.generate_loading_script(plan)
                output_file = args.output_dir / f'load-{task}.sh'

                with open(output_file, 'w') as f:
                    f.write(script)

                output_file.chmod(0o755)  # Make executable
                logger.info(f"\n✓ Loading script: {output_file}")

        except ValueError as e:
            logger.error(f"Error: {e}")

    if args.interactive:
        logger.info("\n=== INTERACTIVE CONTEXT LOADER ===\n")
        logger.info("Available tasks:")
        for i, (task, pattern) in enumerate(loader.task_patterns.items(), 1):
            logger.info(f"  {i}. {task}: {pattern['description']}")

        while True:
            choice = input("\nSelect task (number or name, 'q' to quit): ").strip()

            if choice.lower() == 'q':
                break

            # Handle numeric choice
            if choice.isdigit():
                idx = int(choice) - 1
                tasks = list(loader.task_patterns.keys())
                if 0 <= idx < len(tasks):
                    choice = tasks[idx]

            if choice in loader.task_patterns:
                plan = loader.create_load_plan(choice)
                logger.info(f"\n{plan.rationale}")
            else:
                logger.warning(f"Unknown task: {choice}")


if __name__ == '__main__':
    main()
