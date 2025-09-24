# Claude-Flow Website Optimization & Quality Assurance Mission

## Executive Summary
Conduct a comprehensive assessment and optimization of the williamzujkowski.github.io personal website repository. Focus on code quality, performance, accessibility, and maintainability while preserving the existing design aesthetic and functionality.

## Mission Objectives

### Phase 1: Assessment & Analysis
```yaml
assessment_tasks:
  - Use playwright-mcp to audit the live site (https://williamzujkowski.github.io)
  - Analyze CSS architecture and identify consolidation opportunities
  - Review all /scripts/ directory for active vs. vestigial scripts
  - Check for broken links, missing images, and 404s
  - Assess Core Web Vitals and Lighthouse scores
  - Verify accessibility compliance (WCAG 2.1 AA)
  - Document all findings with evidence
```

### Phase 2: Code Optimization
```yaml
optimization_priorities:
  css:
    - Consolidate redundant CSS files while preserving all styling
    - Optimize Tailwind config for actual usage (purge unused utilities)
    - Ensure dark mode transitions are smooth
    - Verify responsive breakpoints work correctly
    
  javascript:
    - Audit all JS files in /src/assets/js/
    - Remove dead code and consolidate where possible
    - Ensure all event listeners are properly managed
    - Optimize bundle size
    
  performance:
    - Optimize image loading strategies
    - Verify lazy loading implementation
    - Check service worker functionality
    - Ensure proper caching headers
```

### Phase 3: Repository Cleanup
```yaml
cleanup_tasks:
  scripts_directory:
    - Identify which Python scripts are actively used
    - Mark deprecated scripts for review
    - Update script documentation in CLAUDE.md
    - Create deprecation plan for unused scripts
    
  documentation:
    - Update README.md with current state
    - Ensure CLAUDE.md reflects actual implementation
    - Remove outdated documentation
    - Verify all internal links work
    
  general:
    - Remove commented-out code
    - Clean up console.logs and debug statements
    - Standardize code formatting
    - Update package dependencies (security patches only)
```

### Phase 4: Quality Assurance
```yaml
qa_requirements:
  functional_testing:
    - Test all navigation links
    - Verify search functionality
    - Test dark mode toggle
    - Validate form submissions
    - Check mobile menu functionality
    
  cross_browser:
    - Chrome/Edge (latest)
    - Firefox (latest)
    - Safari (if available)
    - Mobile browsers
    
  responsive_testing:
    - 320px (mobile small)
    - 768px (tablet)
    - 1024px (laptop)
    - 1920px (desktop)
    
  accessibility:
    - Keyboard navigation
    - Screen reader compatibility
    - Color contrast ratios
    - Focus indicators
    - ARIA labels
```

## Execution Instructions

### For All Agents:
1. **USE MCP TOOLS**: Leverage playwright-mcp for live site testing, sequential-thinking for complex analysis
2. **NO NEW FILES**: Update existing files only unless absolutely necessary
3. **PRESERVE DESIGN**: Maintain all current styling, animations, and visual elements
4. **DOCUMENT CHANGES**: Create detailed commit messages and update relevant documentation
5. **BE TRUTHFUL**: Report actual findings without exaggeration or speculation

### Critical Constraints:
```javascript
constraints = {
  css: "Keep total CSS under 100KB minified",
  js: "Keep total JS under 200KB minified",
  images: "Optimize but maintain quality",
  functionality: "Do not break any existing features",
  design: "Preserve all visual aesthetics"
}
```

### Specific Agent Tasks:

#### Agent 1: Site Auditor
```bash
# Use playwright-mcp to:
- Screenshot all pages at multiple breakpoints
- Test all interactive elements
- Measure performance metrics
- Check console for errors
- Validate all links
```

#### Agent 2: Code Optimizer
```bash
# Focus on:
- CSS consolidation in /src/assets/css/
- JS optimization in /src/assets/js/
- Remove unused code
- Improve load times
```

#### Agent 3: Repository Cleaner
```bash
# Tasks:
- Analyze /scripts/ directory usage
- Review /docs/ for outdated content
- Clean up root directory files
- Update .gitignore if needed
```

#### Agent 4: Quality Assurance
```bash
# Final verification:
- Test live site after changes
- Verify no regressions
- Ensure all features work
- Validate against original requirements
```

## Success Criteria

### Must Have:
- [ ] All existing features work correctly
- [ ] No visual regressions
- [ ] Improved or maintained Lighthouse scores
- [ ] Clean, organized repository structure
- [ ] Updated, accurate documentation

### Should Have:
- [ ] Reduced CSS/JS file sizes
- [ ] Faster page load times
- [ ] Better accessibility scores
- [ ] Cleaner codebase

### Nice to Have:
- [ ] Perfect Lighthouse scores (95+)
- [ ] Sub-2 second load times
- [ ] Zero console warnings

## Reporting Requirements

Each agent must provide:
1. **Before metrics** (screenshots, file sizes, scores)
2. **Changes made** (specific files and modifications)
3. **After metrics** (with improvements highlighted)
4. **Issues found** (with recommended fixes)
5. **Verification results** (proof of functionality)

## Final Deliverables

1. **Optimization Report**: Detailed analysis of improvements
2. **Cleanup Log**: List of removed/deprecated items
3. **QA Checklist**: Completed with evidence
4. **Documentation Updates**: All changes reflected in docs
5. **Performance Comparison**: Before/after metrics

## Execution Command

```bash
# Initialize swarm with proper configuration
swarm_init topology="hierarchical" agents=[auditor, optimizer, cleaner, qa]

# Execute with sequential phases
run_phases sequential=true rollback_on_failure=true

# Use MCP tools throughout
enable_tools playwright-mcp sequential-thinking

# Final validation
validate_live_site url="https://williamzujkowski.github.io"
```

## Remember:
- Quality over quantity
- Preserve what works
- Document everything
- Test before committing
- Be honest about findings
- Clean up after yourself

**Priority**: Maintain the professional quality and functionality of the site while improving maintainability and performance. The site should work better, load faster, and be easier to maintain - and be visually appealing and functional for users - ensure all menus, buttons, and other things work on desktop, tablet, and mobile and ensure they display correctly.