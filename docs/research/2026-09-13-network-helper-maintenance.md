# Network helper maintenance — September 13, 2026

Scoped repairs for [#622](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/622) and [#624](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/624). This record covers dependency inspection and archived DoH helper notices, not a full review of the February article or a new lab experiment.

## Canonical artifact inspection

Read every file in the seven February-post gists and five removed DoH gists through the GitHub API. Every file reported `truncated: false`. The pre-edit `python3 scripts/gist-drift-check.py --quiet` completed with **45 mapped gists checked, 45 in sync, zero problems**. No matching mirrors for these twelve gists were found under `gists/`; no mirror files were changed.

All twelve gists were created November 3, 2025. These dates establish when the gists appeared, not when underlying code was first written. They neither substantiate earlier experiment claims nor prove those claims fabricated. Preserve original revisions and distinguish the current correction from the original article dates.

| Original revision | Created UTC | Original file SHA-256 |
| --- | --- | --- |
| [2abad62ff98d044d09102ae06ecf3b0f](https://gist.github.com/williamzujkowski/2abad62ff98d044d09102ae06ecf3b0f/0b1b7e6e48e1d7ee045f9c4ac2aca7ad2a30ce6d) | 2025-11-03T02:06:51Z | `network-device-discovery.py`: `1e0d17e90f278f6c4b56a333d93aab495033abc60d3c70fae2f239b2ea46b379` |
| [365d9b3a0dc812e93ec8177e5bf84922](https://gist.github.com/williamzujkowski/365d9b3a0dc812e93ec8177e5bf84922/1b272a785893eecc084bd917dc1b3f14b105376e) | 2025-11-03T22:49:49Z | `doh-troubleshooting.sh`: `bed572a83cdc6a579a0cff121893fe813212d3ccd02d9d8a94f818632530ea34` |
| [48bd7c6e1d18e0d12cfcad67ff4a644c](https://gist.github.com/williamzujkowski/48bd7c6e1d18e0d12cfcad67ff4a644c/9a9e98ec436c2a6b60f0c5cb89f28deeb7c01446) | 2025-11-03T22:49:48Z | `doh-cert-pinning.py`: `27a59753f5939e8bac925a72b1b230f4e3729b94623350c22017b9feb3366b0e`; `doh-firewall-rules.sh`: `8461a2c64b722357966f72fc7c921753737f8a397696dc0e3e44d17920e91d22` |
| [6af94c70d3afd57829d26c12940d1cb1](https://gist.github.com/williamzujkowski/6af94c70d3afd57829d26c12940d1cb1/2a6dc0c2efca0bf3ed0194a67a7a015614496657) | 2025-11-03T02:06:54Z | `dynamic-firewall.py`: `7ed107b2f89304f95255befafd00133e2ae7dd6ca2f5958b3e6f74113d0c4ef8` |
| [6c7c754be164e75b84f6b9e601753531](https://gist.github.com/williamzujkowski/6c7c754be164e75b84f6b9e601753531/f136395de68f72943521fd1de8372d54f21f3908) | 2025-11-03T02:06:52Z | `dns-monitoring.py`: `862fbde85dd0e88080b430aece7db6f4a2185ba8848e8e5a6b4a11110401891c` |
| [7bb056a1b487f9fc2e4a61f9a76ab8a4](https://gist.github.com/williamzujkowski/7bb056a1b487f9fc2e4a61f9a76ab8a4/a7c142f8a727b807994995c97452c7463b85f943) | 2025-11-03T02:06:51Z | `network-security-requirements.txt`: `92d97005a87766d4f88a1c2a2f777e86e59821c8352253608194f39b0c5f6e0e` |
| [82e4d29a006b6fc5b20b881760d6deb9](https://gist.github.com/williamzujkowski/82e4d29a006b6fc5b20b881760d6deb9/c4cf3f103507fd7538b68622d7709dde63fb7612) | 2025-11-03T22:49:47Z | `doh-monitoring-tools.py`: `10a191d0e13e7549a4c338582e5f67887dac9374d380c212868d9820a9686d97` |
| [8749d27f31c0c222e79033fc978069bd](https://gist.github.com/williamzujkowski/8749d27f31c0c222e79033fc978069bd/6d200bff175849dc5490600bbaa6a5cd2a4aa289) | 2025-11-03T22:49:50Z | `doh-geo-selector.py`: `92da58ed97bf9708c8f07f8f10ddb17f5e8b4f02c19da4c9ab444d902d7eb0ac`; `doh-load-balancing.conf`: `a91827b9d2b6d6989d234ecff97a9bc77dca5f31ff0c03b3257dcb3984526fe2` |
| [9ca841f8bdea7bced7c797ee2cfa5597](https://gist.github.com/williamzujkowski/9ca841f8bdea7bced7c797ee2cfa5597/837e2a2594283c1d31921693bb961ed4621c4a57) | 2025-11-03T22:49:46Z | `doh-router-setup.sh`: `bd2115930a99b7b162cde9a0e284a773b7ca26e1829d956b8a1be9feb1c66dbc` |
| [9cc496653878271d7045108bead98a65](https://gist.github.com/williamzujkowski/9cc496653878271d7045108bead98a65/035adaca15e92f993b98f0d8a927639fc6aeec90) | 2025-11-03T02:06:57Z | `security-orchestrator.py`: `007ffd6cfef18fb1f445d4ff2bea7a8933b35944f55160528bf5eee3ca4f089e` |
| [e3e41c782e4099a06a6ac1f482cd3119](https://gist.github.com/williamzujkowski/e3e41c782e4099a06a6ac1f482cd3119/cd37a5b739a41eb28837c6e3da3e1ba324e70225) | 2025-11-03T02:06:53Z | `vulnerability-scanner.py`: `989ea88b8a0face6b1b3836b6b2d17db603fcc016b6cdf27f4e313491402cceb` |
| [f025bd03e6d265b8aa9fdb8d73df9740](https://gist.github.com/williamzujkowski/f025bd03e6d265b8aa9fdb8d73df9740/1450fff2a104cabe73877f0c385ec9c6673a9aea) | 2025-11-03T02:06:55Z | `notification-system.py`: `a864e2ae67fe57041988cd7fcae09d0753f8e83c6e8152f4421771281b588ec8` |

## Dependency correction

The canonical requirements file contained six Python standard-library names, `nmap`, `requests`, and `vulners`. Device discovery and vulnerability scanning import `nmap`; notification imports `requests`; vulnerability scanning imports `vulners`. No inspected fragment imports `schedule`. The orchestrator omits its implementation and cannot establish missing dependencies by inference.

- [Python 3.11 library documentation](https://docs.python.org/3.11/library/index.html) lists `collections`, `email`, `ipaddress`, `smtplib`, `sqlite3`, and `subprocess` as standard-library modules.
- [python-nmap 0.7.1](https://pypi.org/project/python-nmap/0.7.1/) documents installation as `python-nmap` and import as `nmap`. [Nmap's installation reference](https://nmap.org/book/install.html) covers the separate executable and `PATH` requirement.
- [Requests 2.34.2](https://pypi.org/project/requests/2.34.2/) and [Vulners 4.3.0](https://pypi.org/project/vulners/4.3.0/) identify the other two installed distributions.

All linked implementation fragments contain omissions; several have invalid indentation or an out-of-function return. Correcting imports does not make them deployable. This change explicitly limits the Requirements section and tracks their specific syntax and missing-symbol defects separately in [#628](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/628), outside #622's dependency-only scope.

## Clean installation check

A new disposable virtual environment used CPython **3.11.12**. Commands executed:

```sh
uv venv --python 3.11 /tmp/blog-maintenance-evidence-20260913/venv
uv pip install --python /tmp/blog-maintenance-evidence-20260913/venv/bin/python python-nmap requests vulners
uv pip check --python /tmp/blog-maintenance-evidence-20260913/venv/bin/python
```

The installer resolved 27 packages, and its compatibility check passed for all 27. A Python process imported the six standard-library modules plus `nmap`, `requests`, and `vulners`; `importlib.metadata.version` reported `python-nmap==0.7.1`, `requests==2.34.2`, and `vulners==4.3.0`. The import check replaced `socket.create_connection` with a raising function as an additional guard; it was not a network sandbox. No scanner was constructed, and no scan, API request, firewall change, or notification was invoked. Network access was used for package acquisition and primary-source/GitHub reads only.

The command in the article uses standard `venv` and pip; this validation used uv's venv/install interface. The package names and Python import behavior were checked, not every distribution's platform-specific `venv` packaging. These current versions do not reconstruct a February 2025 environment. The unpinned requirements identify imports and are not a lockfile.

Resolved environment:

```text
annotated-types==0.8.0
anyio==4.15.1
brotli==1.2.0
certifi==2026.7.22
charset-normalizer==3.5.1
h11==0.16.0
h2==4.4.1
hpack==4.2.0
httpcore==1.0.9
httpx==0.28.1
hyperframe==6.1.0
idna==3.19
ijson==3.5.1
isal==1.8.0
orjson==3.12.0
pycryptodome==3.23.0
pydantic==2.13.5
pydantic-core==2.46.5
python-nmap==0.7.1
requests==2.34.2
stream-inflate==0.0.43
stream-unzip==0.0.101
typing-extensions==4.16.0
typing-inspection==0.4.4
urllib3==2.7.0
vulners==4.3.0
zstandard==0.25.0

```

## DoH archival notices

Each of the five removed helpers receives an `ARCHIVED / UNSUPPORTED` description and a README dated September 13, 2026. The notice links the [corrected DoH article](https://williamzujkowski.github.io/posts/2025-07-08-implementing-dns-over-https-home-networks/), identifies its concrete limitation, and preserves every original file:

| Helper | Observed limitation |
| --- | --- |
| Router setup | Mixed platform commands and omitted proxy configuration. |
| Monitoring | Undefined benchmark functions/inputs and omitted log analysis. |
| Hardening | Python return outside a function; local IPv4 OUTPUT rules do not enforce network-wide DoH. |
| Troubleshooting | Configuration overwrite and plaintext downgrade selected by a hostname ping. |
| Advanced routing | Undefined geographic helper and incomplete nginx request/TLS configuration. |

The supervising reviewer approved all six exact patches before publication. Each update was followed by a fresh GitHub API read. Descriptions and README/requirements content matched the approved patch exactly. All seven original code/configuration files across the five DoH gists remained byte-identical to the SHA-256 inventory above. The corrected DoH article returned HTTP 200 with its September 13 correction present.

| Updated gist | Verified revision | Original files preserved |
| --- | --- | --- |
| [365d9b3a0dc812e93ec8177e5bf84922](https://gist.github.com/williamzujkowski/365d9b3a0dc812e93ec8177e5bf84922/b49ac6d7bd217006072d96f8078601e87802ccec) | `b49ac6d7bd217006072d96f8078601e87802ccec` | doh-troubleshooting.sh |
| [48bd7c6e1d18e0d12cfcad67ff4a644c](https://gist.github.com/williamzujkowski/48bd7c6e1d18e0d12cfcad67ff4a644c/94133bca6e8e8ee175d1e1ce9229df1f937a56ec) | `94133bca6e8e8ee175d1e1ce9229df1f937a56ec` | doh-cert-pinning.py, doh-firewall-rules.sh |
| [7bb056a1b487f9fc2e4a61f9a76ab8a4](https://gist.github.com/williamzujkowski/7bb056a1b487f9fc2e4a61f9a76ab8a4/d4bbf96fdaad4ee530a88c3e51686e869158c8b7) | `d4bbf96fdaad4ee530a88c3e51686e869158c8b7` | Requirements file intentionally corrected; original revision retained above |
| [82e4d29a006b6fc5b20b881760d6deb9](https://gist.github.com/williamzujkowski/82e4d29a006b6fc5b20b881760d6deb9/954e9edf90e365d096f6f8f16f6a82980812b665) | `954e9edf90e365d096f6f8f16f6a82980812b665` | doh-monitoring-tools.py |
| [8749d27f31c0c222e79033fc978069bd](https://gist.github.com/williamzujkowski/8749d27f31c0c222e79033fc978069bd/55c15fdff1d3baa90559bca215201255c19a9c3a) | `55c15fdff1d3baa90559bca215201255c19a9c3a` | doh-geo-selector.py, doh-load-balancing.conf |
| [9ca841f8bdea7bced7c797ee2cfa5597](https://gist.github.com/williamzujkowski/9ca841f8bdea7bced7c797ee2cfa5597/1d544066a28ebea70ca7c97cc84d601cda5181bb) | `1d544066a28ebea70ca7c97cc84d601cda5181bb` | doh-router-setup.sh |

## Review coverage

Canonical `blog-artifact-check` procedure applied to this maintenance scope: source inventory, dates, distribution/import identity, prerequisite boundary and direct inspection of missing implementations. The dependency correction passes its bounded install/import check. The archived fragments remain unsupported; no full article publication-ready verdict is claimed. No new visual or broad prose changes are involved.

## Website validation

The production build passed. The offline internal-link check inspected 216 pages, 8,511 links and 2,507 anchors; all internal links and anchors resolved. Rendered HTML contains the dated correction, virtual-environment installation command and incomplete-fragment qualification; the invalid original command is absent. A first text-extraction assertion inserted spaces between syntax-highlighting spans and was corrected to normalize the actual rendered text. No content defect was found in that check.

## Follow-up: archive the six February implementation fragments (#628)

The #622 import correction exposed a second, concrete problem: section-local link labels still presented incomplete fragments as working automation. This follow-up reads every canonical file again, adds precise archival README/description notices, and changes the article's nearby claims to intended roles and observed limitations. It does not replace missing implementations or run the scripts.

Fresh reads reported no truncated files and matched the earlier revisions. Python `compile(source, filename, 'exec')` produced a code object or syntax error without executing the object. Five files failed syntax checks. The sixth parses, but source inspection places `self.update_pf_blocker_list(country_code)` inside the class body with those names and method undefined.

| Original file/revision | Compile-only result and inspected limitation | Original SHA-256 |
| --- | --- | --- |
| [network-device-discovery.py](https://gist.github.com/williamzujkowski/2abad62ff98d044d09102ae06ecf3b0f/0b1b7e6e48e1d7ee045f9c4ac2aca7ad2a30ce6d) | `unexpected indent`, line 7. | `1e0d17e90f278f6c4b56a333d93aab495033abc60d3c70fae2f239b2ea46b379` |
| [dynamic-firewall.py](https://gist.github.com/williamzujkowski/6af94c70d3afd57829d26c12940d1cb1/2a6dc0c2efca0bf3ed0194a67a7a015614496657) | Parses; undefined class-body names and method remain (source inspection). | `7ed107b2f89304f95255befafd00133e2ae7dd6ca2f5958b3e6f74113d0c4ef8` |
| [dns-monitoring.py](https://gist.github.com/williamzujkowski/6c7c754be164e75b84f6b9e601753531/f136395de68f72943521fd1de8372d54f21f3908) | `unexpected indent`, line 8. | `862fbde85dd0e88080b430aece7db6f4a2185ba8848e8e5a6b4a11110401891c` |
| [security-orchestrator.py](https://gist.github.com/williamzujkowski/9cc496653878271d7045108bead98a65/035adaca15e92f993b98f0d8a927639fc6aeec90) | `unexpected indent`, line 7. | `007ffd6cfef18fb1f445d4ff2bea7a8933b35944f55160528bf5eee3ca4f089e` |
| [vulnerability-scanner.py](https://gist.github.com/williamzujkowski/e3e41c782e4099a06a6ac1f482cd3119/cd37a5b739a41eb28837c6e3da3e1ba324e70225) | `unexpected indent`, line 8. | `989ea88b8a0face6b1b3836b6b2d17db603fcc016b6cdf27f4e313491402cceb` |
| [notification-system.py](https://gist.github.com/williamzujkowski/f025bd03e6d265b8aa9fdb8d73df9740/1450fff2a104cabe73877f0c385ec9c6673a9aea) | `unexpected indent`, line 8. | `a864e2ae67fe57041988cd7fcae09d0753f8e83c6e8152f4421771281b588ec8` |

The article now labels all six links as archived, incomplete and unsupported. It removes claims that these specific files run hourly/weekly, deliver alerts or implement firewall/orchestration behavior. The metadata no longer promises deployable Ansible/patching examples. The previously verified dependency environment remains an optional import-inspection example, with no claim that installation repairs the archived files. The household features are framed as design requirements rather than implemented features of these fragments.

Original author anecdotes and other unrelated historical statements were not evaluated by this artifact-only repair. Their retention is not independent verification. The original gist creation dates remain November 3, 2025; no inference about when underlying code was first written is added. No new implementation, experiment or measurement is supplied.

The supervising reviewer approved all six exact README/description patches. The second pre-edit drift check again passed **45/45 mapped gists**; none of these six has a local mirror. After publication, fresh API reads matched every approved description and README exactly and confirmed all six original Python files byte-identical. The first immediate read after one update temporarily omitted the new README; a later read showed the complete update. No success was recorded until the contents matched, and that gist was not patched a second time. The linked article returned HTTP 200 with its already-published September 13 dependency correction.

| Archived gist | Verified revision |
| --- | --- |
| [2abad62ff98d044d09102ae06ecf3b0f](https://gist.github.com/williamzujkowski/2abad62ff98d044d09102ae06ecf3b0f/12e2d01136a0b3e2588df5e5ed26391d868407e8) | `12e2d01136a0b3e2588df5e5ed26391d868407e8` |
| [6af94c70d3afd57829d26c12940d1cb1](https://gist.github.com/williamzujkowski/6af94c70d3afd57829d26c12940d1cb1/87a972beced22a1bb0a89c73953384d60c5977c6) | `87a972beced22a1bb0a89c73953384d60c5977c6` |
| [6c7c754be164e75b84f6b9e601753531](https://gist.github.com/williamzujkowski/6c7c754be164e75b84f6b9e601753531/aaa3da3410fea68ebc8e70b6109413e1275b4e24) | `aaa3da3410fea68ebc8e70b6109413e1275b4e24` |
| [9cc496653878271d7045108bead98a65](https://gist.github.com/williamzujkowski/9cc496653878271d7045108bead98a65/943b4f39c2bbab7d313890d0dca115c90f389582) | `943b4f39c2bbab7d313890d0dca115c90f389582` |
| [e3e41c782e4099a06a6ac1f482cd3119](https://gist.github.com/williamzujkowski/e3e41c782e4099a06a6ac1f482cd3119/f8cb3f838e921248c67289d5d42c220e33a3f556) | `f8cb3f838e921248c67289d5d42c220e33a3f556` |
| [f025bd03e6d265b8aa9fdb8d73df9740](https://gist.github.com/williamzujkowski/f025bd03e6d265b8aa9fdb8d73df9740/ea855f155324c637ee74a9f68e76aba97f2b5c16) | `ea855f155324c637ee74a9f68e76aba97f2b5c16` |

The follow-up production build passed. The offline link check again passed for 216 pages, 8,511 links and 2,507 anchors. Rendered HTML inspection verified the dated artifact correction, all six archived/incomplete/unsupported link labels, retention of the corrected optional dependency command, and removal of the previous hourly/weekly/script-delivery promises. No implementation files ran. These checks cover the changed guidance; they do not revalidate unrelated personal history.
