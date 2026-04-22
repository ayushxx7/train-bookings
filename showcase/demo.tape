# Tape file for VHS recording of the train-bookings CLI
Output showcase/demo.gif

Set Shell "bash"
Set FontSize 16
Set Width 1200
Set Height 600
Set Padding 40
Set WindowBar Colorful
Set WindowBarSize 40
Set BorderRadius 10

Type "# Let's search for trains from Ahmedabad (ADI) to Delhi (NDLS)"
Sleep 500ms
Enter

Type "python3 multi_scraper.py --source ADI --dest NDLS --date 20260503"
Sleep 1s
Enter

# Wait for results to come in (fetching)
Sleep 15s

Type "# Notice how the results are cross-verified and Tatkal status is checked."
Sleep 2s
Enter

Type "# Ready for automation!"
Sleep 3s
Enter
