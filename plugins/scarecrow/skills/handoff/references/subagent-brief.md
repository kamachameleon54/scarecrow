# Subagent Brief

How to run a handoff through the current host's native delegation tools when the user cannot reach a chip (Remote Control, or they asked to run it here). Use background execution only when supported. The subagent gets the handoff as its brief; the user gets the report relayed back into this session.

## When this rung applies

- The user is on Remote Control and said "run it" after the chip offer, or asked up front ("run it here," "start it," "I'm on my phone, just do it").
- No `spawn_task` exists but the user wants the work done now rather than pasted elsewhere.

Not a replacement for the chip when the user is at the desktop: delegation does not guarantee a separately reopenable chat.

## Brief shape

Send exactly this, in order:

1. One line of framing: "You are running a handed-off task for [user] inside [project] (cwd [path])."
2. Scratch and safety rules: where temporary files go (the session scratchpad), what must not be written (the vault, user configuration directories, anything the handoff does not name), no installs, no pushes, no messages sent on the user's behalf.
3. The complete handoff text, verbatim, from PROJECT through FIRST INSTRUCTION FOR YOU.
4. Report shape: plain prose and short bullets, no em dashes, a length cap that fits the task, and a closing list of every file or URL opened, so the report preserves references even when the host exposes only the final message.

Do not paraphrase the handoff into the brief. The handoff was written to stand alone; the brief adds rules and a report shape around it.

## Dispatch

- Check the host's tool list and select an available native delegation tool or API. Follow local coordination rules and dispatch only when the user has asked or accepted the offer.
- Inherit the host's or project's model defaults unless local coordination rules specify otherwise. Use background execution only when the selected tool supports it.
- If delegation is unavailable, return the complete handoff in a single copyable code block and explain that this host cannot delegate it here.
- Description: the chip title, or an imperative phrase under 60 characters.
- After a successful dispatch, print one line saying the task is running here and the report will follow in this session. Then withdraw any chip created for the same handoff this turn with `dismiss_task`, if available.

## Relay

The host may not show subagent reports to the user. When the result is available:

- Relay the substance in the session: verdicts, findings, and recommendations in the user's terms, not a pointer to the report.
- Keep the subagent's file list; drop its tool narration.
- If the report ends with a decision for the user, state the options and a recommendation, then stop.
- If the user is on Remote Control, the relay is what they will read on the phone, so it has to stand alone.

## Common mistakes

- Offering the chip only, on the theory that a chip is "one tap" from a phone. It is not visible there.
- Assuming every host supports background execution or requires the same delegation tool or model.
- Launching the `claude` CLI from Bash. That session never appears in the desktop sidebar or in Remote Control.
- Deleting or archiving anything to tidy up before the user has seen the result.
