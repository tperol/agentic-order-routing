# Claude Code Usage Monitoring Guide

This document provides guidance on monitoring and managing Claude Code usage in this repository.

## Monitoring API Usage

### GitHub Actions Dashboard
- All Claude Code runs are logged in the GitHub Actions tab
- Each run shows:
  - Trigger event (issue/PR comment)
  - Run duration
  - Success/failure status
  - Detailed logs of Claude's actions

### Cost Tracking
1. **Set up usage alerts** in your Anthropic console:
   - Log in to [console.anthropic.com](https://console.anthropic.com)
   - Navigate to Usage & Billing
   - Set up spending alerts at appropriate thresholds

2. **Regular usage reviews**:
   - Check weekly API usage in Anthropic console
   - Review GitHub Actions run frequency
   - Identify any unusual spikes in activity

### Best Practices for Cost Management

1. **Limit allowed tools**: The workflow now includes specific allowed tools to prevent unnecessary operations
2. **Monitor for abuse**: Watch for:
   - Excessive @claude mentions
   - Automated or bot-triggered mentions
   - Unusually long-running operations

3. **Set up branch protection**: Consider limiting Claude Code to specific branches if needed

## Usage Metrics to Track

- **Monthly API calls**: Total number of Claude invocations
- **Average tokens per run**: Monitor in Anthropic console
- **Most common use cases**: Review GitHub Actions logs to understand usage patterns
- **User engagement**: Which team members use Claude most frequently

## Optimization Tips

1. **Batch requests**: Encourage users to include multiple tasks in a single @claude mention
2. **Clear instructions**: Well-defined requests reduce back-and-forth and token usage
3. **Use for appropriate tasks**: Claude is best for:
   - Code reviews and improvements
   - Bug fixes
   - Documentation updates
   - Test writing
   - Refactoring suggestions

## Setting Up Dashboards

Consider creating a simple dashboard using GitHub Actions API:
```bash
# Example: Get recent Claude runs
gh api /repos/tperol/agentic-order-routing/actions/workflows/claude.yml/runs \
  --jq '.workflow_runs[] | {created_at, status, conclusion}'
```

## Emergency Controls

If usage spikes unexpectedly:
1. Temporarily disable the workflow by renaming `.github/workflows/claude.yml`
2. Review recent runs for unusual activity
3. Consider adding rate limiting through workflow conditions