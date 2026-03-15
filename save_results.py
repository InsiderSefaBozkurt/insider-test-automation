import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_PORT", "3307")),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "insider123"),
        database=os.environ.get("MYSQL_DATABASE", "test_results"),
    )


def ensure_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_runs (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            run_at        DATETIME        NOT NULL,
            build_number  VARCHAR(50),
            branch        VARCHAR(100),
            total         INT             NOT NULL,
            passed        INT             NOT NULL,
            failed        INT             NOT NULL,
            errors        INT             NOT NULL,
            skipped       INT             NOT NULL,
            duration_sec  FLOAT           NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_cases (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            run_id        INT             NOT NULL,
            classname     VARCHAR(255),
            name          VARCHAR(255)    NOT NULL,
            status        VARCHAR(20)     NOT NULL,
            duration_sec  FLOAT           NOT NULL,
            message       TEXT,
            FOREIGN KEY (run_id) REFERENCES test_runs(id)
        )
    """)
    conn.commit()
    cursor.close()


def parse_junit(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    suites = list(root) if root.tag == "testsuites" else [root]

    total = failed = errors = skipped = 0
    duration = 0.0
    cases = []

    for suite in suites:
        total    += int(suite.attrib.get("tests",    0))
        failed   += int(suite.attrib.get("failures", 0))
        errors   += int(suite.attrib.get("errors",   0))
        skipped  += int(suite.attrib.get("skipped",  0))
        duration += float(suite.attrib.get("time",   0))

        for tc in suite.findall("testcase"):
            name      = tc.attrib.get("name", "")
            classname = tc.attrib.get("classname", "")
            dur       = float(tc.attrib.get("time", 0))
            failure   = tc.find("failure")
            error     = tc.find("error")
            skip      = tc.find("skipped")

            if failure is not None:
                status  = "FAILED"
                message = failure.attrib.get("message", failure.text or "")
            elif error is not None:
                status  = "ERROR"
                message = error.attrib.get("message", error.text or "")
            elif skip is not None:
                status  = "SKIPPED"
                message = ""
            else:
                status  = "PASSED"
                message = ""

            cases.append((classname, name, status, dur, message))

    return {
        "total": total, "passed": total - failed - errors - skipped,
        "failed": failed, "errors": errors, "skipped": skipped,
        "duration": duration, "cases": cases,
    }


def save(xml_path):
    data = parse_junit(xml_path)
    conn = get_db_connection()
    ensure_table(conn)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO test_runs
            (run_at, build_number, branch, total, passed, failed, errors, skipped, duration_sec)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.utcnow(),
        os.environ.get("BUILD_NUMBER", "local"),
        os.environ.get("GIT_BRANCH", "unknown"),
        data["total"], data["passed"], data["failed"],
        data["errors"], data["skipped"], data["duration"],
    ))
    run_id = cursor.lastrowid

    for classname, name, status, dur, message in data["cases"]:
        cursor.execute("""
            INSERT INTO test_cases (run_id, classname, name, status, duration_sec, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (run_id, classname, name, status, dur, message[:2000] if message else ""))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Saved run #{run_id}: {data['passed']} passed, {data['failed']} failed in {data['duration']:.1f}s")


if __name__ == "__main__":
    xml_path = sys.argv[1] if len(sys.argv) > 1 else "reports/junit.xml"
    save(xml_path)
