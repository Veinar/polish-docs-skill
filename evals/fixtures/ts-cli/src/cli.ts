import { loadConfig } from "./config-loader";
import { exportSnapshot, syncTables } from "./sync-engine";

export interface SyncOptions {
  databaseUrl: string;
  batchSize: number;
  dryRun: boolean;
}

export async function runCli(argv: string[]): Promise<number> {
  const config = loadConfig(argv);
  const commandName = argv[2];
  if (commandName === "export") {
    return exportSnapshot(config.databaseUrl, config.outputPath, { compress: config.compress });
  }
  const result = await syncTables(config);
  return result.failedTables.length === 0 ? 0 : 3;
}
