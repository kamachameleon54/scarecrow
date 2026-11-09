# Guided first use

Help someone comfortable with ChatGPT or Claude get one useful result from a second brain. Use normal conversation, short turns, and one question at a time. Teach each concept when it becomes useful; adapt the wording rather than reciting this file. Keep the current assistant's voice and be honest about what this session can access.

## 1. Start from their work

Read the applicable local rules and any onboarding record they name before beginning. If the target folder is unknown, establish it before inspecting personal files. Inspect only that folder and the sources the person selects. A greeting is not permission to scan their computer.

For a new user, explain in two or three sentences: they can keep asking in ordinary language; here the assistant can also work with files in the folder the host permits. Scarecrow saves selected context, decisions, and working preferences there so a future session can read them. It does not retrain the model or automatically import earlier chats, other accounts, or the rest of their device.

For example: "You can talk to me much as you would in chat. We'll keep useful background and decisions in a folder we can return to, so you have less to explain next time. What's one project or recurring task you'd like help picking up more easily?"

If their goal is already known, acknowledge it and ask only the next missing setup question. Treat a pasted conversation as a selected source, with its claims checked like any other source. Keep uncertain facts separate from confirmed decisions.

Briefly set expectations for the first session: choose a purpose, agree on the files and boundaries, create one useful result, then offer a recurring review. Keep this to one sentence when helpful. Start this conversation on the first invocation after installation; claim an install-time launch only if the actual host provides and has verified that mechanism.

Once the goal is clear, offer a natural choice of pace if the person has not already expressed one: "We can build this together one step at a time, or I can propose a starting structure for you to review." Accept ordinary-language answers. Use guided steps for someone asking to be walked through; use a proposal for someone asking to see an example first. Skip the choice if they already selected a path or gave sufficient instructions to proceed.

If the host cannot read or write the intended folder, explain the specific limitation before offering to create it. Help choose an accessible location or draft a setup proposal in chat. State that nothing has been saved; pause file-dependent steps until access exists. Offer terminal commands only when needed, with their purpose explained. Coding knowledge is not a prerequisite for the guided conversation.

## 2. Build together

Use setup's folder inventory to choose build or adopt mode. For an existing notes folder, report what is there and propose additions before changing existing files; preserve its local approval rules. A walkthrough does not authorize moving, deleting, or overwriting existing material.

Use setup's short interview, taking answers from the conversation instead of repeating questions. Cover the purpose, agents, location, first source, and privacy boundaries. Explain the four parts through the person's project, one short sentence each. Start with one project and one source; add more when they ask or the first loop needs them.

In the **guided path**, ask only the next unanswered question, explain the immediately useful part, and build the agreed pieces as information becomes sufficient. In the **proposal path**, use known facts to show a compact starting layout, one example of their work flowing through it, and any assumptions or unanswered boundary questions. A request to propose is not permission to write files: show the plan and wait for approval before scaffolding. After approval, continue the same source-confirmation, preference, and verification steps. Either path can switch pace when the person asks.

Ask about answer style or autonomy only when it affects the task, for example whether they want a brief answer or a worked example. Distinguish a preference for this task from a standing rule. Before recording a standing preference, show the proposed wording and ask whether to remember it for this brain. Save only confirmed preferences in the existing rules or another location those rules specify, with reason and date. Keep credentials and sensitive personal details out of preference records. Apply corrections to the current answer immediately; use the local correction process for durable factual corrections.

## 3. Produce the first useful result

Follow setup's first-ingest procedure: preserve the selected source, read it, present the takeaways, and wait for the owner's confirmation before compiling unless the local rules explicitly allow a pending ingest. Show one practical answer or small work product based on the saved material and cite the actual file. Explain the three useful habits through the work: ask where a claim came from, correct an interpretation, and say when a possibility becomes a decision. Invite a correction without inventing a mistake or requiring a quiz.

If no source is available, finish only the agreed scaffold and record choosing a first source as the next step. If they want a demonstration, offer clearly labeled fictional material; keep it separate from real project knowledge. Do not call a scaffold a completed first-use loop.

## 4. Save progress and make returning easy

After the target and scaffold are agreed, keep a short onboarding record at the location named by local rules, default `_system/onboarding.md`. Add a pointer in newly generated root rules. For existing rules, propose the pointer and get the approval required for modifying them. Keep the record limited to workflow progress, confirmed preference locations, relevant file links, and one next action; it is not a chat transcript or personality profile. Respect local rules that disallow this record and offer a conversational handoff instead.

Use this record shape, filling only facts observed or confirmed:

```markdown
# Getting started

Last updated: YYYY-MM-DD
Stage: started | ready-for-retrieval-check | complete | skipped
Goal: <one useful task>
Approach: guided | proposal | not yet chosen
Completed: <observed steps and relative links to their files>
Working preferences: <link to confirmed rules, or none saved>
Next step: <one action the person can take>
Fresh-session retrieval: not tested | <date, question, cited file, result>
```

Update an existing record without erasing a prior check's evidence. A started record may be resumed; a ready record means the first useful result was saved and structural findings were addressed or disclosed, not that future-session retrieval succeeded. Mark complete only after an observed fresh session or the person's specific report answers a question correctly using saved files and cites them. Label a user-reported result as reported rather than independently observed. If they skip, record that only when writing is already authorized; resume normal work immediately. Offer training again only when requested.

If they pause before agreeing to any files, give a short conversational handoff with the chosen approach, decisions, and next unanswered question. Do not create a progress record merely to retain a declined or unapproved proposal. When they return, use the saved record or supplied handoff to say where things stopped and offer its one next step; ask only for missing context rather than restarting the welcome or interview.

Give one next action at the end, such as opening a fresh session in the same folder and asking a question whose answer is in the saved material. Name the expected page without giving away the answer. Explain that this checks the files, rather than relying on the current chat. Do not claim the check passed before seeing evidence. If they later report a failure, inspect the relevant paths and rules before asking them to re-explain their work.

## 5. Offer a recurring gap check

Once there is a useful starting point, suggest maintenance as part of getting started, in ordinary language: "A short review every four weeks can help keep this useful: we'll check for missing or outdated information and whether the setup still fits your work. Would you like help setting that up, or would you rather check in when you need it?" Ask this as its own turn, not as another question bundled into source or preference confirmation. If the owner already chose a cadence or declined scheduling, honor that answer. Do not make scheduling a prerequisite for completing onboarding.

If they opt in, explain and confirm the delivery mode: a reminder to open a guided review, or an unattended health-check report they can discuss later. Offer only modes the host actually supports. Gather the missing cadence, timezone, local time, and delivery destination one question at a time; reuse provided facts. The default proposal is every four weeks, not a mandatory interval. A guided conversation happens when the person returns; a scheduled unattended run produces findings rather than conducting an interactive interview.

Use health-check's standard scope for the recurring gap check. Its recurring brief should name the accessible brain root, read local rules, inspect missing/stale knowledge and unresolved questions, consider whether the setup fits current work, and return a short prioritized list with one next action. Keep unconfirmed improvement ideas separate from defects. Apply only health-check's permitted maintenance writes (visit log and next-date update when allowed by local rules); leave all proposed repairs and structural/preference changes for the owner's approval. Include the person's on-request-only preference if they have one.

Before creating anything, check the host's scheduling capability and whether an equivalent task already exists. Create a recurring task only with the owner's opt-in and confirmed scheduling details; reuse or update an existing task only within their authorization. Do not install a background process, configure cron, or imply the plugin's installation itself enables a timer. An unattended task requires access to this specific folder when it runs; a local path in a cloud reminder does not provide that access. If access cannot be established, offer the guided-review reminder instead.

Report the actual scheduler result. Save the confirmed cadence, mode, and returned task identifier in the existing onboarding record (or location chosen by local rules) only after successful creation. If scheduling is unavailable or fails, say no recurring task was created, keep the next health-check date in local rules, and give the manual prompt "Review my second brain for gaps and maintenance." A host-specific task is not automatically portable when the folder moves or the person changes harnesses; check the destination/access when that happens.

After the first real use, a brief check-in may ask what was useful or confusing; save a change only after confirmation. The person should leave with a useful result, an understandable next step, and control over what is remembered.
