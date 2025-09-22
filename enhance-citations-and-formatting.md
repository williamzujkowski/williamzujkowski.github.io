# Research Citation Enhancement & Formatting Fix Mission

## OBJECTIVE
Enhance research credibility of williamzujkowski.github.io by adding hyperlinked academic citations while simultaneously fixing all markdown formatting issues, including broken links, raising citation coverage from 45% to 90%+ while maintaining 100% NDA and political compliance.

## CONTEXT
Following a successful compliance audit (Report: COMPLIANCE_REPORT_2025-09-21.md), the repository needs:
- Citation coverage improvement: 45% → 90%+
- Link formatting fixes (missing parentheses, broken markdown)
- General markdown formatting cleanup
- All while maintaining 100% NDA/political compliance ✅

## MISSION PARAMETERS

### Phase 1: Formatting & Citation Audit (DO NOT MODIFY YET)
For each post in src/posts/:

#### A. Link Formatting Issues to Find:
1. **Missing closing parentheses**: `[text](url` instead of `[text](url)`
2. **Missing opening brackets**: `text](url)` instead of `[text](url)`
3. **Space in link syntax**: `[text] (url)` instead of `[text](url)`
4. **Reversed brackets**: `(text)[url]` instead of `[text](url)`
5. **Bare URLs**: `https://example.com` not in link format
6. **Broken image links**: `![alt](path` missing `)`
7. **Malformed reference links**: `[text][ref` missing `]`

#### B. Other Markdown Issues to Find:
1. **Unclosed code blocks**: ``` without closing ```
2. **Broken lists**: Inconsistent indentation or markers
3. **Header issues**: Missing space after #, inconsistent levels
4. **Bold/italic issues**: Unclosed ** or * markers
5. **Quote blocks**: Broken > continuity
6. **Table formatting**: Misaligned columns

#### C. Citation Gaps to Identify:
1. Statistical claims without sources
2. Technical assertions needing backing
3. Performance metrics without references
4. Best practice claims without authority

Output: Combined formatting & citation audit report

### Phase 2: Systematic Fixes

#### A. Fix Link Formatting (PRIORITY 1)
```markdown
# Common fixes needed:

# Missing closing parenthesis
WRONG: [Research by Zhang et al. (2023)](https://doi.org/10.1109/TDSC.2023.3247569
RIGHT: [Research by Zhang et al. (2023)](https://doi.org/10.1109/TDSC.2023.3247569)

# Space in link syntax  
WRONG: [OWASP Top 10] (https://owasp.org/top10/)
RIGHT: [OWASP Top 10](https://owasp.org/top10/)

# Bare URLs
WRONG: Check out https://github.com/williamzujkowski/data-sources for more
RIGHT: Check out [data-sources repository](https://github.com/williamzujkowski/data-sources) for more

# Broken image syntax
WRONG: ![Architecture diagram](/assets/images/arch.png
RIGHT: ![Architecture diagram](/assets/images/arch.png)
```

#### B. Fix Markdown Formatting (PRIORITY 2)
```markdown
# Headers
WRONG: ##No space after hash
RIGHT: ## Space after hash

# Code blocks
WRONG: ```python
       code here
       (no closing ```)
RIGHT: ```python
       code here
       ```

# Lists
WRONG: - Item 1
        - Subitem (wrong indent)
RIGHT: - Item 1
         - Subitem (2 spaces)

# Bold/Italic
WRONG: **bold text without closing
RIGHT: **bold text**
```

### Phase 3: Citation Enhancement
Using https://github.com/williamzujkowski/data-sources:
1. Add citations for all identified gaps
2. Use proper link format (verified working)
3. Maintain consistent citation style
4. Include hyperlinks for all sources

### VALIDATION PATTERNS

#### Link Validation Regex Patterns:
```javascript
// Correct markdown link pattern
/\[([^\]]+)\]\(([^)]+)\)/g

// Find broken links (missing closing paren)
/\[([^\]]+)\]\([^)]*$/gm

// Find bare URLs
/(?<![\[\(])(https?:\/\/[^\s\[\]\(\)]+)(?![\]\)])/g

// Find spaced links
/\[([^\]]+)\]\s+\(([^)]+)\)/g
```

### CRITICAL CONSTRAINTS
**DO NOT:**
- Add any work-related content
- Change the meaning of any claims
- Add political commentary
- Break existing NDA compliance
- Remove homelab examples
- Introduce new formatting errors

**ALWAYS:**
- Test every link after fixing
- Preserve content meaning
- Maintain readability
- Keep compliance at 100%
- Validate markdown syntax

## SYSTEMATIC FIX PROCESS

### For Each Post:
1. **Scan** - Identify all issues (formatting + citations)
2. **Fix Links** - Repair all broken link syntax first
3. **Fix Markdown** - Clean up other formatting issues
4. **Add Citations** - Insert academic sources
5. **Validate** - Test all links work
6. **Review** - Ensure compliance maintained

## COMMON PATTERNS TO FIX

### Link Formatting Fixes:
```markdown
# Type 1: Missing closing parenthesis
Find: ](https://example.com
Fix:  ](https://example.com)

# Type 2: Extra spaces
Find: ] (https://
Fix:  ](https://

# Type 3: Bare academic URLs
Find: https://arxiv.org/abs/2024.12345
Fix:  [arXiv:2024.12345](https://arxiv.org/abs/2024.12345)

# Type 4: DOI links
Find: https://doi.org/10.1234/abc
Fix:  [DOI:10.1234/abc](https://doi.org/10.1234/abc)
```

### Citation Format Standard:
```markdown
# Inline citation with proper formatting
According to [recent research (Smith et al., 2024)](https://doi.org/10.xxxx/xxxxx), 
the vulnerability affects 73% of systems.

# Multiple citations
Several studies [[1]](https://link1) [[2]](https://link2) demonstrate this effect.

# Organization reports
The [2024 Verizon DBIR](https://enterprise.verizon.com/resources/reports/dbir/) 
found that 90% of breaches involved human error.
```

## QUALITY CHECKLIST

### Link Formatting:
- [ ] All links have closing parentheses
- [ ] No spaces between ] and (
- [ ] All URLs are in proper markdown format
- [ ] Image links properly formatted
- [ ] Reference links work correctly

### Markdown Formatting:
- [ ] All code blocks closed
- [ ] Headers have spaces after #
- [ ] Lists properly indented
- [ ] Bold/italic markers paired
- [ ] Tables aligned (if present)

### Citations:
- [ ] 90%+ claims have sources
- [ ] All statistics cited
- [ ] Links are clickable
- [ ] Academic sources prioritized
- [ ] Consistent format throughout

### Compliance:
- [ ] Zero work references
- [ ] NDA compliance 100%
- [ ] Political neutrality maintained
- [ ] Build passes after fixes

## SUCCESS METRICS

### Must Achieve:
- [ ] 100% of broken links fixed
- [ ] 0 markdown syntax errors
- [ ] 90%+ citation coverage
- [ ] All links validated as working
- [ ] Compliance maintained at 100%

### Should Achieve:
- [ ] Consistent formatting throughout
- [ ] 50%+ academic sources
- [ ] Improved readability scores
- [ ] Clean markdown validation

## EXAMPLE TRANSFORMATIONS

### Example 1: Link Fix + Citation
```markdown
# BEFORE (broken + no citation):
[NIST guidelines](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf
Container isolation is more secure.

# AFTER (fixed + cited):
[NIST guidelines](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf)
Container isolation is [proven more secure according to NIST SP 800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf).
```

### Example 2: Multiple Issues
```markdown
# BEFORE:
##Missing Space Header
Check https://owasp.org for more info.
[Security research] (https://arxiv.org/abs/2024.12345
**Bold text not closed

# AFTER:
## Missing Space Header
Check [OWASP](https://owasp.org) for more info.
[Security research](https://arxiv.org/abs/2024.12345)
**Bold text not closed**
```

## AUTOMATED VALIDATION SCRIPT

After fixes, run validation:
```python
# validate_formatting.py
import re
import glob

def check_links(content):
    # Find broken links
    broken = re.findall(r'\[([^\]]+)\]\([^)]*$', content, re.MULTILINE)
    bare_urls = re.findall(r'(?<![\[\(])(https?://[^\s\[\]\(\)]+)(?![\]\)])', content)
    spaced = re.findall(r'\[([^\]]+)\]\s+\(([^)]+)\)', content)
    return broken, bare_urls, spaced

def validate_post(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    broken, bare, spaced = check_links(content)
    
    if broken:
        issues.append(f"Broken links: {len(broken)}")
    if bare:
        issues.append(f"Bare URLs: {len(bare)}")
    if spaced:
        issues.append(f"Spaced links: {len(spaced)}")
    
    # Check for unclosed code blocks
    if content.count('```') % 2 != 0:
        issues.append("Unclosed code block")
    
    return issues

# Validate all posts
for post in glob.glob('src/posts/*.md'):
    issues = validate_post(post)
    if issues:
        print(f"{post}: {', '.join(issues)}")
```

## PRIORITY ORDER

1. **Critical**: Fix broken link syntax (missing parentheses)
2. **High**: Fix bare URLs and formatting issues
3. **High**: Add citations to statistics/claims
4. **Medium**: Enhance with academic sources
5. **Low**: Formatting consistency improvements

## DELIVERABLES

1. **Formatting Audit Report**: List of all issues found
2. **Fixed Posts**: All formatting issues resolved
3. **Citation Report**: Before/after coverage metrics
4. **Validation Log**: Proof all links work
5. **Compliance Confirmation**: 100% maintained

Remember: Fix formatting issues FIRST, then add citations. This ensures clean markdown before enhancing content. Every fix should improve quality without compromising compliance.