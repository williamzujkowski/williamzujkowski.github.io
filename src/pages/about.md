---
title: "About"
layout: page
permalink: /about/
description: "About William Zujkowski — security architecture, identity, and compliance."
eleventyNavigation:
  key: About
  order: 2
---

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

# About William Zujkowski

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
I'm a Senior Security Engineer at Cloud.gov (yes, part of GSA TTS—the folks who help make government tech not terrible). I spend my days designing firewalls, federation systems, and compliance controls for a FedRAMP Moderate platform serving 40+ federal agencies. But I also spend way too many nights in my homelab breaking things to understand how they work.
</p>

Right now, I'm a GS-15 Individual Contributor at Cloud.gov, which means I get to focus on actual engineering work instead of endless meetings. My days involve designing web application firewalls (Palo Alto Prisma Cloud), building network microsegmentation with Cloud Foundry, wrestling with PIV authentication and SAML/OIDC flows for Login.gov integration, and trying to keep our FedRAMP compliance documentation from making people's eyes glaze over. I also govern security tooling across CI/CD pipelines—basically making sure our 100+ application teams can deploy safely without tripping over security scanners.

---

## The Journey

<div class="bg-gradient-to-br from-primary-50 to-indigo-50 dark:from-gray-800/50 dark:to-primary-900/20 p-8 rounded-2xl my-8 shadow-sm border border-primary-100/50 dark:border-primary-800/30">

My path to federal cloud security started in 2005 with an independent IT consulting practice. And by "consulting practice," I mean I fixed broken computers and networks for anyone who'd hire me—small businesses, local offices, whoever needed help and could pay my hourly rate. I vividly remember spending 12 hours at a client's office around 2007 because I fat-fingered a DNS entry and took down their entire email system. Bought pizza for the whole team. Learned to always, *always* double-check before hitting Enter.

Over five years (2005-2010), that evolved from "my computer won't start" house calls into enterprise IT support, then a lucky break into security engineering at the **National Institutes of Health (NIH)** in 2010. I spent over a decade there, working at both the NIH Office of the CIO and the National Human Genome Research Institute, where I discovered I really loved security—especially when it enabled scientists to do their research faster, not slower.

At NIH, I led vulnerability management for the entire enterprise—about **100,000+ assets** spread across **27 Institutes and Centers**. The hardest part wasn't the tech. It was convincing 27 different IT teams to move at the same speed. I spent years learning that security controls only work if people actually use them, which means you have to make the secure path the easy path.

I served as Security Engineering Lead at NHGRI (2018-2021), securing research infrastructure for about **2,200 endpoints**—including million-dollar genomic sequencers that scientists would absolutely revolt over if you tried to patch them during a sequencing run. That taught me more about stakeholder management than any textbook ever could.

After that, I spent time as a Lead HPC Site Reliability Engineer (2023), supporting high-performance computing clusters for biomedical research. Bridging infrastructure, automation, and research workloads taught me that uptime matters just as much as security when people are running week-long molecular dynamics simulations.

Eventually, all of that experience brought me to **Cloud.gov**, where I now help secure a FedRAMP Moderate platform serving 40+ federal agencies. It turns out 20 years of breaking things and learning how to fix them is pretty good preparation for designing secure cloud infrastructure.

</div>

---

## What I Do Now

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8">

  <div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-xl shadow-sm border border-blue-200/50 dark:border-blue-800/30">
    <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
      <svg class="w-6 h-6 mr-2 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
      </svg>
      Cloud Security Architecture
    </h3>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      Design and operate network controls for a multi-tenant FedRAMP Moderate platform—managing Palo Alto Prisma Cloud WAFs, Cloud Foundry network policies for microsegmentation, and Terraform-based automation. Spent months learning Terraform just to avoid clicking through the AWS console for firewall rules. Best decision ever.
    </p>
  </div>

  <div class="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-xl shadow-sm border border-purple-200/50 dark:border-purple-800/30">
    <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
      <svg class="w-6 h-6 mr-2 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
      </svg>
      Identity & Federation
    </h3>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      Implement and maintain PIV-based authentication, SAML/OIDC integrations using UAA (User Account and Authentication), and Login.gov federation for 40+ agency customers. Identity is one of those things nobody notices when it works and everyone notices when it breaks—usually at 3am.
    </p>
  </div>

  <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-xl shadow-sm border border-green-200/50 dark:border-green-800/30">
    <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
      <svg class="w-6 h-6 mr-2 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
      </svg>
      Security Tooling Governance
    </h3>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      Oversee CI/CD vulnerability scanning (using tools like Grype and OSV), repository/IaC scanning, VM scanning with Nessus, and web application security scanning across platform infrastructure. My job is to make sure 100+ app teams can ship code without accidentally deploying CVE-2024-YIKES.
    </p>
  </div>

  <div class="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 p-6 rounded-xl shadow-sm border border-red-200/50 dark:border-red-800/30">
    <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center">
      <svg class="w-6 h-6 mr-2 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      Compliance & Standards
    </h3>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      Key SME for NIST 800-53 Revision 4 → Revision 5 migration (which was basically rewriting every control narrative to map old requirements to new families). I contribute to our FedRAMP annual assessments and write RFC commentary because someone has to read the fine print.
    </p>
  </div>

</div>

---

## Selected Prior Impact

<div class="space-y-6 my-8">

<div class="bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 p-6 rounded-lg border-l-4 border-yellow-400">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2 flex items-center">
    <span class="text-2xl mr-3">🔥</span>
    NIH Log4j Response (2021)
  </h3>
  <p class="text-gray-700 dark:text-gray-300">
    I was designated NIH OCIO's Log4j subject matter expert basically overnight when Log4Shell dropped. Spent 72 hours straight coordinating vulnerability scans across 100,000+ assets, living on coffee and adrenaline. Built relationships with every Institute and Center IT team that still help me today. Also learned that you can survive on gas station sandwiches longer than you'd think.
  </p>
</div>

<div class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-lg border-l-4 border-blue-400">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2 flex items-center">
    <span class="text-2xl mr-3">🏛️</span>
    CISA BOD 22-01 Adoption (2021-2022)
  </h3>
  <p class="text-gray-700 dark:text-gray-300">
    Led NIH's adoption of CISA Binding Operational Directive 22-01 (reducing the known exploited vulnerabilities remediation timeline), coordinating response across all 27 NIH Institutes and Centers. The hardest part wasn't the tech—it was convincing 27 different IT teams to move at the same speed. Learned more about stakeholder management and compromise in those 6 months than in the previous decade. Also learned to always schedule meetings after lunch when people are less cranky.
  </p>
</div>

<div class="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg border-l-4 border-purple-400">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2 flex items-center">
    <span class="text-2xl mr-3">🧬</span>
    NHGRI Research Infrastructure Security (2018-2021)
  </h3>
  <p class="text-gray-700 dark:text-gray-300">
    Secured research infrastructure supporting about 2,200 endpoints—including million-dollar genomic sequencers and electron microscopes that scientists would absolutely revolt over if you tried to patch them mid-experiment. Learned that researchers don't care about security until you explain how it protects their grant-funded experiments and data. Also learned to never, ever interrupt a week-long genome sequencing run. The hard way.
  </p>
</div>

<div class="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg border-l-4 border-green-400">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2 flex items-center">
    <span class="text-2xl mr-3">⚡</span>
    HPC Enablement (2023)
  </h3>
  <p class="text-gray-700 dark:text-gray-300">
    Implemented automation and resilience for high-performance computing clusters supporting molecular dynamics and computational biology research. Learned that uptime matters just as much as security when researchers are running week-long simulations that cost thousands of dollars in compute time. Also learned that "the cluster is down" emails at 2am are surprisingly motivating.
  </p>
</div>

</div>

---

## How I Think About Security

<div class="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-indigo-900/20 dark:via-purple-900/20 dark:to-pink-900/20 p-10 rounded-2xl shadow-md my-12 border border-purple-200/50 dark:border-purple-800/30">

<p class="text-lg text-gray-700 dark:text-gray-300 mb-6">
I believe security should <strong>enable work, not block it</strong>. The best controls? Users never notice them because they just work. Nobody cares about your perfect firewall rules if they can't deploy their app.
</p>

<p class="text-lg text-gray-700 dark:text-gray-300 mb-6">
Here's what I've learned over 20 years in IT and 15 years in security:
</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
  <div class="bg-white/70 dark:bg-gray-800/30 p-6 rounded-xl">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
      <svg class="w-5 h-5 mr-2 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
      Technical Excellence Is Not Enough
    </h4>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      You can design the most elegant network segmentation in the world, but if developers can't deploy their code, they'll find a workaround. Your job is to make the secure path the easy path. I learned this the hard way trying to enforce patching schedules on scientists running week-long experiments.
    </p>
  </div>

  <div class="bg-white/70 dark:bg-gray-800/30 p-6 rounded-xl">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
      <svg class="w-5 h-5 mr-2 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      Compliance Frameworks Are Forcing Functions
    </h4>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      NIST 800-53 and FedRAMP aren't checkbox exercises. They're forcing functions that make you think about threat models, blast radius, and recovery time objectives. I've spent enough time implementing controls to know: compliance done right makes you more secure. Compliance done wrong makes you miserable.
    </p>
  </div>

  <div class="bg-white/70 dark:bg-gray-800/30 p-6 rounded-xl">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
      <svg class="w-5 h-5 mr-2 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
      </svg>
      Automation Isn't About Replacing People
    </h4>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      It's about freeing them to do interesting work instead of clicking buttons. I spent months learning Terraform so our team could manage firewall rules as code instead of logging into consoles. Best investment I've made. Now we spend time on architecture problems, not typos.
    </p>
  </div>

  <div class="bg-white/70 dark:bg-gray-800/30 p-6 rounded-xl">
    <h4 class="font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
      <svg class="w-5 h-5 mr-2 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
      AI Security Is About Governance, Not Just Tech
    </h4>
    <p class="text-sm text-gray-700 dark:text-gray-300">
      I'm exploring how we build and secure AI systems that augment human decision-making rather than replace it. The hard problems aren't the models—they're the humans, policies, and processes around them. Just like every other security problem I've worked on.
    </p>
  </div>
</div>

<p class="text-base text-gray-700 dark:text-gray-300 italic">
If security slows teams down, they'll work around it. If compliance feels like busywork, it won't get done right. If automation is brittle, nobody will trust it. I've been doing this long enough to know: good security is invisible until you need it.
</p>

</div>

---

## Connect

<div class="bg-gradient-to-br from-green-50 via-teal-50 to-emerald-50 dark:from-green-900/20 dark:via-teal-900/20 dark:to-emerald-900/20 p-10 rounded-2xl shadow-lg my-12 border border-green-200/50 dark:border-green-800/30">

<p class="text-xl text-gray-700 dark:text-gray-300 mb-8 text-center leading-relaxed">
I love connecting with folks who geek out about cloud security, identity federation, compliance automation, or AI infrastructure security. Whether you're building something cool, stuck on a problem, or just want to talk shop about homelab setups, feel free to reach out.
</p>

<div class="grid grid-cols-1 md:grid-cols-4 gap-6">

  <div class="group bg-white dark:bg-gray-800/70 p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 text-center">
    <div class="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-800 dark:to-blue-900 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
      <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
      </svg>
    </div>
    <h4 class="text-sm font-bold text-gray-900 dark:text-gray-100 mb-2">Cloud Security</h4>
    <p class="text-xs text-gray-600 dark:text-gray-400">Architecture & FedRAMP</p>
  </div>

  <div class="group bg-white dark:bg-gray-800/70 p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 text-center">
    <div class="w-16 h-16 bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-800 dark:to-purple-900 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
      <svg class="w-8 h-8 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
      </svg>
    </div>
    <h4 class="text-sm font-bold text-gray-900 dark:text-gray-100 mb-2">Identity & Federation</h4>
    <p class="text-xs text-gray-600 dark:text-gray-400">At Scale</p>
  </div>

  <div class="group bg-white dark:bg-gray-800/70 p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 text-center">
    <div class="w-16 h-16 bg-gradient-to-br from-red-100 to-red-200 dark:from-red-800 dark:to-red-900 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
      <svg class="w-8 h-8 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    </div>
    <h4 class="text-sm font-bold text-gray-900 dark:text-gray-100 mb-2">Compliance</h4>
    <p class="text-xs text-gray-600 dark:text-gray-400">NIST 800-53 Automation</p>
  </div>

  <div class="group bg-white dark:bg-gray-800/70 p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 text-center">
    <div class="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 dark:from-green-800 dark:to-green-900 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
      <svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    </div>
    <h4 class="text-sm font-bold text-gray-900 dark:text-gray-100 mb-2">AI Security</h4>
    <p class="text-xs text-gray-600 dark:text-gray-400">Infrastructure & Governance</p>
  </div>

</div>

<div class="flex justify-center gap-6 mt-8">
  <a href="https://github.com/williamzujkowski"
     class="inline-flex items-center justify-center px-8 py-4 bg-gray-800 text-white rounded-xl hover:bg-gray-700 transition-all duration-200 shadow-md hover:shadow-lg min-h-[64px]"
     aria-label="Visit my GitHub profile">
    <svg class="w-6 h-6 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
    <span class="font-medium text-white">GitHub</span>
  </a>

  <a href="https://www.linkedin.com/in/williamzujkowski"
     class="inline-flex items-center justify-center px-8 py-4 bg-blue-700 text-white rounded-xl hover:bg-blue-800 transition-all duration-200 shadow-md hover:shadow-lg min-h-[64px]"
     aria-label="Visit my LinkedIn profile">
    <svg class="w-6 h-6 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
    </svg>
    <span class="font-medium text-white">LinkedIn</span>
  </a>
</div>

</div>

---

## When I'm Not Working

<div class="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-8 rounded-xl my-8">
  <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
    You'll find me in my homelab, which has grown from a single Raspberry Pi in 2015 to a Dell PowerEdge R940 running Proxmox, a fleet of Raspberry Pi 4s handling K3s clusters, and way too many Docker containers. I run my own Wazuh SIEM, self-hosted Bitwarden, and whatever else I'm experimenting with that week.
  </p>

  <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
    I'm also deep into AI/LLM experimentation—not just using ChatGPT, but actually running local models, building agents, and figuring out how to secure these systems in production environments. It's fascinating and terrifying in equal measure.
  </p>

  <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
    <strong>Fair warning:</strong> I've accidentally fried a $400 GPU overclocking it to squeeze out more performance for a local LLM. RIP. Also managed to take down my entire home network for 6 hours trying to implement VLAN segmentation "just to see how it works." My partner was not amused when Netflix stopped working during their favorite show.
  </p>

  <p class="text-lg text-gray-700 dark:text-gray-300 mb-4">
    I'm currently learning Rust by building a vulnerability aggregation tool that I'll probably never finish. But that's the point—curiosity is the best cybersecurity skill there is, and breaking things in my homelab means I don't break them in production.
  </p>

  <p class="text-lg text-gray-700 dark:text-gray-300 italic">
    Favorite debugging method: rubber duck debugging with my actual pet duck. His name is Quackers. He's a surprisingly good listener.
  </p>
</div>

</div>
