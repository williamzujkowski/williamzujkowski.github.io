#!/usr/bin/env node
// The Astro CLI backgrounds itself in agent sessions. Playwright needs to own
// a foreground process. Its documented preview API is experimental; keep this
// adapter small and verify it when upgrading Astro.
import { fileURLToPath } from 'node:url';
import { preview } from 'astro';

const port = Number(process.env.PLAYWRIGHT_PORT ?? 4321);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error('PLAYWRIGHT_PORT must be an integer between 1 and 65535');
}

const server = await preview({
  root: fileURLToPath(new URL('../', import.meta.url)),
  server: { host: '127.0.0.1', port, open: false },
  vite: { preview: { strictPort: true } },
});

let stopping = false;
async function stop() {
  if (stopping) return;
  stopping = true;
  try {
    await server.stop();
  } catch (error) {
    console.error(error);
    process.exitCode = 1;
  }
}
process.once('SIGINT', stop);
process.once('SIGTERM', stop);
await server.closed();
