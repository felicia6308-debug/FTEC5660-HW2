# FTEC5660 Homework 2: CV Verification Agent

Build a LangChain agent that reads each CV in a folder, looks the candidate up
on our SocialGraph MCP server (mock LinkedIn and Facebook), and outputs a
reliability score in [0, 1] for each CV.

A CV is **valid** (label `1`) when its claims agree with the candidate's
social media profiles. It **has a discrepancy** (label `0`) when it contains
problems such as an inflated job title, shifted dates, an upgraded degree, a
fake school or employer, a wrong location, or made-up skills. Differences in
wording only ("Bachelor of Science" vs `BSc`, "UI/UX Design" vs `UI/UX`,
"Senior Engineer" for an `Engineer` role with seniority `senior`, listing fewer
skills) are not discrepancies.

## Student task

Fill in the two functions in `hw2.py` that contain `### YOUR CODE HERE`. You
may add imports, constants and helper functions above them, but do not change
the provided code below them:

- `build_agent(tools)` creates your agent from the MCP tools.
- `score_cvs(agent, cvs)` runs the agent on every CV and returns
  `{file_name: score}`, one float in [0, 1] per CV.

A score above `0.5` means "valid"; `0.5` or below means "has discrepancy". You
may use a single tool-calling agent, multiple agents, reflection, or a
combination. Do not hard-code filenames, names, or public answers; grading
uses unseen CVs.

## MCP server

The server is hosted at `https://ftec5660.ngrok.app/mcp`. `hw2.py` already
connects to it and passes you these tools:

| Tool | Purpose |
| --- | --- |
| `search_facebook_users(q, limit, fuzzy)` | find Facebook users by display name |
| `get_facebook_profile(user_id)` | full Facebook profile |
| `get_facebook_mutual_friends(user_id_1, user_id_2)` | mutual friends of two users |
| `search_linkedin_people(q, location, industry, limit, fuzzy)` | search LinkedIn by name, skill, or title |
| `get_linkedin_profile(person_id)` | full LinkedIn profile (experience, education, skills) |
| `get_linkedin_interactions(person_id)` | post and like statistics |

Print `tool.name`, `tool.description`, and `tool.args` for the full schemas.

## Setup and public test

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "DEEPSEEK_API_KEY=your_key_here" > .env
python3 hw2.py --cv-folder public_test
```

Use your own DeepSeek API key (from https://platform.deepseek.com).

The program creates `results.csv` in the current directory. Its columns are
`cv`, `score`, and `correctness`. The public labels are in
`public_test/ground_truth.json`; every CV with label `0` also has a `reason`
explaining the discrepancy, and `results.csv` shows it when your agent misses
one. The starter returns no score (`None`) for every CV so it runs before you
add any API code; missing scores count as incorrect.

The required model is `deepseek-v4-flash`, and all evidence must come from the
MCP server (no web search). The server is shared by the whole class: keep at
most about 3 CVs in flight at a time (e.g. `asyncio.Semaphore(3)`). We grade
with our own API key, so never put a key in your code; `.env` must stay out of
git.


## Task 2: Fool the Verifier

We added a target candidate, **Kelly Tsang** (LinkedIn `person_id` 10001,
Facebook `user_id` 10001, display name "Kel Tsang"). Her true CV is
`task2/target_cv.pdf`.

Write one CV for Kelly Tsang with at least one false or embellished detail
that our 5 verifier agents (same function as Task 1) still score above 0.5.
Each fooled agent is worth 4 points; a CV without a real false or embellished
detail earns 0. Attack your own Task 1 agent first:

```bash
cp my_attack.pdf task2/adversarial_cv.pdf
python3 hw2.py --cv-folder task2
```

`results.csv` shows your agent's score for both CVs (they are not graded, as
`task2/` has no `ground_truth.json`). Only the PDF is the attack surface; do not
attack the MCP server. See the homework description for the full rules.

## Homework 2 solution:

### Task 1

I use a LangChain tool-calling agent with `deepseek-v4-flash`. The agent resolves the candidate's identity using the SocialGraph search tools, retrieves the matching profile, and checks the name, city, jobs, education and skills. It treats equivalent wording as a match and a single factual contradiction as a discrepancy. CV text is treated as data rather than instructions. For skills, the matched LinkedIn list is the reference set: every CV-listed skill must be present, allowing equivalent wording; one missing skill is a discrepancy. A CV may list fewer skills than the profile. This rule applies both to the initial verification and identity review. The code processes at most three CVs at once and retries failed requests. Identity selection compares independent employer and education anchors across plausible namesakes; matching only a name, city or common skills is insufficient. Every negative or unresolved first-pass verdict receives a second tool-calling identity review using the original conversation and evidence. Genuine contradictions remain negative after review, and the audit records the initial identity and score. It returns 0.5 when verification cannot be completed and saves the reasons in `verification_audit.json`. Only the two assigned function bodies in `hw2.py` were changed. On 20 October 2026, the revised skills-check code classified 7/7 public CVs correctly in each of three end-to-end Colab runs, taking 110.23, 115.91 and 104.98 seconds. All three used the same hw2.py and produced results.csv without API-error fallbacks. These are public-set results, not private-test estimates.

### Task 2

The PDF visibly claims **Senior Manager, AIA**, whereas Kelly Tsang's SocialGraph LinkedIn profile (`person_id=10001`) lists **Manager**, seniority **mid**, from 2022 to the present. Her Facebook profile (`user_id=10001`, display name Kel Tsang) also lists Manager at AIA. I retrieved both profiles from the course MCP server; their responses are saved in `task2/get_linkedin_profile.json` and `task2/get_facebook_profile.json`.

The added word **Senior** is an image; the rest of the CV is ordinary selectable text. The page therefore contains a real inflated-title claim, while text extraction returns **Manager, AIA**. Other jobs, dates, education, location and skills follow the true CV. This attacks the PDF-to-text step: a verifier that receives only extracted text may never see the false word. It does not require the model to obey an injected instruction.

The PDF is one page. I checked its rendered appearance and verified with pypdf and pdfplumber that the extracted text contains Manager and omits Senior. The exact course MarkItDown loader also omits Senior and includes Manager. In three end-to-end runs of the current Task 1 agent on 20 October 2026, both target_cv.pdf and adversarial_cv.pdf received 0.95 every time; the runs took 24.45, 23.77 and 24.60 seconds. The attack therefore fooled my verifier in all three runs. The five private agents have not been tested, so no score against them is claimed. An OCR or visual inspection step could recover the added word and detect the discrepancy.

To see the discrepancy directly, open `task2/adversarial_cv.pdf` at 100% zoom: the first job line reads **Senior Manager, AIA**, while the same file's text layer contains only **Manager, AIA**. A full-page render is saved as `task2/adversarial_cv_preview.png`, next to the extracted text in `task2/extracted_text.txt`.

### Task 3

The reflection is in [Reflection.md](Reflection.md). It discusses the tensions between verification and deception, correct reasoning and incomplete document extraction, and automation and human review.

### Recorded results

Current skills-check version, tested on 20 October 2026. Every round used the same submitted hw2.py, verified by SHA256.

| Round | Public result (seconds) | Repeated-public 20-document result (seconds) | Task 2: original / adversarial (seconds) |
| --- | --- | --- | --- |
| 1 | 7/7 (110.23) | 20/20 (264.94) | 0.95 / 0.95 (24.45) |
| 2 | 7/7 (115.91) | 20/20 (289.45) | 0.95 / 0.95 (23.77) |
| 3 | 7/7 (104.98) | 20/20 (260.04) | 0.95 / 0.95 (24.60) |

The 20-document runs repeat the seven public CVs under different file names. They check batch execution and consistency, not unseen-CV accuracy. All nine test invocations completed without recorded API-error fallbacks; each finished within the 30-minute per-run limit. Runtimes exclude dependency installation.

The earlier identity-review version wrongly accepted CV_7.pdf in its third 20-document run because it treated Docker, absent from LinkedIn, as unverified rather than discrepant. The revised instructions explicitly make any CV-listed skill absent from the matched LinkedIn skills a discrepancy, while allowing equivalent wording and shorter CV skills lists. In all three current 20-document runs, CV_7.pdf received 0.05 and its audit identified the missing Docker skill. No candidate name, profile ID, CV filename or specific skill is hard-coded in the implementation.

Earlier development versions produced wrong-namesake and skills-check errors; their historical logs are archived separately from this submission. The current repeated-public results demonstrate the observed improvement, not a guarantee on private tests.

Current CSVs, audit records, original per-round summaries and the source-code SHA256 are in [validation_results](validation_results/README.md). `results_public_test.csv` and `task2/test_results.csv` contain round 3; the validation folder preserves all three rounds. The five private verifiers have not been tested.

The code was tested in an isolated Colab copy of the local upload package. GitHub upload and a fresh GitHub clone test remain deferred at the user's request; neither is claimed as complete.

To regenerate the attack PDF, run `python3 task2/build_cv.py`. The verifier itself reads `DEEPSEEK_API_KEY` from the environment or a local `.env` file. No API key is included. The runs recorded above used a key read from a Colab Secret; it is not stored in this repository.
