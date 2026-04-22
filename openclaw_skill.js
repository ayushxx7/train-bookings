import { execSync } from 'child_process';
import path from 'path';

export const skill = {
  name: "find_train_tickets",
  description: "Scrapes and ranks train tickets from ADI to NDLS for a specific date using Paytm and ConfirmTkt.",
  parameters: {
    type: "object",
    properties: {
      source: { type: "string", description: "Source station code (e.g., ADI)", default: "ADI" },
      dest: { type: "string", description: "Destination station code (e.g., NDLS)", default: "NDLS" },
      date: { type: "string", description: "Date in YYYYMMDD format", default: "20260503" }
    }
  },
  execute: async ({ source, dest, date }) => {
    // Path to your project directory
    const projectDir = "/Users/air/thevibecoder/projects/self/train-bookings";
    const venvPython = path.join(projectDir, "venv/bin/python3");
    const scriptPath = path.join(projectDir, "multi_scraper.py");

    try {
      const command = `${venvPython} ${scriptPath} --source ${source} --dest ${dest} --date ${date}`;
      console.log(`Executing: ${command}`);
      
      const output = execSync(command, { encoding: 'utf-8', cwd: projectDir });
      
      // Also read the JSON results for structured data if needed
      const fs = await import('fs');
      const resultsPath = path.join(projectDir, "multi_source_results.json");
      const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));

      return {
        summary: output,
        data: results
      };
    } catch (error) {
      return { error: `Failed to run scraper: ${error.message}` };
    }
  }
};
