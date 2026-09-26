export function loadConfig(argv: string[]) {
  const databaseUrl = process.env.DATASYNC_DATABASE_URL ?? "";
  const outputPath = argv.find((arg) => arg.startsWith("--output-path="))?.split("=")[1] ?? "./snapshot";
  const batchSize = Number(process.env.DATASYNC_BATCH_SIZE ?? 500);
  return { databaseUrl, outputPath, batchSize, compress: argv.includes("--compress") };
}
