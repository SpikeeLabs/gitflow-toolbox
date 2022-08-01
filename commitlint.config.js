const scope = ["gitlab", "git", "docker"];

module.exports = {
  extends: ["@commitlint/config-angular"],
  rules: {
    "body-empty": [2, "never", true],
    "scope-enum": [2, "always", scope],
  },
};
