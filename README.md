# NSQ Medicines: India's drug quality alerts as data

Every month, India's national drug regulator, the Central Drugs Standard Control Organization (CDSCO),
publishes lists of medicine batches that failed quality testing ("Not of Standard Quality", NSQ) or were
found to be spurious (counterfeit). This repository collects those lists in machine-readable form.

**Data last collected: 20 October 2026.**

| File | What it is | Rows | Covers |
|---|---|---|---|
| [`data/raw/portal_batches.csv`](data/raw/portal_batches.csv) | One row per reported batch, from CDSCO's online NSQ portal | 6,674 | NSQ: Jan 2019 – Aug 2026<br>Spurious: Jun 2025 – Aug 2026 |
| [`data/raw/pdf_index.csv`](data/raw/pdf_index.csv) | One row per monthly alert PDF, with its link and SHA-256 hash | 197 | Feb 2013 – Jun 2025 |

## Where the data comes from

Everything comes from public pages of CDSCO (Directorate General of Health Services, Ministry of Health &
Family Welfare, Government of India). No login was needed or used.

1. **CDSCO's online NSQ portal**: <https://cdsco.gov.in/opencms/opencms/en/Notifications/nsq-drugs/>.
   This page embeds a table hosted at `cdscoonline.gov.in` that lists, for each reporting month, the batches
   reported as NSQ or spurious by CDSCO's own laboratories and by state drug testing laboratories.
   `portal_batches.csv` holds every month the portal offers: 6,626 NSQ batches over 92 months and 48
   spurious batches over 14 months.

2. **Monthly alert PDFs**: <https://cdsco.gov.in/opencms/opencms/en/Alerts/> (the same list also appears
   under `/en/Notifications/Alerts`). Until June 2025 each month's alert was published as a PDF. On
   28 August 2025 CDSCO posted a notice that NSQ alerts were now available at a new link, the portal above.
   `pdf_index.csv` lists the 197 monthly drug alert PDFs from that page, with each file's direct link and
   SHA-256 hash so any copy can be checked against the original. The PDFs themselves are not in this repository.

The data was collected by a script that requested pages slowly (one request every 2.5 seconds).

## What the data means

- **Not of Standard Quality (NSQ)**: a sample failed one or more tests in its official standard, for example
  *dissolution* (how well a tablet releases its medicine), *assay* (how much active ingredient it contains)
  or *description* (appearance). NSQ does not mean fake, and on its own it does not mean dangerous.
- **Spurious**: defined in Section 17-B of the Drugs and Cosmetics Act, 1940. Broadly, a drug made under
  another drug's name, imitating another drug, or claiming to come from a manufacturer that did not make it.
  Spurious batches often carry the name of a real company that had nothing to do with them. CDSCO's portal
  does not show that company for spurious batches, and neither does this dataset. Product names can still
  include a brand name, e.g. "(TELMA AM)".
- **Central and state**: samples are tested either by CDSCO's own laboratories (*central*) or by state drug
  testing laboratories (*state*). CDSCO has published the two separately since May 2024.
- **Revised lists**: some months were re-issued as a "Revised" list. Both versions are listed in `pdf_index.csv`.

## Files

### `data/raw/portal_batches.csv`

| Column | Meaning |
|---|---|
| `id` | Row ID: a hash of the row's fields. An exact repeat of another row gets a `-2` suffix. |
| `alert_month` | Reporting month shown by the portal (`YYYY-MM`) |
| `category` | `nsq` or `spurious` |
| `source_type` | `central` (CDSCO labs) or `state` (state labs); blank where the portal says "Not applicable" |
| `drug_name_raw` | Product name as published |
| `batch_no` | Batch number as published |
| `mfg_date`, `expiry_date` | Manufacturing and expiry month (`YYYY-MM`), parsed from the published text |
| `manufacturer_raw` | Manufacturer name and address as published. For spurious batches this is the real maker as CDSCO shows it, so far always "Under Investigation". |
| `failure_raw` | The test or tests the sample failed, as published |
| `firm_reply` | Spurious batches only: the reply from the company named on the label |
| `reporting_source_raw` | Reporting source as published ("CDSCO lab", "State Lab", ...) |
| `reporting_lab` | Laboratory or state authority that reported the batch |
| `mfg_date_raw`, `expiry_date_raw` | Dates exactly as published |

### `data/raw/pdf_index.csv`

| Column | Meaning |
|---|---|
| `title` | Title as listed on the CDSCO page (broken character encoding repaired) |
| `alert_month` | Month the alert covers (`YYYY-MM`), parsed from the title |
| `source_type` | `central`, `state`, or `old_combined`: the single monthly list published before May 2024 |
| `is_revised` | `True` if the title says Revise/Revised |
| `release_date` | Date listed on the CDSCO page |
| `pdf_url` | Direct link to the PDF |
| `link_url` | CDSCO's download link for the row (opens a page that displays the PDF) |
| `file` | File name used for the downloaded copy, e.g. `2025-03_central.pdf`. Revised lists get `_revised`; further lists for the same month get `_2`, `_3`. |
| `local_path`, `sha256`, `bytes` | Where the copy was stored when collected (not in this repository), its SHA-256 hash and its size |

The CDSCO alerts page also lists spurious drug lists, medical device alerts and other notices. Only the
monthly drug alert lists are included here.

### `scripts/sync_from_grab.py`

Copies a fresh collection into this repository. It reads the output of the maintainer's local collection
tool, so it will not run elsewhere as is.

## Where it can be used

- **Checking a batch**: pharmacists, hospitals, procurement teams and patients can look up a batch number
  or product name to see whether it appears on a CDSCO list. A batch that is not listed has not necessarily
  been tested: only a small share of batches is ever sampled.
- **Journalism and research**: how reported failures change over time, which tests fail most often,
  and how central and state reporting compare.
- **Public health and pharmacovigilance**: linking quality failures to adverse event reports, recalls
  or procurement records.
- **Software**: a batch search page, notifications when new batches are listed, or joins with other
  drug databases.
- **Teaching**: a real, messy public dataset, with inconsistent spellings, missing dates and two eras of publishing.

## Read this before drawing conclusions

1. **Samples are not random.** Drug inspectors choose what to sample, often where they suspect a problem.
   Counts cannot be read as a company's or a state's failure rate.
2. **More reports can mean more reporting.** Reports from state labs to the portal grew sharply, from 125
   state-reported NSQ batches in 2019 to 1,185 in 2025. A rising count may reflect better reporting rather
   than worse medicines.
3. **NSQ is not "fake".** Many failures are a single test slightly outside its limits.
4. **Don't blame the brand for spurious batches.** The company printed on a spurious medicine's label
   usually says it did not make it. That is why the real maker is often listed as "Under Investigation".
5. **The data is as published.** Spellings, errors and inconsistencies in CDSCO's lists are kept. Check the
   original source before acting on any single row.
6. **This is not medical advice.** If you have an affected batch, ask a pharmacist or doctor, and don't stop
   a prescribed medicine without advice.

## Known data issues

In `portal_batches.csv`:

- 5 rows have a blank `source_type` because the portal gives the source as "Not applicable".
- 104 rows have no manufacturing date and 109 have no expiry date.
- 13 rows show a manufacturing date later than the expiry date, as published.
- 17 rows are exact repeats of another row in the same month. They are kept, and their `id` ends in `-2`.
- Product, manufacturer and lab names are not yet standardised. The same company appears under many
  spellings, and manufacturer names include addresses.

The contents of the PDFs (2013 – 2025) have not yet been extracted into rows.

## Source and credit

Source: Central Drugs Standard Control Organization (CDSCO), Government of India, <https://cdsco.gov.in>.
This is an independent project, not affiliated with or endorsed by CDSCO.

Found a row that doesn't match CDSCO's source? Please open an issue.
