import path from 'node:path';
import { fileURLToPath } from 'node:url';
export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const site = path.join(root, 'site');
export const dist = path.join(root, 'dist');
