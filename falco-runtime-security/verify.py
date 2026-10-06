#!/usr/bin/env python3
"""Structural check of the Falco rules file (no Falco binary needed): fields, priorities, macro/list refs."""
import os
import re
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))
items = yaml.safe_load(open("orders_rules.yaml"))
PRIO = {"EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFORMATIONAL", "DEBUG"}
macros = {i["macro"] for i in items if "macro" in i}
lists = {i["list"] for i in items if "list" in i}
rules = [i for i in items if "rule" in i]
assert rules, "no rules"
for r in rules:
    for k in ("desc", "condition", "output", "priority"):
        assert r.get(k), r["rule"] + ": missing " + k
    assert r["priority"] in PRIO, r["rule"] + ": bad priority"
    words = set(re.findall(r"[a-z_]+", r["condition"]))
    assert words & macros, r["rule"] + ": uses no macro"
    for m in re.findall(r"in \(([a-z_]+)\)", r["condition"]):
        assert m in lists, r["rule"] + ": unknown list " + m
print("ok: %d rules, %d macros, %d lists" % (len(rules), len(macros), len(lists)))
