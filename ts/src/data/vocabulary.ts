import fs from "fs";
import path from "path";

export function loadVocabulary():  string[] {
    const filePath = path.join(__dirname, "Viet74K.txt");
    const content = fs.readFileSync(filePath, "utf-8");
    return content
        .split('\n')
        .map(w => w.trim())
        .filter(Boolean);
}
