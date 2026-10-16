try:
    from datetime import datetime
except ImportError:  # The project remains usable without timestamps.
    datetime = None


# ---------------------------------------------------------------------------
# MODULE 1 — STATE CONTROL ENGINE AND TRAJECTORY GUARDS (UNIT 1)
# ---------------------------------------------------------------------------


def compound_interest(principal, rate_percent, periods):
    """Return compound interest earned, validating the numeric inputs."""
    if not isinstance(principal, (int, float)) or isinstance(principal, bool):
        raise TypeError("Principal must be numeric.")
    if not isinstance(rate_percent, (int, float)) or isinstance(rate_percent, bool):
        raise TypeError("Rate must be numeric.")
    if not isinstance(periods, int) or isinstance(periods, bool):
        raise TypeError("Periods must be an integer.")
    if principal < 0 or rate_percent < 0 or periods < 0:
        raise ValueError("Principal, rate, and periods cannot be negative.")
    final_amount = principal * (1 + rate_percent / 100) ** periods
    return final_amount - principal


def calculate_penalty(amount, penalty_rate_percent):
    """Calculate a percentage penalty using arithmetic operators only."""
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise TypeError("Amount must be numeric.")
    if not isinstance(penalty_rate_percent, (int, float)) or isinstance(penalty_rate_percent, bool):
        raise TypeError("Penalty rate must be numeric.")
    if amount < 0 or penalty_rate_percent < 0:
        raise ValueError("Amount and penalty rate cannot be negative.")
    return amount * penalty_rate_percent / 100


def trajectory_guard(transactions, starting_balance, safety_threshold, terminate_at=None):
    """Apply transactions until the balance is unsafe or a stop index is reached."""
    balance = starting_balance
    for index, amount in enumerate(transactions):
        # Short-circuit evaluation avoids applying a transaction after termination.
        if (terminate_at is not None and index >= terminate_at) or balance < safety_threshold:
            return balance, index, "termination flag" if terminate_at is not None and index >= terminate_at else "safety threshold"
        balance += amount
        if balance < safety_threshold:
            return balance, index + 1, "safety threshold"
    return balance, len(transactions), "completed"


def show_help():
    """Print supported CLI commands."""
    print("Commands: help | interest PRINCIPAL RATE% PERIODS | penalty AMOUNT RATE% | exit")
    print("Example: interest 1000 5 2")


def run_cli():
    """Run a nested-loop command line interface until explicit exit or EOF."""
    print("\nPTMAE interactive CLI. Type 'help' for commands; 'exit' to quit.")
    while True:
        try:
            command = input("ptmae> ").strip()
        except EOFError:
            print("\nInput ended; CLI closed.")
            break
        if command == "exit":
            print("Goodbye.")
            break
        if command == "help":
            show_help()
            continue
        if not command:
            print("Empty command. Type 'help'.")
            continue
        words = command.split()  # CLI tokenization; the manual log parser does not use split().
        try:
            if words[0] == "interest" and len(words) == 4:
                print("Interest earned:", round(compound_interest(float(words[1]), float(words[2]), int(words[3])), 2))
            elif words[0] == "penalty" and len(words) == 3:
                print("Penalty:", round(calculate_penalty(float(words[1]), float(words[2])), 2))
            else:
                print("Invalid command or arguments. Type 'help'.")
        except (TypeError, ValueError) as error:
            print("Input error:", error)


# ---------------------------------------------------------------------------
# MODULE 2 — MANUAL LOG PARSER AND CLOSURE MECHANICS (UNIT 2)
# ---------------------------------------------------------------------------


def parse_raw_log_line(line, delimiter=",", quote_char='"'):
    """Manually parse a delimited line, supporting quoted delimiters and doubled quotes."""
    if not isinstance(line, str):
        raise TypeError("Log line must be a string.")
    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise ValueError("Delimiter must be exactly one character.")
    if not isinstance(quote_char, str) or len(quote_char) != 1:
        raise ValueError("Quote character must be exactly one character.")
    fields = []
    field_chars = []
    in_quotes = False
    field_was_quoted = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == quote_char:
            if in_quotes:
                if index + 1 < len(line) and line[index + 1] == quote_char:
                    field_chars.append(quote_char)
                    index += 2
                    continue
                in_quotes = False
            elif not field_chars:
                in_quotes = True
                field_was_quoted = True
            else:
                raise ValueError("Unexpected quote inside an unquoted field.")
        elif char == delimiter and not in_quotes:
            fields.append("".join(field_chars))
            field_chars = []
            field_was_quoted = False
        else:
            field_chars.append(char)
        index += 1
    if in_quotes:
        raise ValueError("Malformed log record: unterminated quoted field.")
    fields.append("".join(field_chars))
    return fields


def create_audit_filter(threshold):
    """Create an independent audit filter that accepts values >= threshold and counts calls."""
    audit_count = 0

    def validate(value):
        """Count this validation call and return whether value meets the threshold."""
        nonlocal audit_count
        audit_count += 1
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= threshold

    def count():
        """Return the number of validations performed by this filter."""
        return audit_count

    validate.count = count
    return validate


def build_positional_filters():
    """Return lambdas bound to distinct positional indices."""
    filters = []
    for k in range(3):
        filters.append(lambda record, k=k: len(record) > k and bool(record[k]))
    return filters


# ---------------------------------------------------------------------------
# MODULE 3 — DATA INVERSION AND IN-PLACE PROCESSING (UNIT 3)
# ---------------------------------------------------------------------------


def build_reverse_index(branch_records):
    """Build a service-tag index of unique (account_id, branch_id) pairs."""
    reverse_index = {
        tag: sorted({(account_id, branch_id)
                     for branch_id, records in branch_records.items()
                     for account_id, service_tags in records
                     for tag in service_tags})
        for tag in {tag for records in branch_records.values()
                    for account_id, service_tags in records for tag in service_tags}
    }
    return reverse_index


def clean_transaction_queue(data_list):
    """Mutate a heterogeneous queue in place and return the same list object."""
    if not isinstance(data_list, list):
        raise TypeError("Queue must be a list.")
    # Transform nested values first; tuple elements become mutable lists.
    for index in range(len(data_list)):
        item = data_list[index]
        if isinstance(item, tuple):
            data_list[index] = list(item)
            item = data_list[index]
        if isinstance(item, set):
            even_ids = set()
            for value in item:
                if isinstance(value, int) and not isinstance(value, bool) and value % 2 == 0:
                    even_ids.add(value)
            data_list[index] = item.difference(even_ids)
        elif isinstance(item, list):
            item.sort(reverse=True)

    # Only top-level primitive values are deduplicated. Containers are not compared.
    index = 0
    while index < len(data_list):
        current = data_list[index]
        if isinstance(current, (tuple, list, set, dict)):
            index += 1
            continue
        earlier = 0
        duplicate = False
        while earlier < index:
            previous = data_list[earlier]
            if not isinstance(previous, (tuple, list, set, dict)) and type(previous) is type(current) and previous == current:
                duplicate = True
                break
            earlier += 1
        if duplicate:
            del data_list[index]
        else:
            index += 1
    return data_list


# ---------------------------------------------------------------------------
# MODULE 4 — FILE MODIFIER AND ERROR LOGGER (UNIT 4)
# ---------------------------------------------------------------------------


class BaseSystemError(Exception):
    """Base exception for PTMAE domain errors."""


class CorruptedRecordError(BaseSystemError):
    """Raised when a stored or supplied account record is malformed."""


class OutOfBoundsError(BaseSystemError):
    """Raised when a value or transaction exceeds an allowed boundary."""


class InsufficientBalanceError(BaseSystemError):
    """Raised when an account cannot cover a requested transaction."""


def validate_account_record(record):
    """Validate one account record and return (account_id, account_type, balance)."""
    fields = parse_raw_log_line(record.rstrip("\r\n"))
    if len(fields) != 3:
        raise CorruptedRecordError("expected exactly 3 comma-separated fields")
    account_id, account_type, balance_text = fields
    if not account_id or not account_id.isalnum():
        raise CorruptedRecordError("account ID must be non-empty and alphanumeric")
    if account_type not in ("SAVINGS", "CURRENT", "CREDIT"):
        raise CorruptedRecordError("unknown account type")
    try:
        balance = float(balance_text)
    except ValueError:
        raise CorruptedRecordError("balance is not numeric")
    if balance < 0 and account_type != "CURRENT":
        raise CorruptedRecordError("negative balance is only valid for CURRENT accounts")
    return account_id, account_type, balance


def timestamp_text():
    """Return a local timestamp string when datetime is available."""
    if datetime is None:
        return "timestamp-unavailable"
    return datetime.now().isoformat(timespec="seconds")


def append_log(path, message):
    """Append one UTF-8 text line to a log file."""
    with open(path, "a", encoding="utf-8", newline="") as handle:
        handle.write(message + "\n")


def _line_bounds(binary_file, line_number):
    """Return byte offsets (start, end) for a one-based line number, or None."""
    if line_number < 1:
        return None
    binary_file.seek(0)
    current_line = 1
    start = 0
    while True:
        chunk = binary_file.read(1)
        if not chunk:
            if current_line == line_number:
                return start, binary_file.tell()
            return None
        if chunk == b"\n":
            if current_line == line_number:
                return start, binary_file.tell()
            current_line += 1
            start = binary_file.tell()


def replace_line_in_place(path, line_number, replacement):
    """Replace one line with byte-accurate bounded tail shifting in binary mode."""
    if not isinstance(replacement, bytes):
        raise TypeError("Replacement must be bytes.")
    if not replacement.endswith(b"\n"):
        replacement += b"\n"
    with open(path, "r+b") as handle:
        bounds = _line_bounds(handle, line_number)
        if bounds is None:
            raise OutOfBoundsError("line number does not exist")
        start, end = bounds
        old_length = end - start
        handle.seek(0, 2)
        file_size = handle.tell()
        tail_start = end
        tail_length = file_size - tail_start
        new_length = len(replacement)
        delta = new_length - old_length
        if delta > 0:
            # Shift the tail backwards in bounded chunks to avoid overwriting unread bytes.
            position = tail_length
            while position > 0:
                amount = 4096 if position > 4096 else position
                source_start = tail_start + position - amount
                handle.seek(source_start)
                chunk = handle.read(amount)
                handle.seek(source_start + delta)
                handle.write(chunk)
                position -= amount
        elif delta < 0:
            # Shift the tail forwards in bounded chunks when the replacement shrinks.
            position = 0
            while position < tail_length:
                amount = 4096 if tail_length - position > 4096 else tail_length - position
                handle.seek(tail_start + position)
                chunk = handle.read(amount)
                handle.seek(tail_start + position + delta)
                handle.write(chunk)
                position += amount
        handle.seek(start)
        handle.write(replacement)
        handle.truncate(file_size + delta)


def update_account_file(path, updates, corrupted_path="corrupted.log", ledger_path="ledger.txt"):
    """Apply account updates independently, logging each rejection and accepted update.

    Each update is (account_id, account_type, new_balance). The database is edited
    in place; it is not loaded wholesale or rewritten with text mode 'w'.
    """
    processed = 0
    rejected = 0
    try:
        for input_line, update in enumerate(updates, 1):
            processed += 1
            try:
                if not isinstance(update, (tuple, list)) or len(update) != 3:
                    raise CorruptedRecordError("update must be (account_id, account_type, new_balance)")
                account_id, account_type, new_balance = update
                if not isinstance(account_id, str) or not account_id or not account_id.isalnum():
                    raise CorruptedRecordError("invalid account ID")
                if account_type not in ("SAVINGS", "CURRENT", "CREDIT"):
                    raise CorruptedRecordError("unknown account type")
                try:
                    balance = float(new_balance)
                except (TypeError, ValueError):
                    raise CorruptedRecordError("new balance is not numeric")
                if balance < 0 and account_type != "CURRENT":
                    raise CorruptedRecordError("negative balance is only valid for CURRENT accounts")
                found_line = None
                with open(path, "rb") as handle:
                    line_number = 0
                    while True:
                        raw = handle.readline()
                        if not raw:
                            break
                        line_number += 1
                        try:
                            old_id, old_type, old_balance = validate_account_record(raw.decode("utf-8"))
                        except (UnicodeDecodeError, CorruptedRecordError, ValueError) as error:
                            append_log(corrupted_path, "input line " + str(input_line) + "; database line " + str(line_number) + "; " + str(error) + "; record=" + repr(raw))
                            continue
                        if old_id == account_id:
                            found_line = line_number
                            break
                if found_line is None:
                    raise CorruptedRecordError("account ID not found in database")
                replacement = (account_id + "," + account_type + "," + format(balance, ".2f") + "\n").encode("utf-8")
                replace_line_in_place(path, found_line, replacement)
            except (BaseSystemError, TypeError, ValueError, OSError) as error:
                rejected += 1
                append_log(corrupted_path, "input line " + str(input_line) + "; rejected; " + str(error) + "; update=" + repr(update))
            else:
                append_log(ledger_path, timestamp_text() + "; accepted; account=" + account_id + "; type=" + account_type + "; balance=" + format(balance, ".2f"))
    finally:
        print("File update summary: processed=" + str(processed) + ", rejected=" + str(rejected))
    return processed, rejected


# ---------------------------------------------------------------------------
# MODULE 5 — OBJECT-ORIENTED AND POLYMORPHIC ENGINE (UNIT 5)
# ---------------------------------------------------------------------------


class Account:
    """Encapsulated base account with a validated private balance."""
    total_accounts = 0

    def __init__(self, account_id, balance):
        """Create an account with an identifier and starting balance."""
        if not isinstance(account_id, str) or not account_id or not account_id.isalnum():
            raise ValueError("Account ID must be non-empty and alphanumeric.")
        self._account_id = account_id
        self.__balance = 0.0
        self.balance = balance
        Account.total_accounts += 1

    @property
    def balance(self):
        """Return the account balance."""
        return self.__balance

    @balance.setter
    def balance(self, value):
        """Set a finite numeric balance; base accounts cannot be negative."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Balance must be numeric.")
        if value < 0:
            raise OutOfBoundsError("Base balance cannot be negative.")
        self.__balance = float(value)

    @property
    def account_id(self):
        """Return the protected account identifier through a public getter."""
        return self._account_id

    def process_settlement(self, amount):
        """Debit the account when sufficient funds remain."""
        amount = self._validate_amount(amount)
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance.")
        self.balance = self.balance - amount
        return self.balance

    def _validate_amount(self, amount):
        """Validate a strictly positive numeric transaction amount."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Transaction amount must be numeric.")
        if amount <= 0:
            raise OutOfBoundsError("Transaction amount must be positive.")
        return float(amount)


class SavingsAccount(Account):
    """Savings account that must retain at least 1000 after a debit."""

    def __init__(self, account_id, balance):
        """Initialize savings account using cooperative constructor inheritance."""
        super().__init__(account_id, balance)

    def process_settlement(self, amount):
        """Debit only when at least 1000 remains."""
        amount = self._validate_amount(amount)
        if self.balance - amount < 1000:
            raise InsufficientBalanceError("Savings account must retain at least 1000.")
        self.balance = self.balance - amount
        return self.balance


class CurrentAccount(Account):
    """Current account with a private overdraft limit and signed balance."""

    def __init__(self, account_id, balance, overdraft_limit=5000):
        """Initialize current account and its validated overdraft limit."""
        super().__init__(account_id, balance)
        if not isinstance(overdraft_limit, (int, float)) or isinstance(overdraft_limit, bool) or overdraft_limit < 0:
            raise OutOfBoundsError("Overdraft limit must be non-negative and numeric.")
        self.__overdraft_limit = float(overdraft_limit)

    @property
    def balance(self):
        """Return the current account's signed balance."""
        return self.__current_balance

    @balance.setter
    def balance(self, value):
        """Initialize or set a non-negative current account balance."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Balance must be numeric.")
        if value < 0:
            raise OutOfBoundsError("Starting balance cannot be negative.")
        self.__current_balance = float(value)

    def process_settlement(self, amount):
        """Debit while ensuring balance does not pass the negative overdraft limit."""
        amount = self._validate_amount(amount)
        new_balance = self.balance - amount
        if new_balance < -self.__overdraft_limit:
            raise InsufficientBalanceError("Current account overdraft limit exceeded.")
        # This subclass owns a separate signed-balance field so the base class's
        # non-negative balance invariant remains intact for other account types.
        self.__current_balance = new_balance
        return self.balance


class CreditAccount(Account):
    """Credit account where balance means outstanding debt, limited by credit_limit."""

    def __init__(self, account_id, balance, credit_limit=10000):
        """Initialize credit account with outstanding debt and a credit limit."""
        super().__init__(account_id, balance)
        if not isinstance(credit_limit, (int, float)) or isinstance(credit_limit, bool) or credit_limit < 0:
            raise OutOfBoundsError("Credit limit must be non-negative and numeric.")
        self.__credit_limit = float(credit_limit)

    def process_settlement(self, amount):
        """Add a 2.5 percent surcharge and reject debt above the credit limit."""
        amount = self._validate_amount(amount)
        charged_amount = amount + amount * 2.5 / 100
        new_balance = self.balance + charged_amount
        if new_balance > self.__credit_limit:
            raise InsufficientBalanceError("Credit limit exceeded.")
        self.balance = new_balance
        return self.balance


def execute_batch_settlement(account_list, transaction_amount):
    """Settle across mixed account types while isolating failures per account."""
    succeeded = 0
    failed = 0
    for account in account_list:
        try:
            new_balance = account.process_settlement(transaction_amount)
        except (BaseSystemError, TypeError, ValueError) as error:
            failed += 1
            print(account.account_id + ": REJECTED - " + str(error))
        else:
            succeeded += 1
            print(account.account_id + ": accepted; balance=" + format(new_balance, ".2f"))
    print("Settlement summary: successful=" + str(succeeded) + ", failed=" + str(failed))
    return succeeded, failed


# ---------------------------------------------------------------------------
# AUTOMATIC, DETERMINISTIC DEMONSTRATIONS
# ---------------------------------------------------------------------------


def run_demonstrations():
    """Run concise demonstrations for the five syllabus modules."""
    print("=" * 68)
    print("PTMAE — AUTOMATIC DEMONSTRATIONS")
    print("=" * 68)

    print("\n[Unit 1] Financial arithmetic")
    print("Interest on 1000 at 5% for 2 periods:", round(compound_interest(1000, 5, 2), 2), "(expected 102.50)")
    print("Interest on 2000 at 10% for 1 period:", round(compound_interest(2000, 10, 1), 2), "(expected 200.00)")
    print("Penalty on 800 at 2.5%:", round(calculate_penalty(800, 2.5), 2), "(expected 20.00)")
    print("Guard safety stop:", trajectory_guard([-200, 50], 150, 100))
    print("Guard termination stop:", trajectory_guard([10, 20, 30], 100, 0, terminate_at=1))

    print("\n[Unit 2] Manual parser, closures, and lambdas")
    parser_cases = [
        'Acc101,SAVINGS,5200.00',
        'Acc102,"CURRENT, PREMIUM",1200.00',
        '"Acc""103",SAVINGS,200.00',
        'Acc104,,',
        'Acc105,SAVINGS,100.00,',
    ]
    for raw in parser_cases:
        try:
            print(repr(raw), "->", parse_raw_log_line(raw))
        except ValueError as error:
            print(repr(raw), "-> ERROR:", error)
    try:
        parse_raw_log_line('Acc106,"SAVINGS,100.00')
    except ValueError as error:
        print("Malformed quote correctly rejected:", error)
    audit_a = create_audit_filter(100)
    audit_b = create_audit_filter(500)
    print("Audit A checks:", audit_a(120), audit_a(80), "count=", audit_a.count())
    print("Audit B check:", audit_b(600), "count=", audit_b.count())
    filters = build_positional_filters()
    sample_record = ("Acc101", "SAVINGS", "5200.00")
    print("Positional lambda results:", [test(sample_record) for test in filters], "(expected all True)")

    print("\n[Unit 3] Reverse index and in-place queue")
    branches = {
        "BRANCH_01": [("Acc101", {"UPI", "ATM"}), ("Acc102", {"UPI"})],
        "BRANCH_02": [("Acc201", {"UPI", "NEFT"}), ("Acc202", {"ATM"})],
    }
    reverse = build_reverse_index(branches)
    print("UPI mapping:", reverse.get("UPI"), "(expected Acc101/01, Acc102/01, Acc201/02)")
    queue = [(3, 1, 2), [4, 1, 3], {1, 2, 3, 4}, 7, 7, "ok", "ok", 2]
    original_identity = id(queue)
    result = clean_transaction_queue(queue)
    print("Queue:", result)
    print("Identity preserved:", id(result) == original_identity)

    print("\n[Unit 4] Exception hierarchy and safe file demonstrations")
    print("Subclass checks:", issubclass(CorruptedRecordError, BaseSystemError),
          issubclass(OutOfBoundsError, BaseSystemError), issubclass(InsufficientBalanceError, BaseSystemError))
    try:
        raise CorruptedRecordError("sample base-catch check")
    except BaseSystemError as error:
        print("Caught through base class:", error)

    demo_db = "ptmae_demo_accounts.db"
    demo_corrupt = "ptmae_demo_corrupted.log"
    demo_ledger = "ptmae_demo_ledger.txt"
    # Safe reruns: create demo files only when absent; never overwrite existing data.
    created_demo = False
    try:
        with open(demo_db, "xb") as handle:
            handle.write(b"Acc101,SAVINGS,5200.00\r\nAcc102,CURRENT,900.00\r\nAcc103,CREDIT,100.00\r\n")
        created_demo = True
        print("Created dedicated demo database:", demo_db)
    except FileExistsError:
        print("Demo database already exists; leaving it untouched:", demo_db)
    try:
        if not created_demo:
            raise FileExistsError("existing demo database is protected")
        with open(demo_db, "rb") as handle:
            original_records = handle.readlines()
        if len(original_records) >= 3 and original_records[0].startswith(b"Acc101,"):
            # A separate throwaway scratch file is only created if absent, to exercise
            # growth/shrinkage while leaving a user's existing demo database untouched.
            scratch = "ptmae_demo_shift_test.db"
            try:
                with open(scratch, "xb") as handle:
                    handle.write(b"NEIGHBOR_A\r\nAccX,SAVINGS,1.00\r\nNEIGHBOR_B\r\n")
                before = None
                with open(scratch, "rb") as handle:
                    before = handle.readlines()
                replace_line_in_place(scratch, 2, b"AccX,SAVINGS,123456.78\r\n")
                replace_line_in_place(scratch, 2, b"AccX,SAVINGS,1.00\r\n")
                with open(scratch, "rb") as handle:
                    after = handle.readlines()
                print("Grow/shrink line tests passed:", after[0] == before[0] and after[2] == before[2])
            except FileExistsError:
                print("Shift-test file already exists; skipped to protect existing data.")
        updates = [("Acc101", "SAVINGS", 520000.00), ("Missing9", "SAVINGS", 10),
                   ("Acc102", "CURRENT", 950.00), ("Acc103", "CREDIT", "not-a-number")]
        update_account_file(demo_db, updates, demo_corrupt, demo_ledger)
        with open(demo_db, "rb") as handle:
            print("Demo database after attempted updates:")
            for line in handle:
                print(" ", repr(line))
        for log_path in (demo_corrupt, demo_ledger):
            try:
                with open(log_path, "r", encoding="utf-8") as handle:
                    print(log_path + ":")
                    for line in handle:
                        print(" ", line.rstrip("\n"))
            except FileNotFoundError:
                print(log_path + ": not created yet")
    except OSError as error:
        print("File demo skipped due to a recoverable OS error:", error)

    print("\n[Unit 5] Encapsulation and polymorphic settlement")
    savings = SavingsAccount("Sav001", 3000)
    current = CurrentAccount("Cur001", 500, 1000)
    credit = CreditAccount("Cre001", 100, 1000)
    print("Name-mangled balance access:", savings._Account__balance)
    try:
        print(savings.__balance)
    except AttributeError:
        print("External obj.__balance access correctly fails.")
    print("Account.total_accounts:", Account.total_accounts)
    execute_batch_settlement([savings, current, credit], 250)
    print("Batch with mixed outcomes:")
    execute_batch_settlement([SavingsAccount("Sav002", 1100), CurrentAccount("Cur002", 100, 50),
                              CreditAccount("Cre002", 990, 1000)], 200)

    print("\nDemonstrations complete. The CLI starts next.")


def main():
    """Run demonstrations and then launch the interactive command loop."""
    run_demonstrations()
    run_cli()


if __name__ == "__main__":
    main()
