# Skills-check validation — 20 October 2026

Three completed Colab rounds used the identical submitted hw2.py. SHA256: `2c2ffebf07cb16ce8658c9644bb11a688953d1d69da8f302d9dc909a76219ef5`. Original per-round summaries are in round1_summary.json, round2_summary.json and round3_summary.json; summary.json combines them using distinct run names. The original three-round summaries have null commits because those runs preceded GitHub upload. The separate fresh-clone summary below records the tested GitHub commit.

| Round | Public correct / seconds | Repeated-public 20-document correct / seconds | Task 2 original and adversarial / seconds |
| --- | --- | --- | --- |
| 1 | 7/7 / 110.23 | 20/20 / 264.94 | both 0.95 / 24.45 |
| 2 | 7/7 / 115.91 | 20/20 / 289.45 | both 0.95 / 23.77 |
| 3 | 7/7 / 104.98 | 20/20 / 260.04 | both 0.95 / 24.60 |

In all three 20-document runs CV_7.pdf received 0.05. Each audit identifies Docker as absent from the matched LinkedIn skills. The code contains a general reference-set rule, not any candidate name, profile ID, CV filename, specific skill or expected label.

The 20-document batches repeat public CVs and are throughput/consistency checks, not unseen-CV accuracy estimates. The audit reasons are model outputs, not independent proof. passed_execution means process completion with the expected number of valid scores and no recorded API-error fallback; accuracy is separate. All nine invocations passed execution; no fallback occurred. Runtime excludes dependency installation.

Files task2.csv and task2_audit.json alias round 3. Root results_public_test.csv and task2/test_results.csv also show round 3. Every round is separately preserved. Pre-fix development records are archived separately and are not included in this submission. No API key is included.

## Fresh GitHub clone validation

A clean environment installed requirements.txt and ran the public set and Task 2 from GitHub commit `4dddd8fcdcc2ecef89d0e6de9add40c1049a25c4`. Public: 7/7, 101.86 seconds. Task 2: original and adversarial both 0.95, 20.01 seconds. Both invocations passed execution without fallback errors. The code hash is unchanged. See [fresh_clone_summary.json](fresh_clone_summary.json), fresh_clone_public_run1.csv, fresh_clone_task2.csv and their audit JSONs. No additional 20-document run was performed for this clone check. Later documentation commits do not change the tested hw2.py.
