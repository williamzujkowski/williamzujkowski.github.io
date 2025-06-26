---
layout: page
title: Tags
description: Browse all tags and topics covered in my blog posts
permalink: /tags/
eleventyNavigation:
  key: Tags
  parent: Posts
  order: 2
---

# Browse by Tag

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none mb-8">
  <p class="text-gray-600 dark:text-gray-400">
    Explore blog posts organized by topic. Click any tag to see related content.
  </p>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {%- for tag in collections.tagList %}
  {%- set tagCount = collections[tag].length %}
  <a href="/tags/{{ tag | slugify }}/" class="group block p-6 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200 hover:shadow-md">
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400">
        {{ tag }}
      </h3>
      <span class="inline-flex items-center justify-center w-8 h-8 text-sm font-medium text-gray-600 dark:text-gray-400 bg-gray-200 dark:bg-gray-700 rounded-full">
        {{ tagCount }}
      </span>
    </div>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      {%- if tag == "security" %}
        Security engineering, best practices, and tools
      {%- elif tag == "ai" or tag == "ai-ml" or tag == "machine-learning" %}
        Artificial intelligence and machine learning
      {%- elif tag == "homelab" %}
        Home lab setup and experiments
      {%- elif tag == "career" %}
        Career development and professional growth
      {%- elif tag == "python" %}
        Python programming and automation
      {%- elif tag == "automation" %}
        Automation tools and workflows
      {%- elif tag == "networking" %}
        Network engineering and protocols
      {%- elif tag == "linux" %}
        Linux systems and administration
      {%- elif tag == "privacy" %}
        Privacy tools and best practices
      {%- elif tag == "tutorial" %}
        Step-by-step guides and tutorials
      {%- elif tag == "open-source" %}
        Open source projects and contributions
      {%- elif tag == "incident-response" %}
        Incident response and forensics
      {%- else %}
        Posts about {{ tag }}
      {%- endif %}
    </p>
  </a>
  {%- endfor %}
</div>

<div class="mt-12 p-6 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
  <h2 class="text-xl font-semibold mb-2">Looking for something specific?</h2>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    You can also browse all <a href="/posts/" class="text-primary-600 dark:text-primary-400 hover:underline">blog posts</a> chronologically or use the search feature on the posts page.
  </p>
</div>