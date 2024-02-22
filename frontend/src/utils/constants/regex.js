// String must start with alphabets
// Alphanumeric characters
// Single Space between words
// Hyphens or underscores between words with both of  them not coming together e.g [a_-d, a__d,a--d,a-_d, a_ -d, a -d, a _d] (not allowed)
// No space at the beginning of the string and No Space at the end of the string
// Only numbers are not allowed

export const ALPHA_NUMERIC_REGEX =
  /^(?! )(?=[a-zA-Z0-9])[a-zA-Z0-9]*(?:[ _-][a-zA-Z0-9]+)*$/;
export const ALPHA_NUMERIC_WITH_EXTRA_CHARACTERS_REGEX =
  /^(?! )(?=[a-zA-Z0-9])[a-zA-Z0-9]*(?:[ @.,!$+?%()_-][a-zA-Z0-9]+)*$/;

export const ALPHA_NUMERIC_REGEX_STARTING_WITH_ALPHABETS =
  /^(?! )(?=[a-zA-Z])[a-zA-Z0-9]*(?:[ _-][a-zA-Z0-9]+)*$/;

export const ALPHA_NUMERIC_WITH_FOUR_EXTRA_CHARACTERS_REGEX_STARTING_WITH_ALPHABETS =
  /^(?! )(?=[a-zA-Z])[a-zA-Z0-9]*(?:[ @._-][a-zA-Z0-9]+)*$/;

export const ONLY_ALPHABETS = /^(?! )(?=[a-zA-Z])[a-zA-Z]*(?:[ ][a-zA-Z]+)*$/;
