# PTMAE — Pure Python Transactional Micro-Banking & Audit Engine

## 1. Overview

PTMAE is a single-process Python 3.x teaching project demonstrating arithmetic, control flow, manual delimited-record parsing, closures, lambdas, comprehensions, in-place list processing, exception handling, file modification, logging, encapsulation, inheritance, and polymorphism. It uses plain-text files and a command-line interface (CLI); it does not use a database server, GUI, network service, or third-party package.

**Entry point:** `main.py`  
**Run:** `python main.py`

Execution runs the built-in demonstrations first and then starts the interactive CLI. Type `help` for supported commands and `exit` to leave. If standard input closes, the CLI exits on `EOFError`.

> This document describes the supplied `main.py` as implemented. The project is a coursework demonstration, not production banking software. Review the limitations in Section 11 before treating any requirement as fully satisfied.

## 2. Architecture

```text
                       +----------------------+
                       |       main()         |
                       +----------+-----------+
                                  |
                    +-------------+-------------+
                    |                           |
          +---------v----------+      +---------v---------+
          | Automatic demos    |      | Interactive CLI   |
          +---------+----------+      +---------+---------+
                    |                           |
       +------------+-------------+             |
       |            |             |             |
  +----v----+  +----v----+  +-----v------+  +---v------------+
  | Unit 1  |  | Unit 2  |  | Unit 3     |  | Interest /     |
  | Control |  | Parser  |  | Index and  |  | penalty input  |
  | and math|  | closure |  | queue      |  +----------------+
  +---------+  +---------+  +------------+
                    |
              +-----v-----------------------------+
              | Unit 4: file update + audit logs  |
              +----------------+------------------+
                               |
              +----------------v------------------+
              | Unit 5: accounts + batch settlement|
              +-----------------------------------+
```

## 3. Class diagram

```text
Exception
  |
  +-- BaseSystemError
        |-- CorruptedRecordError
        |-- OutOfBoundsError
        +-- InsufficientBalanceError

Account
  |-- SavingsAccount
  |-- CurrentAccount
  +-- CreditAccount

Account
  - __balance
  # _account_id
  + balance (property)
  + account_id (property)
  + process_settlement(amount)

Each account subclass overrides process_settlement(amount).
execute_batch_settlement(...) calls the method polymorphically.
```

Legend: `+` public interface, `#` protected-by-convention attribute, `-` name-mangled private attribute.

## 4. Module-by-module design

### Unit 1 — State control and arithmetic

- `compound_interest(principal, rate_percent, periods)` returns interest earned, not the final principal-plus-interest amount. It uses arithmetic operators and exponentiation.
- `calculate_penalty(amount, penalty_rate_percent)` returns a percentage penalty.
- `trajectory_guard(...)` applies transaction amounts in order and stops when the safety threshold is breached or the configured termination index is reached.
- `run_cli()` accepts `help`, `interest PRINCIPAL RATE PERIODS`, `penalty AMOUNT RATE`, and `exit`.

### Unit 2 — Manual parser and scope

- `parse_raw_log_line(line, delimiter=',', quote_char='"')` scans character-by-character, supports quoted delimiters and doubled quotes, and raises `ValueError` for malformed quoting.
- `create_audit_filter(threshold)` returns a validation closure. Its `nonlocal` counter increments on each call; the returned function's `.count()` helper reports that closure's count.
- `build_positional_filters()` creates three lambdas with default-argument binding (`k=k`) so each checks a different record position.

### Unit 3 — Inversion and queue mutation

- `build_reverse_index(branch_records)` uses nested dictionary/set comprehensions to map each service tag to sorted unique `(account_id, branch_id)` pairs.
- `clean_transaction_queue(data_list)` mutates the same top-level list object. Tuples become lists, embedded lists are sorted descending, even integer values are removed from top-level sets, and duplicate top-level primitive values are removed by scanning and deleting by index.
- Duplicate primitive detection requires the same type as well as equal value; for example, integer `1` and boolean `True` are treated as different values.

### Unit 4 — File updates and audit logs

- `validate_account_record(record)` validates the three comma-separated fields and supported account types.
- `replace_line_in_place(path, line_number, replacement)` uses binary `r+b`, `tell()`, `seek()`, bounded 4096-byte tail shifts, writes the replacement, and truncates to the resulting size.
- `update_account_file(path, updates, corrupted_path, ledger_path)` handles each update separately, records rejections in the corruption log, and writes accepted updates to the ledger.
- The supplied demonstration uses dedicated `ptmae_demo_*` filenames and does not intentionally open `accounts.db` for writing.

### Unit 5 — Account hierarchy

- `Account` provides a validated balance property, an account identifier property, and the shared amount validator.
- `SavingsAccount` rejects a debit that would leave less than 1000.
- `CurrentAccount` permits a negative resulting balance down to its private overdraft limit. Its balance is stored separately from the base-class balance to preserve the base class's non-negative setter rule.
- `CreditAccount` treats `balance` as outstanding debt, adds a 2.5% surcharge to each transaction, and rejects a charge that exceeds its credit limit.
- `execute_batch_settlement(...)` catches errors for each account independently and reports success/failure counts.

## 5. State and scope tracking

| State kind | Example in `main.py` | Purpose / scope |
|---|---|---|
| Local variables | `balance`, `fields`, `index`, `processed` | Exist within a function call and track intermediate results. |
| Closure variable | `audit_count` in `create_audit_filter` | Persists between calls to one returned validator. |
| `nonlocal` | `nonlocal audit_count` | Lets the nested validator update its enclosing counter. |
| Class attribute | `Account.total_accounts` | Counts accounts constructed through the base constructor. |
| Protected-by-convention attribute | `self._account_id` | Internal subclass-facing identifier; Python does not enforce protection. |
| Private/name-mangled attribute | `self.__balance` | Stored under `_Account__balance` by Python name mangling. |
| Subclass private state | `self.__overdraft_limit`, `self.__credit_limit` | Stored under subclass-specific mangled names. |
| Lambda default binding | `lambda record, k=k: ...` | Captures the current loop index as a default argument. |

## 6. Functional requirements traceability

| Requirement | Implementation | Demonstration / status |
|---|---|---|
| FR-1.1 CLI | `show_help`, `run_cli` | Help, invalid command, empty command, and exit are available interactively. **Partial:** implementation uses a single command loop, not nested `while` loops. |
| FR-1.2 interest and penalty | `compound_interest`, `calculate_penalty` | Two interest cases and one penalty case print expected values. |
| FR-1.3 trajectory guard | `trajectory_guard` | Demonstrates safety-threshold and termination-index stops. |
| FR-2.1 manual parser | `parse_raw_log_line` | Demonstrates quoted delimiter, doubled quote, empty field, trailing delimiter, and unterminated quote. |
| FR-2.2 closure audit | `create_audit_filter` | Demonstrates separate filters and call counts. |
| FR-2.3 positional lambdas | `build_positional_filters` | Three positional checks are evaluated against a sample record. |
| FR-3.1 reverse index | `build_reverse_index` | Demonstrates `UPI`, `ATM`, and `NEFT` mappings using two branches. |
| FR-3.2 queue mutation | `clean_transaction_queue` | Prints transformed queue and identity comparison. Duplicate removal applies only to top-level primitive values. |
| FR-4.1 exception hierarchy | Three subclasses of `BaseSystemError` | `issubclass` checks and base-class catch are demonstrated. |
| FR-4.2 in-place file update | `replace_line_in_place`, `update_account_file` | Demo attempts growth and shrinkage on a dedicated scratch file and checks neighboring lines. **Partial:** equal-length replacement is not explicitly demonstrated; replacement line endings are normalized to LF. |
| FR-4.3 dual logging | `append_log`, `update_account_file` | Demo prints ledger and corruption logs when available. |
| FR-4.4 exception flow and counts | `update_account_file` | Per-update `try/except/else`, outer `finally`, and summary counts are implemented. |
| FR-5.1 account hierarchy | `Account`, `SavingsAccount`, `CurrentAccount`, `CreditAccount` | Name mangling, external private access failure, and class count are demonstrated. |
| FR-5.2 polymorphic settlement | Subclass `process_settlement` methods | Demo exercises account types and acceptance/rejection cases. |
| FR-5.3 fault-isolated batch | `execute_batch_settlement` | Mixed batches print per-account outcomes and summary counts. |

## 7. Units 1–5 syllabus compliance checklist

- [x] Unit 1: variables, numeric types, arithmetic, conditions, loops, short-circuit Boolean expressions, input/output, and exception handling.
- [x] Unit 2: character-by-character parsing, indexing, slicing-compatible string operations, nested functions, `nonlocal`, and lambda default binding.
- [x] Unit 3: lists, tuples, sets, dictionaries, comprehensions, sorting, indexed deletion, and in-place mutation.
- [x] Unit 4: custom exception hierarchy, text/binary file I/O, `with`, `seek`, `tell`, `truncate`, and audit logs.
- [x] Unit 5: classes, inheritance, `super()`, properties, name mangling, method overriding, and polymorphic calls.
- [ ] Strict nested-loop CLI requirement: not met by the current `run_cli()` implementation.
- [ ] Exact preservation of the selected record's original line ending: not met; replacement records are written with LF.
- [ ] Full automated assertion-based test suite: not included; demonstrations print results rather than assert every acceptance criterion.

## 8. Test plan and expected outcomes

| Test | Input / action | Expected outcome |
|---|---|---|
| Compound interest A | Principal 1000, rate 5%, 2 periods | Interest `102.50` (rounded to 2 decimals). |
| Compound interest B | Principal 2000, rate 10%, 1 period | Interest `200.00`. |
| Penalty | Amount 800, rate 2.5% | Penalty `20.00`. |
| Invalid arithmetic | Negative principal/rate/periods or wrong numeric type | A `ValueError` or `TypeError` is raised and the CLI reports input errors. |
| Quoted delimiter | `Acc102,"CURRENT, PREMIUM",1200.00` | Comma inside quotes remains part of one field. |
| Doubled quote | `"Acc""103",SAVINGS,200.00` | The escaped quote is represented as one literal quote. |
| Empty/trailing fields | `Acc104,,` and `Acc105,SAVINGS,100.00,` | Empty fields are preserved. |
| Malformed quoted field | Unterminated quoted value | `ValueError` is raised. |
| Closure independence | Two filters with thresholds 100 and 500 | Each filter maintains its own count. |
| Lambda binding | Evaluate all three positional filters | Each lambda checks its own position. |
| Reverse index | Sample branch records | UPI includes `(Acc101, BRANCH_01)`, `(Acc102, BRANCH_01)`, `(Acc201, BRANCH_02)`, sorted alphabetically. |
| Queue identity | Save `id(queue)`, clean queue | Returned object is the same list object. |
| File shift | Replace a line with longer then shorter bytes | Tail records remain in place; the demo checks neighboring records. |
| Unknown account | Submit an ID absent from the database | Update is rejected and written to the corruption log. |
| Invalid update balance | Submit non-numeric balance | Update is rejected; later updates continue. |
| Savings settlement | Debit that leaves under 1000 | `InsufficientBalanceError` is caught by the batch processor. |
| Current overdraft | Debit beyond configured limit | Transaction is rejected. |
| Credit limit | Charge plus 2.5% surcharge exceeds limit | Transaction is rejected. |
| CLI | Type `help`, invalid command, then `exit` | Help is shown, invalid command is explained, and exit closes the loop. |

These are a planned/manual test matrix plus built-in demonstrations. A printed demonstration is not equivalent to an independent automated test assertion.

## 9. Imports and prohibited-shortcut checklist

- [x] No third-party package is required.
- [x] The only import is `datetime` (inside a guarded import statement).
- [x] The manual log parser does not call `str.split()`, `str.replace()`, `csv`, or regular expressions.
- [x] Compound interest and penalty calculations use arithmetic operators without `math`.
- [x] The reverse index uses comprehensions and set uniqueness.
- [x] The queue function does not bind a replacement list to `data_list` and checks object identity in its demo.
- [x] The account database is edited with binary `r+b`, not by loading all records and rewriting the file with `w` mode.
- [x] Files opened by the implementation use context managers.
- [ ] The CLI itself uses `command.split()` for command tokenization. This is outside the manual log parser, but should be reviewed if the evaluator interprets the ban on `str.split()` as global rather than parser-specific.

## 10. File layout, record format, and safe execution

Recommended folder layout:

```text
PTMAE/
|-- main.py
|-- Documentation.md
|-- accounts.db                 # optional real CLI update target; create manually
|-- corrupted.log                # created/appended when records are rejected
|-- ledger.txt                   # created/appended for accepted updates
|-- ptmae_demo_accounts.db       # created by demonstration if absent
|-- ptmae_demo_corrupted.log     # demo rejection log
|-- ptmae_demo_ledger.txt        # demo accepted-update log
|-- ptmae_demo_shift_test.db     # demo line-shift test file
```

Account database records use one UTF-8-compatible record per line:

```text
Acc101,SAVINGS,5200.00
Acc102,CURRENT,900.00
Acc103,CREDIT,100.00
```

Allowed account types are `SAVINGS`, `CURRENT`, and `CREDIT`. Account IDs must be non-empty alphanumeric strings. A current account may have a negative balance in file validation; the other types may not.

**File update API:** `update_account_file(path, updates, corrupted_path="corrupted.log", ledger_path="ledger.txt")`, where each update is a three-item tuple/list `(account_id, account_type, new_balance)`. This function is callable from Python code; the interactive CLI does not expose a file-update command.

**Safe execution notes:** the demonstration creates its demo database with exclusive-create mode (`xb`). If the demo database already exists, the code leaves it untouched and skips the file-update demo rather than overwriting it. The scratch shift-test file is also exclusive-created. To test against a real `accounts.db`, make a backup first and call `update_account_file` explicitly with the intended path.

**Logging:** each rejected update is appended to the corruption log with its input line number and reason; accepted updates are appended to the ledger with a local timestamp when `datetime` is available.

## 11. Unresolved specification issues and implementation limitations

1. **Non-atomic file update:** byte-shifting a file in place is not transactional. A process interruption, disk error, or write failure during shifting can leave the target file partially modified. Use a backup for any real data.
2. **Binary versus text mode:** `replace_line_in_place` deliberately uses `r+b` to perform byte-accurate seeking and bounded shifts. This is appropriate for byte offsets but is not literal text-mode `r+`; this distinction is explicit.
3. **Line endings:** the replacement record is encoded with LF (`\n`). Neighboring records are shifted as bytes, but the replaced line's prior CRLF/LF convention is not preserved. A final line without a newline is also replaced with a newline-terminated record.
4. **CLI loop structure:** `run_cli()` uses one `while True` loop, not the nested `while` loops requested in FR-1.1.
5. **Database record scan:** malformed stored records encountered before a matching account are logged and skipped. If the target record is found later, the update may still proceed. A malformed record is not automatically repaired.
6. **Logging failures:** an operating-system error while writing a log can escape the per-update recovery path. In-place writes and log writes are not coordinated as one transaction.
7. **Validation boundaries:** numeric checks reject booleans but do not explicitly reject floating-point NaN or infinity. They are classroom-level checks, not comprehensive financial validation.
8. **Parser whitespace/quotes:** the parser preserves field whitespace and supports quoted delimiters/doubled quotes, but does not implement a full CSV grammar. For example, whitespace before an opening quote is treated as unquoted content and then a quote may be rejected.
9. **Queue interpretation:** only duplicate top-level primitive values are removed. Containers are skipped for duplicate comparison; duplicates inside nested lists and sets are not removed, except that even integer values are filtered from each top-level set.
10. **Current account representation:** its signed balance is held in a subclass-specific field, separate from `Account`'s private non-negative balance. This is the documented resolution of the base setter/overdraft conflict.
11. **Credit account representation:** `balance` means outstanding debt, not available credit. A settlement increases debt by the amount plus a 2.5% surcharge, up to the configured credit limit.
12. **Demonstration reruns:** existing demo files are protected from overwrite, but this means demonstrations that require creating those files may be skipped on subsequent runs until the user deliberately archives or removes their own demo artifacts.
13. **Rubric marks:** the supplied rubric's component formatting is imperfect; this project preserves the stated target total of 10.0 rather than inferring a different total.
14. **Automated verification:** the program contains demonstrations, not a comprehensive assertion-based test suite. Run the project and inspect output, then test edge cases from Section 8 separately before submission.

## 12. Submission checklist

- [ ] Save `main.py` and `Documentation.md` in the same project folder.
- [ ] Run `python main.py` with Python 3.x.
- [ ] Review all demonstration output, especially file-update and batch-settlement sections.
- [ ] Confirm the demo database and log files are not pre-existing files you need to preserve; the program will not overwrite them.
- [ ] If testing real data, back up `accounts.db` before calling `update_account_file`.
- [ ] Test CLI commands: `help`, `interest 1000 5 2`, `penalty 800 2.5`, an invalid command, and `exit`.
- [ ] Review Section 11 and be prepared to explain the documented limitations during evaluation.
- [ ] Submit both files and any required screenshots/output evidence requested by the instructor.
