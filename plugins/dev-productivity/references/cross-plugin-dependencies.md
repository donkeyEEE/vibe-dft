# Cross-plugin dependencies

`dev-productivity` and `dev-engineering` are independently installable and independently useful. Run every local step without probing the current Codex skill list for the other plugin.

Check a cross-plugin dependency only when the next workflow step invokes it:

1. Preserve all local work and artifacts completed so far.
2. Name the target with its fully qualified Codex invocation, such as `$dev-engineering:setup-matt-pocock-skills`.
3. If the explicit invocation is available, continue the composed workflow normally.
4. If it is unavailable, pause only that dependent step and report the exact skill and provider.

Use this message, substituting the required skill name:

> This step requires `$dev-engineering:<skill>`. Install or enable `dev-engineering`, start a new Codex session, and resume this step. Other `dev-productivity` capabilities remain available.

Do not infer installation state from the initial Codex skills list: Codex may omit skills from that list when its context budget is full. Do not skip the cross-plugin step or implement a reduced local substitute.

Use fully qualified names for every explicit cross-plugin transition. Use `$dev-productivity:<skill>` for a productivity transition and `$dev-engineering:<skill>` for an engineering transition.
