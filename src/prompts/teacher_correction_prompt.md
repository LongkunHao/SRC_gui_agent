Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: You are interacting with a web application at {{server_url}}. {{task}}

NOTE FROM REVIEWER: the previous student attempt was just ROLLED BACK. Reason: {{rollback_reason}}
Take a corrective action that avoids repeating that mistake.

If the current screen already satisfies the task, terminate with success instead of clicking or toggling an already-correct control.

Do not repeat a failed pattern. If recent attempts repeatedly clicked, scrolled, hovered, waited, or navigated without reaching the needed state, choose a materially different strategy.

If the target item, setting, record, or control is not visible after repeated manual navigation, consider using an in-app search, filter, address/search field, command palette, settings search, or other query mechanism when one is available. This guidance is application-agnostic: use whatever query/navigation affordance the current UI actually exposes.

When using a query strategy, output a real executable action, not just a plan. If the field is already focused, use action=type with the exact text to enter. If it is not focused, click the field or control that will focus/open it now. Use action=key with Enter only when the current UI focus makes that key press meaningful.

Prefer one concrete progress-making action. Avoid vague clicks, tiny scrolls that are unlikely to change the screen, and repeated attempts at the same coordinate unless the screenshot clearly shows the previous action failed to take effect.

Previous actions:
{{previous_actions}}
