## Summary

You can carve out your vulnerability blog generator into its own repository by **splitting** its directory (with history) using tools like **git-filter-repo** or **git subtree**, then **publishing** that new repo and **linking** it back to your website via **Git submodules** or **subtrees** to maintain seamless integration and CI/CD support. This approach preserves commit history, keeps your website repo lean, and leverages GitHub Actions to clone, build, and deploy your site alongside the separate blog generator project without breaking existing workflows.

---

## 1. Identify and Prepare the Blog Generator Code

1. **Catalogue relevant items**:
   - Scripts and configuration: `generate-vuln-post.js`, `llm-providers.js`, `OPTIMIZATION_GUIDE.md`, `WORKFLOW_GUIDE.md`, plus `.github/workflows`, `package.json`, `schedule-posts.js`, `setup-cron.sh`, and test scripts.
2. **Create a clean working branch** in your website repo for migration work:
   ```bash
   git checkout -b extract-vuln-blog
   ```
3. **Back up** your repo to avoid mishaps:
   ```bash
   git clone --mirror https://github.com/yourorg/website-repo.git backup-repo.git
   ```

---

## 2. Extract with `git-filter-repo`

This method **preserves full history** of the blog generator’s directory (`scripts/vulnerabilities`, `Prompts`, etc.) inside a brand‑new repository.

1. **Clone the website repo** for extraction:

   ```bash
   git clone https://github.com/yourorg/website-repo.git temp-extract
   cd temp-extract
   ```

2. **Install `git-filter-repo`** (if not already):

   ````bash
   pip install git-filter-repo
   ``` citeturn0search2

   ````

3. **Filter out only the blog generator paths**, mapping them to the new repo root:

   ````bash
   git filter-repo \
     --path scripts/vulnerabilities \
     --path generate-vuln-post.js \
     --path llm-providers.js \
     --path OPTIMIZATION_GUIDE.md \
     --path WORKFLOW_GUIDE.md \
     --path .github/workflows \
     --path package.json \
     --path schedule-posts.js \
     --path setup-cron.sh \
     --path test-data-sources.js \
     --path test-models.js \
     --path test-vuldb.js \
     --path Prompts \
     --path-rename scripts/vulnerabilities/:.
   ``` citeturn0search2

   ````

4. **Review the resulting history** to ensure it contains only the desired files:

   ```bash
   git log --oneline
   ```

---

## 3. Initialize and Publish the New Repository

1. **Create a new empty GitHub repo**, e.g. `vuln-post-generator`.

2. **In your filtered clone**, update `origin` and push:

   ````bash
   git remote remove origin
   git remote add origin git@github.com:yourorg/vuln-post-generator.git
   git push -u origin main
   ``` citeturn0search3

   ````

3. **Protect branches** and set up branch‑protection rules in GitHub to match your website repo policies.

---

## 4. Integrate Back into the Website with a Submodule

Using a **submodule** keeps the blog generator code separate yet version‑controlled within your website repo.

1. **In your website repo**, remove or rename the old blog generator folder:

   ```bash
   git rm -r scripts/vulnerabilities generate-vuln-post.js llm-providers.js ...
   git commit -m "Remove in‑repo blog generator; replacing with submodule"
   ```

2. **Add the new repo as a submodule** in a clear directory (e.g., `tools/vuln-blog`):

   ````bash
   git submodule add git@github.com:yourorg/vuln-post-generator.git tools/vuln-blog
   git submodule update --init --recursive
   git commit -m "Add vuln-post-generator as submodule"
   ``` citeturn1search4

   ````

3. **Document submodule workflow** in your README so contributors know to run:

   ````bash
   git clone --recursive https://github.com/yourorg/website-repo.git
   ``` citeturn1search3
   ````

---

## 5. Update GitHub Actions for CI/CD

1. **Checkout submodules** in your build workflow:

   ```yaml
   - uses: actions/checkout@v4
     with:
       submodules: recursive
   ```

2. **Adjust paths** in your workflow steps (e.g., replace `scripts/vulnerabilities` with `tools/vuln-blog`):

   ```yaml
   - name: Generate Vulnerability Posts
     run: |
       cd tools/vuln-blog
       npm install
       node generate-vuln-post.js --latest --provider openai
   ```

3. **Upload artifacts** from the submodule build if needed:

   ````yaml
   - uses: actions/upload-artifact@v4
     with:
       name: vuln-posts
       path: tools/vuln-blog/output
   ``` citeturn1search0

   ````

4. **Trigger tests** for both repos: add jobs to run `npm test` in `tools/vuln-blog` and the website build in parallel.

---

## 6. Maintain History and Future Updates

- **Pull updates in the submodule**:

  ````bash
  cd tools/vuln-blog
  git pull origin main
  cd ../..
  git add tools/vuln-blog
  git commit -m "Update vuln-post-generator to latest"
  ``` citeturn1search1

  ````

- **Use submodule tags** for versioning: in `vuln-post-generator`, tag releases (e.g., `v1.2.0`) and in the website repo, update the submodule to that tag for reproducible builds. citeturn1search5

- **Alternatively**, manage the external code via **Git subtree** if you prefer merging updates directly into your website repo without manual submodule pointer commits citeturn0search1.

---

By following these steps—**filtering** your generator code, **publishing** it independently, and **reconnecting** via submodules (or subtrees) with updated **GitHub Actions**—you’ll achieve a clean separation of concerns, preserve full history, and ensure your website build continues to consume the blog generator seamlessly.
