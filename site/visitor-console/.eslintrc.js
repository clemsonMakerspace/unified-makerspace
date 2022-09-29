module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ["eslint:recommended", "prettier"],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: "module",
  },
  plugins: ["react", "prettier", "@typescript-eslint"],
  rules: {
    "prettier/prettier": "error",

    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": "off",

    eqeqeq: ["error", "always"],
    "prettier/prettier": [
      "error",
      {
        "endOfLine": "auto"
      },
    ],
  },
};
