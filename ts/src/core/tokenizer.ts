export function tokenize(input: string): string[] {
  return input.toLowerCase().split(/\s+/);
}
