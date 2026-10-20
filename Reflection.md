# Task 3: Reflection on AI Paradoxes

This homework presents a useful tension: the same AI system can help verify information and help construct material that defeats verification. Building the verifier and then attacking it changed how I interpret a successful AI result. A plausible answer, or even a correct answer on a small test set, does not establish that the whole process is reliable.

## Better verification can coexist with easier deception

An agent can reduce the effort needed to compare a CV with several profiles. It can search for candidates, retrieve their records, recognize equivalent degree names and check employment dates. These capabilities could make routine verification more accessible. However, AI and document-generation tools also reduce the effort needed to produce convincing false material. The productivity gain is available to both the verifier and the attacker.

The Task 2 PDF illustrates this problem without relying on an instruction such as “ignore previous instructions.” Kelly Tsang's actual AIA title is Manager, with mid-level seniority. The page visibly claims Senior Manager, but the additional word is an image. The text loader returns Manager. In one test, both the original and the altered CV received 0.95 from our verifier. Improving the model's instructions alone would not restore a word that never reached the model.

## Accurate reasoning can produce an incorrect document-level decision

The verifier may correctly compare every extracted claim against the correct profile and still approve a misleading PDF. Its input is a representation of the document, not the full document itself. The agent's reasoning can therefore be internally consistent while its conclusion about what a human reader sees is wrong.

This matters in business workflows because extraction is often treated as a preliminary technical step. Here it determines what can be verified at all. A stronger design would inspect whether a page mixes text and images, compare extracted text with a rendered view or OCR result, and flag material differences for review. OCR would introduce its own recognition errors, so disagreement should trigger further checking rather than an automatic accusation of fraud.

## More automation increases the importance of human judgment

Automation promises less manual review, yet deciding when to trust automation requires judgment about identity, missing evidence and the cost of mistakes. Our code returns 0.5 when it cannot complete verification. Under the assignment's threshold, that becomes a discrepancy prediction. In a real recruitment process, an unavailable API or an ambiguous name should instead be recorded as unresolved and routed for review. Failure to establish a claim is different from evidence that the claim is false.

The public-test result also requires care. Our agent classified all seven public CVs correctly in one run, but that measures performance on those examples. It does not establish reliability on unseen candidates or resistance to different attacks. The Task 2 result is a concrete example of how high ordinary accuracy and a serious blind spot can exist together.

My main takeaway is that an agent's reliability depends on the entire workflow: what the document contains, what the loader preserves, which person the search resolves, what evidence the tools return and how uncertainty is handled. I would use automation to organize and compare evidence, while keeping a review path for extraction mismatches and unresolved cases. The goal should be a decision supported by inspectable evidence, with confidence limited to what the system actually checked.
