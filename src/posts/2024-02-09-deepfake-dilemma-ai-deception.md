---

date: 2024-02-09
description: Deepfake detection works well on data it has seen and falls apart on data it hasn't. Why the fix is partly cultural, not just technical.
title: 'The Deepfake Dilemma: Navigating the Threat of AI-Generated Deception'
tags:
  - ai
  - ethics
  - security
---
The first time I encountered a convincing deepfake, I spent an hour cross-referencing sources and stepping through the video frame by frame before I was satisfied it was synthetic. I already knew the technology existed. That did not help as much as I expected it to.

That hour is the whole problem in miniature. Verification is expensive, sharing is free, and the asymmetry is getting worse.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/deepfake.png'); width: min(300px, 75%); aspect-ratio: 400/409; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the tell is always on the right</p>

## Detection works right up until it matters

The cleanest measurement of how well deepfake detection actually works comes from Facebook's Deepfake Detection Challenge, which ran in 2019 and published results in 2020. It was a serious effort: a purpose-built dataset, thousands of entrants, real prize money.

The winning model scored **82.56% accuracy on the public test set**. Against the black-box set — 10,000 videos the entrants had never seen, including footage pulled from the internet, makeup tutorials, paintings, AR face filters, and videos with the frame rate and resolution deliberately altered — the same model scored **65.18%** ([Meta AI](https://ai.meta.com/blog/deepfake-detection-challenge-results-an-open-initiative-to-advance-ai/)).

That gap is the finding. A seventeen-point collapse between "deepfakes we trained on" and "deepfakes in the wild" is not a tuning problem. It says the model learned the fingerprints of specific generators rather than anything general about synthesis, and a new generator resets it. Every published detection number should be read with the question *"on which dataset?"* attached, because the answer usually explains the number.

This is why I am wary of detection accuracy quoted without a test set. It is the easiest figure in the field to make look good.

## The technology, briefly

Deepfakes use generative adversarial networks: one network produces fakes, another tries to catch them, and they escalate against each other. The architecture is an arms race by construction, which is a strange thing to be surprised by later.

The relevant fact for anyone thinking about defence is not that the technique exists but that it commoditised. Face-swap tooling is open source, it runs on a consumer gaming GPU, and the skill floor is a working knowledge of Python. The output from a casual attempt is bad — artifacts around the mouth, a certain waxiness — but "bad" is measured against current expectations, and it would have passed inspection a few years earlier. The people who care to do it properly have more patience and better source material than someone poking at it for an afternoon.

## Real-world consequences

**Fraud.** In 2019 a UK energy firm's chief executive authorised a wire transfer of roughly €220,000 — about **$243,000** — after a phone call from what he believed was his German parent company's CEO. It was a voice clone. The case was reported by the *Wall Street Journal* via the firm's insurer, Euler Hermes, and is generally treated as the first documented AI voice-mimicry fraud. What makes it instructive is that the victim knew the voice. Familiarity was the attack surface, not the defence.

Voice cloning has since dropped to needing seconds of reference audio rather than minutes. Over a compressed phone line, the artifacts that give a clone away in a quiet room are mostly gone.

**Speed.** Misinformation outruns correction, and this is measured rather than assumed. Vosoughi, Roy, and Aral analysed roughly 126,000 cascades shared by 3 million Twitter users between 2006 and 2017 and found falsehoods **70% more likely to be retweeted** than true stories, reaching 1,500 people about **six times faster** ([*Science*, 2018](https://mitsloan.mit.edu/ideas-made-to-matter/study-false-news-spreads-faster-truth)). Bots did not explain it. People did. Novelty is more shareable than accuracy, and a fabricated video is by definition novel.

That study predates convincing video synthesis, which is the uncomfortable part. The distribution advantage was already there. Deepfakes just improve the payload.

**Harassment.** The largest category of deepfake content by volume has never been political — it is non-consensual sexual imagery, overwhelmingly of women. It gets less coverage than election scenarios and does more measurable damage to more people. Any policy conversation that treats this as a footnote to the democracy question has the proportions backwards.

## The detection arms race

**Artifact spotting** was the first line: unnatural blinking, inconsistent lighting, warping at the jawline. It worked, briefly, and then generators fixed those specific tells. Training your eye on 2019 artifacts teaches you to catch 2019 fakes.

**Learned detection** replaced it and inherited the DFDC problem above: strong in-distribution, weak out of it.

**Forensic analysis** — compression artifacts, sensor noise patterns, temporal inconsistency — is more durable because it targets the pipeline rather than the generator. It also degrades fast under re-encoding, and every social platform re-encodes everything you upload. The forensic signal is often destroyed by the same platform that would need it.

There is a false-positive trap here that gets underrated. Compression artifacts and synthesis artifacts look alike to a classifier, which means the content most likely to be wrongly flagged is *low-quality authentic footage*: security cameras, older phones, anything that has been re-shared several times. Deploy a detector at a threshold aggressive enough to catch real fakes and you will spend most of your review budget on ordinary bad video.

**Biometric approaches** — heartbeat inferred from skin-tone shifts, idiosyncratic speech timing, micro-expressions — are the most interesting research direction because they key on something the generator has no reason to reproduce. I have not seen evidence they generalise across datasets any better than the rest, and cross-dataset generalisation is the entire game.

## The human element

The technical picture is bleak enough that people reach for "well, humans will notice." They will not, particularly.

Groh, Epstein, Firestone, and Picard ran two studies with **15,016 participants**, showing authentic videos and deepfakes and asking which was which. Ordinary observers and the leading computer-vision detector came out **similarly accurate**, while making different kinds of mistakes ([Groh et al.](https://arxiv.org/abs/2105.06496)). Humans and machines were roughly equally fallible, in complementary ways.

The finding worth sitting with is what happened when they were combined. Participants shown the model's prediction did better on average — but **when the model was wrong, it frequently dragged them into being wrong too**. A detector that is right most of the time and confidently wrong the rest is not a neutral aid. It transfers its errors to the people relying on it, and it does so with an authority that a person's own uncertainty would not have carried.

That should shape how any detection tool gets deployed. A confidence score presented as a verdict makes its failure modes contagious.

## Prevention

No single layer works. The combination is the point.

**Provenance over detection.** Signing content at creation and carrying a tamper-evident record forward is a fundamentally better problem than inferring synthesis after the fact — it is cryptography instead of pattern matching. It needs capture hardware, platforms, and standards to cooperate, which is why it has been perpetually two years away, but it is the only approach that does not lose ground every time generators improve.

**Watermarking**, embedded at generation, has the same appeal and a sharper limit: it only binds actors who choose to be bound. It helps with commercial models and does nothing about an open-source checkpoint with the watermarking stripped out. Useful, not sufficient.

**Media literacy** that transfers. Teaching people the artifacts of current-generation fakes has a shelf life measured in months. Teaching provenance habits — who published this, what corroborates it, does the emotional pull explain why I am about to share it — does not expire when the generators improve.

**Legal and platform frameworks.** Clear penalties for malicious synthesis, obligations on platforms that amplify it, and cross-border coordination, since none of this respects jurisdiction.

## The ethical questions I have not resolved

**Creative use versus impersonation.** Synthetic media has legitimate uses — dubbing, accessibility, satire, film. Drawing a line that catches malicious impersonation without catching parody is genuinely hard, and I do not have a clean rule.

**Privacy versus verification.** Detection systems tend to want biometric analysis. Building infrastructure that fingerprints faces to protect people from having their faces misused is a trade with an obvious failure mode.

**Who decides.** False positives in detection are a censorship mechanism with a technical alibi. Given how badly detectors generalise, a takedown pipeline driven by classifier confidence will remove authentic content, and the people least able to appeal are those whose footage was low-quality to begin with.

**Access.** Detection research runs on hardware and datasets concentrated in a few large labs. Generation tooling runs on a gaming GPU. The offence has been democratised and the defence has not.

## What I tell people

**Interrogate content designed to make you angry.** The material engineered for outrage is the material engineered for sharing, and per the *Science* result, that is a measured effect rather than a vibe.

**Never let one piece of media carry a decision.** Corroboration from independent sources is the practical defence, and it does not depend on any detector working.

**Distrust confident detection.** Including your own. Groh et al. found people and machines about equally accurate, so "I would be able to tell" is a claim with data against it.

**Assume attackers test first.** Anyone deploying a deepfake seriously will have run it against public detectors before release. Detection tools published openly are also a targeting service.

## Conclusion

The technology producing deepfakes will keep improving, and detection will keep being strongest exactly where it is least needed — on the generators it has already seen. Seventeen points of accuracy between a curated test set and the open internet is the honest summary of where automated detection stands.

Which means the durable defences are the ones that do not depend on winning that race: provenance recorded at creation, corroboration habits that survive better fakes, and consequences that make malicious use expensive. Those are slow, institutional, and unglamorous compared with a classifier.

The deepfake that unsettled me would look primitive now. The lesson it taught has held up better than the artifacts did: in an environment where anything can be synthesised, trust has to come from verification rather than from appearance.

### Further Reading:

- [Deepfake Detection Challenge results](https://ai.meta.com/blog/deepfake-detection-challenge-results-an-open-initiative-to-advance-ai/) - Meta AI (the 82.56% / 65.18% gap)
- [The spread of true and false news online](https://mitsloan.mit.edu/ideas-made-to-matter/study-false-news-spreads-faster-truth) - Vosoughi, Roy & Aral, *Science* 2018, summarised by MIT Sloan
- [Deepfake Detection by Human Crowds, Machines, and Machine-informed Crowds](https://arxiv.org/abs/2105.06496) - Groh, Epstein, Firestone & Picard
- [Deepfakes and international conflict](https://www.brookings.edu/articles/deepfakes-and-international-conflict/) - Brookings
- [Deepfakes and Disinformation](https://www.cfr.org/backgrounder/deepfakes-and-disinformation) - Council on Foreign Relations
- [Deepfakes Are Becoming the Hot New Corporate Security Threat](https://www.wired.com/story/covid-drives-real-businesses-deepfake-technology/) - WIRED

### Get Involved:

- [WITNESS](https://www.gen-ai.witness.org/) - human rights organisation working on media authenticity
