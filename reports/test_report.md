# Test Report

**Generated:** 2025-09-20T20:36:13-04:00

## Summary

- **Total Test Categories:** 3
- **Passed:** 1
- **Failed:** 2

## Category Results

### Unit Tests: ❌ FAIL

**Summary:** 2 failed, 6 passed in 0.45s

**Errors:**
```
/home/william/.pyenv/versions/3.12.3/lib/python3.12/site-packages/pytest_asyncio/plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))

```

### Integration Tests: ❌ FAIL

**Summary:** 1 failed, 7 passed in 0.65s

**Errors:**
```
/home/william/.pyenv/versions/3.12.3/lib/python3.12/site-packages/pytest_asyncio/plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))

```

### Smoke Tests: ✅ PASS

**Summary:** 9 passed, 2 warnings in 5.60s


## Test Coverage

To generate coverage report:
```bash
pytest --cov=scripts --cov-report=html --cov-report=term
```

## Next Steps

1. Fix any failing tests
2. Add more test coverage for uncovered code
3. Set up continuous integration to run tests automatically
4. Configure test reporting in GitHub Actions
