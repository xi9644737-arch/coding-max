// 冒烟测试 — 纯静态检查，不实际渲染 React/Next.js 组件
import { describe, it, expect } from "vitest";
import { existsSync, readFileSync } from "fs";
import { join } from "path";

const SRC_DIR = join(__dirname, "..", "src");
const INDEX_TS = join(SRC_DIR, "index.ts");

describe("smoke", () => {
  it("入口文件存在", () => {
    expect(existsSync(INDEX_TS)).toBe(true);
  });

  it("入口文件语法可解析（非空）", () => {
    const content = readFileSync(INDEX_TS, "utf-8");
    expect(content.length).toBeGreaterThan(0);
    // 验证导出
    expect(content).toContain("export");
  });

  it("formatUser 函数定义存在", () => {
    const content = readFileSync(INDEX_TS, "utf-8");
    expect(content).toContain("formatUser");
  });

  it("没有裸 try-catch（空 catch 块）", () => {
    const content = readFileSync(INDEX_TS, "utf-8");
    // 检查 catch 后没有空的 {}
    const bareCatch = /catch\s*\(\s*\w*\s*\)\s*\{\s*\}/g;
    expect(bareCatch.test(content)).toBe(false);
  });
});
