# Tape file for VHS recording of the train-bookings Skill
Output showcase/demo.gif

Set Shell "bash"
Set FontSize 18
Set Width 1200
Set Height 600
Set Padding 40
Set WindowBar Colorful
Set WindowBarSize 40
Set BorderRadius 10
Set Theme "Oceanic-Next"

# Simulate Gemini CLI interaction
Type "# Let's use RailSkeptic as a Gemini CLI Skill..."
Sleep 500ms
Enter

Type "gemini"
Sleep 300ms
Enter
Sleep 500ms

Type "Find available tickets for Ahmedabad to Delhi on May 3"
Sleep 1s
Enter

# Simulate the agent's cross-verification process
Type "# Agent is cross-verifying Paytm and ConfirmTkt data..."
Sleep 2s
Enter

# Show the results (simulated based on actual multi_scraper output)
Type "python3 multi_scraper.py --source ADI --dest NDLS --date 20260503"
Sleep 500ms
Enter

# Wait for results to render
Sleep 15s

Type "# Notice the Tatkal protection and cross-source verified scores."
Sleep 2s
Enter

Type "# Ready for automation!"
Sleep 3s
Enter
