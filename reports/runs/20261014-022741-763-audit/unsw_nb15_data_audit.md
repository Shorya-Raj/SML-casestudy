# UNSW-NB15 Prepared CSV Data Audit

Generated 2026-10-14T02:28:07+05:30 with Python 3.12.10, pandas 3.0.6, and NumPy 2.5.3.
The audit reads the prepared CSVs without editing them; processing steps are recorded below and in the JSON companion.

## Scope and target

- Source as recorded in the project log: official UNSW shared OneDrive folder, `CSV Files/Training and Testing Sets`.
- Grain: one prepared row per network-flow record, as described by the source dataset documentation.
- Target: `label`; positive class `1` means attack.
- Predictor exclusions: `label` (target), `attack_cat` (direct target-derived category), and `id` (row identifier).
- Predictor count after exclusions: 42 (3 categorical and 39 numeric candidates).
- Raw PCAP files and the incomplete archive are out of scope.

## File integrity and dimensions

| Split | Rows | Columns | Bytes | SHA-256 | Matches recorded value |
|---|---:|---:|---:|---|---|
| training | 175,341 | 45 | 32,293,018 | `BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA` | True |
| testing | 82,332 | 45 | 15,380,800 | `734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559` | True |

- Train/test columns and order match: True.
- All expected byte sizes, SHA-256 hashes, and row counts match: True.

## Target and split checks

- Labels are only 0/1 in both files: True.
- Exact full-row matches from training found in test: 0.
- Test rows with the same predictors as training after excluding `id`, `label`, and `attack_cat`: 8,541.
- Among those matched predictor rows, test rows whose label conflicts with the training label: 296.
- These overlap counts are screening diagnostics; repeated flow feature vectors are not automatically proof of invalid partitioning.
- `attack_cat` maps deterministically to `label` in both splits: True; this is why it is excluded as a direct target-derived field.

### Class distribution

| Split | Label | Rows | Share |
|---|---:|---:|---:|
| training | 1 | 119,341 | 68.06% |
| training | 0 | 56,000 | 31.94% |
| testing | 1 | 45,332 | 55.06% |
| testing | 0 | 37,000 | 44.94% |

### Attack category-to-label diagnostic

| Split | `attack_cat` value | Label counts |
|---|---|---|
| training | Analysis | 1: 2,000 |
| training | Backdoor | 1: 1,746 |
| training | DoS | 1: 12,264 |
| training | Exploits | 1: 33,393 |
| training | Fuzzers | 1: 18,184 |
| training | Generic | 1: 40,000 |
| training | Normal | 0: 56,000 |
| training | Reconnaissance | 1: 10,491 |
| training | Shellcode | 1: 1,133 |
| training | Worms | 1: 130 |
| testing | Analysis | 1: 677 |
| testing | Backdoor | 1: 583 |
| testing | DoS | 1: 4,089 |
| testing | Exploits | 1: 11,132 |
| testing | Fuzzers | 1: 6,062 |
| testing | Generic | 1: 18,871 |
| testing | Normal | 0: 37,000 |
| testing | Reconnaissance | 1: 3,496 |
| testing | Shellcode | 1: 378 |
| testing | Worms | 1: 44 |

## Missing and duplicate screening

| Split | Empty cells | Blank-like literal tokens | Duplicate complete rows | Duplicate rows excluding `id` | Rows with repeated predictors | Predictor groups with conflicting labels | Rows in conflicting groups |
|---|---:|---:|---:|---:|---:|---:|---:|
| training | 0 | 0 | 0 | 67,601 | 84,049 | 229 | 940 |
| testing | 0 | 0 | 0 | 26,387 | 34,704 | 6 | 14 |

### Per-column profile

| Column | Distinct | Empty | Blank-like token | Top values (count) |
|---|---:|---:|---:|---|

#### Training

| `id` | 175,341 | 0 | 0 | `1` (1), `2` (1), `3` (1), `4` (1), `5` (1) |
| `dur` | 74,039 | 0 | 0 | `0.000009` (23,031), `0.000003` (11,751), `0.000008` (10,634), `0.000005` (6,690), `0.000004` (5,026) |
| `proto` | 133 | 0 | 0 | `tcp` (79,946), `udp` (63,283), `unas` (12,084), `arp` (2,859), `ospf` (2,595) |
| `service` | 13 | 0 | 0 | `-` (94,168), `dns` (47,294), `http` (18,724), `smtp` (5,058), `ftp-data` (3,995) |
| `state` | 9 | 0 | 0 | `INT` (82,275), `FIN` (77,825), `CON` (13,152), `REQ` (1,991), `RST` (83) |
| `spkts` | 480 | 0 | 0 | `2` (85,200), `10` (27,200), `12` (7,019), `14` (5,051), `4` (4,700) |
| `dpkts` | 443 | 0 | 0 | `0` (84,282), `8` (17,287), `6` (12,262), `2` (9,238), `10` (6,825) |
| `sbytes` | 7,214 | 0 | 0 | `114` (39,121), `200` (23,484), `146` (4,989), `168` (3,578), `564` (3,530) |
| `dbytes` | 6,660 | 0 | 0 | `0` (84,282), `268` (11,512), `354` (9,865), `178` (4,988), `10168` (2,938) |
| `rate` | 76,991 | 0 | 0 | `111111.1072` (23,012), `333333.3215` (11,751), `125000.0003` (10,616), `200000.0051` (6,691), `250000.0006` (5,028) |
| `sttl` | 11 | 0 | 0 | `254` (114,743), `31` (39,455), `62` (17,681), `0` (3,162), `64` (181) |
| `dttl` | 6 | 0 | 0 | `0` (84,372), `252` (50,643), `29` (39,455), `60` (867), `254` (2) |
| `sload` | 80,885 | 0 | 0 | `50666664` (11,997), `88888888` (7,969), `152000000` (6,798), `57000000` (6,386), `91200000` (3,634) |
| `dload` | 77,474 | 0 | 0 | `0` (84,290), `676163.375` (58), `681992.3125` (54), `670433.125` (54), `680688.3125` (53) |
| `sloss` | 409 | 0 | 0 | `0` (95,448), `2` (30,181), `7` (14,649), `3` (8,293), `4` (5,802) |
| `dloss` | 370 | 0 | 0 | `0` (96,637), `1` (25,076), `2` (11,603), `4` (6,857), `8` (5,241) |
| `sinpkt` | 76,161 | 0 | 0 | `0.009` (26,173), `0.003` (12,030), `0.008` (11,857), `0.005` (7,037), `0.004` (5,181) |
| `dinpkt` | 74,245 | 0 | 0 | `0` (84,293), `0.007` (3,556), `0.006` (1,061), `0.002` (794), `0.008` (780) |
| `sjit` | 77,532 | 0 | 0 | `0` (88,494), `10.954517` (51), `10.954515` (49), `987.040687` (48), `1174.32875` (42) |
| `djit` | 76,831 | 0 | 0 | `0` (93,743), `360.513219` (23), `493.566937` (23), `571.17` (21), `453.78075` (21) |
| `swin` | 13 | 0 | 0 | `0` (95,395), `255` (79,935), `31` (1), `232` (1), `14` (1) |
| `stcpb` | 75,265 | 0 | 0 | `0` (96,246), `4125223812` (8), `4223830827` (6), `3795074471` (6), `2037155331` (6) |
| `dtcpb` | 75,089 | 0 | 0 | `0` (96,252), `2296510182` (15), `3330702795` (12), `531409215` (12), `1200223257` (11) |
| `dwin` | 7 | 0 | 0 | `0` (96,253), `255` (79,083), `244` (1), `70` (1), `48` (1) |
| `tcprtt` | 43,319 | 0 | 0 | `0` (96,300), `0.000665` (196), `0.00068` (179), `0.000681` (179), `0.000664` (178) |
| `synack` | 40,142 | 0 | 0 | `0` (96,300), `0.000541` (280), `0.000539` (273), `0.000536` (258), `0.000542` (248) |
| `ackdat` | 37,708 | 0 | 0 | `0` (96,301), `0.000124` (1,226), `0.000125` (1,205), `0.000123` (1,043), `0.000126` (1,007) |
| `smean` | 1,357 | 0 | 0 | `57` (40,645), `100` (23,946), `53` (5,488), `56` (5,293), `73` (5,118) |
| `dmean` | 1,328 | 0 | 0 | `0` (84,282), `45` (11,690), `44` (11,592), `89` (5,296), `565` (2,941) |
| `trans_depth` | 11 | 0 | 0 | `0` (157,501), `1` (17,747), `2` (80), `4` (3), `3` (2) |
| `response_body_len` | 2,386 | 0 | 0 | `0` (164,047), `3924` (2,768), `83` (580), `524288` (386), `109` (333) |
| `ct_srv_src` | 52 | 0 | 0 | `1` (36,250), `2` (20,630), `3` (16,683), `4` (13,312), `5` (10,804) |
| `ct_state_ttl` | 5 | 0 | 0 | `2` (82,054), `1` (49,355), `0` (40,791), `6` (1,930), `3` (1,211) |
| `ct_dst_ltm` | 50 | 0 | 0 | `1` (56,539), `2` (33,331), `3` (18,424), `4` (10,191), `16` (6,632) |
| `ct_src_dport_ltm` | 47 | 0 | 0 | `1` (92,793), `2` (24,949), `3` (9,322), `16` (8,458), `17` (6,325) |
| `ct_dst_sport_ltm` | 32 | 0 | 0 | `1` (109,640), `2` (16,029), `16` (10,619), `17` (7,781), `3` (6,945) |
| `ct_dst_src_ltm` | 54 | 0 | 0 | `1` (47,072), `2` (25,072), `3` (16,809), `4` (13,177), `5` (9,333) |
| `is_ftp_login` | 4 | 0 | 0 | `0` (172,774), `1` (2,545), `4` (16), `2` (6) |
| `ct_ftp_cmd` | 4 | 0 | 0 | `0` (172,774), `1` (2,545), `4` (16), `2` (6) |
| `ct_flw_http_mthd` | 11 | 0 | 0 | `0` (157,501), `1` (16,696), `4` (846), `9` (90), `2` (74) |
| `ct_src_ltm` | 50 | 0 | 0 | `1` (42,715), `2` (33,665), `3` (19,684), `4` (12,380), `5` (8,140) |
| `ct_srv_dst` | 52 | 0 | 0 | `1` (42,203), `2` (19,643), `3` (16,242), `4` (12,515), `5` (10,592) |
| `is_sm_ips_ports` | 2 | 0 | 0 | `0` (172,579), `1` (2,762) |
| `attack_cat` | 10 | 0 | 0 | `Normal` (56,000), `Generic` (40,000), `Exploits` (33,393), `Fuzzers` (18,184), `DoS` (12,264) |
| `label` | 2 | 0 | 0 | `1` (119,341), `0` (56,000) |

#### Testing

| `id` | 82,332 | 0 | 0 | `1` (1), `2` (1), `3` (1), `4` (1), `5` (1) |
| `dur` | 39,888 | 0 | 0 | `0.000009` (5,546), `0.000008` (4,938), `0.000003` (4,111), `0.000004` (3,336), `0.000011` (3,112) |
| `proto` | 131 | 0 | 0 | `tcp` (43,095), `udp` (29,418), `unas` (3,515), `arp` (987), `ospf` (676) |
| `service` | 13 | 0 | 0 | `-` (47,153), `dns` (21,367), `http` (8,287), `smtp` (1,851), `ftp` (1,552) |
| `state` | 7 | 0 | 0 | `FIN` (39,339), `INT` (34,163), `CON` (6,982), `REQ` (1,842), `ACC` (4) |
| `spkts` | 420 | 0 | 0 | `2` (36,982), `10` (16,386), `12` (3,093), `14` (2,648), `16` (2,489) |
| `dpkts` | 436 | 0 | 0 | `0` (36,006), `8` (9,465), `6` (7,464), `2` (5,448), `10` (3,746) |
| `sbytes` | 4,489 | 0 | 0 | `114` (18,158), `200` (7,187), `534` (2,376), `146` (2,140), `1540` (1,661) |
| `dbytes` | 4,034 | 0 | 0 | `0` (36,006), `268` (7,141), `354` (5,497), `178` (2,138), `86` (1,905) |
| `rate` | 40,616 | 0 | 0 | `111111.1072` (5,603), `125000.0003` (4,941), `333333.3215` (3,957), `90909.0902` (3,281), `250000.0006` (3,220) |
| `sttl` | 11 | 0 | 0 | `254` (54,049), `31` (16,702), `62` (10,374), `0` (1,048), `29` (50) |
| `dttl` | 8 | 0 | 0 | `0` (36,067), `252` (29,280), `29` (16,668), `60` (225), `30` (43) |
| `sload` | 42,873 | 0 | 0 | `50666664` (3,271), `57000000` (2,586), `152000000` (1,997), `114000000` (1,994), `41454544` (1,854) |
| `dload` | 40,614 | 0 | 0 | `0` (36,013), `657433.0625` (27), `678741.6875` (25), `664799.25` (24), `676806.125` (24) |
| `sloss` | 253 | 0 | 0 | `0` (39,320), `2` (19,304), `7` (6,005), `4` (3,739), `3` (3,575) |
| `dloss` | 311 | 0 | 0 | `0` (41,204), `1` (15,745), `2` (6,211), `4` (4,119), `8` (2,233) |
| `sinpkt` | 39,970 | 0 | 0 | `0.009` (5,657), `0.008` (5,088), `0.011` (4,395), `0.003` (4,024), `0.01` (3,791) |
| `dinpkt` | 37,617 | 0 | 0 | `0` (36,015), `0.008` (1,331), `0.009` (904), `0.007` (641), `0.002` (508) |
| `sjit` | 39,944 | 0 | 0 | `0` (38,650), `32.106723` (23), `55.640574` (22), `29.430768` (21), `38.80402` (21) |
| `djit` | 38,381 | 0 | 0 | `0` (41,552), `196.928172` (20), `70.142297` (11), `12723.928` (9), `7579.063` (9) |
| `swin` | 11 | 0 | 0 | `255` (43,086), `0` (39,237), `156` (1), `202` (1), `99` (1) |
| `stcpb` | 39,219 | 0 | 0 | `0` (40,881), `3738475984` (16), `1057528719` (12), `3536959022` (9), `2395243350` (9) |
| `dtcpb` | 39,108 | 0 | 0 | `0` (40,894), `1460955064` (24), `3773804157` (18), `463094449` (12), `1649858926` (9) |
| `dwin` | 14 | 0 | 0 | `255` (41,415), `0` (40,904), `27` (2), `81` (1), `160` (1) |
| `tcprtt` | 26,130 | 0 | 0 | `0` (41,127), `0.000665` (85), `0.000678` (80), `0.000667` (80), `0.000675` (78) |
| `synack` | 24,934 | 0 | 0 | `0` (41,127), `0.000548` (120), `0.000551` (113), `0.000535` (107), `0.000543` (106) |
| `ackdat` | 24,020 | 0 | 0 | `0` (41,160), `0.000134` (487), `0.000133` (471), `0.000135` (462), `0.000136` (398) |
| `smean` | 1,282 | 0 | 0 | `57` (18,924), `100` (7,356), `53` (3,754), `73` (2,242), `56` (2,137) |
| `dmean` | 1,222 | 0 | 0 | `0` (36,006), `45` (7,243), `44` (6,283), `89` (2,260), `43` (2,143) |
| `trans_depth` | 8 | 0 | 0 | `0` (74,750), `1` (7,548), `2` (28), `3` (2), `131` (1) |
| `response_body_len` | 1,190 | 0 | 0 | `0` (76,675), `3924` (1,042), `83` (361), `524288` (149), `109` (99) |
| `ct_srv_src` | 57 | 0 | 0 | `1` (13,626), `2` (8,986), `3` (7,799), `4` (6,583), `5` (5,476) |
| `ct_state_ttl` | 7 | 0 | 0 | `2` (34,100), `1` (27,234), `0` (17,045), `3` (2,120), `6` (1,804) |
| `ct_dst_ltm` | 50 | 0 | 0 | `1` (27,088), `2` (15,309), `3` (9,010), `4` (7,122), `5` (3,172) |
| `ct_src_dport_ltm` | 50 | 0 | 0 | `1` (43,181), `2` (11,661), `3` (5,173), `4` (4,645), `6` (2,295) |
| `ct_dst_sport_ltm` | 33 | 0 | 0 | `1` (53,883), `2` (6,524), `4` (5,127), `3` (4,499), `25` (2,251) |
| `ct_dst_src_ltm` | 57 | 0 | 0 | `1` (27,345), `2` (11,534), `3` (8,501), `4` (7,906), `5` (3,828) |
| `is_ftp_login` | 3 | 0 | 0 | `0` (81,654), `1` (674), `2` (4) |
| `ct_ftp_cmd` | 3 | 0 | 0 | `0` (81,652), `1` (670), `2` (10) |
| `ct_flw_http_mthd` | 8 | 0 | 0 | `0` (74,752), `1` (6,908), `4` (478), `9` (126), `16` (32) |
| `ct_src_ltm` | 50 | 0 | 0 | `1` (21,155), `2` (15,300), `3` (9,496), `4` (6,483), `5` (4,157) |
| `ct_srv_dst` | 57 | 0 | 0 | `1` (16,621), `2` (9,102), `3` (7,900), `4` (6,294), `5` (5,400) |
| `is_sm_ips_ports` | 2 | 0 | 0 | `0` (81,416), `1` (916) |
| `attack_cat` | 10 | 0 | 0 | `Normal` (37,000), `Generic` (18,871), `Exploits` (11,132), `Fuzzers` (6,062), `DoS` (4,089) |
| `label` | 2 | 0 | 0 | `1` (45,332), `0` (37,000) |

## Processing record

- 1. Read-only source audit: opened the prepared CSVs under data/raw; source bytes were not changed.
- 2. Integrity: computed SHA-256 in 1 MiB chunks and compared digest, byte size, and row count to the acquisition record.
- 3. Parsing: read as strings with keep_default_na=False and na_filter=False to preserve empty cells and literal text.
- 4. Profiling: counted empty/whitespace/blank-like cells, distinct and frequent values, and numeric ranges/quantiles; numeric coercion was temporary and diagnostic only.
- 5. Target audit: counted label values and cross-tabulated attack_cat against label; label is y and attack_cat is excluded as target-derived.
- 6. Split screen: omitted id, label, and attack_cat from candidate predictors; hashed full rows and predictor-only rows to screen overlap.
- 7. Reporting: generated derived JSON and Markdown outputs; this audit did not train a model.

## Leakage guardrails and evaluation plan

1. Set `y = label`, with attack as the positive class.
2. Exclude `attack_cat` because it encodes the attack family and reveals the binary target; exclude `id` because it is an identifier, not a network measurement.
3. Keep the official test file untouched while selecting models. Create a fixed-seed group-aware fit/validation split from official training using the 42-predictor vector as the group; repeated vectors must not cross fit and validation. Approximate stratification and report actual class counts.
4. Put categorical encoding and numeric imputation/scaling inside each model pipeline so they are fitted only on that model's training partition. Do not resample or fit preprocessing on validation or test rows.
5. Fix model choices and settings using training/validation only, refit selected pipelines on full official training, then evaluate the official test file once. Also report a clearly labeled secondary score on test rows whose predictor vector is unseen in training.
6. Report attack-class precision/recall/F1, macro-F1, confusion matrix, and accuracy with class counts; restrict conclusions to this benchmark split.

### Identifier diagnostics (excluded from predictors)

- Training `id`: 175341 unique for 175341 rows; range 1.0 to 175341.0; Pearson correlation with `label` 0.7271729520215975.
- Testing `id`: 82332 unique for 82332 rows; range 1.0 to 82332.0; Pearson correlation with `label` -0.3874886497428223.
- Numeric IDs shared by both files: 82,332. The ID ranges reset and label association differs between splits, so `id` is excluded from predictors.
- Identifier correlations are diagnostic only and are not a reason to use the identifier as a feature.

## Caveats

- Hash equality was used as a scalable screening method for cross-split duplicate checks; hash matches should be treated as candidate duplicate rows.
- `attack_cat` is omitted from the model feature matrix regardless of whether its raw strings are blank for benign rows.
- This audit does not establish real-world network generalization, and no model performance is included here.
