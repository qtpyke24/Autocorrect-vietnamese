import readline from "readline";
import { autocomplete } from "../core/autocomplete";
import { autocorrect } from "../core/autocorrect";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.setPrompt("Nhập từ: ");
rl.prompt();

rl.on("line", (line) => {
  console.log("🔹 Gợi ý:", autocomplete(line));
  console.log("🔹 Sửa lỗi:", autocorrect(line));
  rl.prompt();
});
