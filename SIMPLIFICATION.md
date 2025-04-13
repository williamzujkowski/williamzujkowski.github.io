# Website Simplification Plan

This document outlines a plan to reduce the complexity of the website while maintaining its core functionality.

## 1. Directory Structure Simplification

### Recommended Changes:
- **Consolidate Data Directories**
  - Move all data to `/src/_data` directory
  - Remove duplicated data in `/_data` and `/scripts/_data`
  - Update all scripts to reference the single data source

- **Simplify Asset Organization**
  - Consolidate image directories into a single structure
  - Remove redundant screenshot directories
  - Create a clearer separation between user-visible assets and internal data

- **Streamline Source Organization**
  - Move all template files to `/src/templates`
  - Keep posts in `/src/posts` for clarity
  - Organize CSS into `/src/styles` with a clear component structure

### Benefits:
- Clearer navigation of the codebase
- Reduced confusion about where files should be stored
- Elimination of synchronization issues between duplicate files

## 2. Build Process Simplification

### Recommended Changes:
- **Reduce npm Scripts**
  - Consolidate processing scripts (combine `process:posts` variants)
  - Create a single CSS build pipeline
  - Simplify blog post processing to a single command

- **Streamline Build Workflow**
  - Create a unified build command with sensible defaults
  - Eliminate fallback data creation in favor of checked-in examples
  - Replace complex screenshot generation with simple static assets

- **Simplify Configuration Files**
  - Consolidate Eleventy configs into a single file
  - Move all configuration parameters into a single source of truth
  - Remove duplicate Tailwind/PostCSS configurations

### Benefits:
- Faster builds with fewer steps
- More maintainable build process
- Clearer documentation of what each command does

## 3. Data Architecture Simplification

### Recommended Changes:
- **Static Default Data**
  - Replace dynamic fallback generation with static JSON files
  - Include sample data in source control for development
  - Remove complex data generation scripts where simple static data would suffice

- **Centralize Configuration**
  - Move all site configuration to `/src/_data/site.js`
  - Eliminate scattered configuration files
  - Create a single source of truth for site metadata

- **Simplify Data Flow**
  - Reduce transformation steps between data sources and templates
  - Eliminate caching layers where not necessary
  - Document data flow clearly for maintainers

### Benefits:
- More predictable data availability during development
- Easier to understand how data flows through the system
- Reduced complexity in CI/CD pipeline

## 4. Template Structure Simplification

### Recommended Changes:
- **Extract Inline Code**
  - Move inline JavaScript to external files
  - Create reusable components for common patterns
  - Standardize template inheritance patterns

- **Simplify Includes**
  - Review and consolidate partial templates
  - Create a clear hierarchy of template components
  - Document component relationships

- **Standardize Layout Structure**
  - Reduce the number of layout variations
  - Create clearer boundaries between layout and content
  - Implement consistent block naming conventions

### Benefits:
- More maintainable templates
- Better separation of concerns
- Easier to understand the template hierarchy

## 5. CSS Simplification

### Recommended Changes:
- **Adopt Component-Based CSS**
  - Organize CSS into logical components
  - Remove global CSS where possible
  - Implement consistent naming conventions

- **Standardize Theme System**
  - Consolidate theme variables into a single source
  - Implement CSS custom properties consistently
  - Simplify theme switching mechanism

- **Optimize CSS Architecture**
  - Eliminate parallel optimization approaches
  - Choose a single methodology for CSS organization
  - Reduce CSS file size through better reuse

### Benefits:
- Faster page loads
- More maintainable styles
- Clearer relationship between components and styles

## 6. JavaScript Simplification

### Recommended Changes:
- **Module Organization**
  - Organize JavaScript into logical modules
  - Use ES modules consistently
  - Remove jQuery dependencies where possible

- **Reduce Runtime Complexity**
  - Simplify event handling
  - Remove unnecessary DOM manipulations
  - Focus on progressive enhancement

- **Standardize Interactive Elements**
  - Create a library of reusable interactive components
  - Document component APIs clearly
  - Ensure accessibility compliance

### Benefits:
- Faster JavaScript execution
- More maintainable code
- Improved user experience

## 7. Content Workflow Simplification

### Recommended Changes:
- **Streamline Post Creation**
  - Simplify frontmatter requirements
  - Create clearer templates for new content
  - Automate more of the post creation process

- **Standardize Media Handling**
  - Implement consistent image optimization
  - Simplify image reference patterns
  - Create clear guidelines for media usage

- **Simplify Post Processing**
  - Remove redundant validation steps
  - Create a single workflow for post creation
  - Implement better error handling and feedback

### Benefits:
- Easier content creation process
- More consistent content quality
- Reduced friction for contributors

## Implementation Timeline

### Phase 1: Analysis and Planning (1-2 weeks)
- Document current architecture in detail
- Identify critical vs. non-critical functionality
- Create detailed plan for each area

### Phase 2: Core Infrastructure (2-3 weeks)
- Implement directory structure changes
- Simplify build process
- Consolidate configuration

### Phase 3: Frontend Simplification (2-3 weeks)
- Implement CSS architecture changes
- Refactor JavaScript
- Create component library

### Phase 4: Content Workflow (1-2 weeks)
- Simplify post creation process
- Update documentation
- Create new examples and templates

### Phase 5: Testing and Optimization (1-2 weeks)
- Comprehensive testing of simplified system
- Performance optimization
- Documentation updates

## Measuring Success

The simplification effort should be measured by:

1. **Reduced Build Time**: Measure before and after build completion times
2. **Reduced Code Size**: Track reduction in lines of code and file count
3. **Simplified Navigation**: Survey developers on ease of finding files
4. **Maintenance Efficiency**: Track time required for common maintenance tasks
5. **Content Creation Speed**: Measure time needed to create and publish content