import { loadVocabulary } from "../data/vocabulary";
import { tokenize } from "./tokenizer";

const vocabulary = loadVocabulary();

export function autocomplete(input: string): string[] {
  const tokens = tokenize(input);
  const lastWord = tokens[tokens.length - 1];

  return vocabulary
    .filter(word => word.startsWith(lastWord))
    .slice(0, 10);
}
