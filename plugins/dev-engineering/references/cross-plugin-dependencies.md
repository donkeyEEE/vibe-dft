# Cross-plugin dependencies

`dev-engineering` and `dev-productivity` are independently installable and independently useful. Run every local step without probing the current Codex skill list for the other plugin.

Check a cross-plugin dependency only when the next workflow step invokes it:

1. Preserve all local work and artifacts completed so far.
2. Name the target with its fully qualified Codex invocation, such as `$dev-productivity:grilling`.
3. If the explicit invocation is available, continue the composed workflow normally.
4. If it is unavailable, pause only that dependent step and report the exact skill and provider.

Use this message, substituting the required skill name:

> This step requires `$dev-productivity:<skill>`. Install or enable `dev-productivity`, start a new Codex session, and resume this step. Other `dev-engineering` capabilities remain available.

Do not infer installation state from the initial Codex skills list: Codex may omit skills from that list when its context budget is full. Do not skip the cross-plugin step or implement a reduced local substitute.

Use fully qualified names for every explicit cross-plugin transition. Use `$dev-engineering:<skill>` for an explicit engineering transition and `$dev-productivity:<skill>` for a productivity transition.
