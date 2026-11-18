// Every scenario in spec/ is carried by a test that names its id in brackets.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const read = (dir, ext) =>
  readdirSync(dir, { recursive: true })
    .filter((f) => String(f).endsWith(ext))
    .map((f) => readFileSync(join(dir, String(f)), "utf8"))
    .join("\n");
const ids = [...read("spec", ".feature").matchAll(/Scenario: (\S+)/g)].map((m) => m[1]);
const tests = read("test", ".ts");
const missing = ids.filter((id) => !tests.includes(`[${id}]`));
if (missing.length) {
  console.error(`scenarios without a test: ${missing.join(", ")}`);
  process.exit(1);
}
console.log(`${ids.length} scenarios, each with a test`);
