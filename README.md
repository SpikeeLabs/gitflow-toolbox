# gitflow-toolbox

A simple toolkit to aggregate Gitflow tools and simplify their error handling

## During development

### First setup

```shell
poetry install
poetry run pre-commit install --install-hook
poetry run pre-commit install --install-hooks --hook-type commit-msg
```

### Test && Coverage

To run all tests and retrieve coverage

```shell
# Remove previous run
coverage erase

# Run test and collect coverage
coverage run

# Generate HTML report
coverage html

# Console coverage report
coverage report -m
```

or

```shell
coverage erase && coverage run && coverage html && coverage report -m
```

## VS Code

```json
{
  "python.linting.enabled": true,
  "python.linting.pylamaEnabled": true,

  "python.formatting.provider": "black",
  "python.formatting.blackArgs": [
    "--exclude",
    "((.git|.tox|migrations))",
    "--include",
    ".pyi?$",
    "--line-length",
    "120"
  ],
  "editor.formatOnSave": true
}
```
