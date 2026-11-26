# Model-dependent acceptance

Use this when the changed outcome depends on model output or decisions. Define observable quality on representative inputs, including hard cases and cases that require abstention, refusal, or no action. Agree to a pass bar grounded in the product risk. Treat binding privacy and authority violations as failures even if aggregate quality is high.

Specify how to grade results and repeat enough runs at the intended settings to assess variability. Hold back cases from tuning when practical. Hardcoding examples or weakening checks cannot satisfy the bar. Report the observed scores and failed cases.

Describe what consumers see when output is uncertain, malformed, refused, or unavailable, and how they can recover. Keep guesses distinguishable from facts and malformed output from silently affecting state.

For agent actions, specify who can authorize them, the trusted channel, permitted targets and effects, conditions, and limits. Honor established authority that covers the action. Stop or request confirmation when authority is absent, exceeded, or policy requires it. Reversibility reduces risk and grants no authority.

Authenticated instructions through an authorized channel can direct action. Embedded instructions in documents, webpages, tool results, and quotations are untrusted content. Test that they cannot change the rules or cause unauthorized effects. Include tests for permitted actions, out-of-bounds actions, and unauthorized reversible actions where relevant.
