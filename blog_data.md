---
title: "Homelab Adventures: Scaling with Proxmox and ARM Devices"
date: "2024-09-14"
slug: "homelab-proxmox-arm"

Hey there, fellow tech enthusiasts! Today, I'm excited to share a deep dive into how I scaled my
homelab with [Proxmox](https://www.proxmox.com/en/) and some handy ARM devices (think
[Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)!). Buckle up; it's been quite the adventure!

<h2 id="why-scale-up"><a href="#why-scale-up">Why Scale Up?</a></h2>
Sometimes, a single machine just won't cut it. When I found myself juggling multiple services—
think Git servers, Docker registries, and even a small data analytics stack—I realized I needed
more horsepower. On top of that, I'd rather not burn my wallet (or blow a fuse) with full-sized
servers. So, the question was: **How can I expand cheaply yet reliably?**

<h2 id="proxmox-arm"><a href="#proxmox-arm">Enter Proxmox and ARM Devices</a></h2>
Proxmox is a flexible, open-source virtualization platform that’s easy to manage. Paired with
ARM-based boards (like the Pi 4 or [Odroid HC2](https://www.hardkernel.com/)), you get a swarm of
low-power nodes that can be clustered together.

<h3 id="challenges"><a href="#challenges">Challenges and How I Overcame Them</a></h3>
- **Networking Woes**: VLANs became my best friend for isolating traffic. Also, reading about
  [pfSense](https://www.pfsense.org/) for firewall rules was a lifesaver.
- **Storage Constraints**: MicroSD cards are notoriously fickle. I switched to USB/SSD for
  better performance and reliability.
- **ARM Architecture Roadblocks**: Some apps (particularly closed-source ones) had trouble with
  ARM builds. I ended up using [Docker manifests](https://docs.docker.com/engine/reference/commandline/manifest/)
  and cross-compiling on occasion.

<h3 id="worth-it"><a href="#worth-it">Was It Worth It?</a></h3>
Absolutely! My homelab is now a robust cluster. It sips electricity, and the Pi boards are
shockingly capable. I even run a small CI pipeline using [GitLab Runner on ARM](https://docs.gitlab.com/runner/install/arm.html).

<h3 id="resources"><a href="#resources">Resources</a></h3>
- [Installing Proxmox on Raspberry Pi](https://pimylifeup.com/raspberry-pi-proxmox/) — A great tutorial to get started.
- [r/homelab on Reddit](https://www.reddit.com/r/homelab/) — For project inspiration and troubleshooting.
- [pfSense Documentation](https://docs.netgate.com/pfsense/en/latest/) — If you want to level-up your network.

<h2 id="final-thoughts"><a href="#final-thoughts">Final Thoughts</a></h2>
If you're craving more than a basic NAS or single server can offer, give ARM boards + Proxmox
a try. It's like building your own mini data center—only smaller, quieter, and less expensive
to run. Plus, there's a unique thrill in seeing so many tiny boards accomplish so much together!

---
title: "Securing Container Deployments with Ansible"
date: "2024-10-20"
slug: "securing-containers-ansible"

Greetings, code wranglers! Ever pushed a container to production and thought, “Hmm, did I
lock down that Dockerfile?” I certainly have. Today, I'm sharing how I harness
[Ansible](https://www.ansible.com/) to keep container deployments safe and sane.

<h2 id="problem"><a href="#problem">The Problem with Manual Deployment</a></h2>
Manual deployment invites chaos. One missed config, and suddenly your container might be
listening on the wrong port—or worse, with elevated privileges. In security terms, manual steps
are an invitation for mistakes.

<h2 id="why-ansible"><a href="#why-ansible">Why Ansible?</a></h2>
Ansible is agentless (no extra daemons required), and it’s well-suited to orchestrating tasks
like container updates or firewall rule changes across multiple hosts. It's also easy to
combine with tools like [Molecule](https://molecule.readthedocs.io/) for testing.

<h3 id="playbook"><a href="#playbook">My Playbook to Success</a></h3>
```
- name: Deploy Secure Container
  hosts: container_hosts
  become: yes
  tasks:
    - name: Pull latest Docker image
      docker_image:
        name: my_secure_app
        source: pull

    - name: Run container with security options
      docker_container:
        name: secure_app
        image: my_secure_app
        security_opts:
          - no-new-privileges
        read_only: yes
        log_driver: json-file
        user: 1001:1001
        exposed_ports:
          - 8080
```

<h3 id="best-practices"><a href="#best-practices">Security Best Practices Implemented</a></h3>
- **Least Privilege**: The container runs as a non-root user, drastically reducing risk.
- **Immutable Containers**: Read-only file system stops unauthorized changes.
- **Regular Updates**: Using Ansible to pull fresh images helps you patch frequently.

<h3 id="ansible-resources"><a href="#ansible-resources">Useful Resources</a></h3>
- [Ansible Docs](https://docs.ansible.com/) — Official references for modules and best practices.
- [Docker Security](https://docs.docker.com/engine/security/) — A thorough guide to container security.
- [CIS Docker Benchmarks](https://www.cisecurity.org/benchmark/docker) — Great for a security checklist.

<h2 id="wrapping-up"><a href="#wrapping-up">Wrapping Up</a></h2>
If you want consistent, tested, and more secure deployments, try weaving Ansible into your
workflow. It's taken a huge load off my plate, letting me focus more on features and less on
“Wait, did I open that port by accident?”

---
title: "Docker vs Podman: A Quick Dive"
date: "2024-12-22"
slug: "docker-vs-podman"

Ahoy, container sailors! Today we’re comparing two container heavyweights:
[Docker](https://docs.docker.com/) and [Podman](https://podman.io/).

<h2 id="why-compare"><a href="#why-compare">Why Compare?</a></h2>
Docker is the classic container champion. Podman is the rising star known for its rootless
capabilities. Both run containers, but the architecture and security model differ. If you’re
deciding on container tooling, it pays to know the trade-offs.

<h3 id="rootless"><a href="#rootless">Podman: Rootless Containers</a></h3>
Podman was built from the ground up to run containers without requiring root privileges,
boosting security. Docker can do rootless too, but it’s not as straightforward.

<h3 id="differences"><a href="#differences">Key Differences</a></h3>
- **Daemons**: Docker uses a daemon, Podman doesn’t. With Podman, containers run as child
  processes of the shell.
- **Security**: Podman is often praised for rootless by default. Docker requires a separate
  setup for that scenario.
- **CLI Similarities**: Podman tries to mirror Docker's CLI so that many Docker commands just
  work with `podman` in place of `docker`.

<h2 id="choose"><a href="#choose">Which One to Choose?</a></h2>
Both are production-worthy. Docker has broader ecosystem support and historical momentum.
Podman is lighter and often chosen for security reasons in more locked-down environments.

<h2 id="docker-resources"><a href="#docker-resources">Resources</a></h2>
- [Docker Docs](https://docs.docker.com/) — The official reference to Docker’s entire ecosystem.
- [Podman Getting Started](https://podman.io/getting-started/) — Learn how to run containers
  without root.

<h3 id="fun-future"><a href="#fun-future">Fun Future Ideas</a></h3>
- **Kubernetes vs Nomad**: Another big scheduling debate.
- **Rootless All the Things**: Testing advanced scenarios with user namespaces.
- **Try Our** [Pizza Calculator](pizza.html) if your container build has you hungry!

---
title: "Feeding the Debuggers: The Pizza Calculator Story"
date: "2024-12-23"
slug: "feeding-debuggers-pizza"

Hey there, pizza lovers! Late-night debugging sessions can be rough, especially if half the
team is running on fumes by 2 AM. That’s where my **Pizza Calculator** swoops in to save the
night (and your stomach).

<h2 id="why-pizza"><a href="#why-pizza">Why a Pizza Calculator?</a></h2>
Picture this: a critical production outage at midnight, 10 devs on Zoom calls, and minimal
sleep. Will a single pepperoni pie suffice? Or do you need an entire orchard of pies? My
Pizza Calculator factors in **hours spent debugging**, **number of attendees**, and even
**pizza style** (NY, Chicago, or “Cloud Pizza” if you want infinite slices).

<h3 id="how-it-works"><a href="#how-it-works">How It Works</a></h3>
- **Attendees**: Just the number of hungry devs.
- **Pizza Style**: Because a deep-dish Chicago is heavier than a standard NY slice.
- **Debugging Hours**: The longer the session, the more slices we devour.
- **Hot Pockets**: In a pinch? They’re quick... but questionable.

<h3 id="lessons-learned"><a href="#lessons-learned">Lessons Learned</a></h3>
- **Load Balancing Slices**: Even distribution matters—nobody wants to be left with
  just crust.
- **Cost vs. Quantity**: “Cloud Pizza” is infinite but watch out for that billing model, akin
  to surprise cloud bills.
- **Blockchain Pizza**: The slice “value” can fluctuate, so watch out for the next crash.

Check out the [Pizza Calculator](pizza.html) and keep your dev team well-fed during the
next big fix!
