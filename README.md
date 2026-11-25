# Florida Election Analysis: a plain-language guide

**Start here if this is your first time.** This page explains, without the math, what this project is, where every number came from, and how to check it yourself.

> **\*2026 figures are UNOFFICIAL.** They are the Florida Division of Elections (DOS) Florida Election Watch county returns for the Nov 3, 2026 general election. 2022 figures are DOS official results. Governor race only. Denominator: ballots cast (DOS county turnout) in both years. Registration: DOS book-closing active registered voters by party (Oct 11, 2022; Oct 5, 2026). Population (sort order only): U.S. Census Bureau Vintage 2025. These pages measure a pattern; they make no claim about intent, fraud or cause.

## What is this?

This project compares the 2022 and 2026 races for Governor of Florida, county by county, for all 67 counties. It asks one simple question:

> **Did the Democratic candidate's share of the ballots change by more or less than the Democratic Party's share of registered voters?**

If a party loses registered voters but its candidate's share of the vote goes up, those two numbers have moved apart. This project measures how far apart, in every county.

It is part of a state-by-state series that uses the same method, which Morissa Benson developed in Nebraska. It began with her [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit). Each state uses only its own numbers.

## Where the numbers came from

**Every number comes directly from the Florida Division of Elections' official websites:**

- **dos.fl.gov**: the book-closing reports showing how many active registered voters each party had in each county (Oct 11, 2022 and Oct 5, 2026)
- **results.elections.myflorida.com**: the official 2022 governor results and 2022 ballots cast, county by county
- **floridaelectionwatch.gov**: the 2026 governor results and 2026 ballots cast, county by county (*2026 unofficial)

Nothing was estimated, and no other source was mixed in.

**You can check the underlying data yourself.** The sidebar links to the **Florida County PDF**, a table of all 67 counties showing registered Democrats, Democratic votes and ballots cast in both years, with the changes. [Open the county PDF here](https://raw.githubusercontent.com/mbenson8989/Florida-Election-Analysis/main/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf).

## What reverse-factoring does, in plain terms

For each county, in each year, Morissa compares two percentages:

1. **The Democratic share of the ballots**: of everyone who cast a ballot, what percent voted for the Democratic governor candidate.
2. **The Democratic share of registration**: of everyone registered, what percent are registered Democrats.

**The difference between them is the "surplus."** If Democrats are 30% of registered voters but the Democratic candidate gets 48% of the ballots, the surplus is 18 points. Then she compares 2022 with 2026 to see how much the surplus grew or shrank, and works backward ("reverse-factoring") to ask how many votes that change represents.

**What Florida shows:**

- Statewide, the Democratic share of ballots went from 39.84% in 2022 to 48.30% in 2026, while the Democratic share of registration went from 34.28% to 30.25%.
- So the statewide surplus grew from +5.56 to +18.04 points.
- The surplus grew in all 67 counties, and every county had fewer registered Democrats in 2026 than in 2022.
- There were no counties where votes added up to more than the ballots cast, in either year.

## How Morissa derived the numbers

- **County by county.** All 67 counties were computed one at a time from the state's own files.
- **Checked twice, independently.** Two separate programs, written differently and reading the numbers from different copies of the state's reports where the state publishes them twice, computed every figure from scratch. Every number had to match exactly, to the last decimal, before anything was published. County totals were also checked against the state's own statewide totals.
- **Florida's own line.** She graphed every county's surplus against its Democratic registration share and fitted a straight line through the points: **S = m × (D/100) + b**. Here D is the Democratic share of registration, **m** (the multiplier) says how much the surplus tends to change as the Democratic share of registration changes, and **b** (the offset) is where the line starts. For Florida, the 2022 line is S = -12.80 × (D/100) + 2.31 and the 2026 line is S = 24.64 × (D/100) + 4.87. In Florida, registration share explains little of the difference between counties, so the line is a loose fit. The [Locked Florida Formula](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Locked-Florida-Formula) page shows exactly how loose.

## This is a hypothesis, not a settled fact

These numbers measure a **pattern**. They do not prove fraud, error or intent by anyone. Ordinary things can also move them: people voting across party lines, changes in who turned out, people moving, and voter-roll cleanups (Florida's total active registration fell by 799,483 between the two reports).

Morissa's view is that election manipulation, if it exists, would be **multifaceted**: several methods working together, not a single trick. This analysis is **one lens** on that question. Her hypothesis, which is not proven, names four possible pieces:

1. **USB batch-acceptance overrides**: update media used to make systems accept batches they otherwise would not
2. **An absentee batch chain-of-custody gap**: absentee ballot batches moving without a complete custody record
3. **Ghost voters fed with real voter data**: registrations that use real people's information
4. **Cloud-layer number swaps**: totals changed in the reporting layer after counting

Each of these is a hypothesis to be tested with records, not a finding of this project. For the story behind the numbers and why she thinks these pieces fit together, read her write-up: **[The Burden Just Flipped](https://moebenson.substack.com/p/the-burden-just-flipped)**.

## Where to go next

| Page | What you'll find |
|---|---|
| [Home](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Home) | Overview and statewide numbers |
| [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) | Where the method began (Nebraska) |
| [Floor and Ceiling](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Floor-and-Ceiling) | The counties at the top and bottom |
| [Reverse Math](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Reverse-Math) | One county, then the ten largest, then all 67 |
| [Graphs](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Graphs) | All charts |
| [Florida County PDF Information](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Florida-County-PDF-Information) | The downloadable 67-county table |
| [Locked Florida Formula](https://github.com/mbenson8989/Florida-Election-Analysis/wiki/Locked-Florida-Formula) | Florida's surplus equation and a fill-in worksheet |

## Hash verification: proving the files are unchanged

Every file the state published that this project used is saved, unchanged, in the [`raw/`](https://github.com/mbenson8989/Florida-Election-Analysis/tree/main/raw) folder of the repository. Each one has a **SHA-256 fingerprint**: a 64-character code that changes completely if even one character of the file changes. If your fingerprint matches the one below, your copy is identical to the one used here.

**How to check:** download the file from the repository, then run `sha256sum <file>` (Mac or Linux) or `Get-FileHash <file> -Algorithm SHA256` (Windows PowerShell) and compare. The state sometimes updates files at the same address, so a fresh download from the state site can differ from the copy saved on the date listed in [MANIFEST.md](https://github.com/mbenson8989/Florida-Election-Analysis/blob/main/MANIFEST.md).

| File in `raw/` | Source | SHA-256 |
|---|---|---|
| `raw/20261103_ElecResultsFL.txt` | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL.txt?v=52821560 | `6da5bdddd2f6dbd05e5f20b3a0f9e35dd64ef969401ed27ff3d4cc708035da90` |
| `raw/20261103_ElecResultsFL.xls` | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL.xls?v=52821560 | `6da5bdddd2f6dbd05e5f20b3a0f9e35dd64ef969401ed27ff3d4cc708035da90` |
| `raw/20261103_ElecResultsFL_PipeDlm_Info.txt` | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL_PipeDlm_Info.txt?v=52821560 | `7311ccd89e95411b07ebe3ca6ae17830dd6e34bca5a38136adc24ffe94bfc9fe` |
| `raw/20261103_ElecResultsFL_PipeDlm_Votes.txt` | https://flelectionfiles.floridados.gov/enightfilespublic/20261103_ElecResultsFL_PipeDlm_Votes.txt?v=52821560 | `a8a8365475a472ff43a67a80ee7eac96a0289479b1140548ea2681668db52bd7` |
| `raw/ResultsFileLayoutPipeDelimited.pdf` | https://flelectionfiles.floridados.gov/enightfilespublic/ResultsFileLayoutPipeDelimited.pdf?v=52821560 | `1d9359422347c65da59c915c558411a0b3f0a94c988a552d64a2b89b3f2e1814` |
| `raw/bookclosing_2022gen_1_party_by_county.pdf` | https://files.floridados.gov/media/706001/1-by-party-by-county.pdf | `a2a1e25a4cce642de71713b960b2aa9b337a6c48952b859657ff1610440e9886` |
| `raw/bookclosing_2022gen_3_party_by_county_by_race.pdf` | https://files.floridados.gov/media/706005/3-by-party-by-county-by-race.pdf | `37fd26098fcca8848156f236062bce6641d418a95954bc67f2dfbd39a73ebf0f` |
| `raw/bookclosing_2026gen_1_party_by_county.pdf` | https://dos.fl.gov/media/711452/1-party-by-county.pdf | `00e87ffee4e26e083ead52dbbcbd72fd59ff072326071062bcf684d31872d9e9` |
| `raw/bookclosing_2026gen_1_party_by_county.xlsx` | https://dos.fl.gov/media/711453/1-party-by-county.xlsx | `4784f9f82e2074dbfde75403fcef1424302674add5195b7964176ad8961aac52` |
| `raw/bookclosing_2026gen_3_party_by_county_by_race.xlsx` | https://dos.fl.gov/media/711457/3-party-by-county-by-race.xlsx | `336fc66c2bcf282d091531a53b12ac65f329d8bef8ece7c872e38801b325503d` |
| `raw/dos_bookclosing_page.html` | https://dos.fl.gov/elections/data-statistics/voter-registration-statistics/bookclosing/ | `d9270fcdbc0bd7008b3c56cb788c66757cf50f1bc4f33dd9d392f8d86499200c` |
| `raw/dos_voter_turnout_page.html` | https://dos.fl.gov/elections/data-statistics/elections-data/voter-turnout/ | `440dec73d5974730198e08bae873b9e29a07d902a37e7999436cd52c1d5dc6bd` |
| `raw/few_CountyReportingStatus.html` | https://floridaelectionwatch.gov/CountyReportingStatus | `35413739f9ee1b6b78fefd9c4fa9ad6246f3efa0357a69c1198033d14a58fb6d` |
| `raw/few_Downloads.html` | https://floridaelectionwatch.gov/Downloads | `374e7172658a4b1d5aeebe34ae53a4a9c6bc0c0427050d148f62622c3561b747` |
| `raw/few_ElectionDayTurnout.html` | https://floridaelectionwatch.gov/ElectionDayTurnout | `9d9b4cacb18ea23c12788e683e6cd515b60a37d36e869265151c36a52016fa80` |
| `raw/few_Timeline.html` | https://floridaelectionwatch.gov/Timeline | `0085a24aa3b83232f0c596faf822f5e2ccb70cbe24f9426d6bd42e3dbd16a179` |
| `raw/few_gov_by_county_2026.html` | https://floridaelectionwatch.gov/ContestResultsByCounty/160000 | `ae7093ec9d26581ecb36e728c9839779e9b6b9e8b0c8fa47eb7edd8ff66440fb` |
| `raw/few_governor_statewide_2026.html` | https://floridaelectionwatch.gov/StateOffices/Governor | `69364ba761dc08920b3c48b8986a5f393264688aa768d71135e19367477a808a` |
| `raw/few_home.html` | https://floridaelectionwatch.gov/ | `996641edbd14d5dbb7e20070d877823640096a89b00623070dcc86a99ab4bb91` |
| `raw/few_trackcounty_ALA.html` | https://floridaelectionwatch.gov/TrackCounty/ALA | `6c25d2d43d07e4c2b60ce7a1c338ce12205e3379d265efd4ab3b05544fdf0939` |
| `raw/fl_gov_detail_20221108.html` | https://results.elections.myflorida.com/DetailRpt.Asp?ELECTIONDATE=11/8/2022&RACE=GOV&PARTY=&DIST=&GRP=&DATAMODE= | `d135b0fe8c7ce367fcc2d76443fe9290f59886a94cecf06c32edd4e073d22dbf` |
| `raw/fl_results_20221108_extract.txt` | POST https://results.elections.myflorida.com/ResultsExtract.Asp (ElectionDate=11/8/2022, OfficialResults=Y, PartyRaces=N) | `38dc8a11148b4ac6b7c020299e44346df51892c1dc115e549b6697e488b6cd3a` |
| `raw/fl_turnout_20221108.html` | https://results.elections.myflorida.com/TurnoutRpt.asp?ElectionDate=11/8/2022&DATAMODE= | `a7bfb88c5e6c3f2bc6d6c0cfc5b68917aaa4cfd0016285f832d9f9fb20b0c1dc` |
| `raw/home_results.html` | https://results.elections.myflorida.com/ | `d99f120d3eb0e5073701f78c16c20c4caa97685e5bdb44c4635543bb9d4e8eaa` |
| `raw/results_11-8-2022.txt` | https://results.elections.myflorida.com/downloadresults.asp?ElectionDate=11/8/2022&DATAMODE= | `85f1c41bc59705eba648733854172004c02e369d30c693fd792301b90aa9580b` |
| `raw/vr_archive_2022.zip` | https://dos.fl.gov/media/709149/2022-archived.zip | `411d00366375bd77c61c9837fc2f583b1cf66cc37638474e61c189a857404580` |

Published outputs:

| File | SHA-256 |
|---|---|
| `pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf` | `64779e475c0d6574a0497d539e4c13451c105f29bc1d43b44faabb0b08531f88` |
| `data/florida_governor_2022_2026_by_county.csv` | `e88b1f2dacf0940eb94cf76941507e368eb9eada52528d21143df23a1ec79c55` |

## Disclaimers

1. **This measures a pattern, not a cause.** It makes no claim about intent, fraud or wrongdoing by any person, office or party.
2. **Votes are not voters.** "Democratic votes" counts votes for the Democratic governor ticket, not registered Democrats who voted.
3. **Florida only.** No other state's numbers are used in any Florida figure.
