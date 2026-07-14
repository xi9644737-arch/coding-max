// Static smoke checks; do not render framework components.
import { describe, it, expect } from "vitest";
import { existsSync, readFileSync } from "fs";
import { join } from "path";

const SRC_DIR = join(__dirname, "..", "src");
const INDEX_TS = join(SRC_DIR, "index.ts");

describe("smoke", () => {
  it("has an entry file", () => {
    expect(existsSync(INDEX_TS)).toBe(true);
  });

  it("has a non-empty entry file", () => {
    const content = readFileSync(INDEX_TS, "utf-8");
    expect(content.length).toBeGreaterThan(0);
    // Verify a public export exists.
    expect(content).toContain("export");
  });

  it("defines formatUser", () => {
    const content = readFileSync(INDEX_TS, "utf-8");
    expect(content).toContain("formatUser");
  });

  it("has no empty catch block", () => {
    const content = readFileSync(INDEX_TS, "utf-8");
    // Match only an empty catch body, not a normal catch binding.
    const bareCatch = /catch\s*\(\s*\w*\s*\)\s*\{\s*\}/g;
    expect(bareCatch.test(content)).toBe(false);
  });
});
