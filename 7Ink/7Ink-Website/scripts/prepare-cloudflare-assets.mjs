import { cpSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import { join } from "node:path";

const rootDir = process.cwd();
const outDirName = ".assets";
const outDir = join(rootDir, outDirName);

const copyDirectories = [
  "admin",
  "api",
  "assets",
  "cpanel",
  "forms",
  "javascripts",
  "stylesheets"
];

const copyFiles = ["vercel.json"];

function cleanOutputDirectory() {
  rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });
}

function copyRootHtmlFiles() {
  const items = readdirSync(rootDir);

  for (const item of items) {
    if (!item.toLowerCase().endsWith(".html")) continue;

    const source = join(rootDir, item);
    if (!statSync(source).isFile()) continue;

    const destination = join(outDir, item);
    cpSync(source, destination);
  }
}

function copyKnownDirectories() {
  for (const dir of copyDirectories) {
    const source = join(rootDir, dir);
    if (!existsSync(source) || !statSync(source).isDirectory()) continue;

    const destination = join(outDir, dir);
    cpSync(source, destination, { recursive: true });
  }
}

function copyKnownFiles() {
  for (const file of copyFiles) {
    const source = join(rootDir, file);
    if (!existsSync(source) || !statSync(source).isFile()) continue;

    const destination = join(outDir, file);
    cpSync(source, destination);
  }
}

cleanOutputDirectory();
copyRootHtmlFiles();
copyKnownDirectories();
copyKnownFiles();

console.log(`Prepared ${outDirName} for Cloudflare deploy.`);
