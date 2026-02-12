---
name: fetch-skills
description: "Sync skills submodule with upstream anthropics/skills. Use when the user wants to update skills from the upstream repo."
---

# Fetch Skills

Sync the local skills fork (p3ob7o/skills) with upstream (anthropics/skills).

## Steps

1. Run the following commands in `/Users/paolo/Ponyo/skills`:

```bash
cd /Users/paolo/Ponyo/skills && git fetch upstream && git log --oneline HEAD..upstream/main
```

2. If there are no new upstream commits, tell the user skills are already up to date and stop.

3. If there are new commits, show the user what's incoming and merge:

```bash
cd /Users/paolo/Ponyo/skills && git merge upstream/main
```

4. If the merge succeeds, push to the fork and update the submodule ref in Ponyo:

```bash
cd /Users/paolo/Ponyo/skills && git push origin main
cd /Users/paolo/Ponyo && git add skills && git commit -m "Update skills submodule" && git push origin main
```

5. If there are merge conflicts, show them to the user and help resolve them before pushing.
